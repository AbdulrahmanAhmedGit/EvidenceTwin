import {test,expect} from '@playwright/test'
test('homepage framing controls and case navigation',async({page})=>{await page.goto('/');await expect(page.getByRole('heading',{name:'Same data. Different story.'})).toBeVisible();await page.getByRole('button',{name:'Neutral baseline',exact:true}).click();await expect(page.getByText('Neutral display · zero baseline').first()).toBeVisible();await page.goto('/app/library/a1');await expect(page.getByRole('heading',{name:'Truncated axis'})).toBeVisible();await page.getByRole('link',{name:'New Analysis',exact:true}).last().click();await expect(page.getByRole('heading',{name:'Evidence',exact:true})).toBeVisible()})
test('wizard prevents empty evidence',async({page})=>{await page.goto('/app/analyses/new?prepare=1');await page.getByRole('button',{name:'Continue',exact:true}).click();await expect(page.getByRole('alert')).toContainText('Add evidence')})
test('mobile navigation, language and theme',async({page})=>{await page.setViewportSize({width:390,height:844});await page.goto('/');await page.getByRole('button',{name:'Toggle navigation'}).click();await page.getByRole('link',{name:'Methodology',exact:true}).first().click();await expect(page).toHaveURL(/methodology/);await page.getByRole('button',{name:'Change language'}).click();await expect(page.locator('.root')).toHaveAttribute('dir','rtl');await page.getByRole('button',{name:'تبديل السمة'}).click();await expect(page.locator('.root')).toHaveClass(/dark/)})
test('mobile menu supports focus, Escape, dismissal and route focus',async({page})=>{
 await page.setViewportSize({width:390,height:844});await page.goto('/');
 const toggle=page.getByRole('button',{name:'Toggle navigation'});
 await toggle.click();await expect(page.getByRole('navigation',{name:'Main navigation'}).getByRole('link',{name:'Features',exact:true})).toBeFocused();
 await page.keyboard.press('Escape');await expect(toggle).toBeFocused();await expect(toggle).toHaveAttribute('aria-expanded','false');
 await toggle.click();await page.getByRole('link',{name:'Methodology',exact:true}).first().click();
 await expect(page.locator('#main')).toBeFocused();await expect(toggle).toHaveAttribute('aria-expanded','false');
 await toggle.click();await page.getByRole('heading',{name:'Planned evaluation',exact:true}).click();await expect(toggle).toHaveAttribute('aria-expanded','false');
 await page.goto('/app');await toggle.click();await expect(toggle).toHaveAttribute('aria-expanded','true');await page.getByRole('navigation',{name:'Main navigation'}).getByRole('link',{name:'Settings',exact:true}).click();await expect(page).toHaveURL(/settings/);await expect(toggle).toHaveAttribute('aria-expanded','false');await expect(page.locator('#main')).toBeFocused();
})
test('wizard announces its current step and moves focus',async({page})=>{
 await page.goto('/app/analyses/new?case=a1');await page.getByRole('button',{name:'Continue',exact:true}).click();
 await expect(page.locator('#wizard-step-title')).toBeFocused();await expect(page.locator('[aria-current="step"]')).toContainText('Source & Study');
})
test('reduced motion setting is applied immediately and survives reload',async({page})=>{
 await page.goto('/app/settings');await page.getByLabel('Motion',{exact:true}).selectOption('Reduced');
 await expect(page.locator('html')).toHaveAttribute('data-motion','reduced');
 await page.reload();await expect(page.locator('html')).toHaveAttribute('data-motion','reduced');
 await expect(page.locator('.route-content')).toHaveCSS('animation-name','none');
})
test('system reduced motion suppresses page transitions',async({page})=>{
 await page.emulateMedia({reducedMotion:'reduce'});await page.goto('/');
 await expect(page.locator('.route-content')).toHaveCSS('animation-name','none');
})
test('documentation searches content and opens the matching section',async({page})=>{
 await page.goto('/docs');await page.getByRole('searchbox',{name:'Search documentation'}).fill('idempotency');
 await expect(page.getByRole('heading',{name:'Search results'})).toBeVisible();
 await page.getByRole('link',{name:'Analysis acceptance'}).click();
 await expect(page).toHaveURL(/docs\/api#submission/);await expect(page.locator('#submission')).toBeFocused();
})
test('public Arabic content uses distinct translated section titles',async({page})=>{
 await page.goto('/methodology');await page.getByRole('button',{name:'Change language'}).click();
 await expect(page.getByRole('heading',{name:'الدراسات الرصدية والسببية'})).toBeVisible();
 await page.getByRole('navigation',{name:'في هذه الصفحة'}).getByRole('link',{name:'الإجماع لا يعني الصحة'}).click();
 await expect(page.locator('#consensus')).toBeFocused();await expect(page.locator('html')).toHaveAttribute('lang','ar');
})
test('desktop sidebar collapse preserves labeled navigation',async({page})=>{
 await page.goto('/app');await page.getByRole('button',{name:'Collapse navigation'}).click();
 await expect(page.getByRole('button',{name:'Expand navigation'})).toHaveAttribute('aria-expanded','false');
 await page.getByRole('link',{name:'Case Library',exact:true}).first().click();await expect(page).toHaveURL(/app\/library/);
})


test('motion has one public scroll owner and releases it for research and reduced motion',async({page})=>{
 await page.goto('/')
 await expect(page.locator('.root')).toHaveAttribute('data-motion-engine','gsap')
 await expect(page.locator('.root')).toHaveAttribute('data-scroll-engine','lenis')
 await page.goto('/app/library')
 await expect(page.locator('.root')).not.toHaveAttribute('data-motion-engine','gsap')
 await expect(page.locator('.root')).not.toHaveAttribute('data-scroll-engine','lenis')
 await expect(page.locator('html')).not.toHaveClass(/lenis/)
 await page.goto('/methodology')
 await expect(page.locator('.root')).toHaveAttribute('data-scroll-engine','lenis')
 await page.emulateMedia({reducedMotion:'reduce'})
 await expect(page.locator('.root')).not.toHaveAttribute('data-motion-engine','gsap')
 await expect(page.locator('html')).not.toHaveClass(/lenis/)
 await expect(page.locator('main h1')).toBeVisible()
 await page.emulateMedia({reducedMotion:'no-preference'})
 await expect(page.locator('.root')).toHaveAttribute('data-scroll-engine','lenis')
})
test('split headings retain a single accessible Arabic name and skip motion loading when reduced',async({page})=>{
 const motionRequests:string[]=[]
 page.on('request',r=>{if(r.url().includes('/motion/siteMotion'))motionRequests.push(r.url())})
 await page.addInitScript(()=>{localStorage.setItem('locale','ar');localStorage.setItem('Motion','Reduced')})
 await page.goto('/')
 const heading=page.getByRole('heading',{name:'نفس البيانات. قصة مختلفة.',exact:true})
 await expect(heading).toBeVisible()
 await expect(heading).toHaveCount(1)
 await expect(heading).toHaveText('نفس البيانات.قصة مختلفة.')
 await expect(page.locator('.root')).not.toHaveAttribute('data-motion-engine','gsap')
 expect(motionRequests).toEqual([])
})
test('JavaScript-disabled visitors receive a complete honest reading fallback',async({browser,baseURL})=>{
 const context=await browser.newContext({javaScriptEnabled:false,baseURL})
 try{
  const page=await context.newPage()
  await page.goto('/')
  await expect(page.getByRole('heading',{name:'Same data. Different story.'})).toBeVisible()
  await expect(page.getByRole('table')).toContainText('42%')
  await expect(page.getByRole('table')).toContainText('40%')
  await expect(page.getByText(/interactive workspace.*require JavaScript/)).toBeVisible()
  await expect(page.getByRole('heading',{name:'Agreement is not scientific proof.'})).toBeVisible()
 }finally{await context.close()}
})


test('Arabic uses Alan Sans, mobile fields avoid undersized text, and control edges retain contrast',async({page})=>{
 await page.addInitScript(()=>{localStorage.setItem('locale','ar');localStorage.setItem('Motion','Reduced')})
 await page.setViewportSize({width:390,height:844})
 for(const theme of ['light','dark']){
  await page.goto('/app/analyses/new?case=a1')
  await page.evaluate(value=>localStorage.setItem('theme',value),theme)
  await page.reload()
  const field=page.locator('.form-panel select').first()
  await expect(field).toHaveCSS('font-size','16px')
  await expect(field).toHaveCSS('font-family','"Alan Sans Variable", sans-serif')
  await page.evaluate(()=>document.fonts.ready)
  expect(await page.evaluate(()=>document.fonts.check('400 16px "Alan Sans Variable"','العربية'))).toBeTruthy()
  const ratios=await field.evaluate(el=>{
   const s=getComputedStyle(el)
   const luminance=(color:string)=>{const rgb=color.match(/[\d.]+/g)!.slice(0,3).map(Number).map(c=>{c/=255;return c<=.04045?c/12.92:((c+.055)/1.055)**2.4});return rgb.reduce((sum,v,i)=>sum+v*[.2126,.7152,.0722][i],0)}
   const contrast=(a:string,b:string)=>{const x=luminance(a),y=luminance(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05)}
   return {text:contrast(s.color,s.backgroundColor),border:contrast(s.borderTopColor,s.backgroundColor)}
  })
  expect(ratios.text).toBeGreaterThanOrEqual(4.5)
  expect(ratios.border).toBeGreaterThanOrEqual(3)
 }
 await page.setViewportSize({width:640,height:900})
 await page.evaluate(()=>document.documentElement.style.fontSize='200%')
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBeTruthy()
 await expect(page.locator('.form-panel select').first()).toHaveCSS('font-size','32px')
})

test('dashboard scopes workflow counts to loaded records and keeps unavailable totals distinct from zero',async({page})=>{
 let offline=false
 await page.route('**/api/analyses?*',route=>offline?route.fulfill({status:503,json:{error:{message:'Research database unavailable'}}}):route.fulfill({json:{items:[{id:'scope-test',title:'Scoped research record',createdAt:'2026-11-03T00:00:00Z',status:'running',mode:'exploratory',reportAvailable:false}],total:26,page:1,pageSize:10}}))
 await page.goto('/app')
 await expect(page.locator('.workspace-stat').nth(0).locator('.stat-value')).toHaveText('26')
 await expect(page.locator('.workspace-stat').nth(1).locator('.stat-value')).toHaveText('1')
 await expect(page.locator('.workspace-stat').nth(1)).toContainText('In the latest 1 record')
 await expect(page.getByRole('img',{name:'Running: 1'})).toBeVisible()
 await expect(page.getByText('Execution status only. Completion does not establish scientific verification.')).toBeVisible()
 offline=true
 await page.reload()
 await expect(page.getByRole('heading',{name:'Research records unavailable'})).toBeVisible()
 await expect(page.locator('.workspace-stats')).toHaveCount(0)
 await expect(page.getByRole('heading',{name:'No analyses yet.'})).toHaveCount(0)
 offline=false
 await page.getByRole('alert').getByRole('button',{name:'Retry connection'}).click()
 await expect(page.getByRole('link',{name:'Scoped research record',exact:true})).toBeVisible()
})

test('research pages reflow at 320px and at doubled text size in both languages',async({page})=>{
 await page.route('**/api/capabilities',route=>route.fulfill({json:{analyses:{}}}))
 await page.route('**/api/analyses?*',route=>route.fulfill({json:{items:[],total:0,page:1,pageSize:10}}))
 for(const locale of ['en','ar']){
  await page.goto('/app/settings')
  await page.getByRole('combobox',{name:locale==='ar'?'Language':'Language',exact:true}).selectOption(locale)
  for(const width of [320,768]){
   await page.setViewportSize({width,height:900})
   for(const path of ['/app','/app/analyses','/app/analyses/new','/app/settings','/docs']){
    await page.goto(path)
    await page.locator('main h1').first().waitFor()
    await page.evaluate(size=>{document.documentElement.style.fontSize=size},width===768?'200%':'100%')
    expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${locale} ${path} at ${width}`).toBeTruthy()
    if(width===768&&path.startsWith('/app')){expect(await page.locator('.app-layout>aside').evaluate(e=>e.scrollWidth<=e.clientWidth),'Sidebar text remains readable without horizontal clipping').toBeTruthy()}
   }
  }
  await page.evaluate(()=>{document.documentElement.style.fontSize=''})
 }
})
