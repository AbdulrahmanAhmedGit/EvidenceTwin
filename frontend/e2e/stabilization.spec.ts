import {test,expect} from '@playwright/test'
import {mockInspection,rootId} from './helpers/inspection'
import {mockResearch,report} from './helpers/research'
import {analysisFixture} from '../src/features/inspection/fixtures/data'

test('identity mismatch blocks every section and job action until a matching response recovers',async({page})=>{
 await mockInspection(page)
 let mismatched=true
 const relatedRequests:string[]=[]
 const mutations:string[]=[]
 page.on('request',request=>{
  const path=new URL(request.url()).pathname
  if(path.startsWith('/api/analyses/'+rootId+'/'))relatedRequests.push(path)
  if(request.method()!=='GET'&&path.startsWith('/api/analyses/'))mutations.push(path)
 })
 await page.route('**/api/analyses/'+rootId,route=>route.fulfill({json:mismatched?{...analysisFixture,id:'foreign-analysis',title:'Foreign analysis must never render',status:'failed',actions:{retry:true,cancel:true}}:{...analysisFixture,id:rootId}}))
 for(const section of ['', 'evidence','visualizations','council','audit','report']){
  await page.goto('/app/analyses/'+rootId+(section?'/'+section:''))
  await expect(page.getByRole('heading',{name:'Research data unavailable'})).toBeVisible()
  await expect(page.getByText('Foreign analysis must never render',{exact:true})).toHaveCount(0)
  await expect(page.getByRole('button',{name:'Retry analysis',exact:true})).toHaveCount(0)
  await expect(page.getByRole('button',{name:'Cancel analysis',exact:true})).toHaveCount(0)
 }
 expect(relatedRequests).toEqual([])
 expect(mutations).toEqual([])
 mismatched=false
 await page.getByRole('button',{name:'Retry',exact:true}).click()
 await expect(page.locator('.report-document')).toBeVisible()
 await expect(page.locator('main h1').first()).toContainText('Axis framing')
 expect(relatedRequests).toContain('/api/analyses/'+rootId+'/report')
 expect(mutations).toEqual([])
})

test('a background identity mismatch hides cached metadata, closes confirmation and stops polling until recovery',async({page})=>{
 await page.emulateMedia({reducedMotion:'reduce'})
 await page.clock.install()
 await mockInspection(page)
 let phase:'valid'|'mismatch'|'recovered'='valid'
 let reads=0
 const relatedRequests:string[]=[]
 const mutations:string[]=[]
 await page.route('**/api/analyses/'+rootId,route=>{reads++;return route.fulfill({json:{...analysisFixture,id:phase==='mismatch'?'foreign':rootId,title:phase==='mismatch'?'Foreign analysis':'Previously validated analysis',status:phase==='recovered'?'completed_with_limitations':'running',actions:{cancel:true,retry:true}}})})
 page.on('request',request=>{const path=new URL(request.url()).pathname;if(path.startsWith('/api/analyses/'+rootId+'/'))relatedRequests.push(path);if(request.method()!=='GET'&&path.startsWith('/api/analyses/'))mutations.push(path)})
 await page.goto('/app/analyses/'+rootId)
 await page.getByRole('button',{name:'Cancel analysis',exact:true}).click()
 await expect(page.getByRole('dialog')).toBeVisible()
 phase='mismatch'
 await page.clock.fastForward(5200)
 await expect(page.getByRole('heading',{name:'Research data unavailable'})).toBeVisible()
 await expect(page.getByRole('dialog')).not.toBeVisible()
 await expect(page.getByRole('heading',{name:'Previously validated analysis',exact:true})).toHaveCount(0)
 await expect(page.getByRole('button',{name:'Cancel analysis',exact:true})).toHaveCount(0)
 await expect(page.getByText('Foreign analysis',{exact:true})).toHaveCount(0)
 const stopped=reads
 await page.clock.fastForward(60000)
 expect(reads).toBe(stopped)
 const navigationRead=page.waitForResponse(response=>new URL(response.url()).pathname==='/api/analyses/'+rootId)
 await page.getByRole('navigation',{name:'Analysis views'}).getByRole('link',{name:'Evidence',exact:true}).click()
 await (await navigationRead).finished()
 await page.clock.runFor(250)
 await expect(page.getByRole('heading',{name:'Research data unavailable'})).toBeVisible()
 expect(relatedRequests).toEqual([])
 expect(mutations).toEqual([])
 phase='recovered'
 await page.getByRole('button',{name:'Retry',exact:true}).click()
 await expect(page.getByRole('heading',{name:'Previously validated analysis',exact:true})).toBeVisible()
 await expect.poll(()=>relatedRequests.includes('/api/analyses/'+rootId+'/evidence')).toBeTruthy()
 expect(mutations).toEqual([])
})

async function comparisonSetup(page:import('@playwright/test').Page){
 await mockResearch(page)
 await mockInspection(page)
 await page.route('**/api/analyses?*',route=>route.fulfill({json:{items:[{id:rootId,title:'Current research analysis',createdAt:analysisFixture.createdAt,status:'completed',mode:'exploratory'},{id:'b',title:'Other research analysis',createdAt:analysisFixture.createdAt,status:'completed',mode:'exploratory'}],total:2,page:1,pageSize:10}}))
}

test('Compare analyses from overview preselects the current analysis using a and preserves it on refresh',async({page})=>{
 await comparisonSetup(page)
 await page.goto('/app/analyses/'+rootId)
 await page.getByRole('link',{name:'Compare analyses'}).click()
 await expect(page).toHaveURL('/app/compare?a='+rootId)
 const selected=page.getByRole('group',{name:'Analysis A',exact:true}).getByRole('radio',{name:/Current research analysis/})
 await expect(selected).toBeChecked()
 await page.reload()
 await expect(selected).toBeChecked()
 await page.getByRole('group',{name:'Analysis B',exact:true}).getByRole('radio',{name:/Other research analysis/}).click()
 await expect(page).toHaveURL('/app/compare?a='+rootId+'&b=b')
 await expect(page.getByRole('heading',{name:'These analyses are not scientifically comparable'})).toBeVisible()
})

test('legacy comparison links canonicalize to a and b without overriding canonical values or restoring cleared selections',async({page})=>{
 await comparisonSetup(page)
 await page.goto('/app/compare?analysisA='+rootId+'&analysisB=b')
 await expect(page).toHaveURL('/app/compare?a='+rootId+'&b=b')
 await expect(page.getByRole('group',{name:'Analysis A',exact:true}).getByRole('radio',{name:/Current research analysis/})).toBeChecked()
 await page.goto('/app/compare?a=b&analysisA=ignored&analysisB='+rootId)
 await expect(page).toHaveURL('/app/compare?a=b&b='+rootId)
 const group=page.getByRole('group',{name:'Analysis A',exact:true})
 await expect(group.getByRole('radio',{name:/Other research analysis/})).toBeChecked()
 await group.getByRole('button',{name:'Clear selection',exact:true}).click()
 await expect(page).toHaveURL('/app/compare?b='+rootId)
 await expect(group.getByRole('radio',{name:/Other research analysis/})).not.toBeChecked()
})

test('report filters and pagination survive reload and back/forward while filter changes reset the page',async({page})=>{
 await mockResearch(page)
 const requests:URLSearchParams[]=[]
 await page.route('**/api/reports?*',route=>{const params=new URL(route.request().url()).searchParams;requests.push(params);return route.fulfill({json:{items:[report],total:30,page:Number(params.get('page')),pageSize:10}})})
 const initial='/app/reports?search=authored&status=insufficient_evidence&mode=exploratory&from=2026-01-01&to=2026-11-03&sort=title%3Aasc&page=2'
 await page.goto(initial)
 const assertFilters=async()=>{
  await expect(page.getByRole('searchbox',{name:'Search reports'})).toHaveValue('authored')
  await expect(page.getByRole('combobox',{name:'Report assessment'})).toHaveValue('insufficient_evidence')
  await expect(page.getByRole('combobox',{name:'Report mode'})).toHaveValue('exploratory')
  await expect(page.getByLabel('Created from')).toHaveValue('2026-01-01')
  await expect(page.getByLabel('Created through')).toHaveValue('2026-11-03')
  await expect(page.getByRole('combobox',{name:'Sort reports'})).toHaveValue('title:asc')
 }
 await assertFilters()
 await expect(page.getByRole('status').filter({hasText:'Page 2 / 3'})).toBeVisible()
 await page.getByRole('button',{name:'Next',exact:true}).click()
 await expect(page).toHaveURL(/page=3/)
 await page.reload()
 await assertFilters()
 await expect(page.getByRole('status').filter({hasText:'Page 3 / 3'})).toBeVisible()
 await page.getByRole('combobox',{name:'Report mode'}).selectOption('verified')
 await expect.poll(()=>new URL(page.url()).searchParams.get('page')).toBeNull()
 await expect.poll(()=>requests.some(p=>p.get('mode')==='verified'&&p.get('page')==='1'&&p.get('search')==='authored')).toBeTruthy()
 await page.goBack()
 await assertFilters()
 await expect(page).toHaveURL(/page=3/)
 await page.goForward()
 await expect(page.getByRole('combobox',{name:'Report mode'})).toHaveValue('verified')
 await expect.poll(()=>new URL(page.url()).searchParams.get('page')).toBeNull()
})

test('invalid report URL controls fall back to supported defaults',async({page})=>{
 await mockResearch(page)
 const requests:URLSearchParams[]=[]
 page.on('request',request=>{if(new URL(request.url()).pathname==='/api/reports')requests.push(new URL(request.url()).searchParams)})
 await page.goto('/app/reports?status=invalid&mode=invalid&sort=invalid&page=-4&from=2026-99-99')
 await expect(page.getByRole('combobox',{name:'Report assessment'})).toHaveValue('')
 await expect(page.getByRole('combobox',{name:'Report mode'})).toHaveValue('')
 await expect(page.getByRole('combobox',{name:'Sort reports'})).toHaveValue('createdAt:desc')
 await expect.poll(()=>requests.some(p=>p.get('page')==='1'&&p.get('status')===''&&p.get('mode')===''&&p.get('sort')==='createdAt:desc'&&p.get('from')==='')).toBeTruthy()
})

test('native theme and browser chrome follow explicit and system themes across changes and refresh',async({page})=>{
 await mockResearch(page)
 await page.emulateMedia({colorScheme:'light'})
 await page.goto('/app/reports')
 const scheme=()=>page.getByRole('searchbox',{name:'Search reports'}).evaluate(el=>getComputedStyle(el).colorScheme)
 await expect.poll(scheme).toBe('light')
 await page.getByRole('button',{name:'Toggle theme',exact:true}).click()
 await expect.poll(scheme).toBe('dark')
 await expect(page.locator('meta[name="theme-color"]')).toHaveAttribute('content','#14221f')
 await page.reload()
 await expect.poll(scheme).toBe('dark')
 await page.goto('/app/settings')
 await page.getByLabel('Theme',{exact:true}).selectOption('light')
 await page.emulateMedia({colorScheme:'dark'})
 await expect(page.locator('html')).toHaveCSS('color-scheme','light')
 await expect(page.locator('meta[name="theme-color"]')).toHaveAttribute('content','#f6f5f0')
 await page.getByLabel('Theme',{exact:true}).selectOption('system')
 await expect(page.locator('html')).toHaveCSS('color-scheme','dark')
 await page.emulateMedia({colorScheme:'light'})
 await expect(page.locator('html')).toHaveCSS('color-scheme','light')
 await expect(page.locator('meta[name="theme-color"]')).toHaveAttribute('content','#f6f5f0')
})

test('rapid report edits preserve typed search while other filters change',async({page})=>{
 await mockResearch(page)
 const requests:URLSearchParams[]=[]
 page.on('request',request=>{if(new URL(request.url()).pathname==='/api/reports')requests.push(new URL(request.url()).searchParams)})
 await page.goto('/app/reports')
 const search=page.getByRole('searchbox',{name:'Search reports'})
 await search.pressSequentially('research evidence',{delay:0})
 await page.getByRole('combobox',{name:'Report mode'}).selectOption('exploratory')
 await page.getByLabel('Created from').fill('2026-01-01')
 await expect(search).toHaveValue('research evidence')
 await expect.poll(()=>requests.some(p=>p.get('search')==='research evidence'&&p.get('mode')==='exploratory'&&p.get('from')==='2026-01-01')).toBeTruthy()
 await page.reload()
 await expect(search).toHaveValue('research evidence')
 await expect(page.getByRole('combobox',{name:'Report mode'})).toHaveValue('exploratory')
 await expect(page.getByLabel('Created from')).toHaveValue('2026-01-01')
})
