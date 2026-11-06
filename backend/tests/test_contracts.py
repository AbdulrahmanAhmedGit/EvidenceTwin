"""Synthetic values are type-validation inputs only, never endpoint results."""
import json
import pytest
from pydantic import TypeAdapter, ValidationError
from evidencetwin_backend.contracts.common import PublicLink, IntegrationLink, validate_contract
from evidencetwin_backend.contracts.analyses import Analysis, AnalysisCreateMetadata
from evidencetwin_backend.contracts.inspection import Dataset, SectionResponse
from evidencetwin_backend.contracts.research import BenchmarkCreate, Metric, ComparisonResponse, BenchmarkResponse
from evidencetwin_backend.contracts.queries import DatasetQuery, ReportListQuery
from evidencetwin_backend.contracts.registry import SCHEMAS

METADATA={'source':'Supplied title','url':'','studyDate':'','studyDesign':'Unknown','population':'','uncertainty':'','context':'','claims':['An owner-submitted claim'],'claim':'An owner-submitted claim','mode':'exploratory','reviewDepth':'focused'}
BENCHMARK={'name':'Schema input only','description':'An owner-defined research objective','caseIds':['a1'],'conditions':['standard','council'],'modelConfigRef':'owner-config','rubricRef':'owner-rubric','repetitions':1,'seed':'owner-seed','preserveControls':True,'outputs':['summary','per_case']}
ANALYSIS={'id':'id','title':'Schema input only','createdAt':'2026-11-03T10:00:00Z','claim':'Supplied claim','mode':'exploratory','status':'awaiting_evidence','limitations':[],'findings':[]}

def test_all_named_contracts_export_json_schema():
    assert len(SCHEMAS)>=20
    for name,schema in SCHEMAS.items():
        exported=TypeAdapter(schema).json_schema()
        assert isinstance(exported,dict),name
        json.dumps(exported,allow_nan=False)

def test_analysis_metadata_matches_the_actual_builder_fields():
    assert validate_contract(AnalysisCreateMetadata,METADATA)==METADATA
    assert validate_contract(AnalysisCreateMetadata,{**METADATA,'caseId':'a1'})['caseId']=='a1'
    with pytest.raises(ValidationError):validate_contract(AnalysisCreateMetadata,{**METADATA,'claims':['  ']})
    with pytest.raises(ValidationError):validate_contract(AnalysisCreateMetadata,{**METADATA,'studyDate':'2026-02-30'})
    with pytest.raises(ValidationError):validate_contract(AnalysisCreateMetadata,{**METADATA,'studyDate':'20261103'})

def test_omitted_fields_do_not_invent_results_but_null_is_not_optional():
    value=validate_contract(Analysis,ANALYSIS)
    assert 'assessment' not in value and 'actions' not in value and 'sourceStatus' not in value
    assert validate_contract(SectionResponse,{})=={}
    with pytest.raises(ValidationError):validate_contract(Analysis,{**ANALYSIS,'assessment':None})
    with pytest.raises(ValidationError):validate_contract(Analysis,{**ANALYSIS,'createdAt':'2026-11-03T10:00:00'})

@pytest.mark.parametrize('change',[{'caseIds':[]},{'caseIds':['a1','a1']},{'repetitions':1.5},{'repetitions':True},{'preserveControls':False},{'preserveControls':1},{'conditions':['council']},{'outputs':[]}])
def test_benchmark_input_constraints(change):
    with pytest.raises(ValidationError):validate_contract(BenchmarkCreate,{**BENCHMARK,**change})

def test_benchmark_input_preserves_controls_without_executing():
    assert validate_contract(BenchmarkCreate,BENCHMARK)==BENCHMARK

def test_dataset_contract_preserves_null_and_typed_scalars():
    data={'columns':['label','number','missing','flag'],'rows':[['input',1,None,True]]}
    assert validate_contract(Dataset,data)==data
    with pytest.raises(ValidationError):validate_contract(Dataset,{'columns':['x'],'rows':[[1,2]]})
    with pytest.raises(ValidationError):validate_contract(Dataset,{'columns':['x'],'rows':[[1]],'serverPaginated':True})
    with pytest.raises(ValidationError):validate_contract(Dataset,{'columns':['x'],'rows':[[float('nan')]]})

def test_query_wire_names_and_numeric_text():
    assert validate_contract(DatasetQuery,{'page':'1','pageSize':'25','search':'','sort':'-1','direction':'asc'})=={'page':1,'pageSize':25,'search':'','sort':-1,'direction':'asc'}
    assert validate_contract(ReportListQuery,{'from':'','to':'2026-11-03','status':'','page':'2'})['page']==2
    for value in ['1.5','1.0','false']:
        with pytest.raises(ValidationError):validate_contract(ReportListQuery,{'page':value})
    with pytest.raises(ValidationError):validate_contract(DatasetQuery,{'page':1,'pageSize':10,'search':'','sort':-1,'direction':'asc'})

def test_metric_type_constraints_do_not_calculate_or_infer_measurements():
    unavailable={'key':'coverage','label':'Coverage','definition':'Owner-defined denominator','value':None,'unit':'rate','condition':'standard'}
    assert validate_contract(Metric,unavailable)==unavailable
    with pytest.raises(ValidationError):validate_contract(Metric,{**unavailable,'value':.5})
    with pytest.raises(ValidationError):validate_contract(Metric,{**unavailable,'value':1.5,'denominator':2})
    with pytest.raises(ValidationError):validate_contract(Metric,{**unavailable,'value':.5,'denominator':2,'numerator':3})
    with pytest.raises(ValidationError):validate_contract(Metric,{**unavailable,'value':1,'unit':'currency'})

def test_comparison_missing_values_are_required_nulls_not_omitted_zeroes():
    payload={'analysisA':'a','analysisB':'b','comparability':'unknown','reasons':[], 'dimensions':[{'key':'input','label':'Supplied field','a':None,'b':None,'relation':'unknown'}]}
    assert validate_contract(ComparisonResponse,payload)==payload
    del payload['dimensions'][0]['a']
    with pytest.raises(ValidationError):validate_contract(ComparisonResponse,payload)

@pytest.mark.parametrize('value',['javascript:alert(1)','//host.test/path','https://user:pass@host.test'])
def test_unsafe_link_schemes_and_credentials_rejected(value):
    with pytest.raises(ValidationError):TypeAdapter(PublicLink).validate_python(value,strict=True)

def test_public_integration_url_does_not_accept_private_query_tokens():
    with pytest.raises(ValidationError):TypeAdapter(IntegrationLink).validate_python('https://host.test?api_key=TEST_ONLY',strict=True)
    assert TypeAdapter(IntegrationLink).validate_python('/api/mcp',strict=True)=='/api/mcp'

def test_schema_export_contains_definitions_not_results(tmp_path):
    from evidencetwin_backend.export_contracts import export_contracts
    assert export_contracts(tmp_path)==len(SCHEMAS)
    analysis=json.loads((tmp_path/'Analysis.schema.json').read_text())
    assert 'id' in analysis['required']
    assert 'assessment' not in analysis['required']
    assert 'PRIVATE_TEST_VALUE' not in (tmp_path/'CapabilitiesResponse.schema.json').read_text()
