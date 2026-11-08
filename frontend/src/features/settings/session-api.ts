import {z} from 'zod'
import {useQuery} from '@tanstack/react-query'
import {request} from '../../api'
export const sessionSchema=z.object({accountsEnabled:z.boolean(),authenticated:z.boolean(),operator:z.boolean(),name:z.string().nullable(),workspaceId:z.string().nullable()})
export function useSession(){return useQuery({queryKey:['session'],queryFn:async()=>sessionSchema.parse(await request('/session')),retry:false,staleTime:60000})}
