"""Bounded public-source snapshots with pinned DNS and robots policy checks.

No proxies, cookies, credentials, JS, paywall bypass, decompression or PDF parser.
"""
import hashlib
import http.client
import ipaddress
import socket
import ssl
from threading import Timer
from time import monotonic
from datetime import datetime, timezone
from scrapling import Selector
from .youtube import youtube_video_id, retrieve_transcript
from urllib.parse import urlsplit, urljoin, urlunsplit, unquote
from urllib.robotparser import RobotFileParser

MAX_BYTES = 2 * 1024 * 1024
AGENT = 'EvidenceTwinResearch/1.0'


class RetrievalError(Exception):
    pass


def validate_target(url):
    parsed = urlsplit(url)
    if (parsed.scheme not in ('http', 'https') or not parsed.hostname or parsed.username or parsed.password
            or parsed.port not in (None, 80, 443) or len(url) > 2048
            or any(ord(c) < 33 for c in url)):
        raise RetrievalError('The source needs a public HTTP(S) URL on a standard port, without credentials.')
    if (any(segment in ('.', '..') for segment in parsed.path.split('/'))
            or any(encoded in parsed.path.lower() for encoded in ('%2f', '%5c', '%2e', '%25'))):
        raise RetrievalError('Ambiguously encoded source paths are unsupported by the access-policy checker.')
    try:
        addresses = socket.getaddrinfo(parsed.hostname, parsed.port or (443 if parsed.scheme == 'https' else 80), type=socket.SOCK_STREAM)
    except OSError:
        raise RetrievalError('The source hostname could not be resolved.') from None
    ips = list(dict.fromkeys(item[4][0] for item in addresses))
    addresses = [ipaddress.ip_address(ip) for ip in ips]
    if not addresses or any(not ip.is_global or ip.is_multicast or ip.is_reserved
                            or (isinstance(ip, ipaddress.IPv6Address) and (ip.sixtofour or ip.teredo)) for ip in addresses):
        raise RetrievalError('Retrieval is blocked for private, local or non-public network targets.')
    return parsed, ips[0]


class PinnedHTTPS(http.client.HTTPSConnection):
    def __init__(self, hostname, port, ip, timeout):
        super().__init__(hostname, port, timeout=timeout, context=ssl.create_default_context())
        self.target_ip = ip

    def connect(self):
        raw = socket.create_connection((self.target_ip, self.port), self.timeout)
        self.retrieval_socket = raw
        try:
            self.sock = self._context.wrap_socket(raw, server_hostname=self.host)
            self.retrieval_socket = self.sock
        except BaseException:
            raw.close()
            raise


class PinnedHTTP(http.client.HTTPConnection):
    def connect(self):
        super().connect()
        self.retrieval_socket = self.sock


def download(url, limit=MAX_BYTES, deadline=None, method='GET', body=None):
    # Every redirect is resolved and validated afresh, then pinned for connect.
    parsed, ip = validate_target(url)
    budget = min(15, deadline - monotonic()) if deadline is not None else 15
    if budget <= 0:
        raise RetrievalError('Source retrieval exceeded its time budget.')
    port = parsed.port or (443 if parsed.scheme == 'https' else 80)
    connection = PinnedHTTPS(parsed.hostname, port, ip, min(10, budget)) if parsed.scheme == 'https' else PinnedHTTP(ip, port, timeout=min(10, budget))
    def interrupt():
        sock = getattr(connection, 'retrieval_socket', None)
        if sock:
            try:
                sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            sock.close()
    timer = Timer(budget, interrupt)
    timer.daemon = True
    timer.start()
    path = urlunsplit(('', '', parsed.path or '/', parsed.query, ''))
    try:
        connection.request(method, path, body=body, headers={'Host': parsed.netloc, 'User-Agent': AGENT,
                                                 'Accept': 'text/html, text/plain, text/csv, application/json, application/pdf',
                                                 **({'Content-Type': 'application/json'} if body is not None else {}),
                                                 'Accept-Encoding': 'identity'})
        response = connection.getresponse()
        if response.status in (301, 302, 303, 307, 308):
            target = response.getheader('Location')
            if not target:
                raise RetrievalError('Source redirect has no destination.')
            # Caller checks the destination's robots policy before fetching it.
            return urljoin(url, target), response.status, '', b''
        if response.status != 200:
            return url, response.status, '', b''
        if response.getheader('Content-Encoding', 'identity').lower() != 'identity':
            raise RetrievalError('Compressed source responses are unsupported by the bounded extractor.')
        length = response.getheader('Content-Length')
        if length and int(length) > limit:
            raise RetrievalError('The source exceeds the snapshot size limit.')
        body = response.read(limit + 1)
        if len(body) > limit:
            raise RetrievalError('The source exceeds the snapshot size limit.')
        return url, response.status, response.getheader('Content-Type', '').split(';')[0].strip().lower(), body
    finally:
        timer.cancel()
        connection.close()


def retrieve_source(url, directory):
    result = {'url': url, 'retrievedAt': datetime.now(timezone.utc).isoformat(),
              'status': 'unavailable', 'authenticity': 'unverified', 'contentVerification': 'not_performed'}
    if youtube_video_id(url):
        return {**result, **retrieve_transcript(url, directory, download)}
    try:
        deadline = monotonic() + 45
        candidate = url
        for _ in range(4):
            parsed, _ = validate_target(candidate)
            robots_url = urlunsplit((parsed.scheme, parsed.netloc, '/robots.txt', '', ''))
            _, robots_status, _, robots_body = download(robots_url, 128 * 1024, deadline)
            if robots_status not in (200, 404):
                raise RetrievalError('Access policy could not be established from robots.txt. Redirected or restricted policies require operator review.')
            policy = RobotFileParser()
            policy_lines = robots_body.decode('utf-8-sig').splitlines() if robots_status == 200 else []
            for line in policy_lines:
                field, _, value = line.partition(':')
                value = value.split('#', 1)[0].strip()
                if field.strip().lower() in ('allow', 'disallow') and ('*' in value or '$' in value):
                    raise RetrievalError('The source uses extended robots path rules. A reviewed connector is required for this policy.')
            policy.parse(policy_lines)
            if robots_status == 200 and not policy.can_fetch(AGENT, candidate):
                raise RetrievalError('The source robots policy disallows automated retrieval.')
            # The stdlib uses first-match rules. Be conservative when a broader
            # Allow precedes a matching Disallow, rather than weakening policy.
            entries = [*policy.entries, *([policy.default_entry] if policy.default_entry else [])]
            requested_path = unquote(parsed.path or '/') + ('?' + parsed.query if parsed.query else '')
            if any(entry.applies_to(AGENT) and any(not rule.allowance and
                   (rule.path == '*' or requested_path.startswith(unquote(rule.path))) for rule in entry.rulelines)
                   for entry in entries):
                raise RetrievalError('The source robots policy disallows automated retrieval.')
            if robots_status == 200 and (policy.crawl_delay(AGENT) or policy.request_rate(AGENT)):
                raise RetrievalError('The source specifies crawl scheduling. This one-shot retriever requires an operator-approved scheduled connector.')
            final_url, status, media, body = download(candidate, deadline=deadline)
            if status not in (301, 302, 303, 307, 308):
                break
            candidate = final_url
        else:
            raise RetrievalError('The source exceeded the redirect limit.')
        if status != 200:
            raise RetrievalError(f'The source returned HTTP {status}. No restricted content was retrieved.')
        allowed = ('text/html', 'text/plain', 'text/csv', 'application/json', 'application/pdf')
        if media not in allowed:
            raise RetrievalError('The source content type is unsupported.')
        if media == 'application/pdf' and not body.startswith(b'%PDF-'):
            raise RetrievalError('The response does not contain a valid PDF signature.')
        digest = hashlib.sha256(body).hexdigest()
        artifact = 'source-' + digest
        path = directory / artifact
        path.write_bytes(body)
        path.chmod(0o600)
        result.update(status='retrieved', finalUrl=final_url, mediaType=media, size=len(body),
                      sha256=digest, artifact=artifact,
                      text='', extraction='unavailable' if media == 'application/pdf' else 'readable_text',
                      reason='PDF bytes retained. Text extraction is unavailable in this evidence pipeline.' if media == 'application/pdf' else '')
        if media != 'application/pdf':
            try:
                text = body.decode('utf-8-sig')
                if media == 'text/html':
                    page = Selector(text, url=final_url, adaptive=False, huge_tree=False)
                    text = str(page.get_all_text(separator='\n', strip=True, ignore_tags=('script', 'style', 'noscript', 'template')))
                    result.update(extraction='scrapling_html', extractor='scrapling/0.5.1',
                                  title=page.css('title::text').get() or '',
                                  description=page.css('meta[name="description"]::attr(content)').get() or '')
                result['text'] = text
            except UnicodeError:
                result.update(extraction='unavailable', reason='Source bytes were retrieved and preserved. Text extraction requires UTF-8 content.')
    except RetrievalError as error:
        result['reason'] = str(error)
    except (OSError, ValueError, UnicodeError, http.client.HTTPException):
        result['reason'] = 'The source request failed, timed out or could not be safely decoded.'
    return result
