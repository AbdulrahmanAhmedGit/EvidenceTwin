# EvidenceTwin V1 — R04 source retrieval, proof and temporal contracts

Author: Abdulrahman Ahmed. Date: 2026-11-06.

**Status: Recommended for owner approval.** This refines R04 after approval to continue from the [statistical contract](STATISTICAL_CONTRACTS_DRAFT.md). **All 24 gates remain OPEN.** Source connectors, parsers, canonicalization/status predicates, archive acceptance rules, isolation mechanisms, numeric limits and final schemas are not selected. No production implementation, deployment or capability enablement is authorized. All acceptance obligations are unexecuted specifications.

Partially Supported remains a proposed/unresolved claim verdict. Source Verified is an authenticity/provenance assessment under an approved source policy, not proof that the publication's scientific conclusions or supplied claims are correct.

## 1. Distinct source objects and facts

| Logical object | Required distinction |
| --- | --- |
| Supplied reference | What the researcher claims the source is: URL/identifier, title, publisher, date and relationship to the claim. Supplied metadata is not established metadata. |
| Official record | Attributable publisher/repository record used to establish source identity/version under a reviewed procedure. A familiar domain or matching title alone is insufficient. |
| Retrieval attempt | One actual attempt with original/final locations, connection/result facts, time, limits, failure/partial-content reason and authorized case scope. |
| Source snapshot | Accepted retained content with stable identity, exact artifact/hash/version references and retrieval provenance. An incomplete response cannot masquerade as the complete source. |
| Extracted evidence | Versioned extraction with exact document/table/cell/chart locators, parser/configuration and interpretation limitations. Extraction is separate from authentication. |
| Source assessment | Applicable policy/check results and status for the declared snapshot/scope/time, with blockers and known discrepancies. |
| Claim binding | Which assertion uses which exact source passage/value/dataset version; researcher intent is distinct from proof that the binding is correct. |

All records remain authorized and revision-aware. Public source identity does not grant access to another researcher's private snapshot or annotations. Repeated URL/title/hash alone cannot establish that two research evaluations share the same authenticated source version.

## 2. Retrieval request and result contracts

### Request

Identify the authorized case, source-reference revision, claimed source family, permitted retrieval purpose, original location, source-policy revision, required content scope and the bounded retrieval configuration. The request must not import application credentials, provider keys or unrelated private network access into the retrieval boundary.

Request-controlled URL components, redirects and retries remain untrusted. Concrete parsing/canonicalization, host eligibility and connector rules require approval. Preserve original and derived location identities without silently stripping meaningful version/query/path information. Do not expose secret-bearing locations or request credentials in public source manifests or ordinary logs.

### Result

Retain actual request/final locations and redirect provenance; observation time; relevant safe transport/response facts; claimed/detected type; accepted/partial byte scope; retained artifact/hash algorithm/reference; limits encountered; safe error/retry information and the producing task identity. Connection success/HTTP success/content availability remain separate from authenticity and source completeness.

A timeout, blocked destination, unreadable response, unsupported type, truncated body and official-record mismatch are distinct conditions. Partial bytes may be retained under policy as a failed/limited attempt, but they do not establish a full-source snapshot or a completed content check. A login/challenge/error page returned successfully is not automatically the requested scientific document.

## 3. Isolated retrieval and parsing boundary

The recommended Q12 direction requires enforced network isolation, not simply another process. Apply approved protocol/destination rules to DNS resolution, connection and any redirects/retries; prevent access to private/infrastructure metadata destinations and avoid unchecked re-resolution. Bound response, decompression, parse resources and time. Do not forward application cookies/secrets to sources. [OWASP SSRF guidance](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html) is a reference for connection-time and network controls, not a selected implementation.

Use a controlled task/artifact handoff rather than granting the retrieval process unrestricted application DB/object-store credentials or private-service reachability. Exact isolation, egress, handoff permissions and acceptance/reconciliation mechanisms remain D03/D06 design decisions. Parser/content instructions cannot modify the scientific policy, request new secrets or grant additional network access.

Source content may refer to additional files, scripts, embeds or remote resources. Those are new retrieval candidates subject to explicit approved scope and the same boundary, not automatically executed/fetched dependencies. Active content, workbook code/external links and unsupported OCR remain outside an implicitly trusted extraction path.

## 4. Common source-proof contract

Each proof record binds the exact source/snapshot/claim scope, check/policy/procedure version, applicability, performed/unperformed facts, requirement determination, establishing evidence locator, known discrepancies, limitations and next evidence required. The canonical Separate Typed Axes validator applies; proof-field presence alone does not validate correspondence.

| Proof class | Proposed procedure obligation | Required evidence/result |
| --- | --- | --- |
| Identity | Establish attributable publisher/repository and the relevant official record, distinguishing original from secondary/mirror/repost. | Official-record provenance, claimed versus established organization/identifier and procedure that established the relation. |
| Canonical location | Establish the canonical record/artifact relation under an approved rule, retaining redirects and meaningful location/version information. | Supplied/original/canonical/final locations and why they refer to the assessed object. A redirect alone is not authenticity proof. |
| Publication metadata | Compare title, authors/organization where applicable, date and publication identifier with the actual official record and content. | Field-level observed matches/discrepancies/unknowns, locators and policy-defined applicability. No generated metadata fills gaps. |
| Version/integrity | Establish exact content/version and its relation to the official record; preserve retrieved bytes and cryptographic hash. | Artifact/hash/version references and evidence linking them. Hash proves retained content identity, not the publisher or publication date. |
| Content inspection | Inspect the relevant source material rather than only metadata/abstracts. | Actual passages/tables/cells/figures and bounded extraction/coverage facts with locators. |
| Data provenance | Establish provider, dataset/version documentation, variable/unit/collection definitions and relevant transformations. | Traceable original-to-derived lineage and missing provenance, scoped to the actual numerical finding. |
| Submission correspondence | Compare supplied charts/values/excerpts with the original in context, including labels/units/time/denominators. | Specific observed agreement/discrepancy and transformations; unexplained differences remain blockers/findings. |
| Publication notices | Inspect applicable official correction/retraction/revision records; supplementary registry information is discovery evidence only until matched. | Search scope/time, exact notices or absence observed within scope, affected source versions/claims and unknown coverage. |

Source authenticity and scientific reliability must not be collapsed. An authentic corrected/retracted source may still be accurately attributed, while affected scientific conclusions need separate assessment. A source identity mismatch is an observed provenance issue, not automatic proof that every substantive claim is false.

## 5. Source-family procedure sheets

These are procedure contracts to make connector development testable. They do not select a site-specific API, selector, parser library, registry or operational connector.

### Official publisher HTML

1. Resolve the claimed publication to an attributable official record using an approved identity procedure.
2. Retain the exact inspected content/snapshot and observed metadata; distinguish publication data from navigation, abstracts, update banners and unrelated page material.
3. Locate the relevant assertion/table/figure and preserve surrounding context, units and methodological references.
4. Establish links to any original dataset/version rather than assuming a nearby download is the report's actual input.
5. Inspect applicable official notices and record what could not be inspected.

Unsupported dynamic rendering or missing relevant content remains an extraction/content blocker. A successful page download does not establish that all figures or linked files were inspected.

### Official CSV/XLSX download

1. Establish the official release/reference record and its relation to the requested artifact.
2. Retain exact bytes, accepted type/encoding information, hash/version and actual retrieval time.
3. Bind documentation/provider/variables/units and dataset scope to the inspected records.
4. Apply approved bounded ingestion, worksheet/formula/selection and transformation rules; keep source authenticity and parsing correctness separate.
5. Match reported numerical findings to their exact data records and inspect revision notices.

A valid file format, matching rounded figure or familiar filename does not prove publication-time identity. Unsupported/excluded sheets/ranges cannot count as inspected evidence for dependent claims.

### Versioned repository record

1. Establish the official repository/publisher and persistent record identity.
2. Identify the relevant release/version and artifact relation, including mutable versus specifically versioned metadata.
3. Retain content/documentation, published checksums where applicable, observed integrity and revision history.
4. Match the relevant data/content to its claimed record/version and inspect applicable notices.

A persistent identifier is useful attribution evidence, not a content-integrity or correctness guarantee. The [DOI Foundation](https://www.doi.org/the-identifier/what-is-a-doi/) describes persistent identification and updateable associated metadata; therefore the assessed artifact/version still needs an explicit binding. No DOI/registry connector is selected here.

### Bounded text-based research PDF

1. Establish the official publication/repository record and match title/authors/date/identifier/version against retained content.
2. Retain exact PDF bytes/hash and accepted bounded extraction configuration.
3. Locate relevant pages/sections/tables/figures and record extraction/layout ambiguity and actually inspected scope.
4. Match quoted values/excerpts in context and link required datasets/methodology.
5. Inspect official notices and retain version-specific findings.

Text extraction alone does not validate a chart image, table reconstruction or underlying numerical dataset. Scanned/unreadable relevant content remains unavailable under the unapproved OCR pipeline. No parser/renderer is selected by these steps.

## 6. Source status and availability semantics

The four agreed source labels remain Verified, Partially Verified, Unverified and Inaccessible. Their final machine predicates, precedence and time/freshness policy still require approval; this draft states constraints rather than silently selecting a full classifier.

| Label | Constraint to preserve |
| --- | --- |
| Verified | All applicable mandatory identity/authenticity/integrity/content/provenance requirements established under the approved family policy. Optional/unknown information remains disclosed. This is not scientific correctness. |
| Partially Verified | Identity is established but important verification remains incomplete, under an explicit intermediate predicate still to be specified. Do not infer it from a count of arbitrary passed checks. |
| Unverified | Authenticity/provenance is not sufficiently established. Retain known negative findings separately; the label must not conceal a demonstrated discrepancy or imply a verdict about claim truth. |
| Inaccessible | Relevant content cannot currently be retrieved/inspected under the recorded attempt/policy. This is not evidence of falsity, inauthenticity or unreliability by itself. |

A failed mandatory source check cannot yield Verified. Exact classification for established identity plus conflicting metadata, or failed current retrieval with an existing retained snapshot, remains an explicit policy question. Preserve the facts rather than inventing an unapproved priority rule.

Store retrieval availability per attempt separately from snapshot-bound source assessment. A later outage does not silently rewrite an earlier authenticated snapshot. Conversely, an old assessment must not be displayed as a new current-content check. Display the assessed version/time and the actual latest retrieval result. Freshness/revalidation rules remain OPEN.

## 7. Corrections, retractions and change attribution

Notice discovery records where/when it searched, which official records/content were available, exact notice identity/date/type, affected versions and any content-matching uncertainty. Supplemental registry results require attributable matching, not automatic acceptance.

An empty bounded search means no notice was observed within that search scope, not proof that no notice exists anywhere. Inaccessible notice records remain Unknown/unperformed as applicable; they cannot silently pass a mandatory notice requirement.

Determine impact at claim/evidence level: a correction may change a table, methodology or interpretation without invalidating every fact in the source. Retain the official notice and affected evidence, and record whether the scientific impact can be established. An AI explanation cannot invent the reason or extent of a revision.

## 8. Historical/current identity and revision comparisons

### Historical binding request

Identify the exact publication/assertion date/version, claimed historical dataset and methodology, relevant original report values/precision and the attributable proof needed to connect those inputs at publication. Candidate proof includes official versioned releases, attributable dated archives or publisher-attributed historical files with sufficient provenance; exact acceptance rules remain OPEN.

Preserve the proof artifact and its relationship to exact dataset/methodology bytes or identifiers under the approved policy. A version label by itself needs its official-record/artifact relation established. A new retrieval hash proves what was retained now; it does not establish that those bytes existed at publication.

Retrieval time, a Last-Modified header, a familiar filename or a later numerical match alone cannot establish the historical binding. If required proof is missing, the historical assessment remains Historical Verification Incomplete rather than Historically Supported or Contradicted.

### Current binding and refresh

Researcher-triggered refresh creates a new snapshot and assessment with its actual identified dataset/methodology/version and retrieval metadata. Preserve the previous current and historical records. No scheduled refresh is implicitly implemented or approved.

The comparison records reported value/precision, historically reproduced value only where the historical binding is established, independently reproduced current value and exact evidence/methodology references. Distinguish a report-associated reference computation from authenticated historical reproduction.

Record signed/absolute differences, units and relative base, documented revision dates/reasons and interpretation effect. Unknown reasons remain unknown. Different numbers can leave a rounded claim unchanged; do not infer a changed conclusion without the approved precision/applicability rule.

## 9. Source-to-submission comparison contract

The request binds uploaded chart/dataset/excerpt and original source evidence to exact revisions, with a declared comparison dimension. Output identifies which values, labels, units, timeframes, denominators, visual content or excerpt context were compared, how they were matched and any recorded transformations.

Confirmed researcher bindings help resolve intent but do not establish actual correspondence. Image-only approximate readings cannot silently become exact numerical data. Missing original visual content blocks that fidelity check without hiding bounded observations from the supplied chart.

An unexplained mismatch remains a specific finding/blocker. Do not “repair” the source or uploaded evidence in place, infer a transformation after the fact or silently choose whichever version supports the claim. Any new evidence/correction creates an attributable revision and reassessment scope.

## 10. Publication, privacy and reproducibility

Validate all proof/assessment records with the canonical whole-record contract and current guarded publication context. Invalid source proof is not fixed by a believable narrative. Partially Supported cannot be used as a convenient final outcome for unresolved provenance or correspondence.

An eligible incomplete report may show retained source proof, arithmetic and limitations; it cannot be marked fully verified while a mandatory source/historical requirement remains unestablished. Source status remains separate from scientific claim verdict and report coverage/conclusion.

Retained snapshots obey private ownership, content rights, approved retention and deletion/export policies. Artifact references must not grant unrestricted access; a public source URL does not make private annotations/case membership public. A hash without retained/accessible permitted content cannot support an unconditional reproducibility promise after deletion.

## 11. Acceptance obligations — unexecuted specifications

| ID | Required future observable behavior |
| --- | --- |
| SP01 | HTTP success, known domain, DOI/title match or hash alone cannot create Source Verified. |
| SP02 | Partial/error/login content cannot masquerade as a complete relevant scientific snapshot. |
| SP03 | DNS/connection/redirect/retry policy blocks unauthorized destinations without leaking credentials or reaching private infrastructure. |
| SP04 | Unsupported render/PDF/OCR/worksheet extraction stays explicit; dependent content is not reported inspected. |
| SP05 | Claimed versus established metadata and known discrepancies remain separately traceable. |
| SP06 | Original, secondary, mirrored and reposted content retain their actual attribution/provenance relationships. |
| SP07 | Corrected/retracted but authentic sources keep identity separate from claim-specific notice impact. |
| SP08 | Unknown or bounded-negative notice discovery is not fabricated as exhaustive absence of notices. |
| SP09 | Source/dataset/version/methodology bindings reject a merely matching number or later timestamp as historical proof. |
| SP10 | Current refresh creates new immutable evidence/results without overwriting historical/current predecessors. |
| SP11 | Current unreachability does not silently rewrite the assessment of a retained historical snapshot or imply fresh inspection. |
| SP12 | Uploaded values/chart labels/units/time/denominators/excerpts are checked in context; unexplained differences remain visible. |
| SP13 | Unknown revision date/reason remains unknown; numerical change alone does not establish changed interpretation. |
| SP14 | Cross-account proof/snapshot/publication access is denied and does not reveal protected case existence. |
| SP15 | Missing mandatory source proof keeps verification incomplete while eligible completed work remains inspectable. |
| SP16 | Partially Supported remains unresolved; source deficiencies cannot be silently mapped to that final verdict. |

No SP case has executed or passed. The [Ember reference investigation](ember-2025-acceptance/acceptance_case.md) still lacks established publication-time dataset/methodology identity and original-chart inspection; it is not a successful end-to-end acceptance case.

## 12. Open specification record and next step

Still OPEN: concrete official-record/connectors; canonicalization and content matching; intermediate source-status/precedence/freshness predicates; notice search coverage; archive/historical proof rules; hash/schema definitions; isolation/handoff implementation; limits/retention/rights; reviewed expected artifacts and actual acceptance evidence.

The source procedure contracts now make retrieval, identity, content, data lineage, notices, time and claim correspondence independently testable. References checked on 2026-11-06: official [OWASP SSRF guidance](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html) and [DOI Foundation description](https://www.doi.org/the-identifier/what-is-a-doi/). No retrieval connector, parser, library or provider is selected by those references; no scientific-source retrieval or acceptance execution occurred during drafting.

R05 confirmation/revision contracts are the next ordered refinement. **Status remains Recommended for owner approval; all 24 gates remain OPEN.**
