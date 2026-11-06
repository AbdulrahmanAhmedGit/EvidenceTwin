import {describe,it,expect,vi,afterEach} from 'vitest'
import {analysisSchema,datasetSchema,sectionSchema,readAnalysis,AnalysisIdentityError} from '../../research-api'
import {redact,redactText} from './utils'
import {analysisFixture,auditFixture} from './fixtures/data'
afterEach(()=>vi.unstubAllGlobals())
describe('scientific inspection boundaries',()=>{
 it('rejects values that do not align with their column definitions',()=>{expect(()=>datasetSchema.parse({columns:['Year','Rate'],rows:[[2021]]})).toThrow('row widths')})
 it('does not invent a verdict, source verification or job action',()=>{const {assessment:_assessment,sourceStatus:_sourceStatus,actions:_actions,...input}=analysisFixture;const result=analysisSchema.parse(input);expect(result.assessment).toBeUndefined();expect(result.sourceStatus).toBe('unknown');expect(result.actions.cancel).toBe(false)})
 it('keeps missing uncertainty bounds missing',()=>{const result=sectionSchema.parse({uncertainty:[]});expect(result.dataset).toBeUndefined();expect(result.uncertainty).toEqual([])})
 it('redacts nested credentials in structured events',()=>{const event=sectionSchema.parse(auditFixture).events?.[0];expect(JSON.stringify(event)).not.toContain('TEST_ONLY_REDACT_ME');expect(event?.metadata?.apiKey).toBe('[redacted]')})
 it('rejects executable and credential-bearing source links',()=>{for(const url of ['javascript:alert(1)','https://user:password@example.org'])expect(()=>sectionSchema.parse({sources:[{id:'a',title:'source',status:'unverified',checked:'none',url}]})).toThrow()})
 it('does not fall back to a sample result on API failure',async()=>{vi.stubGlobal('fetch',vi.fn().mockRejectedValue(new TypeError('offline')));await expect(readAnalysis('sample-a1',new AbortController().signal)).rejects.toThrow('Could not reach')})
 it('redacts log-style token strings without altering ordinary scientific text',()=>{expect(redactText('Bearer pretend-secret')).toBe('Bearer [redacted]');expect(redactText('42 minus 40 = 2')).toBe('42 minus 40 = 2');expect(redact({nested:{access_token:'dummy'}})).toEqual({nested:{access_token:'[redacted]'}})})
})

describe('analysis response identity',()=>{
 it('rejects a schema-valid response for another analysis',async()=>{
  vi.stubGlobal('fetch',vi.fn().mockResolvedValue(Response.json({...analysisFixture,id:'foreign'})))
  await expect(readAnalysis('requested',new AbortController().signal)).rejects.toBeInstanceOf(AnalysisIdentityError)
 })
 it('accepts only the exact requested ID and encodes it in the request path',async()=>{
  const id='analysis/with space'
  const fetcher=vi.fn().mockResolvedValue(Response.json({...analysisFixture,id}))
  vi.stubGlobal('fetch',fetcher)
  await expect(readAnalysis(id,new AbortController().signal)).resolves.toMatchObject({id})
  expect(fetcher.mock.calls[0][0]).toBe('/api/analyses/analysis%2Fwith%20space')
 })
 it('can recover through a fresh matching response after rejection',async()=>{
  const fetcher=vi.fn().mockResolvedValueOnce(Response.json({...analysisFixture,id:'foreign'})).mockResolvedValueOnce(Response.json({...analysisFixture,id:'requested'}))
  vi.stubGlobal('fetch',fetcher)
  await expect(readAnalysis('requested',new AbortController().signal)).rejects.toThrow('Analysis response ID mismatch.')
  await expect(readAnalysis('requested',new AbortController().signal)).resolves.toMatchObject({id:'requested'})
  expect(fetcher).toHaveBeenCalledTimes(2)
 })
})
