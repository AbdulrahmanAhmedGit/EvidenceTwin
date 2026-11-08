"""Focused regressions for complete-table access and public-source boundaries."""
from decimal import Decimal
import socket
import pytest
from evidencetwin_backend.science.datasets import inspect_dataset, query_dataset
from evidencetwin_backend.science.sources import validate_target, RetrievalError


def test_relevant_record_after_old_context_limit_is_selected():
    table = {'columns': ['Entity', 'Code', 'Year', 'Reported rate (%)'],
             'rows': [[f'Other {i}', 'X', '2024', '1'] for i in range(430)] +
                     [['Group Alpha', 'A', '2024', '22.4'], ['Group Beta', 'B', '2024', '13.7']]}
    report = inspect_dataset(table, ['Group Alpha was higher than Group Beta in 2024'], 'file', 'hash', 'revision')
    result = report['comparisons'][0]
    assert [o['rowNumber'] for o in result['observations']] == [432, 433]
    assert Decimal(result['difference']) == Decimal('8.7')
    assert result['differenceUnit'] == 'percentage points'
    assert query_dataset(table, {'Entity': 'Group Beta'})['totalMatches'] == 1


def test_ambiguous_records_and_unknown_columns_do_not_become_findings():
    table = {'columns': ['Entity', 'Year', 'Value'], 'rows': [['Group Alpha','2024','1'],['Group Alpha','2024','2'],['Group Beta','2024','0']]}
    assert not inspect_dataset(table, ['Group Alpha Group Beta 2024'], 'f', None, 'r')['comparisons']
    with pytest.raises(ValueError):
        query_dataset(table, {'Unknown': 'value'})
    assert query_dataset(table, {'Entity': 'Absent'})['totalMatches'] == 0


@pytest.mark.parametrize('ip', ['127.0.0.1','10.0.0.1','169.254.169.254','::1','ff02::1','100.64.0.1'])
def test_retrieval_blocks_non_public_dns_and_multicast(monkeypatch, ip):
    monkeypatch.setattr(socket, 'getaddrinfo', lambda *a, **kw: [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (ip,80))])
    with pytest.raises(RetrievalError):
        validate_target('https://source.example/data')


def test_mixed_public_private_dns_is_rejected(monkeypatch):
    monkeypatch.setattr(socket, 'getaddrinfo', lambda *a, **kw: [(2,1,6,'',('8.8.8.8',443)),(2,1,6,'',('127.0.0.1',443))])
    with pytest.raises(RetrievalError):
        validate_target('https://source.example')


def test_redirect_target_is_checked_before_its_policy_or_content_is_requested(tmp_path, monkeypatch):
    from evidencetwin_backend.science import sources
    seen = []
    monkeypatch.setattr(socket, 'getaddrinfo', lambda host, *a, **kw: [(2,1,6,'',('127.0.0.1' if host == 'internal.example' else '8.8.8.8',443))])
    def transport(url, limit=sources.MAX_BYTES, deadline=None):
        seen.append(url)
        if url.endswith('/robots.txt'):
            return url, 404, '', b''
        return 'https://internal.example/data', 302, '', b''
    monkeypatch.setattr(sources, 'download', transport)
    result = sources.retrieve_source('https://public.example/data', tmp_path)
    assert result['status'] == 'unavailable'
    assert 'private' in result['reason']
    assert not any('internal.example' in url for url in seen)


def test_robots_restriction_blocks_content_request(tmp_path, monkeypatch):
    from evidencetwin_backend.science import sources
    seen = []
    monkeypatch.setattr(socket, 'getaddrinfo', lambda *a, **kw: [(2,1,6,'',('8.8.8.8',443))])
    def transport(url, limit=sources.MAX_BYTES, deadline=None):
        seen.append(url)
        return url, 200, 'text/plain', b'User-agent: *\nDisallow: /\n'
    monkeypatch.setattr(sources, 'download', transport)
    result = sources.retrieve_source('https://public.example/data', tmp_path)
    assert result['status'] == 'unavailable' and 'robots' in result['reason']
    assert seen == ['https://public.example/robots.txt']


def test_download_and_extraction_outcomes_stay_separate(tmp_path, monkeypatch):
    from evidencetwin_backend.science import sources
    monkeypatch.setattr(socket, 'getaddrinfo', lambda *a, **kw: [(2,1,6,'',('8.8.8.8',443))])
    def transport(url, limit=sources.MAX_BYTES, deadline=None):
        return (url,404,'',b'') if url.endswith('/robots.txt') else (url,200,'text/plain',b'\xffnot-UTF8')
    monkeypatch.setattr(sources, 'download', transport)
    result = sources.retrieve_source('https://public.example/data', tmp_path)
    assert result['status'] == 'retrieved' and result['extraction'] == 'unavailable'
    assert (tmp_path/result['artifact']).read_bytes() == b'\xffnot-UTF8'
