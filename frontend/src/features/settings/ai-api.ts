import {z} from 'zod'
import {request} from '../../api'
export const providerIDs=['ollama','openai','google','anthropic','openrouter','deepseek'] as const
export type ProviderID=typeof providerIDs[number]
export const aiSettingsSchema=z.object({activeProvider:z.enum(providerIDs),providers:z.array(z.object({id:z.enum(providerIDs),name:z.string(),model:z.string(),configured:z.boolean(),keyConfigured:z.boolean(),keySource:z.enum(['server','environment','none']),requiresKey:z.boolean(),ollamaHost:z.string().optional()}))}).superRefine((value,ctx)=>{if(!value.providers.some(p=>p.id===value.activeProvider)||new Set(value.providers.map(p=>p.id)).size!==value.providers.length)ctx.addIssue({code:'custom',message:'Invalid provider configuration response'})})
export type AISettings= z.infer<typeof aiSettingsSchema>
export type AISettingsInput={provider:ProviderID;model:string;apiKey?:string;removeKey?:boolean;ollamaHost?:string}
export async function readAISettings(signal:AbortSignal){return aiSettingsSchema.parse(await request('/settings/ai',{signal}))}
export async function saveAISettings(input:AISettingsInput){return aiSettingsSchema.parse(await request('/settings/ai',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(input)}))}
export async function testAISettings(){return z.object({status:z.enum(['reachable','failed']),message:z.enum(['model_found','model_unconfirmed']),checkedAt:z.iso.datetime({offset:true})}).parse(await request('/settings/ai/test',{method:'POST'},20000))}
