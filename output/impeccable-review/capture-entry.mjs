import {chromium} from '../../frontend/node_modules/playwright/index.mjs'
import fs from 'node:fs/promises'
import {fileURLToPath} from 'node:url'
const out=new URL('../../.impeccable/review/',import.meta.url)
await fs.mkdir(out,{recursive:true})
const browser=await chromium.launch()
try{
 for(const [locale,theme,width,name] of [['en','light',1440,'desktop'],['ar','dark',390,'mobile']]){
  const context=await browser.newContext({viewport:{width,height:900},reducedMotion:'reduce'})
  await context.addInitScript(({locale,theme})=>{localStorage.setItem('locale',locale);localStorage.setItem('theme',theme)},{locale,theme})
  const page=await context.newPage()
  await page.route('**/api/**',r=>r.fulfill({status:503,json:{error:'Read-only UI capture, no backend connection'}}))
  await page.goto('http://127.0.0.1:5194/app/analyses/new')
  await page.locator('.research-question').waitFor()
  await page.evaluate(()=>document.fonts.ready)
  await page.screenshot({path:fileURLToPath(new URL(name+'.png',out)),fullPage:true})
  await page.getByRole('button',{name:locale==='ar'?'إضافة أدلة':'Add evidence',exact:true}).click()
  await page.getByRole('menu').waitFor()
  await page.screenshot({path:fileURLToPath(new URL(name+'-menu.png',out)),fullPage:true})
  await page.keyboard.press('Escape')
  await page.getByRole('button',{name:locale==='ar'?'ابدأ البحث':'Start Investigation',exact:true}).click()
  await page.getByRole('alert').waitFor()
  await page.screenshot({path:fileURLToPath(new URL(name+'-validation.png',out)),fullPage:true})
  await page.locator('.research-question').fill(locale==='ar'?'هل تدعم البيانات انخفاضاً بنسبة 20%؟\nStudy 2025 — original evidence':'Does the original evidence support a 20% decline?\nCompare the claim with the supplied data.')
  await page.getByLabel(locale==='ar'?'إرفاق ملفات الأدلة':'Attach evidence files').setInputFiles([{name:'study-data.csv',mimeType:'text/csv',buffer:Buffer.from('value\n20')},{name:'supplement.xlsx',mimeType:'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',buffer:Buffer.from('Authored frontend screenshot selection only')}])
  await page.locator('.composer-attachments li').first().waitFor()
  await page.screenshot({path:fileURLToPath(new URL(name+'-draft.png',out)),fullPage:true})
  await context.close()
 }
}finally{await browser.close()}
