import {useSyncExternalStore} from 'react'
import {z} from 'zod'
import {readPreference} from '../settings/preferences'
export const DRAFT_KEY='evidencetwin.draft.v1'
export const studyDesigns=['Unknown','Randomized experimental','Observational','Cross-sectional','Repeated cross-sectional','Longitudinal','Meta-analysis','Other'] as const
export const draftSchema=z.object({source:z.string().max(500),url:z.string().max(2000),studyDate:z.string().max(10),studyDesign:z.enum(studyDesigns),population:z.string().max(3000),uncertainty:z.string().max(3000),context:z.string().max(5000),claims:z.array(z.string().max(10000)).min(1).max(10),mode:z.enum(['exploratory','verified']),reviewDepth:z.enum(['focused','council']),caseId:z.enum(['a1','a2','a3']).optional()})
export type AnalysisDraft=z.infer<typeof draftSchema>
export function blankDraft():AnalysisDraft{return {source:'',url:'',studyDate:'',studyDesign:'Unknown',population:'',uncertainty:'',context:'',claims:[''],mode:'exploratory',reviewDepth:readPreference('Review depth','Focused')==='Full Council'?'council':'focused'}}
type State={ownerId:string|null;draft:AnalysisDraft;files:File[];persist:boolean;notice:'restored'|'storage_error'|null;modified:boolean;pending:boolean;acceptedId?:string}
const listeners=new Set<()=>void>()
const states=new Map<string,State>()
let ownerId:string|null=null
function key(owner:string){return owner==='local'?DRAFT_KEY:DRAFT_KEY+'.account.'+encodeURIComponent(owner)}
function empty(owner:string|null):State{return {ownerId:owner,draft:blankDraft(),files:[],persist:false,notice:null,modified:false,pending:false}}
function initial(owner:string):State{try{const saved=localStorage.getItem(key(owner));if(saved){const parsed=z.object({version:z.literal(1),consented:z.literal(true),draft:draftSchema}).safeParse(JSON.parse(saved));if(parsed.success)return {...empty(owner),draft:parsed.data.draft,persist:true,notice:'restored',modified:true}}}catch{/* Blocked storage must not prevent research. */}return empty(owner)}
let state=empty(null)
function emit(){listeners.forEach(fn=>fn())}
function replace(next:State){if(next.ownerId)states.set(next.ownerId,next);if(next.ownerId===ownerId){state=next;emit()}}
function selected(owner:string|null){return owner===ownerId?state:owner?states.get(owner):undefined}
function persist(next:State):State{if(!next.persist||!next.ownerId)return next;try{localStorage.setItem(key(next.ownerId),JSON.stringify({version:1,consented:true,draft:next.draft}));return {...next,notice:next.notice==='storage_error'?null:next.notice}}catch{return {...next,notice:'storage_error'}}}
export function setDraftOwner(owner:string|null){if(owner===ownerId)return;if(ownerId)states.set(ownerId,state);ownerId=owner;state=owner?(states.get(owner)||initial(owner)):empty(null);emit()}
export function getDraftOwner(){return ownerId}
export function updateDraft(patch:Partial<AnalysisDraft>){if(state.pending||!ownerId)return;replace(persist({...state,draft:{...state.draft,...patch},modified:true}))}
export function setDraftFiles(files:File[]){if(state.pending||!ownerId)return;replace({...state,files,modified:true})}
export function prepareDraft(){if(!state.modified)replace({...state,draft:blankDraft()})}
export function setDraftPersistence(enabled:boolean){if(state.pending||!ownerId)return;let next={...state,persist:enabled,notice:null} as State;if(enabled)next=persist(next);else try{localStorage.removeItem(key(ownerId))}catch{next.notice='storage_error'}replace(next)}
export function clearDraft(owner=ownerId){let notice:State['notice']=null;if(owner)try{localStorage.removeItem(key(owner))}catch{notice='storage_error'}replace({...empty(owner),notice});return notice===null}
export function useAnalysisDraft(){return useSyncExternalStore(subscribe,()=>state)}
function subscribe(listener:()=>void){listeners.add(listener);return()=>{listeners.delete(listener)}}
export function validateStep(step:number,draft:AnalysisDraft,fileCount:number):Record<string,string>{const errors:Record<string,string>={};if(step===0&&!fileCount&&!draft.caseId)errors.files='evidence';if(step===1){if(draft.url.trim()){try{const url=new URL(draft.url);if(!['https:','http:'].includes(url.protocol)||url.username||url.password)errors.url='url'}catch{errors.url='url'}}if(draft.studyDate&&!z.iso.date().safeParse(draft.studyDate).success)errors.studyDate='date'}if(step===2){draft.claims.forEach((claim,i)=>{if(!claim.trim())errors['claim-'+i]='claim'})}return errors}
export function setDraftPending(pending:boolean,owner=ownerId){const target=selected(owner);if(target)replace({...target,pending})}
export function acceptDraft(id:string,owner=ownerId){clearDraft(owner);const target=selected(owner);if(target)replace({...target,acceptedId:id})}
