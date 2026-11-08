import CoverageList from './CoverageList'
import {coverageStatus} from './coverage'
import {safeUrl} from './utils'
import {useQuery} from '@tanstack/react-query'
import {apiBase} from '../../api'
import {readProcessing} from './evidence-processing'
import type {Comparison} from './evidence-processing'
import './evidence-findings.css'


export function ComparisonFigure({data,ar}:{data:Comparison;ar:boolean}) {
  const numeric = data.observations.map(item=>Number(item.value))
  const min = data.plot?Number(data.plot.domain[0]):Math.min(0,...numeric)
  const max = data.plot?Number(data.plot.domain[1]):Math.max(0,...numeric)
  const span = max-min || 1
  const x = (value:number)=>(value-min)/span*100
  const relation = {higher:['higher than','أعلى من'],lower:['lower than','أقل من'],equal:['equal to','مساوٍ لـ']}[data.relation][ar?1:0]
  const left = data.observations[0], right = data.observations[1]
  if (!left || !right) return null
  return <figure className="evidence-comparison">
    <figcaption><h3 dir="auto">{data.indicator}</h3><span>{data.year} · {ar?'القيم المبلغ عنها':'Reported observations'}</span></figcaption>
    <p className="dataset-answer" dir="auto"><bdi>{left.label}</bdi> {relation} <bdi>{right.label}</bdi></p>
    {data.unit && numeric.every(Number.isFinite) && <div className="comparison-plot" aria-label={ar?'مقارنة القيم المبلغ عنها':'Comparison of reported values'}>
      {data.observations.map((item,index)=><div className="plot-observation" key={item.rowNumber}>
        <div className="plot-label"><bdi>{item.label}</bdi><strong><bdi>{item.value}{data.unit}</bdi></strong></div>
        <div className="plot-track" dir="ltr" aria-hidden="true"><span className="plot-zero" style={{insetInlineStart:x(0)+'%'}}/><span className={'plot-bar '+(index?'comparison-secondary':'comparison-primary')} style={{insetInlineStart:Math.min(x(0),x(numeric[index]))+'%',inlineSize:Math.abs(x(numeric[index])-x(0))+'%'}}/></div>
      </div>)}
      <div className="comparison-axis" dir="ltr" aria-hidden="true"><span>{min}{data.unit}</span><span>{max}{data.unit}</span></div>
    </div>}
    <dl className="comparison-calculations">
      <div><dt>{ar?'الفرق (الأول − الثاني)':'Difference (first − second)'}</dt><dd><bdi>{data.difference}</bdi> {data.unit==='%'?(ar?'نقطة مئوية':'percentage points'):data.unit||(ar?'بنفس الوحدات المقدمة':'in supplied units')}</dd></div>
      <div><dt>{ar?'النسبة (الأول ÷ الثاني)':'Ratio (first ÷ second)'}</dt><dd><bdi>{data.ratio?Number(data.ratio).toLocaleString(ar?'ar':'en',{maximumFractionDigits:4}):'—'}</bdi></dd></div>
    </dl>
    <details><summary>{ar?'القيم الدقيقة وطريقة الحساب':'Exact observations and method'}</summary>
      <table><caption>{data.year} · {data.unit|| (ar?'الوحدة غير محددة':'Unit unspecified')}</caption><thead><tr><th>{ar?'الملاحظة':'Observation'}</th><th>{ar?'القيمة':'Value'}</th><th>{ar?'صف المصدر':'Source record row'}</th></tr></thead><tbody>{data.observations.map(item=><tr key={item.rowNumber}><th dir="auto">{item.label}</th><td><bdi>{item.value}</bdi></td><td>{item.rowNumber}</td></tr>)}</tbody></table>
      <p dir="auto">{data.method}</p><p>{ar?'النسبة الدقيقة':'Exact ratio'} <bdi>{data.ratio||'—'}</bdi></p>
      {data.plot&&<p>{ar?'رسم خطي بقيم المصدر الأصلية وخط أساس صفري. إصدار الرسم':'Linear display of original values with a zero baseline. Plot version'} <bdi>{data.plot.version}</bdi></p>}
      <p dir="auto">{data.scope}</p>
    </details>
  </figure>
}

export default function EvidenceFindings({id,path,ar,chartsOnly=false}:{id?:string;path?:string;ar:boolean;chartsOnly?:boolean}) {
  const endpoint = path || `/analyses/${encodeURIComponent(id || '')}/processing`
  const query = useQuery({queryKey:['evidence-processing',endpoint],queryFn:({signal})=>readProcessing(endpoint,signal),retry:false,staleTime:10000})
  const t = (en:string,arabic:string)=>ar?arabic:en
  if(query.isPending) return <p role="status">{t('Inspecting evidence records…','جارٍ فحص سجلات الأدلة…')}</p>
  if(query.error) return <div className="notice error" role="status"><p>{t('Evidence processing could not be loaded.','تعذر تحميل معالجة الأدلة.')}</p><button onClick={()=>query.refetch()}>{t('Try again','المحاولة مجدداً')}</button></div>
  const arabicLimits:Record<string,[string,string]>={
    authenticity:['لم تُثبت أصالة المصدر وتوافق المنهجية بشكل مستقل.','افحص تعريفات المصدر والسكان والوحدات والمنهجية قبل تعميم النتيجة الوصفية.'],
    'ai-interpretation':['مخرجات المجلس تفسيرات بالذكاء الاصطناعي. قد تتشارك النماذج الأخطاء؛ اتفاقها لا يثبت الحقيقة العلمية.','افحص الملاحظات والحسابات والخلافات غير المحسومة بشكل مستقل.'],
    'blind-optics':['إعادة بناء الرسوم المعماة غير متاحة. ما زال بروتوكول التعمية والرسم يحتاج إلى تحديد وقبول.','افحص الرسم الوصفي والصورة الأصلية بشكل منفصل. لا يمثل أي منهما إعادة بناء محايدة معتمدة.'],
    'pdf-extraction':['بايتات ملفات PDF محفوظة، لكن محتوياتها لم تُستخرج ولم تُرسل إلى المجلس.','قدم بيانات منظمة مدعومة أو مصدراً مقروءاً متاحاً.'],
    educational:['أُدرج مثال تعليمي مختار صراحةً. قيمه توضيحية وليست ملاحظات بحثية حية متحققاً منها.','قدم أدلة حقيقية لإجراء بحث.'],
  }
  const data=query.data
  if (!data || data.historical) return <p className="scientific-boundary">{t('This historical run predates complete-table processing. Start a new review from the saved investigation to use the current evidence pipeline. The original findings remain below.','تسبق هذه المراجعة التاريخية معالجة الجدول الكامل. ابدأ مراجعة جديدة من البحث المحفوظ لاستخدام المعالجة الحالية. النتائج الأصلية محفوظة أدناه.')}</p>
  const comparisons=data.datasets.flatMap(table=>table.comparisons)
  const sources=data.sources||(data.source?[data.source]:[])
  return <section className="evidence-findings" aria-label={t('Evidence findings','نتائج الأدلة')}>
    <header className="evidence-finding-heading"><h2>{t('What the evidence shows','ما توضحه الأدلة')}</h2><p>{comparisons.length?t('A reproducible comparison of reported dataset values.','مقارنة قابلة للتكرار للقيم المبلغ عنها في البيانات.'):t('A numerical comparison has not been established. Review the selection limits below.','لم تثبت مقارنة رقمية. راجع حدود اختيار البيانات أدناه.')}</p></header>
    {data.datasets.map(table=><section key={table.evidenceId} className="dataset-finding-group">
      {table.comparisons.map(c=><ComparisonFigure key={c.id} data={c} ar={ar}/>)}
      {table.filename&&<p className="caption">{t('Source','المصدر')} · <bdi>{table.filename}</bdi></p>}
      <details className="evidence-provenance"><summary>{table.rowCount.toLocaleString(ar?'ar':'en')} {t('rows available · inspect provenance','صفاً متاحاً · فحص التتبع')}</summary><p dir="auto">{table.columns.join(' · ')}</p><dl><dt>{t('Evidence','الدليل')}</dt><dd><bdi>{table.evidenceId}</bdi></dd><dt>{t('Evidence revision','نسخة الأدلة')}</dt><dd><bdi>{table.revisionId}</bdi></dd><dt>SHA-256</dt><dd><bdi>{table.sha256||'—'}</bdi></dd></dl></details>
    </section>)}
    <p className="scientific-boundary">{t('These calculations describe the submitted observations. The full scientific claim, methodology and source authenticity remain unverified.','تصف هذه الحسابات الملاحظات المقدمة. يظل الادعاء العلمي الكامل والمنهجية وأصالة المصدر دون تحقق مستقل.')}</p>
    {!chartsOnly&&<>
    <section className="processing-coverage"><h3>{t('Checks and evidence coverage','الفحوص وتغطية الأدلة')}</h3><CoverageList items={data.coverage} ar={ar}/></section>
    {sources.length>0&&<section className="retrieved-source"><h3>{t('Source materials','مواد المصادر')}</h3>{sources.map((source,index)=><article key={source.evidenceId||source.url}>
      <p>{safeUrl(source.url)?<a href={safeUrl(source.url)} target="_blank" rel="noreferrer"><bdi>{source.url}</bdi></a>:<bdi>{source.url}</bdi>}</p>
      <p>{coverageStatus(source.status,ar)}{source.origin?.startsWith('claim-')?' · '+t('Detected in the question','كُشف في السؤال'):source.origin==='context'?' · '+t('Detected in research notes','كُشف في ملاحظات البحث'):''}</p>
      {source.extraction==='youtube_transcript'&&<p>{t('YouTube captions','نص فيديو YouTube')} · <bdi>{source.language}</bdi> · {source.isGenerated?t('Automatically generated','مولد آلياً'):t('Manual caption track','مسار ترجمة نصية يدوي')}</p>}
      {source.reason&&<p dir="auto">{source.reason}</p>}
      {id&&source.status==='retrieved'&&<a href={`${apiBase}/analyses/${encodeURIComponent(id)}/source-snapshot?sourceId=${encodeURIComponent(source.evidenceId|| (index===0?'retrieved-source':`retrieved-source-${index+1}`))}`} download>{source.extraction==='youtube_transcript'?t('Download timed transcript','تنزيل النص مع التوقيت'):t('Download retained source snapshot','تنزيل نسخة المصدر المحفوظة')}</a>}
      {source.retrievedAt&&<p><time dateTime={source.retrievedAt}>{new Date(source.retrievedAt).toLocaleString(ar?'ar':'en')}</time></p>}
    </article>)}</section>}
    <section className="processing-limitations"><h3>{t('Limits and next steps','الحدود والخطوات التالية')}</h3>{data.limitations.map(item=><details key={item.id}><summary dir="auto">{ar?arabicLimits[item.id]?.[0]||item.explanation:item.explanation}</summary><p dir="auto">{ar?arabicLimits[item.id]?.[1]||item.nextStep:item.nextStep}</p>{item.classification&&<p className="caption">{t('AI reviewer concern. Inspect the original Council outputs for each perspective.','ملاحظة من مراجع بالذكاء الاصطناعي. افحص مخرجات المجلس الأصلية لكل منظور.')}</p>}{item.variants?.map((variant,index)=><p key={index} dir="auto">{variant.explanation}{variant.cause?' · '+variant.cause:''}</p>)}</details>)}</section>
    </>}
  </section>
}
