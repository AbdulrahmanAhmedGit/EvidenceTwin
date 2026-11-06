import {useSyncExternalStore} from 'react'
import {z} from 'zod'
import {readPreference} from '../settings/preferences'
export const DRAFT_KEY='evidencetwin.draft.v1'
export const studyDesigns=['Unknown','Randomized experimental','Observational','Cross-sectional','Repeated cross-sectional','Longitudinal','Meta-analysis','Other'] as const
export const draftSchema=z.object({source:z.string().max(500),url:z.string().max(2000),studyDate:z.string().max(10),studyDesign:z.enum(studyDesigns),population:z.string().max(3000),uncertainty:z.string().max(3000),context:z.string().max(5000),claims:z.array(z.string().max(10000)).min(1).max(10),mode:z.enum(['exploratory','verified']),reviewDepth:z.enum(['focused','council']),caseId:z.enum(['a1','a2','a3']).optional()})
export type AnalysisDraft=z.infer<typeof draftSchema>
export function blankDraft():AnalysisDraft{return {source:'',url:'',studyDate:'',studyDesign:'Unknown',population:'',uncertainty:'',context:'',claims:[''],mode:readPreference('Default mode','Exploratory')==='Verified'?'verified':'exploratory',reviewDepth:readPreference('Review depth','Focused')==='Full Council'?'council':'focused'}}
type State={draft:AnalysisDraft;files:File[];persist:boolean;notice:'restored'|'storage_error'|null;modified:boolean;pending:boolean;acceptedId?:string}
function initial():State{try{const saved=localStorage.getItem(DRAFT_KEY);if(saved){const result=z.object({version:z.literal(1),consented:z.literal(true),draft:draftSchema}).safeParse(JSON.parse(saved));if(result.success)return {draft:result.data.draft,files:[],persist:true,notice:'restored',modified:true,pending:false}}}catch{/* Keep the form usable when storage is blocked or stale. */}return {draft:blankDraft(),files:[],persist:false,notice:null,modified:false,pending:false}}
let state=initial()
const listeners=new Set<()=>void>()
function emit(){listeners.forEach(fn=>fn())}
function persist(){if(!state.persist)return;try{localStorage.setItem(DRAFT_KEY,JSON.stringify({version:1,consented:true,draft:state.draft}));state={...state,notice:state.notice==='storage_error'?null:state.notice}}catch{state={...state,notice:'storage_error'}}}
export function updateDraft(patch:Partial<AnalysisDraft>){if(state.pending)return;state={...state,draft:{...state.draft,...patch},modified:true};persist();emit()}
export function setDraftFiles(files:File[]){if(state.pending)return;state={...state,files,modified:true};emit()}
export function prepareDraft(){if(!state.modified){state={...state,draft:blankDraft()};emit()}}
export function setDraftPersistence(enabled:boolean){if(state.pending)return;state={...state,persist:enabled,notice:null};if(enabled)persist();else try{localStorage.removeItem(DRAFT_KEY)}catch{state={...state,notice:'storage_error'}}emit()}
export function clearDraft(){let notice:State['notice']=null;try{localStorage.removeItem(DRAFT_KEY)}catch{notice='storage_error'}state={draft:blankDraft(),files:[],persist:false,notice,modified:false,pending:false};emit();return notice===null}
export function useAnalysisDraft(){return useSyncExternalStore(fn=>{listeners.add(fn);return()=>{listeners.delete(fn)}},()=>state)}
export function validateStep(step:number,draft:AnalysisDraft,fileCount:number):Record<string,string>{const errors:Record<string,string>={};if(step===0&&!fileCount&&!draft.caseId)errors.files='evidence';if(step===1){if(draft.url.trim()){try{const url=new URL(draft.url);if(!['https:','http:'].includes(url.protocol))errors.url='url'}catch{errors.url='url'}}if(draft.studyDate&&!/^\d{4}-\d{2}-\d{2}$/.test(draft.studyDate))errors.studyDate='date'}if(step===2){draft.claims.forEach((claim,i)=>{if(!claim.trim())errors['claim-'+i]='claim'})}return errors}

export function setDraftPending(pending:boolean){state={...state,pending};emit()}
export function acceptDraft(id:string){clearDraft();state={...state,acceptedId:id};emit()}
