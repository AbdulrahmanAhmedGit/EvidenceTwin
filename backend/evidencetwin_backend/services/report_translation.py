"""Ownership-scoped, versioned report derivatives through operator-managed LibreTranslate."""
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from collections import Counter
import hashlib
import html
import json
import re
import textwrap
from threading import BoundedSemaphore
from time import monotonic
from urllib.parse import urlsplit
from urllib.request import Request, build_opener, ProxyHandler
from scrapling import Selector
from werkzeug.exceptions import Conflict, ServiceUnavailable, UnprocessableEntity, NotFound
from .provider import NoRedirect
from .store import now
from ..science.coverage import humanize_legacy_coverage

PROTECTED = re.compile(r'https?://[^\s<>]+|\b[0-9]{4}-[0-9]{2}-[0-9]{2}\b|\b[0-9a-fA-F]{32,64}\b|\b[A-Z]{2,5}-\d+\b|\b[A-Za-z][A-Za-z0-9_-]*[0-9₀-₉][A-Za-z0-9₀-₉_-]*\b|[+-]?[0-9٠-٩]+(?:[.,][0-9٠-٩]+)*(?:[eE][+-]?[0-9]+)?%?')


class TranslationIntegrityError(ValueError):
    """A derivative must retain source observations and references exactly."""


def report_hash(report):
    return hashlib.sha256(json.dumps(report, sort_keys=True, ensure_ascii=False, allow_nan=False).encode()).hexdigest()


class LibreTranslateClient:
    def __init__(self, config):
        self.base = config['LIBRETRANSLATE_URL'].rstrip('/')
        parsed = urlsplit(self.base)
        if (parsed.scheme not in ('http','https') or not parsed.hostname or parsed.username or parsed.password
                or parsed.query or parsed.fragment or (parsed.scheme == 'http' and parsed.hostname not in ('localhost','127.0.0.1','::1'))):
            raise ValueError('LibreTranslate needs an operator-configured HTTPS endpoint or loopback HTTP endpoint without credentials or query parameters.')
        self.key = config['LIBRETRANSLATE_API_KEY']

    def request(self, path, payload=None, timeout=30):
        if payload is not None and self.key:
            payload = {**payload, 'api_key': self.key}
        data = json.dumps(payload, ensure_ascii=False).encode() if payload is not None else None
        request = Request(self.base + path, data=data, headers={'Content-Type':'application/json'}, method='POST' if payload is not None else 'GET')
        with build_opener(ProxyHandler({}), NoRedirect()).open(request, timeout=timeout) as response:
            body = response.read(256 * 1024 + 1)
            if len(body) > 256 * 1024:
                raise ValueError('Translation response exceeds the size limit.')
            return json.loads(body)

    def capabilities(self):
        try:
            languages = self.request('/languages', timeout=3)
            pairs = {item['code']: item.get('targets', []) for item in languages if isinstance(item, dict)}
            targets = [code for code in ('ar','en') if code in pairs and any(code in available for available in pairs.values())]
            return {'available': bool(targets), 'targets': targets, 'provider': 'LibreTranslate'}
        except Exception:
            return {'available': False, 'targets': [], 'provider': 'LibreTranslate'}

    def translate(self, text, target, literals=()):
        pattern = re.compile('|'.join(re.escape(value) for value in literals) + '|' + PROTECTED.pattern) if literals else PROTECTED
        linguistic_text = pattern.sub('', text)
        arabic = len(re.findall(r'[\u0620-\u064a]', linguistic_text))
        latin = len(re.findall(r'[A-Za-z]', linguistic_text))
        source = 'ar' if arabic > latin else 'en' if latin else 'auto'
        if source == target or not any(char.isalpha() for char in linguistic_text):
            return text
        references = []
        def protect(value):
            index = len(references)
            references.append(value)
            return f'<span translate="no" data-etref="{index}">{html.escape(value)}</span>'
        def prose(value):
            return html.escape(value) if any(char.isalpha() for char in value) else protect(value)
        pieces = []; start = 0
        for match in pattern.finditer(text):
            pieces.append(prose(text[start:match.start()]))
            pieces.append(protect(match.group())); start = match.end()
        pieces.append(prose(text[start:]))
        payload = '<div>' + ''.join(pieces) + '</div>'
        if len(payload) > 2900:
            raise ValueError('This text block exceeds the protected translation limit.')
        response = self.request('/translate', {'q': payload, 'source': source, 'target': target, 'format': 'html'})
        translated = response.get('translatedText')
        if not isinstance(translated, str):
            raise ValueError('The translator returned an invalid text response.')
        page = Selector(translated, adaptive=False, huge_tree=False)
        kept = page.css('span[data-etref]')
        recovered = {node.attrib.get('data-etref'): str(node.get_all_text(separator='', strip=False)) for node in kept}
        if len(kept) != len(references) or any(recovered.get(str(index)) != value for index, value in enumerate(references)):
            raise TranslationIntegrityError('The translation did not preserve protected observations or references.')
        result = str(page.get_all_text(separator='', strip=False))
        if Counter(pattern.findall(result)) != Counter(pattern.findall(text)):
            raise TranslationIntegrityError('The translation changed numerical observations or source references.')
        return result


def text_blocks(text):
    blocks = []
    for line in text.splitlines(keepends=True):
        ending = '\n' if line.endswith('\n') else ''
        line = line.removesuffix('\n')
        wrapped = textwrap.wrap(line, width=600, replace_whitespace=False, drop_whitespace=False,
                                break_long_words=False, break_on_hyphens=False) or ['']
        for index, part in enumerate(wrapped):
            if len(part) > 600 and not (len(part) <= 2048 and PROTECTED.fullmatch(part)):
                raise UnprocessableEntity('The report contains an unsupported oversized text token.')
            blocks.append((part, ending if index == len(wrapped)-1 else ' '))
    return blocks or [('', '')]


class ReportTranslations:
    def __init__(self, store, config):
        self.store = store
        self.client = LibreTranslateClient(config)
        self.pool = ThreadPoolExecutor(max_workers=1, thread_name_prefix='report-translation')
        self.slots = BoundedSemaphore(3)
        for item in store.all('report_translation'):
            if item['status'] in ('queued','running'):
                item.update(status='failed', error='Translation was interrupted. Request it again to retry.', finishedAt=now())
                store.put('report_translation', item)

    def submit(self, analysis, owner_id, target):
        if target not in ('ar','en'):
            raise UnprocessableEntity()
        if not analysis.get('report'):
            raise NotFound()
        source = deepcopy(analysis['report'])
        digest = report_hash(source)
        for section in source.get('sections', []):
            if section['id'] == 'coverage':
                section['body'] = humanize_legacy_coverage(section['body'])
        record_id = hashlib.sha256(f'{owner_id}:{analysis["id"]}:{digest}:{target}'.encode()).hexdigest()[:32]
        try:
            current = self.store.get('report_translation', record_id)
            if current['status'] in ('queued','running','completed'):
                return current
        except NotFound:
            current = None
        availability = self.client.capabilities()
        if not availability['available'] or target not in availability['targets']:
            raise ServiceUnavailable()
        if len(json.dumps(source, ensure_ascii=False)) > 60000:
            raise UnprocessableEntity('The report exceeds the bounded translation size.')
        work = [('title', text_blocks(source.get('report', {}).get('title', ''))),
                ('reproducibility', text_blocks(source.get('report', {}).get('reproducibility', '')))]
        for index, section in enumerate(source.get('sections', [])):
            work.extend([(f'{index}.title', text_blocks(section['title'])), (f'{index}.body', text_blocks(section['body']))])
        total = sum(len(blocks) for _, blocks in work)
        if total > 240:
            raise UnprocessableEntity('The report exceeds the translation block limit.')
        with self.store.lock:
            try:
                current = self.store.get('report_translation', record_id)
                if current['status'] in ('queued','running','completed'):
                    return current
            except NotFound:
                current = None
            if not self.slots.acquire(blocking=False):
                raise ServiceUnavailable()
            item = {'id': record_id, 'analysisId': analysis['id'], 'ownerId': owner_id, 'sourceReportHash': digest,
                    'targetLanguage': target, 'status': 'queued', 'createdAt': now(), 'completedBlocks': 0, 'totalBlocks': total,
                    'provider': 'LibreTranslate', 'modelVersion': 'not_reported', 'clientVersion': 'protected-report-translation/2',
                    'coverageDisplayVersion': 'coverage-labels/1', 'retainedOriginalBlocks': [],
                    'protectedLiterals': [*[file['name'] for file in analysis.get('files', [])],
                                          *[item['id'] for item in analysis.get('packet', {}).get('evidence', [])
                                            if len(item['id']) >= 24 or '-' in item['id']]],
                    'classification': 'Machine translation. Review scientific terminology against the original report.',
                    'attemptHistory': [*(current or {}).get('attemptHistory', []), *([{key:value for key,value in current.items() if key!='attemptHistory'}] if current else [])]}
            try:
                self.store.put('report_translation', item)
                receipt = deepcopy(item)
                future = self.pool.submit(self.run, item, source, work)
                future.add_done_callback(lambda _: self.slots.release())
            except BaseException:
                self.slots.release()
                raise
            return receipt

    def run(self, item, original, work):
        try:
            output = {}; deadline = monotonic() + 300
            item.update(status='running', startedAt=now())
            self.store.put('report_translation', item)
            for key, blocks in work:
                pieces = []
                for block_index, (text, ending) in enumerate(blocks):
                    if monotonic() > deadline:
                        raise ValueError('Translation time budget exceeded.')
                    try:
                        translated_text = self.client.translate(text, item['targetLanguage'], item['protectedLiterals'])
                    except TranslationIntegrityError:
                        translated_text = text
                        item['retainedOriginalBlocks'].append({'field': key, 'block': block_index,
                            'reason': 'Original wording retained because numerical or reference preservation could not be confirmed.'})
                    pieces.append(translated_text + ending)
                    item['completedBlocks'] += 1
                    self.store.put('report_translation', item)
                output[key] = ''.join(pieces)
            current = self.store.get('analysis', item['analysisId'])
            if not current.get('report') or report_hash(current['report']) != item['sourceReportHash']:
                raise Conflict()
            translated = deepcopy(original)
            translated['report']['title'] = output['title']
            translated['report']['reproducibility'] = output['reproducibility']
            for index, section in enumerate(translated['sections']):
                section.update(title=output[f'{index}.title'], body=output[f'{index}.body'])
            if item['retainedOriginalBlocks']:
                item['classification'] = 'Partial machine translation. Some passages retain their original wording for numerical and reference safety. Review scientific terminology against the original.'
            item.update(status='completed', finishedAt=now(), translatedReport=translated)
            self.store.put('report_translation', item)
        except Exception:
            item.update(status='failed', finishedAt=now(), error='Translation could not be completed safely. The original report remains available. Check LibreTranslate availability and supported text limits before retrying.')
            self.store.put('report_translation', item)

    def shutdown(self):
        self.pool.shutdown(wait=True, cancel_futures=True)


def install_report_translations(app, runtime):
    from flask import jsonify, request
    from .access import owned, principal
    service = runtime.translations
    def public(item):
        return {key:value for key,value in item.items() if key not in ('ownerId','protectedLiterals','attemptHistory')}

    def available(analysis_id):
        analysis = runtime.record(analysis_id)
        if not analysis.get('report'):
            raise NotFound()
        owner_id = principal()['id']
        digest = report_hash(analysis['report'])
        items = [public(item) for item in runtime.store.all('report_translation') if item['analysisId'] == analysis_id
                 and item['ownerId'] == owner_id and item['sourceReportHash'] == digest]
        return jsonify({**service.client.capabilities(), 'sourceReportHash': digest, 'translations': items})

    def start(analysis_id):
        analysis = runtime.record(analysis_id)
        data = request.get_json(silent=True)
        if not isinstance(data, dict) or set(data) != {'targetLanguage'}:
            raise UnprocessableEntity()
        item = service.submit(analysis, principal()['id'], data['targetLanguage'])
        return jsonify(public(item)), 200 if item['status'] == 'completed' else 202

    def get(analysis_id, translation_id):
        analysis = runtime.record(analysis_id)
        item = owned(runtime.store, 'report_translation', translation_id)
        if item['analysisId'] != analysis_id:
            raise NotFound()
        if not analysis.get('report') or report_hash(analysis['report']) != item['sourceReportHash']:
            raise Conflict()
        return jsonify(public(item))

    app.add_url_rule('/api/analyses/<analysis_id>/report-translations', 'report_translations.available', available, methods=['GET'])
    app.add_url_rule('/api/analyses/<analysis_id>/report-translations', 'report_translations.start', start, methods=['POST'])
    app.add_url_rule('/api/analyses/<analysis_id>/report-translations/<translation_id>', 'report_translations.get', get, methods=['GET'])
