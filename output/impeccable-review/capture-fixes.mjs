import {chromium} from '../../frontend/node_modules/playwright/index.mjs'
import {fileURLToPath} from 'node:url'
const browser=await chromium.launch()
try{
 const context=await browser.newContext({viewport:{width:1440,height:1000},reducedMotion:'reduce'})
 const page=await context.newPage()
 await page.route('**/api/**',r=>r.fulfill({status:503,json:{error:'Frontend review capture only'}}))
 await page.goto('http://127.0.0.1:5194/docs/api')
 await page.locator('main h1').waitFor()
 await page.evaluate(()=>document.fonts.ready)
 await page.screenshot({path:fileURLToPath(new URL('../../.impeccable/review/docs-fixed.png',import.meta.url)),fullPage:true})
 await page.goto('http://127.0.0.1:5194/app/analyses/new?prepare=1')
 const select=page.getByLabel('Educational case (optional)',{exact:true})
 await select.selectOption('a1')
 await select.selectOption('a2')
 if(new URL(page.url()).searchParams.get('prepare')!=='1')throw new Error('Preparation route changed unexpectedly')
 await page.getByRole('heading',{name:'Evidence',exact:true}).waitFor()
 await page.screenshot({path:fileURLToPath(new URL('../../.impeccable/review/case-preparation-fixed.png',import.meta.url)),fullPage:true})
 await context.close()
}finally{await browser.close()}
