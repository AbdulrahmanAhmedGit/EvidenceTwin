import {researchTitle} from '../../research-title'
import {Link} from 'react-router-dom'
import type {AnalysisRecord} from '../../workspace-api'
import {statusNames,verdictNames} from '../../workspace-api'
import {Button} from '../../components/ui/WorkspacePrimitives'

export type RecordControls={selected:string[];pending:boolean;permissions:{delete:boolean;retry:boolean};toggle:(id:string)=>void;requestDelete:(ids:string[])=>void;retry:(id:string)=>void}
export function ExecutionStatus({status,ar}:{status:AnalysisRecord['status'];ar:boolean}) {
 return <span className={'status-label status-'+status}><span className="status-mark" aria-hidden="true"/>{statusNames[status][ar?1:0]}</span>
}
function Identity({record,ar}:{record:AnalysisRecord;ar:boolean}) {
 const title=record.title.trim()||(ar?'تحليل بلا عنوان':'Untitled analysis')
 return <><h3><Link dir="auto" title={title} to={'/app/analyses/'+encodeURIComponent(record.id)}>{researchTitle(title,120)} →</Link></h3><div className="record-description">{record.researchCaseId&&<span>{ar?'محفوظ ضمن البحث':'Retained with investigation'}</span>}<span>{ar?(record.mode==='verified'?'تحقق بالأدلة':'استكشافي'):record.mode==='verified'?'Verified Mode':'Exploratory Mode'}</span>{record.assessment&&<span>{verdictNames[record.assessment][ar?1:0]}</span>}</div>{(record.source||record.summary)&&<details className="record-source"><summary>{ar?'المصدر والسياق':'Source & context'}</summary><p dir="auto">{record.source}</p>{record.summary&&<p dir="auto">{record.summary}</p>}</details>}</>
}
function Actions({record,controls,ar}:{record:AnalysisRecord;controls:RecordControls;ar:boolean}) {
 return <div className="record-actions">{record.reportAvailable&&<Link to={'/app/analyses/'+encodeURIComponent(record.id)+'/report'}>{ar?'التقرير':'Report'} →</Link>}{record.status==='failed'&&<Button variant="quiet" disabled={!controls.permissions.retry||controls.pending} onClick={()=>controls.retry(record.id)}>{ar?'إعادة التحليل':'Retry analysis'}</Button>}{record.researchCaseId?<Link to={'/app/cases/'+encodeURIComponent(record.researchCaseId)}>{ar?'ملف البحث':'Investigation'}</Link>:<Button variant="quiet" disabled={!controls.permissions.delete||controls.pending} onClick={()=>controls.requestDelete([record.id])}>{ar?'حذف':'Delete'}</Button>}{record.status==='failed'&&!controls.permissions.retry&&<span className="action-explanation">{ar?'إعادة التحليل غير متاحة حالياً. يمكنك فتح السجل لفحص الخطأ.':'Retry is unavailable right now. Open the record to review the failure.'}</span>}</div>
}
function Selection({record,controls,ar}:{record:AnalysisRecord;controls:RecordControls;ar:boolean}) {
 if(record.researchCaseId)return null
 return <input type="checkbox" aria-label={(ar?'حدد ':'Select ')+record.title} checked={controls.selected.includes(record.id)} disabled={controls.pending} onChange={()=>controls.toggle(record.id)}/>
}
export function AnalysisTable({items,controls,ar}:{items:AnalysisRecord[];controls:RecordControls;ar:boolean}) {
 return <div className="review-record-list">{items.map(record=><article className="analysis-record" key={record.id}><div className="selection-cell"><Selection record={record} controls={controls} ar={ar}/></div><div className="record-main"><div className="record-topline"><ExecutionStatus status={record.status} ar={ar}/><time dateTime={record.createdAt}>{new Intl.DateTimeFormat(ar?'ar':'en',{dateStyle:'medium'}).format(new Date(record.createdAt))}</time></div><Identity record={record} ar={ar}/><Actions record={record} controls={controls} ar={ar}/></div></article>)}</div>
}
export function AnalysisGrid({items,controls,ar}:{items:AnalysisRecord[];controls:RecordControls;ar:boolean}) {
 return <div className="record-grid">{items.map(record=><article className="analysis-record" key={record.id}><div className="record-grid-top"><Selection record={record} controls={controls} ar={ar}/><ExecutionStatus status={record.status} ar={ar}/></div><div className="record-body"><Identity record={record} ar={ar}/><time dateTime={record.createdAt}>{new Intl.DateTimeFormat(ar?'ar':'en',{dateStyle:'medium'}).format(new Date(record.createdAt))}</time><Actions record={record} controls={controls} ar={ar}/></div></article>)}</div>
}
