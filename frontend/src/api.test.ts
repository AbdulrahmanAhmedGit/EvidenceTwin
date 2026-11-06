import {afterEach,describe,it,expect,vi} from 'vitest'
import {api,ApiError} from './api'
afterEach(()=>vi.restoreAllMocks())
describe('Flask boundary',()=>{
it('rejects SPA HTML instead of reporting a healthy backend',async()=>{vi.stubGlobal('fetch',vi.fn().mockResolvedValue(new Response('<html/>',{headers:{'content-type':'text/html'}})));await expect(api.health()).rejects.toThrow('incompatible response')})
it('preserves authorization status',async()=>{vi.stubGlobal('fetch',vi.fn().mockResolvedValue(new Response('',{status:401})));await expect(api.health()).rejects.toMatchObject({status:401})})
it('normalizes network failure without a fixture fallback',async()=>{vi.stubGlobal('fetch',vi.fn().mockRejectedValue(new TypeError('network')));await expect(api.health()).rejects.toBeInstanceOf(ApiError)})
it('reads JSON health information',async()=>{vi.stubGlobal('fetch',vi.fn().mockResolvedValue(Response.json({status:'ok'})));await expect(api.health()).resolves.toEqual({status:'ok'})})
})
describe('analysis acceptance',()=>{
it('returns a server ID without performing browser navigation',async()=>{vi.stubGlobal('fetch',vi.fn().mockResolvedValue(Response.json({id:'accepted-id'})));await expect(api.createAnalysis({claim:'User supplied'},[])).resolves.toEqual({id:'accepted-id'})})
it('rejects successful HTTP without an actual analysis ID',async()=>{vi.stubGlobal('fetch',vi.fn().mockResolvedValue(Response.json({id:123})));await expect(api.createAnalysis({claim:'User supplied'},[])).rejects.toThrow('valid analysis ID')})
it('supports deletion responses with no JSON payload',async()=>{vi.stubGlobal('fetch',vi.fn().mockResolvedValue(new Response(null,{status:204})));const {request}=await import('./api');await expect(request('/analyses/id',{method:'DELETE'})).resolves.toBeUndefined()})
})
