import {test,expect} from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'
import {mockResearch} from './helpers/research'
import {mockInspection,rootId} from './helpers/inspection'

const inspection='/app/analyses/'+rootId
const publicRoutes=['/','/features','/how-it-works','/methodology','/integrations','/about','/privacy','/terms','/docs','/docs/getting-started','/docs/api','/docs/mcp','/docs/skills']
const workspaceRoutes=['/app','/app/analyses','/app/analyses/new','/app/library','/app/library/a1','/app/settings','/app/settings/ai','/app/compare?a=a&b=b','/app/benchmarks','/app/benchmarks/new','/app/benchmarks/run-1','/app/reports','/app/integrations',inspection,inspection+'/evidence',inspection+'/visualizations',inspection+'/council',inspection+'/audit',inspection+'/report']
const captures=new Map([['/','home'],['/app','workspace'],['/app/analyses/new','builder'],['/docs/api','docs'],[inspection+'/evidence','evidence'],[inspection+'/council','council'],[inspection+'/report','report']])

test.beforeEach(async({page})=>{
 await page.route('**/api/**',route=>route.fulfill({status:503,json:{error:'Deliberate frontend test unavailable state'}}))
 await mockResearch(page)
 await mockInspection(page)
})

for(const locale of ['en','ar'])for(const theme of ['light','dark'])test(`dossier route matrix ${locale} ${theme}`,async({page})=>{
 test.setTimeout(180000)
 const errors:string[]=[]
 page.on('pageerror',error=>errors.push(error.message))
 await page.emulateMedia({reducedMotion:'reduce'})
 await page.addInitScript(({locale,theme})=>{localStorage.setItem('locale',locale);localStorage.setItem('theme',theme)},{locale,theme})
 for(const width of [320,768,1440]){
  await page.setViewportSize({width,height:1000})
  for(const route of [...publicRoutes,...workspaceRoutes]){
   await page.goto(route)
   await expect(page.locator('main h1')).toBeVisible()
   await page.evaluate(()=>document.fonts.ready)
   await expect(page.locator('.root')).toHaveAttribute('dir',locale==='ar'?'rtl':'ltr')
   expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${route} ${width} ${locale} ${theme}`).toBeTruthy()
   if(captures.has(route)&&((width===1440&&locale==='en'&&theme==='light')||(width===320&&locale==='ar'&&theme==='dark'))){
    await page.screenshot({path:`output/playwright/dossier-${captures.get(route)}-${locale}-${theme}-${width}.png`,fullPage:true})
   }
  }
 }
 expect(errors).toEqual([])
})

for(const locale of ['en','ar'])for(const theme of ['light','dark'])test(`dossier accessibility ${locale} ${theme}`,async({page})=>{
 test.setTimeout(120000)
 await page.emulateMedia({reducedMotion:'reduce'})
 await page.addInitScript(({locale,theme})=>{localStorage.setItem('locale',locale);localStorage.setItem('theme',theme)},{locale,theme})
 for(const route of ['/','/docs/api','/app','/app/analyses/new','/app/library','/app/settings',inspection+'/evidence',inspection+'/visualizations',inspection+'/council',inspection+'/report']){
  await page.goto(route)
  await expect(page.locator('main h1')).toBeVisible()
  const audit=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa','wcag22aa']).analyze()
  expect(audit.violations,route).toEqual([])
 }
})

test('unavailable submission is disclosed before entering evidence and preserves the draft',async({page})=>{
 await page.route('**/api/capabilities',route=>route.fulfill({json:{analyses:{create:false}}}))
 await page.setViewportSize({width:390,height:844})
 await page.goto('/app/analyses/new?prepare=1')
 await expect(page.locator('.submission-readiness')).toContainText('Analysis submission is currently unavailable.')
 await expect(page.locator('.step-position')).toHaveText('Step 1 of 5 · Evidence')
 await page.getByLabel('Educational case (optional)').selectOption('a1')
 await page.getByRole('button',{name:'Continue',exact:true}).click()
 await expect(page.locator('.step-position')).toHaveText('Step 2 of 5 · Source & Study')
 await page.getByRole('button',{name:'Back',exact:true}).click()
 await expect(page.getByLabel('Educational case (optional)')).toHaveValue('a1')
})

test('source index and mobile category select retain inspection and citation navigation',async({page})=>{
 await page.setViewportSize({width:1440,height:1000})
 await page.goto(inspection+'/evidence')
 await page.getByRole('navigation',{name:'Evidence categories'}).getByRole('button',{name:'Data values',exact:true}).click()
 await expect(page.getByRole('heading',{name:'Data values',exact:true})).toBeVisible()
 await expect(page.getByRole('table')).toBeVisible()
 await page.getByRole('navigation',{name:'Evidence categories'}).getByRole('button',{name:'Evidence Contract',exact:true}).click()
 await expect(page.getByRole('heading',{name:'Evidence Contract',exact:true})).toBeVisible()
 await page.setViewportSize({width:390,height:844})
 await page.getByLabel('Evidence category',{exact:true}).selectOption('sources')
 await expect(page.getByRole('heading',{name:'Original sources',exact:true})).toBeVisible()
 await page.goto(inspection+'/council')
 await page.getByRole('link',{name:'Inspect reference brief-a1'}).first().click()
 await expect(page.locator('.source-record.highlighted')).toBeVisible()
})

test('Arabic keeps provider identifiers and structured records isolated without mirroring charts',async({page})=>{
 await page.addInitScript(()=>localStorage.setItem('locale','ar'))
 await page.goto(inspection+'/council')
 await page.getByRole('button',{name:'افحص المراجعة المنظمة'}).first().click()
 await expect(page.getByRole('dialog')).toBeVisible()
 await page.getByRole('button',{name:'إغلاق المراجعة'}).click()
 await page.getByRole('button',{name:'افحص الاستجابة JSON'}).click()
 await expect(page.locator('.json-view pre').first()).toHaveAttribute('dir','ltr')
 await expect(page.locator('.json-view pre').first()).toHaveCSS('direction','ltr')
 await page.goto(inspection+'/visualizations')
 await expect(page.locator('.chart-window').first()).toBeVisible()
 await page.getByLabel('عرض المقارنة',{exact:true}).selectOption('slider')
 await expect(page.locator('input[type=range]').first()).toHaveCSS('direction','ltr')
})
