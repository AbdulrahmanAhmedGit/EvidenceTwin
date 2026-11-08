"""Bounded connector and derivative-report regression checks, using isolated records."""
from copy import deepcopy
from time import monotonic, sleep
import pytest
from evidencetwin_backend.science.source_links import discover_sources
from evidencetwin_backend.science.youtube import youtube_video_id, CaptionSession
from evidencetwin_backend.services.report_translation import ReportTranslations, report_hash, text_blocks
from evidencetwin_backend.services.store import Store


def test_links_discovered_without_mutating_original_inputs():
    metadata = {'url': 'https://first.example/a', 'claims': ['See (https://second.example/study). https://first.example/a#figure'],
                'context': 'https://third.example/table.csv، https://user:password@private.example'}
    original = deepcopy(metadata)
    result = discover_sources(metadata)
    assert metadata == original
    assert result['detectedCount'] == 3 and result['rejectedCount'] == 1
    assert [item['evidenceId'] for item in result['candidates']] == ['retrieved-source', 'retrieved-source-2', 'retrieved-source-3']
    assert result['candidates'][1]['url'] == 'https://second.example/study'


def test_link_limits_are_reported():
    result = discover_sources({'claims': [' '.join(f'https://source.example/{index}' for index in range(12))]})
    assert result['detectedCount'] == 12 and len(result['candidates']) == 10 and result['retrievalLimit'] == 3


@pytest.mark.parametrize('url', ['https://youtu.be/abcdefghijk', 'https://www.youtube.com/watch?v=abcdefghijk', 'https://youtube.com/shorts/abcdefghijk'])
def test_public_video_id(url):
    assert youtube_video_id(url) == 'abcdefghijk'


def test_caption_connector_rejects_unapproved_destinations():
    with CaptionSession(lambda *a, **kw: pytest.fail('No request may escape the connector'), monotonic()+10) as session:
        with pytest.raises(ValueError):
            session.get('https://unrelated.example/transcript')
    assert youtube_video_id('https://youtube.com.evil.example/watch?v=abcdefghijk') is None


def test_report_derivative_preserves_original_and_reuses_completed_job(tmp_path):
    store = Store(tmp_path)
    analysis = {'id': 'isolated-analysis', 'files': [], 'report': {'report': {'title': 'Original title'}, 'sections': [{'id':'answer','title':'Answer','body':'Reported value 22.4%.'}]}}
    original = deepcopy(analysis)
    store.put('analysis', analysis)
    service = ReportTranslations(store, {'LIBRETRANSLATE_URL':'http://127.0.0.1:5002','LIBRETRANSLATE_API_KEY':''})
    service.client.capabilities = lambda: {'available':True, 'targets':['ar','en']}
    service.client.translate = lambda text, target, literals: 'Translated '+text if text else text
    try:
        receipt = service.submit(analysis, 'owner', 'ar')
        deadline = monotonic()+5
        while monotonic()<deadline and store.get('report_translation', receipt['id'])['status'] in ('queued','running'):
            sleep(.01)
        result = store.get('report_translation', receipt['id'])
        assert result['status'] == 'completed'
        assert result['sourceReportHash'] == report_hash(original['report'])
        assert store.get('analysis', analysis['id']) == original
        assert service.submit(analysis, 'owner', 'ar')['id'] == receipt['id']
        assert service.submit(analysis, 'other-owner', 'ar')['id'] != receipt['id']
    finally:
        service.shutdown()


def test_translation_blocks_preserve_whitespace():
    text = 'Original sentence.\n\nAnother sentence.\n'
    assert ''.join(part+ending for part, ending in text_blocks(text)) == text


def test_partial_source_access_keeps_later_evidence_references(tmp_path, monkeypatch):
    from evidencetwin_backend.science import processing
    record = {'id':'isolated-analysis','files':[], 'metadata':{'claims':['https://first.example https://second.example'], 'context':''}, 'packet':{'evidence':[],'scientific_pipeline':{}}}
    def retrieve(url, directory):
        if 'first' in url:
            return {'url':url,'status':'unavailable','reason':'Blocked'}
        return {'url':url,'finalUrl':url,'status':'retrieved','text':'Actual retained excerpt','sha256':'a'*64,'mediaType':'text/plain'}
    monkeypatch.setattr(processing,'retrieve_source',retrieve)
    preview = processing.process_record(record,tmp_path,retrieve=False)
    assert all(source['status']=='not_requested' for source in preview['sources'])
    result = processing.process_record(record,tmp_path,retrieve=True)
    assert next(item for item in result['coverage'] if item['check']=='source_retrieval')['status']=='partially_retrieved'
    packet = processing.prepare_packet(record,result)
    assert [item['id'] for item in packet['evidence'] if item['kind']=='source_snapshot']==['retrieved-source-2']
    assert packet['retrieved_sources'][1]['excerpts'][0]['text']=='Actual retained excerpt'
    assert packet['scientific_pipeline']['source_retrieval']=='partially_retrieved'


def test_caption_snapshot_retains_language_timings_and_raw_bytes(tmp_path, monkeypatch):
    from evidencetwin_backend.science import youtube
    class Captions:
        language='English'
        language_code='en'
        is_generated=False
        def to_raw_data(self):
            return [{'text':'Explicitly authored connector test caption.','start':1.5,'duration':2.0}]
    class Track:
        language_code='en'
        is_generated=False
        def fetch(self):
            return Captions()
    class TestCaptionApi:
        def __init__(self,http_client):
            self.session=http_client
        def list(self,video):
            self.session.get('https://www.youtube.com/api/timedtext?v='+video)
            return [Track()]
    monkeypatch.setattr(youtube,'YouTubeTranscriptApi',TestCaptionApi)
    raw=b'<transcript>isolated test bytes</transcript>'
    result=youtube.retrieve_transcript('https://youtu.be/abcdefghijk',tmp_path,lambda url,**kw:(url,200,'text/xml',raw))
    assert result['status']=='retrieved' and result['languageCode']=='en' and not result['isGenerated']
    assert '[1; 1.5s; duration 2.0s]' in result['text']
    assert (tmp_path/result['rawArtifact']).read_bytes()==raw


def test_unsafe_translation_passage_remains_original_and_is_labeled(tmp_path):
    from evidencetwin_backend.services.report_translation import TranslationIntegrityError
    store=Store(tmp_path)
    analysis={'id':'translation-safety-check','files':[], 'report':{'report':{'title':'Report'},'sections':[{'id':'methods','title':'Methods','body':'Precision 64. No inference.'}]}}
    store.put('analysis',analysis)
    service=ReportTranslations(store,{'LIBRETRANSLATE_URL':'http://127.0.0.1:5002','LIBRETRANSLATE_API_KEY':''})
    service.client.capabilities=lambda:{'available':True,'targets':['ar']}
    def translate(text,target,literals):
        if text.startswith('Precision'):
            raise TranslationIntegrityError('Numeric preservation could not be confirmed.')
        return text
    service.client.translate=translate
    try:
        receipt=service.submit(analysis,'owner','ar')
        service.shutdown()
        result=store.get('report_translation',receipt['id'])
        assert result['status']=='completed' and 'Partial' in result['classification']
        assert result['translatedReport']['sections'][0]['body']=='Precision 64. No inference.'
        assert result['retainedOriginalBlocks'][0]['field']=='0.body'
        assert store.get('analysis',analysis['id'])==analysis
    finally:
        service.shutdown()


def test_translation_guard_rejects_added_number():
    from evidencetwin_backend.services.report_translation import LibreTranslateClient,TranslationIntegrityError
    client=LibreTranslateClient({'LIBRETRANSLATE_URL':'http://127.0.0.1:5002','LIBRETRANSLATE_API_KEY':''})
    client.request=lambda path,payload:{'translatedText':payload['q'].replace('Method','طريقة 11')}
    with pytest.raises(TranslationIntegrityError):
        client.translate('Method precision 64.','ar')
