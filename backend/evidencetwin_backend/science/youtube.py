"""Public captions through youtube-transcript-api over the bounded pinned transport."""
import hashlib
import json
import math
import re
from time import monotonic
from urllib.parse import urlsplit, parse_qs, urlencode
from requests import Session, Response, Request
from youtube_transcript_api import YouTubeTranscriptApi


def youtube_video_id(url):
    parsed = urlsplit(url)
    host = (parsed.hostname or '').lower()
    if parsed.username or parsed.password:
        return None
    if host in ('youtu.be', 'www.youtu.be'):
        video = parsed.path.strip('/').split('/')[0]
    elif host in ('youtube.com', 'www.youtube.com', 'm.youtube.com'):
        parts = parsed.path.strip('/').split('/')
        video = parse_qs(parsed.query).get('v', [''])[0] if parsed.path == '/watch' else parts[1] if len(parts) == 2 and parts[0] in ('shorts','embed','live') else ''
    else:
        return None
    return video if re.fullmatch(r'[A-Za-z0-9_-]{11}', video) else None


class CaptionSession(Session):
    def __init__(self, transport, deadline):
        super().__init__()
        self.trust_env = False
        self.transport = transport
        self.deadline = deadline
        self.request_count = 0
        self.caption_bytes = None

    def request(self, method, url, **kwargs):
        self.request_count += 1
        parsed = urlsplit(url)
        if (self.request_count > 8 or monotonic() >= self.deadline or method.upper() not in ('GET','POST')
                or parsed.scheme != 'https' or parsed.hostname not in ('www.youtube.com','youtube.com','youtubei.googleapis.com')):
            raise ValueError('Caption request exceeded its supported network boundary.')
        if kwargs.get('params'):
            url += ('&' if parsed.query else '?') + urlencode(kwargs['params'])
        body = json.dumps(kwargs['json']).encode() if 'json' in kwargs else None
        if body and len(body) > 65536:
            raise ValueError('Caption request exceeds the body limit.')
        _, status, media, content = self.transport(url, deadline=self.deadline, method=method.upper(), body=body)
        if 300 <= status < 400:
            raise ValueError('Caption redirects require a supported public destination.')
        response = Response()
        response.status_code = status
        response.url = url
        response._content = content
        response.encoding = 'utf-8'
        response.headers['Content-Type'] = media
        response.request = Request(method, url).prepare()
        if status == 200 and parsed.path.endswith('/timedtext'):
            self.caption_bytes = content
        return response


def retrieve_transcript(url, directory, transport):
    result = {'url': url, 'finalUrl': url, 'status': 'unavailable', 'authenticity': 'unverified',
              'contentVerification': 'not_performed', 'extractor': 'youtube-transcript-api/1.2.5'}
    try:
        video_id = youtube_video_id(url)
        if video_id is None:
            raise ValueError('A supported YouTube video URL is required.')
        with CaptionSession(transport, monotonic() + 45) as session:
            tracks = list(YouTubeTranscriptApi(http_client=session).list(video_id))
            generated = next((track for track in tracks if track.is_generated), None)
            selected = next((track for track in tracks if generated and not track.is_generated and track.language_code == generated.language_code), generated or (tracks[0] if tracks else None))
            if selected is None:
                raise ValueError('No public caption track was available.')
            fetched = selected.fetch()
            segments = fetched.to_raw_data()
            if (not segments or len(segments) > 20000 or sum(len(segment['text']) for segment in segments) > 200000
                    or any(not math.isfinite(segment[key]) or segment[key] < 0 for segment in segments for key in ('start','duration'))):
                raise ValueError('The transcript exceeds supported limits or has invalid timings.')
            snapshot = {'videoId': video_id, 'language': fetched.language, 'languageCode': fetched.language_code,
                        'isGenerated': fetched.is_generated, 'segments': segments}
            content = json.dumps(snapshot, ensure_ascii=False, allow_nan=False).encode()
            digest = hashlib.sha256(content).hexdigest()
            artifact = 'source-' + digest
            (directory / artifact).write_bytes(content)
            (directory / artifact).chmod(0o600)
            result.update(status='retrieved', mediaType='application/json', size=len(content), sha256=digest, artifact=artifact,
                          extraction='youtube_transcript', videoId=video_id, language=fetched.language,
                          languageCode=fetched.language_code, isGenerated=fetched.is_generated, segmentCount=len(segments),
                          languageSelection='Prefer manual captions in the generated track language when available; otherwise retain an available original track. No transcript translation requested.',
                          text='\n'.join(f"[{index + 1}; {segment['start']}s; duration {segment['duration']}s] {segment['text']}" for index, segment in enumerate(segments)),
                          reason='Public captions retrieved. Caption accuracy and scientific assertions await independent checking.')
            if session.caption_bytes:
                raw_hash = hashlib.sha256(session.caption_bytes).hexdigest()
                raw_artifact = 'source-' + raw_hash
                (directory / raw_artifact).write_bytes(session.caption_bytes)
                (directory / raw_artifact).chmod(0o600)
                result.update(rawCaptionSha256=raw_hash, rawArtifact=raw_artifact)
    except Exception as error:
        reasons = {'TranscriptsDisabled': 'Captions are disabled for this video.', 'NoTranscriptFound': 'No public transcript track is available.',
                   'VideoUnavailable': 'The video is unavailable.', 'VideoUnplayable': 'The video cannot be accessed through this public caption connector.',
                   'AgeRestricted': 'This video requires restricted access.', 'RequestBlocked': 'YouTube blocked this transcript request.',
                   'IpBlocked': 'YouTube blocked transcript requests from this network.'}
        result.update(reason=reasons.get(type(error).__name__, 'The public transcript could not be retrieved within the supported access, format or resource limits.'),
                      failureCode=type(error).__name__)
    return result
