import {useQuery} from '@tanstack/react-query'
import {z} from 'zod'
import {request} from '../../api'

const observation = z.object({label:z.string(), value:z.string(), rowNumber:z.number(), queryId:z.string()})
const comparison = z.object({id:z.string(), indicator:z.string(), year:z.string(), unit:z.string().nullable(),
  observations:z.array(observation), difference:z.string(), absoluteDifference:z.string(), differenceUnit:z.string(),
  ratio:z.string().nullable(), relation:z.enum(['higher','lower','equal']), scope:z.string(), method:z.string(),
  plot:z.object({version:z.string(),kind:z.literal('horizontal_bar'),scale:z.literal('linear'),domain:z.tuple([z.string(),z.string()]),baseline:z.literal('0'),transformation:z.literal('identity'),uncertaintyIntervals:z.string()}).optional()})
const sourceSchema=z.object({url:z.string(), status:z.string(), reason:z.string().optional(), retrievedAt:z.string().optional(),
    sha256:z.string().optional(), mediaType:z.string().optional(), evidenceId:z.string().optional(),origin:z.string().optional(),language:z.string().optional(),isGenerated:z.boolean().optional(),extraction:z.string().optional()})
export const processingSchema = z.object({version:z.string(), historical:z.boolean().optional(),
  datasets:z.array(z.object({evidenceId:z.string(), filename:z.string().nullable().optional(), sha256:z.string().nullable(), revisionId:z.string(),
    columns:z.array(z.string()), rowCount:z.number(), comparisons:z.array(comparison), queries:z.array(z.unknown())})),
  source:sourceSchema.nullable(), sources:z.array(sourceSchema).optional(),
  coverage:z.array(z.object({check:z.string(),status:z.string(),label:z.string().optional(),statusLabel:z.string().optional(),explanation:z.string().optional()})),
  limitations:z.array(z.object({id:z.string(),category:z.string(),importance:z.string(),check:z.string(),explanation:z.string(),nextStep:z.string(),
    classification:z.string().optional(),reportedBy:z.array(z.string()).optional(),
    variants:z.array(z.object({role:z.string(),explanation:z.string(),cause:z.string().nullable()})).optional()}))})
export type Comparison = z.infer<typeof comparison>
export async function readProcessing(path:string, signal:AbortSignal) {
  return processingSchema.parse(await request<unknown>(path,{signal}))
}

export function useEvidenceProcessing(id:string) {
  const endpoint = `/analyses/${encodeURIComponent(id)}/processing`
  return useQuery({queryKey:['evidence-processing',endpoint],queryFn:({signal})=>readProcessing(endpoint,signal),retry:false,staleTime:10000})
}
