import {chromium} from '../../frontend/node_modules/playwright/index.mjs';
import fs from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import * as f from '../../frontend/src/features/inspection/fixtures/data.ts';
const out=new URL('./',import.meta.url);const browser=await chromium.launch();const results=[];const logs=[];
const routes=['/','/app/analyses/new','/app/analyses/inspection-1/visualizations'];
try {
for(const locale of ['en','ar'])for(const theme of ['light']){
 const context=await browser.newContext({viewport:{width:1440,height:1000},reducedMotion:'reduce'});const page=await context.newPage();
 await page.addInitScript(({locale,theme})=>{localStorage.setItem('locale',locale);localStorage.setItem('theme',theme)},{locale,theme});
 await page.route('**/api/**',async r=>{const u=new URL(r.request().url());if(r.request().method()!=='GET')return r.fulfill({status:405,json:{error:'Audit read-only guard'}});const part=u.pathname.split('/').slice(4).join('/');const data={'':{...f.analysisFixture,id:'inspection-1'},evidence:f.evidenceFixture,visualizations:f.visualizationFixture('/__inspection__/original.svg','/__inspection__/neutral.svg'),council:f.councilFixture,audit:f.auditFixture,report:f.reportFixture};if(u.pathname.startsWith('/api/analyses/inspection-1'))return r.fulfill({json:data[part]??{}});return r.fulfill({status:503,json:{error:'Audit intentionally unavailable backend; inspection records use labeled authored request fixtures'}})});
 await page.route('**/__inspection__/*.svg',async r=>r.fulfill({contentType:'image/svg+xml',body:await fs.readFile(new URL('../../frontend/src/features/inspection/fixtures/'+(r.request().url().includes('original')?'original.svg':'neutral.svg'),import.meta.url),'utf8')}));
 page.on('pageerror',e=>logs.push({locale,theme,type:'pageerror',text:e.message}));page.on('console',m=>{if(m.text().toLowerCase().includes('impeccable'))logs.push({locale,theme,type:m.type(),text:m.text()})});
 for(const route of routes){
  await page.goto('http://127.0.0.1:5194'+route);await page.locator('main h1').waitFor();await page.evaluate(()=>document.fonts.ready);await page.waitForTimeout(200);
  const axe=[];
  const dimensions=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,dir:document.documentElement.dir,lang:document.documentElement.lang}));
  const key=route.replaceAll('/','_')||'home';
  results.push({locale,theme,route,viewport:'desktop',dimensions,axe});
  if(theme==='light')for(const width of [320,360,768]){
   await page.setViewportSize({width,height:900});await page.waitForTimeout(100);
   const mobile=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,overflow:[...document.querySelectorAll('main *')].filter(e=>{const r=e.getBoundingClientRect();return r.width&&r.right>innerWidth+2}).slice(0,10).map(e=>({tag:e.tagName,cls:e.className,text:e.textContent.slice(0,80),width:e.getBoundingClientRect().width})),targets:[...document.querySelectorAll('button,a,input,select,summary')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0&&(r.width<24||r.height<24)}).slice(0,15).map(e=>({html:e.outerHTML.slice(0,160),w:e.getBoundingClientRect().width,h:e.getBoundingClientRect().height}))}));
   results.push({locale,theme,route,viewport:width,dimensions:mobile});
   if(width===360)await page.screenshot({path:fileURLToPath(new URL(`mobile-${locale}-${key}.png`,out)),fullPage:true});
  }
  await page.setViewportSize({width:1440,height:1000});
 }
 await context.close();
}
}finally{await fs.writeFile(new URL('browser-b-clean-mobile.json',out),JSON.stringify({results,logs},null,2));await browser.close()}
