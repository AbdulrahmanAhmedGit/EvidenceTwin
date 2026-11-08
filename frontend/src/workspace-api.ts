import {z} from 'zod'
import {request} from './api'
export const statuses=['draft','awaiting_evidence','queued','running','completed','completed_with_limitations','failed','cancelled'] as const
export const verdicts=['supported','unsupported','partially_supported','insufficient_evidence','unresolved','not_evaluated'] as const
const record=z.object({id:z.string(),researchCaseId:z.string().optional(),title:z.string(),createdAt:z.iso.datetime({offset:true}),status:z.enum(statuses),mode:z.enum(['verified','exploratory']),source:z.string().optional(),assessment:z.enum(verdicts).optional(),summary:z.string().optional(),reportAvailable:z.boolean().default(false)})
export type AnalysisRecord=z.infer<typeof record>
const list=z.object({items:z.array(record),total:z.number().int().nonnegative(),page:z.number().int().positive(),pageSize:z.number().int().positive()})
const capabilities=z.object({providers:z.array(z.object({name:z.string(),status:z.enum(['configured','not_configured','unavailable'])})).default([]),jobAvailability:z.enum(['available','unavailable','unknown']).default('unknown'),activity:z.boolean().default(false),analyses:z.object({create:z.boolean().default(false),maxClaims:z.number().int().min(1).max(10).default(1),delete:z.boolean().default(false),retry:z.boolean().default(false),modes:z.array(z.enum(['exploratory','verified'])).default(['exploratory']),reviewDepths:z.array(z.enum(['focused','council'])).default(['focused'])}).default({create:false,maxClaims:1,delete:false,retry:false,modes:['exploratory'],reviewDepths:['focused']}),services:z.array(z.object({name:z.string(),status:z.enum(['available','unavailable','not_configured'])})).default([])})
export type ListOptions={search:string;status:string;mode:string;verdict:string;sort:string;page:number}
export async function getAnalyses(options:ListOptions,signal:AbortSignal){const query=new URLSearchParams({...options,page:String(options.page),pageSize:'10'});return list.parse(await request('/analyses?'+query,{signal}))}
export async function getCapabilities(signal:AbortSignal){return capabilities.parse(await request('/capabilities',{signal}))}
export async function deleteAnalysis(id:string){await request<void>('/analyses/'+encodeURIComponent(id),{method:'DELETE'})}
export async function retryAnalysis(id:string){await request('/analyses/'+encodeURIComponent(id)+'/retry',{method:'POST'})}
export const statusNames:Record<string,[string,string]>={draft:['Draft','مسودة'],awaiting_evidence:['Awaiting evidence','بانتظار الأدلة'],queued:['Queued','في قائمة الانتظار'],running:['Running','قيد التشغيل'],completed:['Completed','مكتمل'],completed_with_limitations:['Review complete','اكتملت المراجعة'],failed:['Failed','أخفق'],cancelled:['Cancelled','ملغى']}
export const verdictNames:Record<string,[string,string]>={supported:['Supported','مدعوم'],unsupported:['Unsupported','غير مدعوم'],partially_supported:['Partially supported','مدعوم جزئياً'],insufficient_evidence:['Insufficient evidence','أدلة غير كافية'],unresolved:['Unresolved','غير محسوم'],not_evaluated:['Not evaluated','لم يُقيّم']}

const activity=z.object({items:z.array(z.object({id:z.string(),timestamp:z.iso.datetime({offset:true}),description:z.string(),analysisId:z.string().optional()}))})
export async function getActivity(signal:AbortSignal){return activity.parse(await request('/activity?limit=10',{signal}))}
