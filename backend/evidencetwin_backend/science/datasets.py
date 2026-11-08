"""Read-only complete-table selection and exact descriptive arithmetic, version 1.

Row numbers refer to a header followed by original CSV records (multiline cells
count as one record). JSON tables use the same header-plus-record convention.
"""
from decimal import Decimal, InvalidOperation, localcontext
import hashlib
import json
import re

VERSION = 'descriptive-evidence/1'
MAX_QUERY_ROWS = 100
MAX_CONTEXT_BYTES = 64000


def bounded_records(records):
    selected = []
    size = 0
    for record in records:
        size += len(json.dumps(record, ensure_ascii=False).encode())
        if size > MAX_CONTEXT_BYTES or len(selected) >= MAX_QUERY_ROWS:
            break
        selected.append(record)
    return selected


def query_dataset(dataset, filters, limit=MAX_QUERY_ROWS):
    columns = dataset['columns']
    if not isinstance(filters, dict) or len(filters) > 6 or not filters:
        raise ValueError('Supply one to six exact column filters.')
    if any(key not in columns or not isinstance(value, (str, int, float)) or isinstance(value, bool)
           for key, value in filters.items()):
        raise ValueError('Unknown column or unsupported filter value.')
    if type(limit) is not int or not 1 <= limit <= MAX_QUERY_ROWS:
        raise ValueError('Query limit must be between 1 and 100.')
    indexed = [(columns.index(key), str(value).casefold()) for key, value in filters.items()]
    matches = [(i + 2, row) for i, row in enumerate(dataset['rows'])
               if all(str(row[index]).casefold() == value for index, value in indexed)]
    records = bounded_records([{'rowNumber': i, 'values': row} for i, row in matches[:limit]])
    return {'filters': filters, 'columns': columns, 'totalMatches': len(matches),
            'records': records, 'limited': len(matches) > len(records),
            'constraint': 'At most 100 records and 64,000 serialized UTF-8 bytes per query. Complete input retained.',
            'method': 'case-insensitive exact equality over the complete table'}


def number(value):
    try:
        result = Decimal(str(value))
        if not result.is_finite():
            return None
        digits = result.as_tuple()
        return result if len(digits.digits) <= 28 and -28 <= digits.exponent <= 28 and -28 <= result.adjusted() <= 28 else None
    except InvalidOperation:
        return None


def inspect_dataset(dataset, claims, evidence_id, sha256, revision, filename=None):
    result = {'version': VERSION, 'revisionId': revision, 'evidenceId': evidence_id,
              'filename': filename,
              'sha256': sha256, 'columns': dataset['columns'], 'rowCount': len(dataset['rows']),
              'variables': dataset.get('variables', []), 'notes': dataset.get('notes', []),
              'queries': [], 'comparisons': [], 'records': [], 'limitations': []}
    columns = dataset['columns']
    # Explicit schema support, not guessed meanings for arbitrary columns.
    entity = next((c for c in columns if c.casefold() in ('entity', 'country', 'location')), None)
    year = next((c for c in columns if c.casefold() == 'year'), None)
    if entity is None or year is None:
        result['limitations'].append('Automatic selection needs an Entity, Country or Location column and a Year column. Use exact dataset queries for other schemas.')
        return result
    text = '\n'.join(claims).casefold()
    names = list(dict.fromkeys(str(row[columns.index(entity)]) for row in dataset['rows']))
    mentioned = [name for name in names if len(name) > 2 and re.search(r'(?<!\w)' + re.escape(name.casefold()) + r'(?!\w)', text)]
    years = sorted(set(re.findall(r'(?<!\d)(?:19|20)\d{2}(?!\d)', text)))
    # Reject ambiguous automatic extraction; never infer an alias or a year.
    if not mentioned or len(mentioned) > 8 or not years or len(years) > 4:
        result['limitations'].append('No unambiguous entity/year selection was found in the original question. Exact names and years or an explicit dataset query are needed.')
        return result
    mentioned.sort(key=lambda name: text.index(name.casefold()))
    for name in mentioned:
        for selected_year in years:
            query = query_dataset(dataset, {entity: name, year: selected_year})
            query['id'] = 'query-' + evidence_id + '-' + hashlib.sha256(json.dumps(query['filters'], sort_keys=True).encode()).hexdigest()[:12]
            result['queries'].append(query)
            result['records'].extend(query['records'])
            if not query['totalMatches']:
                result['limitations'].append(f'No exact record for {name}, {selected_year}, exists in the complete submitted table.')
            elif query['limited']:
                result['limitations'].append(f'The query for {name}, {selected_year}, exceeded a documented context budget. Matching rows exist in the preserved table.')
    metrics = [c for c in columns if c not in (entity, year) and c.casefold() not in ('code', 'iso', 'iso_code')]
    # A multi-indicator table needs an explicit indicator choice, not a guess.
    if len(metrics) != 1:
        result['limitations'].append('Automatic comparison requires exactly one measurement column. Select an indicator explicitly for multi-indicator tables.')
        return result
    metric = metrics[0]
    variables = dataset.get('variables', [])
    if not isinstance(variables, list):
        variables = []
    declared_unit = next((v['unit'] for v in variables if isinstance(v, dict) and v.get('name') == metric
                          and isinstance(v.get('unit'), str) and v['unit'].strip() and len(v['unit']) <= 200), None)
    unit = '%' if '%' in metric else declared_unit
    for selected_year in years:
        selected = [q for q in result['queries'] if q['filters'][year] == selected_year]
        if len(selected) != 2 or any(q['totalMatches'] != 1 or len(q['records']) != 1 for q in selected):
            continue
        observations = []
        for q in selected:
            row = q['records'][0]
            value = number(row['values'][columns.index(metric)])
            if value is None:
                break
            observations.append({'label': q['filters'][entity], 'value': str(value),
                                 'rowNumber': row['rowNumber'], 'queryId': q['id']})
        if len(observations) != 2:
            result['limitations'].append('A selected measurement is missing, non-numeric or outside the descriptive decimal input bounds (28 digits and exponent ±28). No comparison was produced.')
            continue
        with localcontext() as context:
            context.prec = 64
            left, right = [Decimal(o['value']) for o in observations]
            difference = str(left - right)
            absolute_difference = str(abs(left - right))
            context.prec = 34
            comparison = {'id': f'comparison-{evidence_id}-{selected_year}', 'indicator': metric, 'year': selected_year,
                          'unit': unit, 'observations': observations, 'difference': difference,
                          'absoluteDifference': absolute_difference,
                          'differenceUnit': 'percentage points' if unit == '%' else unit or 'same supplied units',
                          'ratio': str(left / right) if right != 0 else None,
                          'plot': {'version': 'reported-comparison/1', 'kind': 'horizontal_bar', 'scale': 'linear',
                                   'domain': [str(min(Decimal(0), left, right)), str(max(Decimal(0), left, right))],
                                   'baseline': '0', 'transformation': 'identity', 'uncertaintyIntervals': 'not_generated'},
                          'relation': 'higher' if left > right else 'lower' if left < right else 'equal',
                          'scope': 'Reported values in the same submitted indicator and year. Population definitions, age-standardization, methodology and source authenticity have not been independently established.',
                          'method': 'Decimal subtraction at precision 64; first-value / second-value ratio at precision 34 with half-even rounding. Inputs limited to 28 digits and exponent ±28. No significance test or causal inference.'}
        result['comparisons'].append(comparison)
    return result
