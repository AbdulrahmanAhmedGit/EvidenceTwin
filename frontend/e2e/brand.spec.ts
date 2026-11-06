import {test,expect} from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'
import {mockResearch} from './helpers/research'
import {mockInspection,rootId} from './helpers/inspection'
import type {Locator} from '@playwright/test'
async function visibleArtwork(logo:Locator,theme:'light'|'dark',variant:'full'|'icon'='full'){
 const image=logo.locator('.brand-logo__'+theme)
 await expect(image).toBeVisible()
 await expect(logo.locator('.brand-logo__'+(theme==='dark'?'light':'dark'))).not.toBeVisible()
 await expect.poll(()=>image.evaluate((el:HTMLImageElement)=>el.complete&&el.naturalWidth>0)).toBeTruthy()
 const box=await image.boundingBox()
 expect(box!.width/box!.height).toBeCloseTo(variant==='full'?1277/298:317/339,2)
 await expect(image).toHaveCSS('transform','none')
}
test.beforeEach(async({page})=>{await mockResearch(page)})
test('branding follows app preference instead of OS preference and updates SVG/PNG favicons immediately',async({page})=>{
 await page.emulateMedia({colorScheme:'dark'})
 await page.addInitScript(()=>localStorage.setItem('theme','light'))
 await page.goto('/')
 const logo=page.locator('header .brand-logo--full')
 await visibleArtwork(logo,'light')
 await expect(page.locator('#app-favicon')).toHaveAttribute('href','/brand/evidencetwin-icon.svg')
 await page.getByRole('button',{name:'Toggle theme',exact:true}).click()
 await visibleArtwork(logo,'dark')
 await expect(page.locator('#app-favicon')).toHaveAttribute('href','/brand/evidencetwin-icon-dark.svg')
 await expect(page.locator('#app-favicon-png')).toHaveAttribute('href','/brand/favicon-32-dark.png')
 await page.emulateMedia({colorScheme:'light'})
 await visibleArtwork(logo,'dark')
 await page.goto('/app/settings')
 await page.getByLabel('Theme',{exact:true}).selectOption('system')
 const sidebar=page.locator('.sidebar-brand .brand-logo--full')
 await visibleArtwork(sidebar,'light')
 await page.emulateMedia({colorScheme:'dark'})
 await visibleArtwork(sidebar,'dark')
})
test('expanded/collapsed sidebar uses one prominent logo and retains accessible keyboard navigation',async({page})=>{
 await page.goto('/app')
 await expect(page.locator('header .workspace-header-brand')).not.toBeVisible()
 await visibleArtwork(page.locator('.sidebar-brand .brand-logo--full'),'light')
 await page.getByRole('button',{name:'Collapse navigation',exact:true}).click()
 await visibleArtwork(page.locator('.sidebar-brand .brand-logo--icon'),'light','icon')
 await expect(page.locator('.sidebar-brand .brand-logo--full')).not.toBeVisible()
 await expect(page.getByRole('link',{name:'EvidenceTwin home',exact:true})).toHaveAttribute('title','EvidenceTwin home')
 await page.getByRole('link',{name:'Case Library',exact:true}).first().focus()
 await page.keyboard.press('Enter')
 await expect(page).toHaveURL('/app/library')
 await page.getByRole('button',{name:'Expand navigation',exact:true}).click()
 await visibleArtwork(page.locator('.sidebar-brand .brand-logo--full'),'light')
 await page.getByRole('link',{name:'EvidenceTwin home',exact:true}).focus()
 await page.keyboard.press('Enter')
 await expect(page).toHaveURL('/')
})
for(const locale of ['en','ar'])for(const theme of ['light','dark'] as const)test(`brand layout and visual inspection ${locale} ${theme}`,async({page})=>{
 const errors:string[]=[];const assetFailures:string[]=[]
 page.on('pageerror',error=>errors.push(error.message))
 page.on('response',response=>{if(response.url().includes('/brand/')&&response.status()>=400)assetFailures.push(response.url())})
 await page.addInitScript(({locale,theme})=>{localStorage.setItem('locale',locale);localStorage.setItem('theme',theme)},{locale,theme})
 for(const route of ['/','/app'])for(const width of [360,390,768,1024,1440,1920]){
  await page.setViewportSize({width,height:900})
  await page.goto(route)
  await expect(page.locator('main h1')).toBeVisible()
  const mobile=width<=760;const workspace=route==='/app'
  const selector=workspace&&!mobile?'.sidebar-brand .brand-logo--full':width<=380?'header .brand-logo--icon':'header .brand-logo--full'
  await visibleArtwork(page.locator(selector),theme,width<=380?'icon':'full')
  await expect(page.locator(selector)).toHaveAttribute('dir','ltr')
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBeTruthy()
  if(width===390||width===1440){
   await page.screenshot({path:`output/playwright/brand-${locale}-${theme}-${workspace?'workspace':'home'}-${width}.png`,fullPage:true})
   const axe=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa','wcag22aa']).analyze()
   expect(axe.violations).toEqual([])
   if(workspace&&width===1440){
    await page.getByRole('button',{name:locale==='ar'?'طي القائمة':'Collapse navigation',exact:true}).click()
    await visibleArtwork(page.locator('.sidebar-brand .brand-logo--icon'),theme,'icon')
    await page.screenshot({path:`output/playwright/brand-${locale}-${theme}-workspace-collapsed-1440.png`})
    await page.getByRole('button',{name:locale==='ar'?'توسيع':'Expand navigation',exact:true}).click()
   }
   if(!workspace&&width===390){
    const toggle=page.getByRole('button',{name:locale==='ar'?'تبديل قائمة التنقل':'Toggle navigation',exact:true})
    await toggle.click();await expect(toggle).toHaveAttribute('aria-expanded','true')
    await page.keyboard.press('Escape');await expect(toggle).toBeFocused()
   }
  }
 }
 expect(errors).toEqual([]);expect(assetFailures).toEqual([])
})
test('public routes share official header/footer branding without temporary symbols',async({page})=>{
 for(const route of ['/how-it-works','/methodology','/features','/integrations','/about','/docs','/docs/getting-started','/docs/api','/docs/mcp','/docs/skills','/privacy','/terms','/not-a-page']){
  await page.goto(route)
  await visibleArtwork(page.locator('header .brand-logo--full'),'light')
  await expect(page.locator('footer .brand-logo--full .brand-logo__light')).toHaveAttribute('src','/brand/evidencetwin-logo.svg')
  await expect(page.locator('body')).not.toContainText('Ⅱ')
 }
})
test('report masthead uses the dark artwork on screen and the light artwork for print',async({page})=>{
 await mockInspection(page)
 await page.addInitScript(()=>localStorage.setItem('theme','dark'))
 await page.goto('/app/analyses/'+rootId+'/report')
 const logo=page.locator('.report-masthead .brand-logo')
 await visibleArtwork(logo,'dark')
 await page.emulateMedia({media:'print'})
 await visibleArtwork(logo,'light')
 await expect(page.locator('.report-document')).toBeVisible()
})
test('all official assets and derived icons load with correct dimensions',async({page})=>{
 await page.goto('/')
 const paths=['evidencetwin-logo.svg','evidencetwin-logo-dark.svg','evidencetwin-icon.svg','evidencetwin-icon-dark.svg','favicon-16.png','favicon-16-dark.png','favicon-32.png','favicon-32-dark.png','apple-touch-icon.png']
 for(const name of paths){const response=await page.request.get('/brand/'+name);expect(response.status(),name).toBe(200);expect(response.headers()['content-type']).toContain(name.endsWith('.svg')?'image/svg+xml':'image/png')}
 const sizes=await page.evaluate(async(paths)=>Promise.all(paths.filter(p=>p.endsWith('.png')).map(async name=>{const image=new Image();image.src='/brand/'+name;await image.decode();return{name,width:image.naturalWidth,height:image.naturalHeight}})),paths)
 for(const icon of sizes){const size=icon.name.startsWith('apple')?180:icon.name.includes('16')?16:32;expect(icon.width).toBe(size);expect(icon.height).toBe(size)}
 await expect(page.locator('link[rel="apple-touch-icon"]')).toHaveAttribute('href','/brand/apple-touch-icon.png')
})
