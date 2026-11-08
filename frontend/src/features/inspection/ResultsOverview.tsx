import {useState} from 'react'
import {useQuery} from '@tanstack/react-query'
import {Link} from 'react-router-dom'
import {readAnalysisSection} from '../../research-api'
import type {Analysis, Reviewer, SectionData} from '../../research-api'
import {verdictNames} from '../../workspace-api'
import {ResearchText} from '../../research-display'
import {ComparisonFigure} from './EvidenceFindings'
import {useEvidenceProcessing} from './evidence-processing'
import {researchTitle} from '../../research-title'
import {structuredReview} from './review-output'
import CoverageList from './CoverageList'
import {Citation} from './shared'
import {apiBase} from '../../api'
import {safeUrl} from './utils'
import './results-overview.css'

const roleNames: Record<string,[string,string]> = {
  visual:['Visual analyst','المحلل البصري'], statistical:['Statistical auditor','المدقق الإحصائي'],
  scientific:['Scientific skeptic','المراجع العلمي'], counterfactual:['Counterfactual analyst','محلل السيناريو البديل'],
}
const categoryNames: Record<string,[string,string]> = {
  evidence_gap:['Missing evidence','الأدلة الناقصة'],
  evidence_scope:['Evidence scope','نطاق الأدلة'], missing_evidence:['Missing evidence','الأدلة الناقصة'], verification_gap:['Verification gaps','فجوات التحقق'], method_limitation:['Method limitations','حدود المنهج'], unavailable_capability:['Unavailable methods','الطرق غير المتاحة'], processing_constraint:['Data selection and processing','اختيار البيانات ومعالجتها'], processing_failure:['Source access and extraction','إتاحة المصادر واستخراجها'],
  evidence:['Missing evidence','الأدلة الناقصة'], source:['Source access','إتاحة المصادر'],
  verification:['Source verification','التحقق من المصادر'], statistical:['Statistical methods','الطرق الإحصائية'],
  visualization:['Visualization','التصورات'], methodology:['Methods and scope','المنهجية والنطاق'],
  capability:['Unavailable methods','الطرق غير المتاحة'], 'ai-interpretation':['AI interpretation','تفسير الذكاء الاصطناعي'],
}
function Perspective({review,id,ar}:{review:Reviewer;id:string;ar:boolean}) {
  const t=(en:string,arabic:string)=>ar?arabic:en
  const output=review.report?.output
  const findings=output&&typeof output==='object'&&'findings' in output&&Array.isArray(output.findings)?output.findings:[]
  const assessments=output&&typeof output==='object'&&'claim_assessments' in output&&Array.isArray(output.claim_assessments)?output.claim_assessments:[]
  const positions:Record<string,[string,string]>={supports:['Supports','يدعم'],partially_supports:['Partially supports','يدعم جزئياً'],contradicts:['Contradicts','يناقض'],cannot_assess:['Cannot assess','يتعذر التقييم']}
  const first=findings[0]
  const title=first&&typeof first==='object'&&'title' in first&&typeof first.title==='string'?first.title:review.findings[0]
  const role=roleNames[review.roleKey||'']?.[ar?1:0]||review.role
  return <details className="result-perspective">
    <summary><strong dir="auto">{role}</strong><span dir="auto">{title||t('Read the recorded perspective','اقرأ الرأي المسجل')}</span></summary>
    <p className="caption">{t('AI reviewer · ','مراجع بالذكاء الاصطناعي · ')}{review.status==='completed'?t('Review recorded','مراجعة مسجلة'):t('Completion not confirmed','الاكتمال غير مؤكد')}</p>
    {assessments.map((claim,index)=>claim&&typeof claim==='object'&&'position' in claim&&typeof claim.position==='string'&&positions[claim.position]?<p key={index}>{t('AI position on claim','موقف الذكاء الاصطناعي من الادعاء')} {index+1} · {positions[claim.position][ar?1:0]}</p>:null)}
    <ResearchText text={review.summary}/>
    {review.uncertainty.length>0&&<ul>{review.uncertainty.map((note,index)=><li dir="auto" key={index}>{note}</li>)}</ul>}
    <div className="citation-list">{review.citations.map(ref=><Citation key={ref} id={ref} analysisId={id} ar={ar}/>)}</div>
    <Link to={`/app/analyses/${encodeURIComponent(id)}/council`}>{t('Full output and provenance','المخرجات الكاملة ومنشؤها')}</Link>
  </details>
}

export default function ResultsOverview({analysis:a,ar}:{analysis:Analysis;ar:boolean}) {
  const t=(en:string,arabic:string)=>ar?arabic:en
  const base=`/app/analyses/${encodeURIComponent(a.id)}`
  const processing=useEvidenceProcessing(a.id)
  const council=useQuery({queryKey:['analysis',a.id,'council'],queryFn:({signal})=>readAnalysisSection(a.id,'council',signal),retry:false,staleTime:15000})
  const evidence=useQuery({queryKey:['analysis',a.id,'evidence'],queryFn:({signal})=>readAnalysisSection(a.id,'evidence',signal),retry:false,staleTime:15000})
  const visuals=useQuery({queryKey:['analysis',a.id,'visualizations'],queryFn:({signal})=>readAnalysisSection(a.id,'visualizations',signal),retry:false,staleTime:15000})
  const [panel,setPanel]=useState<'charts'|'data'|'sources'>('charts')
  const data=processing.data
  const tables=data?.historical?[]:data?.datasets||[]
  const comparisons=tables.flatMap(table=>table.comparisons.map(comparison=>({comparison,table})))
  const sources=data?.sources||(data?.source?[data.source]:[])
  const independent=council.data?.reviews?.filter(review=>review.phase==='independent')||[]
  const disagreements=council.data?.disagreements||[]
  const limitations=data?.limitations||[]
  const groups=new Map<string,typeof limitations>()
  for (const item of limitations) {
    const group=groups.get(item.category)||[]
    group.push(item)
    groups.set(item.category,group)
  }
  const original=safeUrl(visuals.data?.visualizations?.original||'')
  const files=evidence.data?.files||[]
  const imageFiles=files.filter(file=>file.mediaType.startsWith('image/')&&safeUrl(file.url||''))
  const dataset=evidence.data?.dataset
  const visualReview=independent.find(review=>review.roleKey==='visual'||review.role==='Visual Analyst')
  const visualOutput=structuredReview.safeParse(visualReview?.report?.output)
  const visualFindings=visualOutput.success?visualOutput.data.findings:(visualReview?.findings||[]).map((finding,index)=>({finding_id:String(index),title:researchTitle(finding),observation:finding,why_it_matters:'',recommendation:'',evidence_refs:visualReview?.citations||[]}))
  const assessment=a.assessment||'not_evaluated'
  return <div className="results-workspace">
    <div className="results-introduction">
      <section className="result-assessment" aria-labelledby="result-assessment-title">
        <div className="assessment-heading"><h2 id="result-assessment-title">{t('Visual assessment','التقييم البصري')}</h2><span>{t('AI visual review','مراجعة بصرية بالذكاء الاصطناعي')}</span></div>
        <p className="result-verdict">{council.isPending?t('Loading the visual review…','جارٍ تحميل المراجعة البصرية…'):visualReview?.status==='completed'?(visualFindings.length?t('Potential visual issues reported','أُبلغ عن مشكلات بصرية محتملة'):t('No structured visual issues recorded','لم تُسجل مشكلات بصرية منظمة')):t('Visual assessment unavailable','التقييم البصري غير متاح')}</p>
        <p className="assessment-qualification">{t('Examine the original chart and the cited evidence. A non-zero baseline, logarithmic scale or unusual encoding alone does not establish misleading presentation.','افحص الرسم الأصلي والأدلة المشار إليها. لا يثبت خط أساس غير صفري أو مقياس لوغاريتمي أو ترميز غير مألوف وحده أن العرض مضلل.')}</p>
        {visualReview?.summary&&<details className="visual-review-opening"><summary>{t('Read the recorded visual interpretation','قراءة التفسير البصري المسجل')}</summary><ResearchText text={visualReview.summary}/></details>}
        <p className="caption">{t('Independent confirmation and clinical implications require supporting evidence. No validated misleading-plot verdict is recorded by this interface.','يتطلب التأكيد المستقل والآثار الطبية أدلة داعمة. لا تسجل هذه الواجهة حكماً معتمداً بأن الرسم مضلل.')}</p>
      </section>
      <details className="result-original-question"><summary>{t('Original question or inspection request','السؤال الأصلي أو طلب الفحص')}</summary>{(a.claims?.length?a.claims:[a.claim]).map((claim,index)=><ResearchText key={index} text={claim}/>)}</details>
      <nav className="result-section-links" aria-label={t('On this page','في هذه الصفحة')}>
        <a href="#result-findings">{t('Visual issues','المشكلات البصرية')}</a><a href="#result-council">{t('Council','المجلس')}</a><a href="#result-limitations">{t('Limitations','الحدود')}</a><a href="#result-coverage">{t('Checks performed','الفحوص المنفذة')}</a>
      </nav>
    </div>
    <aside className="results-evidence" aria-label={t('Plot comparison','مقارنة الرسوم')}>
      <div className="result-evidence-heading"><h2>{t('Plot comparison','مقارنة الرسوم')}</h2><Link to={base+'/evidence'}>{t('Open inspector','فتح الفاحص')}</Link></div>
      <div className="result-evidence-switch" role="group" aria-label={t('Evidence view','عرض الأدلة')}>{(['charts','data','sources'] as const).map((key,index)=><button key={key} aria-pressed={panel===key} onClick={()=>setPanel(key)}>{(ar?['الرسوم','البيانات','المصادر']:['Charts','Data','Sources'])[index]}</button>)}</div>
      <div className="result-evidence-content">
        {panel==='charts'&&<><section className="result-original-visuals"><h3>{t('Original scientific chart','الرسم العلمي الأصلي')}</h3>{imageFiles.length?imageFiles.map(file=><figure key={file.id}><a href={safeUrl(file.url||'')} target="_blank" rel="noreferrer"><img src={safeUrl(file.url||'')} alt={file.name}/></a><figcaption><bdi>{file.name}</bdi> · {t('Submitted image','صورة مقدمة')}</figcaption></figure>):original?<figure><a href={original} target="_blank" rel="noreferrer"><img src={original} alt={t('Original submitted visualization','التصور الأصلي المقدم')}/></a><figcaption>{t('Original submitted visualization','التصور الأصلي المقدم')}</figcaption></figure>:<p className="caption">{visuals.isPending?t('Loading original assets…','جارٍ تحميل الملفات الأصلية…'):t('No original image is available in this record.','لا تتوفر صورة أصلية في هذا السجل.')}</p>}<Link to={base+'/visualizations'}>{t('Inspect chart scale and provenance','فحص مقياس الرسم ومنشئه')}</Link></section>      <section className="result-blind-optics"><h3>{t('Blind Optics','البصريات المعماة')}</h3><strong>{t('Independent reconstruction unavailable','إعادة البناء المستقلة غير متاحة')}</strong><p>{t('An approved blinding and rendering protocol has not been implemented. The charts above show recorded descriptive calculations or original images. No validated neutral reconstruction or framing judgment was performed.','لم يُنفذ بروتوكول تعمية ورسم معتمد. تعرض الرسوم أعلاه الحسابات الوصفية المسجلة أو الصور الأصلية. لم تُنفذ إعادة بناء محايدة معتمدة أو تقييم للتأطير البصري.')}</p><Link to={base+'/visualizations'}>{t('Visualization methods and limits','طرق التصور وحدوده')}</Link></section><section className="supporting-chart-calculations"><h3>{t('Supporting numerical checks','الفحوص الرقمية الداعمة')}</h3>{comparisons.map(({comparison,table})=><div key={comparison.id}><ComparisonFigure data={comparison} ar={ar}/><p className="caption">{t('Source','المصدر')} · <bdi>{table.filename||table.evidenceId}</bdi></p></div>)}{!comparisons.length&&<p className="evidence-empty">{processing.isPending?t('Loading recorded calculations…','جارٍ تحميل الحسابات المسجلة…'):t('No reproducible comparison chart is available for this run. Inspect the original chart and source records for available evidence.','لا يتوفر رسم مقارنة قابل للتكرار لهذا التشغيل. افحص الرسم الأصلي وسجلات المصادر للأدلة المتاحة.')}</p>}
        </section></>}
        {panel==='data'&&<>{tables.map(table=><article className="result-data-record" key={table.evidenceId}><h3 dir="auto">{table.filename||t('Retrieved table','جدول مسترجع')}</h3><p>{table.rowCount.toLocaleString(ar?'ar':'en')} {t('parsed rows','صف محلل')}</p><details><summary>{t('Columns and provenance','الأعمدة والمنشأ')}</summary><p dir="auto">{table.columns.join(' · ')}</p><p className="record-hash"><bdi>{table.sha256}</bdi></p><p className="record-hash"><bdi>{table.revisionId}</bdi></p></details></article>)}{dataset&&<ObservationTable data={dataset} ar={ar}/>}<Link to={base+'/evidence?category=dataset'}>{t('Inspect and query the original data','فحص البيانات الأصلية والاستعلام عنها')}</Link>{!tables.length&&!dataset&&<p>{t('No structured numerical table is available. Upload a supported CSV or JSON dataset in the investigation for a new review.','لا يتوفر جدول رقمي منظم. ارفع بيانات CSV أو JSON مدعومة في البحث لإجراء مراجعة جديدة.')}</p>}</>}
        {panel==='sources'&&<>{sources.map((source,index)=><article className="result-source-record" key={source.evidenceId||source.url}><h3>{t('Source','المصدر')} {index+1}</h3><p><a href={safeUrl(source.url)} target="_blank" rel="noreferrer"><bdi>{source.url}</bdi></a></p><p>{source.status==='retrieved'?t('Retrieved · authenticity unverified','مسترجع · الأصالة غير متحققة'):t('Content not retrieved','لم يُسترجع المحتوى')}</p>{source.reason&&<p dir="auto">{source.reason}</p>}{source.status==='retrieved'&&<a href={`${apiBase}/analyses/${encodeURIComponent(a.id)}/source-snapshot?sourceId=${encodeURIComponent(source.evidenceId||'retrieved-source')}`} download>{t('Download retained snapshot','تنزيل النسخة المحفوظة')}</a>}</article>)}{!sources.length&&<p>{t('No source retrieval was recorded. Links inside older research questions require a new authorized review to be processed.','لم يُسجل استرجاع مصادر. تتطلب الروابط داخل الأسئلة القديمة مراجعة جديدة مصرحاً بها لمعالجتها.')}</p>}<Link to={base+'/evidence'}>{t('Inspect all sources and files','فحص جميع المصادر والملفات')}</Link></>}
        {(evidence.error||visuals.error)&&<p className="notice error">{t('Some evidence could not be loaded. Open the inspector to retry.','تعذر تحميل بعض الأدلة. افتح الفاحص للمحاولة مجدداً.')}</p>}
      </div>

    </aside>
    <div className="results-narrative">
      <section id="result-findings" className="result-section">
        <h2>{t('Detected visual concerns','الملاحظات البصرية المكتشفة')}</h2>
        <p className="caption">{t('AI observations and suspected issues. Inspect the evidence before treating a concern as established.','ملاحظات ومشكلات مشتبه بها من الذكاء الاصطناعي. افحص الأدلة قبل اعتبار الملاحظة ثابتة.')}</p>
        <div className="result-recorded-findings">{visualFindings.slice(0,3).map(finding=><details key={finding.finding_id}><summary dir="auto">{finding.title}</summary><ResearchText text={finding.observation}/>{finding.why_it_matters&&<><h3>{t('Why it matters','لماذا تهم')}</h3><ResearchText text={finding.why_it_matters}/></>}{finding.recommendation&&<><h3>{t('Suggested correction','التصحيح المقترح')}</h3><ResearchText text={finding.recommendation}/></>}<div className="citation-list">{finding.evidence_refs.map(ref=><Citation key={ref} id={ref} analysisId={a.id} ar={ar}/>)}</div></details>)}</div>
        {!visualFindings.length&&<p>{t('No structured visual findings were supplied. Inspect the original reviewer record for its explanation and limits.','لم تُقدم نتائج بصرية منظمة. افحص سجل المراجع الأصلي لشرحه وحدوده.')}</p>}
        <Link to={base+'/council'}>{t('Inspect all visual findings and reviewer evidence','فحص جميع النتائج البصرية وأدلة المراجعين')}</Link>
        <details className="supporting-claim-assessment"><summary>{t('Supporting claim assessment and calculations','تقييم الادعاء والحسابات الداعمة')}</summary><p>{verdictNames[assessment][ar?1:0]}</p>{a.suggestedInterpretation&&<ResearchText text={a.suggestedInterpretation}/>}        {comparisons.length>0&&<ul className="result-observations">{comparisons.map(({comparison:c})=><li key={c.id}><span dir="auto">{c.indicator} · <bdi>{c.year}</bdi></span><p>{c.observations.map((value,index)=><span key={value.rowNumber}>{index>0?' / ':''}<bdi>{value.label}</bdi> <strong><bdi>{value.value}{c.unit||''}</bdi></strong></span>)}</p><p className="caption">{t('Difference, first minus second','الفرق، الأول ناقص الثاني')} <bdi>{c.difference}</bdi> {c.unit==='%'?t('percentage points','نقطة مئوية'):c.unit||t('in supplied units','بالوحدات المقدمة')}</p></li>)}</ul>}
{a.findings.map((finding,index)=><details key={finding.id||index}><summary dir="auto">{researchTitle(finding.text)}</summary><ResearchText text={finding.text}/><div className="citation-list">{finding.citations.map(ref=><Citation key={ref} id={ref} analysisId={a.id} ar={ar}/>)}</div></details>)}</details>
        <div className="result-scope"><h3>{t('What this does not establish','ما لا تثبته النتائج')}</h3><p>{t('Descriptive values and Council interpretations do not independently establish source authenticity, causation or statistical significance. Unperformed checks remain explicit below.','لا تثبت القيم الوصفية وتفسيرات المجلس بمفردها أصالة المصدر أو السببية أو الدلالة الإحصائية. تظهر الفحوص غير المنفذة بوضوح أدناه.')}</p></div>
      </section>
      <section id="result-council" className="result-section">
        <div className="result-section-heading"><h2>{t('Council perspectives','وجهات نظر المجلس')}</h2><Link to={base+'/council'}>{t('Inspect all reviews','فحص جميع المراجعات')}</Link></div>
        <p className="caption">{t('AI interpretations of the submitted evidence. Agreement is not scientific proof.','تفسيرات بالذكاء الاصطناعي للأدلة المقدمة. الاتفاق ليس برهاناً علمياً.')}</p>
        {independent.map(review=><Perspective key={review.id} review={review} id={a.id} ar={ar}/>)}
        {!independent.length&&<p>{council.isPending?t('Loading recorded perspectives…','جارٍ تحميل الآراء المسجلة…'):t('No independent review records are available.','لا تتوفر سجلات مراجعة مستقلة.')}</p>}
        {council.error&&<button onClick={()=>council.refetch()}>{t('Retry Council records','إعادة تحميل سجلات المجلس')}</button>}
        <div className="result-disagreements"><h3>{t('Disagreements','الخلافات')}</h3>{disagreements.length?disagreements.map((item,index)=><details key={item.id||index}><summary dir="auto">{item.claim}</summary><p className="caption">{item.status==='resolved'?t('Resolution recorded','سُجل حسم للخلاف'):t('Resolution not established','لم يثبت حسم الخلاف')}</p><ul>{item.positions.map((position,i)=><li key={i} dir="auto">{position}</li>)}</ul>{item.resolution&&<ResearchText text={item.resolution}/>}<Link to={base+'/council'}>{t('Evidence and full disagreement record','الأدلة وسجل الخلاف الكامل')}</Link></details>):<p className="caption">{t('No disagreement record was supplied. Agreement or independent execution cannot be inferred from its absence.','لم يُقدم سجل خلاف. لا يمكن استنتاج الاتفاق أو التنفيذ المستقل من غيابه.')}</p>}</div>
      </section>
      <section id="result-limitations" className="result-section">
        <h2>{t('Limitations and next steps','الحدود والخطوات التالية')}</h2>
        {[...groups].map(([category,items])=><details className="result-limitation-group" key={category}><summary><strong>{categoryNames[category]?.[ar?1:0]||t('Evidence and method limits','حدود الأدلة والمنهج')}</strong><span>{new Set(items.map(item=>item.explanation)).size}</span></summary>{items.filter((item,index)=>items.findIndex(other=>other.explanation===item.explanation)===index).map(item=><article key={item.id}><ResearchText text={item.explanation}/><p className="limit-next-step" dir="auto">{item.nextStep}</p>{item.variants?.length?<Link to={base+'/council'}>{t('Inspect reviewer concerns','فحص ملاحظات المراجعين')}</Link>:null}</article>)}</details>)}
        {!limitations.length&&<p>{t('No categorized limitations were supplied. Inspect the preserved record for any original caveats.','لم تُقدم حدود مصنفة. افحص السجل المحفوظ للتحفظات الأصلية.')}</p>}
        {a.limitations.length>0&&<details><summary>{t('Original assessment caveats','تحفظات التقييم الأصلية')}</summary><ul>{[...new Set(a.limitations)].map((item,index)=><li key={index} dir="auto">{item}</li>)}</ul></details>}
      </section>
      <section id="result-coverage" className="result-section"><h2>{t('Checks performed and unavailable','الفحوص المنفذة وغير المتاحة')}</h2>{data?.coverage?<CoverageList items={data.coverage} ar={ar}/>:<p>{t('Processing coverage is unavailable for this record.','تغطية المعالجة غير متاحة لهذا السجل.')}</p>}{processing.error&&<button onClick={()=>processing.refetch()}>{t('Retry evidence records','إعادة تحميل سجلات الأدلة')}</button>}{data?.historical&&<p>{t('This historical run predates the current processing pipeline. Its original findings are preserved.','يسبق هذا التشغيل التاريخي مسار المعالجة الحالي. نتائجه الأصلية محفوظة.')}</p>}</section>
      <footer className="result-footer"><Link to={base+'/audit'}>{t('Execution and audit history','تاريخ التنفيذ والتدقيق')}</Link>{a.reportAvailable&&<Link to={base+'/report'}>{t('Read or export the report','قراءة التقرير أو تصديره')}</Link>}<Link to={'/app/compare?a='+encodeURIComponent(a.id)}>{t('Compare analyses','مقارنة التحليلات')}</Link></footer>
    </div>

  </div>
}

function ObservationTable({data,ar}:{data:NonNullable<SectionData['dataset']>;ar:boolean}) {
  return <div className="result-observation-table" tabIndex={0} role="region" aria-label={ar?'معاينة الملاحظات الأصلية':'Original observations preview'}><table><caption>{ar?'أول خمسة صفوف من الصفحة المحملة. القيم كما وردت.':'First five rows of the loaded page. Values as supplied.'}</caption><thead><tr>{data.columns.map((column,index)=><th key={index} dir="auto">{column}</th>)}</tr></thead><tbody>{data.rows.slice(0,5).map((row,index)=><tr key={index}>{row.map((value,column)=><td key={column}><bdi>{value===null?'—':String(value)}</bdi></td>)}</tr>)}</tbody></table></div>
}
