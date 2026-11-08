import {useState,useEffect,useRef,Fragment} from 'react'
import {useQuery} from '@tanstack/react-query'
import {readAnalysisSection} from '../../research-api'
import {useLocation} from 'react-router-dom'
import type {Analysis,SectionData} from '../../research-api'
import {researchSubjectTitle} from '../../research-title'
import {ResearchText} from '../../research-display'
import BrandLogo from '../../components/brand/BrandLogo'
import ReportTranslationControls from './ReportTranslationControls'
import {useReportTranslation} from './report-translations'
import {useEvidenceProcessing} from './evidence-processing'
import {ComparisonFigure} from './EvidenceFindings'
import CoverageList from './CoverageList'
import {parseLegacyCoverage} from './coverage'
import {Empty} from './shared'
import {downloadJson,safeUrl,dateLabel,redactText} from './utils'
import './report-reader.css'

export default function ResearchReport({data,analysis,ar}:{data:SectionData;analysis:Analysis;ar:boolean}) {
  const documentRef=useRef<HTMLElement>(null)
  const translation=useReportTranslation(analysis.id,ar)
  const translated=translation.translated?.translatedReport
  const display=translated?{...data,report:translated.report,sections:translated.sections}:data
  const [message,setMessage]=useState('')
  const {hash}=useLocation()
  const docAr=translation.translated?translation.translated.targetLanguage==='ar':ar
  const text=(en:string,arabic:string)=>ar?arabic:en
  const sourceSections=(display.sections||[]).filter(section=>section.body.trim()||section.references?.length)
  const leadingId=sourceSections.some(section=>section.id==='visual_summary')?'visual_summary':sourceSections.some(section=>section.id==='visual_analyst')?'visual_analyst':'summary'
  const sections=[...sourceSections].sort((left,right)=>Number(right.id===leadingId)-Number(left.id===leadingId))
  const mobileContents=<details className="report-contents-mobile"><summary>{text('In this report','في هذا التقرير')}</summary><nav aria-label={text('Report contents','محتويات التقرير')}>{sections.map((section,index)=><a href={'#report-'+index} key={section.id} dir="auto">{section.title}</a>)}</nav></details>
  useEffect(()=>{
    if(!hash)return
    let id:string
    try{id=decodeURIComponent(hash.slice(1))}catch{return}
    const frame=requestAnimationFrame(()=>{
      const heading=document.getElementById(id)
      heading?.scrollIntoView({behavior:'instant'})
      heading?.focus({preventScroll:true})
    })
    return()=>cancelAnimationFrame(frame)
  },[hash,display.sections])
  useEffect(()=>{
    const previous=new Map<HTMLDetailsElement,boolean>()
    function expand() {
      documentRef.current?.querySelectorAll('details').forEach(details=>{
        if(!previous.has(details))previous.set(details,details.open)
        details.open=true
      })
    }
    function restore() {
      previous.forEach((open,details)=>{details.open=open})
      previous.clear()
    }
    window.addEventListener('beforeprint',expand)
    window.addEventListener('afterprint',restore)
    return()=>{
      restore()
      window.removeEventListener('beforeprint',expand)
      window.removeEventListener('afterprint',restore)
    }
  },[])
  async function copy(section:NonNullable<SectionData['sections']>[number]) {
    try {
      await navigator.clipboard.writeText(redactText(section.title+'\n'+section.body+(section.references?.length?'\n'+section.references.map(ref=>ref.title+' '+ref.url).join('\n'):'')))
      setMessage('copied')
    } catch {setMessage('failed')}
  }
  if(!sections.length)return <Empty ar={ar} title={text('Report content unavailable','محتوى التقرير غير متاح')} body={text('No supported report sections were supplied.','لم تُقدم أقسام تقرير مدعومة.')}/>
  return <div className="report-layout unified-report-reader">
    <div className="report-toolbar">
      <button className="primary" onClick={()=>window.print()}>{text('Print / save PDF','طباعة / حفظ PDF')}</button>
      {data.permissions.reportJson&&<button onClick={()=>downloadJson({analysis,report:data.report,sections:data.sections},analysis.id+'-report.json')}>{text('Original JSON','JSON الأصلي')}</button>}
      <details className="report-translation-options"><summary>{text('Translate','ترجمة')}</summary><ReportTranslationControls state={translation} ar={ar}/></details>

      <span role="status">{message==='copied'?text('Section copied.','نُسخ القسم.'):message==='failed'?text('Copy unavailable.','النسخ غير متاح.'):''}</span>
    </div>
    <nav className="report-contents" aria-label={text('Report contents','محتويات التقرير')}>
      <strong>{text('In this report','في هذا التقرير')}</strong>
      {sections.map((section,index)=><a href={'#report-'+index} key={section.id} dir="auto">{section.title}</a>)}
    </nav>

    <article ref={documentRef} className={'report-document'+(translated?' translated-report':'')} lang={translation.translated?.targetLanguage} dir={translation.translated?.targetLanguage==='ar'?'rtl':translation.translated?'ltr':undefined}>
      <div className="report-masthead"><BrandLogo label="EvidenceTwin Council"/><span>{docAr?'تقرير بحثي':'Research report'}</span></div>
      {translated&&<p className="report-machine-label">{translation.translated?.retainedOriginalBlocks.length?(docAr?'ترجمة آلية جزئية · تبقى بعض المقاطع بلغتها الأصلية لحماية الأرقام والمراجع.':'Partial machine translation · Some passages retain original wording for numerical and reference safety.'):(docAr?'ترجمة آلية · راجع المصطلحات العلمية مع التقرير الأصلي.':'Machine translation · Review scientific terminology against the original report.')}</p>}
      <details className="report-heading report-document-metadata"><summary>{text('Report metadata','بيانات التقرير')}</summary>
        <h2 dir="auto">{researchSubjectTitle(display.report?.title||text('Evidence-linked research report','تقرير بحثي مرتبط بالأدلة'))}</h2>
        <dl>{display.report?.generatedAt&&<div><dt>{text('Generated','تاريخ الإنشاء')}</dt><dd>{dateLabel(display.report.generatedAt,ar)}</dd></div>}{display.report?.version&&<div><dt>{text('Report version','إصدار التقرير')}</dt><dd><bdi>{display.report.version}</bdi></dd></div>}</dl>
        <details><summary>{text('Record reference','مرجع السجل')}</summary><bdi>{analysis.id}</bdi></details>
      </details>
      {!sections.some(section=>section.id===leadingId)&&mobileContents}
      {sections.map((section,index)=>{
        const coverage=section.id==='coverage'?parseLegacyCoverage(section.body):null
        const appendix=['claim','evidence','reproducibility','quantitative'].includes(section.id)
        const reviewer=section.id.endsWith('_analyst')||section.id.endsWith('_auditor')||section.id.endsWith('_skeptic')||section.id==='cross_reviewer'||section.id==='evidence_judge'
        return <Fragment key={section.id}><section className={'report-section'+(section.id===leadingId?' report-executive-finding':'')} key={section.id}>
          <div className="report-section-heading"><h3 dir="auto" id={'report-'+index} tabIndex={-1}>{section.title}</h3><button onClick={()=>copy(section)}>{text('Copy section','نسخ القسم')}</button></div>
          {translation.translated?.retainedOriginalBlocks.some(block=>block.field===`${display.sections!.indexOf(section)}.body`)&&<p className="report-retained-language">{docAr?'تتضمن هذه الفقرة نصاً أصلياً تعذر تأكيد ترجمته بأمان.':'This section includes original-language passages whose safe translation could not be confirmed.'}</p>}
          {section.id===leadingId&&<ReportVisualEvidence id={analysis.id} ar={docAr}/>}
          {appendix?<details className="report-record-appendix"><summary>{section.id==='quantitative'?text('Exact observations and calculation method','الملاحظات الدقيقة وطريقة الحساب'):text('Inspect the preserved record','فحص السجل المحفوظ')}</summary><ResearchText className="report-body" text={section.body}/></details>:coverage?<CoverageList items={coverage} ar={docAr}/>:reviewer&&section.id!==leadingId?<details className="report-review-contribution"><summary>{text('Read this AI contribution','قراءة هذه المساهمة بالذكاء الاصطناعي')}</summary><ResearchText className="report-body" text={section.body}/></details>:<ResearchText className="report-body" text={section.body}/>}
          {section.id==='quantitative'&&<ReportPlots id={analysis.id} ar={docAr}/>}
          {!!section.references?.length&&<ul className="report-references">{section.references.map(ref=><li key={ref.url}>{safeUrl(ref.url)?<a href={safeUrl(ref.url)} target="_blank" rel="noreferrer"><bdi>{ref.title}</bdi></a>:ref.title}</li>)}</ul>}
        </section>{section.id===leadingId&&mobileContents}</Fragment>
      })}
      {display.report?.reproducibility&&<section className="report-section"><h3>{text('Reproducibility information','معلومات إعادة الإنتاج')}</h3><ResearchText className="report-body" text={display.report.reproducibility}/></section>}
      <div className="report-endnote"><p>{text('PDF uses your browser’s print dialog. Original records remain available separately from machine translations.','يستخدم حفظ PDF نافذة الطباعة في المتصفح. تتوفر السجلات الأصلية بصورة منفصلة عن الترجمة الآلية.')}</p>{docAr?'تظل حدود الأدلة جزءاً من التقييم. اتفاق النماذج ليس برهاناً علمياً.':'Evidence limitations remain part of the assessment. Agreement between models is not scientific proof.'}</div>
    </article>
  </div>
}

function ReportPlots({id,ar}:{id:string;ar:boolean}) {
  const query=useEvidenceProcessing(id)
  if(!query.data||query.data.historical)return null
  return <div className="report-recorded-plots">{query.data.datasets.map(table=><div key={table.evidenceId}>{table.comparisons.map(comparison=><ComparisonFigure data={comparison} ar={ar} key={comparison.id}/>)}{table.comparisons.length>0&&<p className="caption"><bdi>{table.filename||table.evidenceId}</bdi></p>}</div>)}</div>
}

function ReportVisualEvidence({id,ar}:{id:string;ar:boolean}) {
  const query=useQuery({queryKey:['analysis',id,'visualizations'],queryFn:({signal})=>readAnalysisSection(id,'visualizations',signal),retry:false,staleTime:15000})
  const original=safeUrl(query.data?.visualizations?.original||'')
  return <div className="report-visual-evidence">
    {original&&<figure><img src={original} alt={ar?'الرسم العلمي الأصلي المقدم':'Original submitted scientific chart'}/><figcaption>{ar?'الرسم الأصلي · تفاصيل المصدر والمنهج في الأقسام المحفوظة أدناه.':'Original chart · Source and method details are retained below.'}</figcaption></figure>}
    <p>{ar?'إعادة البناء المعماة غير متاحة حالياً. الرسم الوصفي إن وجد فحص داعم، وليس إعادة بناء معماة معتمدة.':'Blind reconstruction is currently unavailable. Any descriptive calculation plot is a supporting check and has no validated blind-reconstruction status.'}</p>
  </div>
}
