"""Discover references in original inputs without altering them or making requests."""
import re
from urllib.parse import urlsplit, urlunsplit

MAX_SOURCE_REFERENCES = 10
MAX_RETRIEVED_SOURCES = 3
URL_PATTERN = re.compile(r'https?://[^\s<>\[\]"“”]+', re.IGNORECASE)


def discover_sources(metadata):
    fields = [('source_field', metadata.get('url', ''))]
    fields.extend((f'claim-{index + 1}', claim) for index, claim in enumerate(metadata.get('claims', [])))
    fields.append(('context', metadata.get('context', '')))
    seen = set()
    candidates = []
    rejected = 0
    for field, text in fields:
        for match in URL_PATTERN.finditer(text):
            url = match.group().rstrip('.,;:!?،؛؟\'’')
            while url.endswith(')') and url.count(')') > url.count('('):
                url = url[:-1]
            try:
                parsed = urlsplit(url)
                if (parsed.scheme.lower() not in ('http', 'https') or not parsed.hostname or parsed.username
                        or parsed.password or parsed.port not in (None, 80, 443) or len(url) > 2048):
                    raise ValueError()
                # Fragments identify locations inside one document, not another download.
                key = urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), parsed.path, parsed.query, ''))
            except ValueError:
                rejected += 1
                continue
            if key in seen:
                continue
            seen.add(key)
            if len(candidates) < MAX_SOURCE_REFERENCES:
                index = len(candidates)
                candidates.append({'url': url, 'origin': field,
                                   'evidenceId': 'retrieved-source' if index == 0 else f'retrieved-source-{index + 1}'})
    return {'candidates': candidates, 'detectedCount': len(seen), 'rejectedCount': rejected,
            'referenceLimit': MAX_SOURCE_REFERENCES, 'retrievalLimit': MAX_RETRIEVED_SOURCES}
