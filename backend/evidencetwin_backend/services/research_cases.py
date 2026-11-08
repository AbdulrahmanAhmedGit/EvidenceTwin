"""Revisioned researcher cases around the existing bounded exploratory workflow."""
from copy import deepcopy
import csv
import json
import shutil
from uuid import UUID
from flask import jsonify, request, send_file
from PIL import Image
from pydantic import ValidationError
from werkzeug.exceptions import Conflict, NotFound, ServiceUnavailable, UnprocessableEntity
from .access import owned, principal
from .store import new_id, now
from ..science.processing import process_record
from ..science.datasets import query_dataset
from ..errors import api_error
from ..science.source_links import discover_sources


def install_research_cases(app, runtime):
    store = runtime.store

    def case_record(case_id):
        return owned(store, 'research_case', case_id)

    def snapshot(case, revision_id=None):
        revision_id = revision_id or case['currentRevision']
        if revision_id not in case['revisions']:
            raise NotFound()
        return owned(store, 'case_revision', revision_id)

    def summary(case):
        return {k: case[k] for k in ('id', 'title', 'createdAt', 'updatedAt', 'currentRevision')} | {
            'revisionCount': len(case['revisions']), 'analysisCount': len(case['analyses'])}

    def detail(case):
        revision = snapshot(case)
        return summary(case) | {
            'metadata': revision['metadata'], 'files': revision['files'],
            'revisions': [{'id': r, 'createdAt': snapshot(case, r)['analysis']['createdAt']} for r in case['revisions']],
            'analyses': [runtime.summary(runtime.record(a)) for a in case['analyses']],
            'limitations': revision['packet']['limitations'],
            'sourceCount': discover_sources(revision['metadata'])['detectedCount'],
        }

    def list_cases():
        query = request.args.get('search', '').casefold().strip()
        try:
            page = int(request.args.get('page', '1'))
        except ValueError:
            raise UnprocessableEntity() from None
        if page < 1 or page > 100000:
            raise UnprocessableEntity()
        cases = [r for r in runtime.records('research_case') if query in r['title'].casefold()]
        cases.sort(key=lambda c: c['updatedAt'], reverse=True)
        return jsonify({'items': [summary(c) for c in cases[(page-1)*20:page*20]], 'total': len(cases), 'page': page, 'pageSize': 20})

    def save_case(case_id=None):
        # Whole-record writes are serialized with revision preconditions. Files are
        # bounded by the same ingestion policy as legacy exploratory submissions.
        with store.lock:
            case = case_record(case_id) if case_id else None
            if case and request.headers.get('If-Match') != case['currentRevision']:
                raise Conflict()
            base = snapshot(case) if case else None
            revision = runtime.build_record(base)
            revision['analysis']['status'] = 'draft'
            runtime.store.event(revision, 'research', 'revision_saved')
            if case is None:
                case = {'id': revision['id'], 'ownerId': principal()['id'], 'createdAt': now(), 'revisions': [], 'analyses': [], 'runRequests': {}}
            case.update(title=revision['analysis']['title'], updatedAt=now(), currentRevision=revision['id'])
            case['revisions'].append(revision['id'])
            try:
                # Both records commit atomically; a case never points at an absent revision.
                with store.connection() as db:
                    for kind, value in [('case_revision', revision), ('research_case', case)]:
                        db.execute('INSERT INTO records VALUES (?,?,?) ON CONFLICT(kind,id) DO UPDATE SET body=excluded.body',
                                   (kind, value['id'], json.dumps(value, ensure_ascii=False, allow_nan=False)))
            except BaseException:
                shutil.rmtree(store.uploads/revision['id'], ignore_errors=True)
                raise
        return jsonify(detail(case)), 201

    def get_case(case_id):
        return jsonify(detail(case_record(case_id)))

    def get_revision(case_id, revision_id):
        r = snapshot(case_record(case_id), revision_id)
        return jsonify({'id': r['id'], 'metadata': r['metadata'], 'files': r['files'], 'createdAt': r['analysis']['createdAt']})

    def file_asset(case_id, revision_id, file_id):
        r = snapshot(case_record(case_id), revision_id)
        file = next((f for f in r['files'] if f['id'] == file_id), None)
        if not file:
            raise NotFound()
        return send_file(store.uploads/r['id']/file_id, mimetype=file['mediaType'],
                         download_name=file['name'], as_attachment=not (request.args.get('preview')=='1' and file['mediaType'].startswith('image/')))

    def dataset(case_id, revision_id):
        return runtime.dataset_response(snapshot(case_record(case_id), revision_id))

    def processing(case_id, revision_id):
        return jsonify(process_record(snapshot(case_record(case_id), revision_id), store.uploads))

    def analysis_processing(analysis_id):
        record = runtime.record(analysis_id)
        # Never reinterpret a historical run as having used newer processing.
        processing = record.get('processing')
        if not processing:
            return jsonify({'version': 'legacy', 'datasets': [], 'source': None, 'limitations': [], 'coverage': [], 'historical': True})
        source = processing.get('source')
        public_sources = [{key: value for key, value in entry.items() if key not in ('text', 'dataset')}
                          for entry in processing.get('sources', [source] if source else [])]
        return jsonify({**processing, 'source': {key: value for key, value in source.items() if key not in ('text', 'dataset')} if source else None,
                        'sources': public_sources})

    def analysis_query(analysis_id):
        record = runtime.record(analysis_id)
        if not record.get('dataset'):
            raise NotFound()
        try:
            raw_filters = request.args.get('filters', '{}')
            if len(raw_filters) > 5000:
                raise ValueError()
            filters = json.loads(raw_filters)
            limit = int(request.args.get('limit', '25'))
        except (ValueError, TypeError):
            return api_error('dataset_query_invalid', 'Supply bounded JSON column filters and an integer row limit.', 422)
        try:
            return jsonify(query_dataset(record['dataset'], filters, limit))
        except ValueError as error:
            return api_error('dataset_query_invalid', str(error), 422)

    def source_snapshot(analysis_id):
        record = runtime.record(analysis_id)
        source = record.get('processing', {}).get('source')
        source_id = request.args.get('sourceId')
        if source_id:
            source = next((entry for entry in record.get('processing', {}).get('sources', [source] if source else [])
                           if entry.get('evidenceId', 'retrieved-source') == source_id), None)
        if not source or source['status'] != 'retrieved':
            raise NotFound()
        artifact = source.get('rawArtifact') if request.args.get('raw') == '1' else source['artifact']
        if not artifact:
            raise NotFound()
        filename = ('youtube-captions.xml' if request.args.get('raw') == '1' else 'youtube-transcript.json') if source.get('extraction') == 'youtube_transcript' else 'source-snapshot'
        return send_file(store.uploads/analysis_id/artifact, as_attachment=True,
                         mimetype='application/octet-stream', download_name=filename)

    def start(case_id):
        data = request.get_json(silent=True)
        if not isinstance(data, dict) or set(data) != {'revisionId', 'requestId', 'consent'} or data['consent'] is not True:
            raise UnprocessableEntity()
        try:
            UUID(data['requestId'])
        except (ValueError, TypeError, AttributeError):
            raise UnprocessableEntity() from None
        with store.lock:
            case = case_record(case_id)
            receipt = case['runRequests'].get(data['requestId'])
            if receipt:
                if receipt['revisionId'] != data['revisionId']:
                    raise Conflict()
                return jsonify({'id': receipt['id']}), 200
            if case['currentRevision'] != data['revisionId']:
                raise Conflict()
            if not runtime.provider.configured:
                raise ServiceUnavailable()
            if any(runtime.record(a)['analysis']['status'] in ('queued', 'running') for a in case['analyses']):
                raise Conflict()
            record = deepcopy(snapshot(case))
            if not record['files'] and not record['metadata'].get('caseId') and not discover_sources(record['metadata'])['candidates']:
                # Saving a question is valid; running an evidence review needs evidence.
                raise UnprocessableEntity()
            revision_id = record['id']
            record_id = new_id()
            directory = store.uploads/record_id
            directory.mkdir(mode=0o700)
            try:
                for file in record['files']:
                    shutil.copyfile(store.uploads/revision_id/file['id'], directory/file['id'])
                    (directory/file['id']).chmod(0o600)
                record.update(id=record_id, researchCaseId=case_id, evidenceRevision=revision_id)
                record['packet']['case_id'] = record_id
                record['analysis'].update(id=record_id, createdAt=now())
                store.event(record, 'research', 'external_processing_authorized', revisionId=revision_id)
                case['analyses'].append(record_id)
                case['runRequests'][data['requestId']] = {'id': record_id, 'revisionId': revision_id}
                case['updatedAt'] = now()
                runtime.workflow.submit(record, related=[('research_case', case)])
            except BaseException:
                # If acceptance already persisted, retain its evidence and receipt
                # for reconciliation rather than deleting worker inputs.
                try:
                    store.get('analysis', record_id)
                except NotFound:
                    shutil.rmtree(directory, ignore_errors=True)
                raise
        return jsonify({'id': record_id}), 202

    routes = [
        ('/api/research-cases', 'GET', list_cases), ('/api/research-cases', 'POST', save_case),
        ('/api/research-cases/<case_id>', 'GET', get_case),
        ('/api/research-cases/<case_id>/revisions', 'POST', save_case),
        ('/api/research-cases/<case_id>/revisions/<revision_id>', 'GET', get_revision),
        ('/api/research-cases/<case_id>/revisions/<revision_id>/files/<file_id>', 'GET', file_asset),
        ('/api/research-cases/<case_id>/revisions/<revision_id>/dataset', 'GET', dataset),
        ('/api/research-cases/<case_id>/analyses', 'POST', start),
        ('/api/research-cases/<case_id>/revisions/<revision_id>/processing', 'GET', processing),
        ('/api/analyses/<analysis_id>/processing', 'GET', analysis_processing),
        ('/api/analyses/<analysis_id>/dataset-query', 'GET', analysis_query),
        ('/api/analyses/<analysis_id>/source-snapshot', 'GET', source_snapshot),
    ]
    def wrap(handler):
        def view(**params):
            try:
                return handler(**params)
            except (ValidationError, json.JSONDecodeError, UnicodeError, csv.Error, Image.DecompressionBombError, Image.DecompressionBombWarning, TypeError):
                raise UnprocessableEntity() from None
        return view
    for index, (path, method, handler) in enumerate(routes):
        app.add_url_rule(path, endpoint=f'research_cases.{handler.__name__}_{index}', view_func=wrap(handler), methods=[method])
