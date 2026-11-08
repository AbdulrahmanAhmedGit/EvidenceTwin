import {z} from 'zod'
import {request,apiBase} from '../../api'
import {draftSchema} from './draft-store'
import type {AnalysisDraft} from './draft-store'

const fileSchema=z.object({id:z.string(),name:z.string(),size:z.number(),mediaType:z.string(),sha256:z.string()})
const summarySchema=z.object({id:z.string(),title:z.string(),createdAt:z.string(),updatedAt:z.string(),currentRevision:z.string(),revisionCount:z.number(),analysisCount:z.number()})
const caseSchema=summarySchema.extend({sourceCount:z.number().optional(),metadata:draftSchema.extend({claim:z.string()}),files:z.array(fileSchema),revisions:z.array(z.object({id:z.string(),createdAt:z.string()})),analyses:z.array(z.object({id:z.string(),title:z.string(),status:z.string(),createdAt:z.string(),reportAvailable:z.boolean().optional()})),limitations:z.array(z.string())})
export type ResearchCase=z.infer<typeof caseSchema>
export type CaseSummary=z.infer<typeof summarySchema>
export type EvidenceFile=z.infer<typeof fileSchema>
export const caseFilesUrl=(id:string,revision:string,file:string)=>`${apiBase}/research-cases/${encodeURIComponent(id)}/revisions/${encodeURIComponent(revision)}/files/${encodeURIComponent(file)}`
export async function readCases(search='',page=1,signal?:AbortSignal){return z.object({items:z.array(summarySchema),total:z.number(),page:z.number(),pageSize:z.number()}).parse(await request('/research-cases?'+new URLSearchParams({search,page:String(page)}),{signal}))}
export async function readCase(id:string,signal?:AbortSignal){const value=caseSchema.parse(await request('/research-cases/'+encodeURIComponent(id),{signal}));if(value.id!==id)throw new Error('Case identity mismatch');return value}
export async function saveCase(draft:AnalysisDraft,files:File[],current?:ResearchCase,retained:EvidenceFile[]=[]){
 const body=new FormData();body.append('metadata',JSON.stringify({...draft,claim:draft.claims[0]}));files.forEach(file=>body.append('files',file));body.append('retainedFiles',JSON.stringify(retained.map(f=>f.id)))
 return caseSchema.parse(await request('/research-cases'+(current?'/'+encodeURIComponent(current.id)+'/revisions':''),{method:'POST',body,headers:current?{'If-Match':current.currentRevision}:{},},120000))
}
export async function runCase(current:ResearchCase,requestId:string){return z.object({id:z.string().min(1)}).parse(await request('/research-cases/'+encodeURIComponent(current.id)+'/analyses',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({revisionId:current.currentRevision,requestId,consent:true})},120000))}
