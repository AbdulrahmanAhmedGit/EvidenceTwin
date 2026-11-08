import {lazy,Suspense,useCallback,useState} from 'react'
import {useQuery} from '@tanstack/react-query'
import {request} from '../../api'
import {datasetSchema} from '../../research-api'
import type {DatasetOptions} from '../../research-api'
import type {ResearchCase} from './cases-api'
import '../inspection/inspection.css'
const DatasetTable=lazy(()=>import('../inspection/EvidenceInspector').then(module=>({default:module.DatasetTable})))
export default function CaseDataset({current,ar}:{current:ResearchCase;ar:boolean}){
 const [open,setOpen]=useState(false);const id='case:'+current.id+':'+current.currentRevision
 const read=useCallback(async(_id:string,options:DatasetOptions,signal:AbortSignal)=>{
  const params=new URLSearchParams({...options,page:String(options.page),sort:String(options.sort),pageSize:'25'})
  const data=datasetSchema.parse(await request('/research-cases/'+encodeURIComponent(current.id)+'/revisions/'+encodeURIComponent(current.currentRevision)+'/dataset?'+params,{signal}))
  if(data.page!==options.page||data.pageSize!==25)throw new Error('Dataset page mismatch')
  return data
 },[current.id,current.currentRevision])
 const q=useQuery({queryKey:['dataset',id,1,'',-1,'asc'],queryFn:({signal})=>read(id,{page:1,search:'',sort:-1,direction:'asc'},signal),enabled:open,retry:false,staleTime:15000})
 return <details className="case-dataset research-disclosure" open={open} onToggle={event=>setOpen(event.currentTarget.open)}><summary>{ar?'فحص جدول البيانات المحفوظ':'Inspect saved data table'}</summary><p className="caption">{ar?'هذه القيم كما وردت في الملف. لم تُجرَ اختبارات علمية أو إحصائية.':'These are the values supplied in the file. No scientific or statistical checks were performed.'}</p>{open&&(q.isPending?<p role="status">{ar?'جارٍ تحميل البيانات…':'Loading data…'}</p>:q.error?<div role="alert"><p>{ar?'تعذر تحميل الجدول.':'The table could not be loaded.'}</p><button type="button" onClick={()=>q.refetch()}>{ar?'حاول مجدداً':'Try again'}</button></div>:q.data&&<Suspense fallback={<p role="status">{ar?'جارٍ فتح الجدول…':'Opening table…'}</p>}><DatasetTable key={id} data={q.data} id={id} ar={ar} readPage={read}/></Suspense>)}</details>
}
