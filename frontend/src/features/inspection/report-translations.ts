import {useState} from 'react'
import {useQuery,useQueryClient} from '@tanstack/react-query'
import {z} from 'zod'
import {request,ApiError} from '../../api'

const section=z.object({id:z.string(),title:z.string(),body:z.string(),references:z.array(z.object({title:z.string(),url:z.string()})).default([])})
const jobSchema=z.object({id:z.string(),analysisId:z.string(),sourceReportHash:z.string(),targetLanguage:z.enum(['ar','en']),
 status:z.enum(['queued','running','completed','failed']),completedBlocks:z.number(),totalBlocks:z.number(),
 provider:z.string(),clientVersion:z.string(),modelVersion:z.string(),classification:z.string(),
 retainedOriginalBlocks:z.array(z.object({field:z.string(),block:z.number(),reason:z.string()})).default([]),
 createdAt:z.string(),finishedAt:z.string().optional(),error:z.string().optional(),
 translatedReport:z.object({report:z.object({title:z.string().optional(),generatedAt:z.string().optional(),version:z.string().optional(),reproducibility:z.string().optional()}),sections:z.array(section)}).optional()})
const availabilitySchema=z.object({available:z.boolean(),targets:z.array(z.string()),sourceReportHash:z.string(),translations:z.array(jobSchema)})
export type ReportTranslation=z.infer<typeof jobSchema>

export function useReportTranslation(id:string,ar:boolean){
 const cache=useQueryClient()
 const [selectedId,setSelectedId]=useState<string|null>(null)
 const [target,setTarget]=useState<'ar'|'en'>(ar?'en':'ar')
 const [requesting,setRequesting]=useState(false)
 const [error,setError]=useState('')
 const base=`/analyses/${encodeURIComponent(id)}/report-translations`
 const availability=useQuery({queryKey:['report-translations',id],queryFn:async({signal})=>availabilitySchema.parse(await request(base,{signal})),retry:false,staleTime:30000})
 const job=useQuery({queryKey:['report-translation',id,selectedId],queryFn:async({signal})=>jobSchema.parse(await request(`${base}/${encodeURIComponent(selectedId!)}`,{signal})),enabled:!!selectedId,retry:false,
  refetchInterval:query=>query.state.data&&['queued','running'].includes(query.state.data.status)?1500:false})
 async function start(){
  if(requesting)return
  setRequesting(true);setError('')
  try{
   const value=jobSchema.parse(await request(base,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({targetLanguage:target})}))
   if(value.analysisId!==id)throw new Error('Translation identity mismatch')
   cache.setQueryData(['report-translation',id,value.id],value);setSelectedId(value.id)
   void cache.invalidateQueries({queryKey:['report-translations',id]})
  }catch(error){setError(error instanceof ApiError&&error.status===422?(ar?'التقرير يتجاوز حدود الترجمة المدعومة. يبقى الأصل متاحاً.':'This report exceeds the supported translation limits. The original remains available.'):(ar?'تعذر بدء الترجمة. تحقق من خدمة الترجمة وحاول مجدداً.':'Translation could not start. Check the translation service and try again.'))}
  finally{setRequesting(false)}
 }
 const selected=job.data?.analysisId===id&&job.data.sourceReportHash===availability.data?.sourceReportHash?job.data:undefined
 const translated=selected?.status==='completed'&&selected.translatedReport?selected:undefined
 return {availability,job,selected,translated,selectedId,setSelectedId,target,setTarget,requesting,error,start}
}
