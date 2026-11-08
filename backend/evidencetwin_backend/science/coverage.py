"""Human-readable explanations of actual performed, missing and unavailable checks."""
LABELS = {
    'complete_dataset_queries': 'Structured data inspection',
    'descriptive_comparison': 'Reported value comparison',
    'source_retrieval': 'Source reading',
    'source_authenticity': 'Independent source authentication',
    'statistical_inference': 'Statistical inference',
    'blind_optics': 'Blind plot reconstruction',
}
STATUSES = {'performed': 'Performed', 'no_dataset': 'No structured table', 'not_performed': 'Not performed',
            'retrieved': 'Retrieved', 'partially_retrieved': 'Some sources retrieved', 'unavailable': 'Unavailable',
            'not_requested': 'Awaiting a new review', 'no_url': 'No supported source link'}


def build_coverage(record, datasets, sources):
    comparisons = any(table['comparisons'] for table in datasets)
    retrieved = sum(source['status'] == 'retrieved' for source in sources)
    if not sources:
        source_status = 'no_url'
        source_reason = 'No supported HTTP(S) source link was found in the source field, original questions or research notes.'
    elif all(source['status'] == 'not_requested' for source in sources):
        source_status = 'not_requested'
        source_reason = f'{len(sources)} source links were detected. Retrieval starts after you authorize a new review.'
    elif retrieved:
        source_status = 'retrieved' if retrieved == len(sources) else 'partially_retrieved'
        source_reason = f'{retrieved} of {len(sources)} recorded source links were retrieved. Inspect each source outcome below.'
    else:
        source_status = 'unavailable'
        source_reason = 'Source links were detected, but retrieval was blocked or unsuccessful. Inspect each source outcome for its reason.'
    image_only = bool(record['files']) and all(file['mediaType'].startswith('image/') for file in record['files'])
    table_reason = (f'{len(datasets)} complete parsed tables are available for bounded queries.' if datasets else
                    'Only chart images were submitted. Exact numerical values require a supported CSV or structured JSON table, or a retrieved dataset.' if image_only else
                    'No supported structured table was parsed from the submitted or retrieved evidence.')
    comparison_reason = ('The exact selected observations and arithmetic are recorded above.' if comparisons else
                         'A comparison needs structured numerical observations. Chart images alone do not provide a reproducible numerical table.' if not datasets else
                         'The available table did not produce an unambiguous compatible pair. Inspect the data-selection limits for the exact reason.')
    items = [
        ('complete_dataset_queries', 'performed' if datasets else 'no_dataset', table_reason),
        ('descriptive_comparison', 'performed' if comparisons else 'not_performed', comparison_reason),
        ('source_retrieval', source_status, source_reason),
        ('source_authenticity', 'not_performed', 'Independent source authentication is unavailable in this pipeline. Retrieved content retains unverified provenance.'),
        ('statistical_inference', 'not_performed', 'Validated inferential statistical procedures are unavailable. Descriptive arithmetic is reported separately.'),
        ('blind_optics', 'unavailable', 'Blind reconstruction requires an approved blinding/rendering protocol and acceptance. Original images remain inspectable.'),
    ]
    return [{'check': check, 'status': status, 'label': LABELS[check], 'statusLabel': STATUSES[status], 'explanation': reason}
            for check, status, reason in items]


def format_coverage(items):
    return '\n\n'.join(item.get('label', LABELS.get(item['check'], item['check'])) + ' — ' +
                       item.get('statusLabel', STATUSES.get(item['status'], item['status'])) +
                       ('\n' + item['explanation'] if item.get('explanation') else '') for item in items)


def humanize_legacy_coverage(body):
    items = []
    for line in body.splitlines():
        if not line.strip():
            continue
        parts = line.strip().split(' — ')
        if len(parts) != 2 or parts[0] not in LABELS or parts[1] not in STATUSES:
            return body
        items.append({'check': parts[0], 'status': parts[1]})
    return format_coverage(items) if items else body
