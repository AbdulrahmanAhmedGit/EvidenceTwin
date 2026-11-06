"""Endpoint inventory for handoff/tests; it does not register or implement routes."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Operation:
    blueprint: str
    function: str
    method: str
    path: str
    request_schema: str
    response_schema: str
    frontend_consumer: str
    owner_work: str
    status: int

OPERATIONS = (
    Operation(
        'system',
        'health',
        'GET',
        '/health',
        'No body',
        'HealthResponse',
        'api.ts health; ConnectionBadge',
        'Infrastructure liveness only',
        200,
    ),
    Operation(
        'system',
        'capabilities',
        'GET',
        '/capabilities',
        'No body',
        'CapabilitiesResponse',
        'workspace-api.ts / research hooks',
        'Owner service availability mapping',
        200,
    ),
    Operation(
        'system',
        'list_activity',
        'GET',
        '/activity',
        'ActivityQuery',
        'ActivityResponse',
        'workspace-api.ts getActivity',
        'services.activity: authorized real activity records',
        501,
    ),
    Operation(
        'analyses',
        'create_analysis',
        'POST',
        '/analyses',
        'multipart metadata: AnalysisCreateMetadata; repeated files parts',
        'AcceptedID',
        'api.ts createAnalysis; AnalysisBuilder',
        ('services.analyses: validate supplied metadata/files; authorize storage and '
 'invoke owner verification workflow; return ID only after actual acceptance'),
        501,
    ),
    Operation(
        'analyses',
        'list_analyses',
        'GET',
        '/analyses',
        'AnalysisListQuery',
        'AnalysisList',
        'workspace-api.ts getAnalyses; dashboard/history/compare selectors',
        ('services.analyses: authorized search/filter/sort and server pagination over '
 'real records'),
        501,
    ),
    Operation(
        'analyses',
        'get_analysis',
        'GET',
        '/analyses/<analysis_id>',
        'analysis_id path; no body',
        'Analysis',
        'research-api.ts readAnalysis; processing polling',
        ('services.analyses: retrieve authorized record and actual job state; return '
 'exactly the requested ID and no synthesized stages'),
        501,
    ),
    Operation(
        'analyses',
        'delete_analysis',
        'DELETE',
        '/analyses/<analysis_id>',
        'analysis_id path; no body',
        'ActionAcknowledgement or HTTP 204',
        'workspace-api.ts deleteAnalysis; history confirmation',
        ('services.analyses: authorize deletion and owner-defined retention semantics; '
 'acknowledge only confirmed deletion'),
        501,
    ),
    Operation(
        'analyses',
        'retry_analysis',
        'POST',
        '/analyses/<analysis_id>/retry',
        'analysis_id path; no body',
        'ActionAcknowledgement',
        'workspace-api.ts retryAnalysis; research-api.ts analysisAction',
        ('services.analyses: authorize retry, verify state/eligibility and request '
 'real owner job restart; return confirmed acknowledgement'),
        501,
    ),
    Operation(
        'analyses',
        'cancel_analysis',
        'POST',
        '/analyses/<analysis_id>/cancel',
        'analysis_id path; no body',
        'ActionAcknowledgement',
        'research-api.ts analysisAction; confirmation dialog',
        ('services.analyses: authorize cancellation and connect actual job transport; '
 'acknowledge request, expose resulting state via record reads'),
        501,
    ),
    Operation(
        'evidence',
        'get_analysis_evidence',
        'GET',
        '/analyses/<analysis_id>/evidence',
        'analysis_id path; no body',
        'SectionResponse (evidence fields)',
        'research-api.ts readAnalysisSection; EvidenceInspector',
        ('services.evidence: authorize access and map supplied/verified source, file, '
 'dataset and evidence-contract records; distinguish computed facts from '
 'source authentication'),
        501,
    ),
    Operation(
        'evidence',
        'get_analysis_dataset',
        'GET',
        '/analyses/<analysis_id>/dataset',
        'analysis_id path; DatasetQuery',
        'Dataset',
        'research-api.ts readDataset; DatasetViewer',
        ('services.evidence: apply authorized full-dataset search/sort and return the '
 'requested 25-row page with matching columns/page metadata; do not impute '
 'data'),
        501,
    ),
    Operation(
        'visualizations',
        'get_analysis_visualizations',
        'GET',
        '/analyses/<analysis_id>/visualizations',
        'analysis_id path; no body',
        'SectionResponse (visualizations/dataset fields)',
        'research-api.ts readAnalysisSection; VisualizationLab/overview',
        ('services.visualizations: map owner-generated immutable assets, rendering '
 'provenance and recorded controlled changes; serve only permitted assets and '
 'explicit missing-twin reasons'),
        501,
    ),
    Operation(
        'council',
        'get_analysis_council',
        'GET',
        '/analyses/<analysis_id>/council',
        'analysis_id path; no body',
        'SectionResponse (reviews/disagreements)',
        'research-api.ts readAnalysisSection; CouncilView',
        ('services.council: map actual owner independent/cross-review/judge results, '
 'citations, execution isolation and unresolved disputes; never infer truth '
 'from agreement'),
        501,
    ),
    Operation(
        'audit',
        'list_analysis_audit',
        'GET',
        '/analyses/<analysis_id>/audit',
        'analysis_id path; no body',
        'SectionResponse (events)',
        'research-api.ts readAnalysisSection; AuditTrail',
        ('services.audit: authorize real chronological events with actual '
 'timestamps/references; sanitize secrets before any serialization or download'),
        501,
    ),
    Operation(
        'reports',
        'get_analysis_report',
        'GET',
        '/analyses/<analysis_id>/report',
        'analysis_id path; no body',
        'SectionResponse (report/sections)',
        'research-api.ts readAnalysisSection; ResearchReport',
        ('services.reports: retrieve an authorized real report with evidence-linked '
 'plain text and genuine references; expose actual JSON permission'),
        501,
    ),
    Operation(
        'comparisons',
        'compare_analyses',
        'GET',
        '/comparisons',
        'ComparisonQuery (analysisA/analysisB)',
        'ComparisonResponse',
        'features/research/api.ts readComparison; Comparison',
        ('services.comparisons: authorize both records and use owner comparability '
 'rules to return supplied dimensions/reasons with matching requested IDs; do '
 'not invent a winner'),
        501,
    ),
    Operation(
        'benchmarks',
        'create_benchmark',
        'POST',
        '/benchmarks',
        'JSON BenchmarkCreate',
        'AcceptedID',
        'features/research/api.ts createBenchmark; BenchmarkBuilder',
        ('services.benchmarks: authorize and validate configuration/cases/model/rubric '
 'references; enforce owner control protocol and accept a real evaluation run; '
 'return its ID'),
        501,
    ),
    Operation(
        'benchmarks',
        'list_benchmarks',
        'GET',
        '/benchmarks',
        'BenchmarkListQuery',
        'BenchmarkList',
        'features/research/api.ts readBenchmarks; BenchmarkList',
        ('services.benchmarks: authorized paginated search/filter/sort over actual run '
 'metadata; do not produce synthetic metrics or progress'),
        501,
    ),
    Operation(
        'benchmarks',
        'get_benchmark',
        'GET',
        '/benchmarks/<benchmark_id>',
        'benchmark_id path; no body',
        'BenchmarkResponse',
        'features/research/api.ts readBenchmark; BenchmarkDetail polling',
        ('services.benchmarks: return the matching real run, configuration, actual '
 'measurements/denominators/failures and limitations; preserve unavailable '
 'metrics as null'),
        501,
    ),
    Operation(
        'reports',
        'list_reports',
        'GET',
        '/reports',
        'ReportListQuery',
        'ReportList',
        'features/research/api.ts readReports; Reports library',
        ('services.reports: authorize search/date/status/mode/sort and pagination over '
 'reports that actually exist; report per-record permissions'),
        501,
    ),
    Operation(
        'reports',
        'get_report',
        'GET',
        '/reports/<report_id>',
        'report_id path; no body',
        'SectionResponse (report/sections)',
        'features/research/api.ts readReport; report preview/export',
        ('services.reports: retrieve the authorized report resource and actual export '
 'permission; reconcile report ID to its analysis without leaking another '
 'record'),
        501,
    ),
    Operation(
        'reports',
        'delete_report',
        'DELETE',
        '/reports/<report_id>',
        'report_id path; no body',
        'ActionAcknowledgement or HTTP 204',
        'features/research/api.ts deleteReport; Reports confirmation',
        ('services.reports: authorize and delete only the intended report using owner '
 'retention policy; do not assume associated analysis deletion'),
        501,
    ),
    Operation(
        'integrations',
        'list_integrations',
        'GET',
        '/integrations',
        'No body',
        'IntegrationList',
        'features/research/api.ts readIntegrations; workspace management',
        ('services.integrations: return only public, configured/planned availability '
 'metadata and real requirements/tool names; never expose keys, signed tokens '
 'or invented installation packages'),
        501,
    ),
    Operation(
        'integrations',
        'test_integration',
        'POST',
        '/integrations/<integration_id>/test',
        'integration_id path; no body',
        'IntegrationTestResponse',
        'features/research/api.ts testIntegration; integration test action',
        ('services.integrations: authorize a configured connection test and report '
 'real reachable/failed status and check timestamp; this is not scientific '
 'validation or an MCP server implementation'),
        501,
    ),
    Operation(
        'cases',
        'list_research_cases',
        'GET',
        '/cases',
        'No body; query contract not yet defined',
        'JsonObject (owner contract pending)',
        'Reserved: React currently uses content/cases.ts locally',
        ('services.cases: agree the catalogue DTO with the owner/frontend before '
 'implementing authorized real case retrieval; do not copy educational '
 'fixtures into fake live results'),
        501,
    ),
    Operation(
        'cases',
        'get_research_case',
        'GET',
        '/cases/<case_id>',
        'case_id path; no body',
        'JsonObject (owner contract pending)',
        'Reserved: React currently uses content/cases.ts locally',
        ('services.cases: agree the case DTO before implementing authorized real '
 'source/data/provenance retrieval; retain sample labels and unavailable '
 'uncertainty when appropriate'),
        501,
    ),
)
