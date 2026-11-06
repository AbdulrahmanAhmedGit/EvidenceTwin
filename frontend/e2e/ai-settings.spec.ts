import {test,expect} from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'
test('AI configuration saves, masks keys, survives reload and recovers from save errors',async({page})=>{
 let saved=false,failed=false
 const posts:unknown[]=[]
 const state=()=>({activeProvider:'ollama',providers:[{id:'ollama',name:'Ollama',model:saved?'test-model':'',configured:saved,keyConfigured:saved,keySource:saved?'server':'none',requiresKey:true,ollamaHost:'https://ollama.com'}]})
 await page.route('**/api/health',r=>r.fulfill({json:{status:'ok'}}))
 await page.route('**/api/capabilities',r=>r.fulfill({json:{analyses:{create:saved},providers:[],services:[]}}))
 await page.route('**/api/settings/ai',async r=>{
  if(r.request().method()==='POST'){posts.push(r.request().postDataJSON());if(failed){await r.fulfill({status:503,json:{error:{code:'service_unavailable'}}});return}saved=true}
  await r.fulfill({json:state()})
 })
 await page.route('**/api/settings/ai/test',r=>r.fulfill({json:{status:'reachable',message:'model_found',checkedAt:'2026-11-05T10:00:00Z'}}))
 await page.goto('/app/settings')
 await page.getByRole('link',{name:'Configure AI APIs'}).click()
 await expect(page.getByRole('heading',{name:'AI APIs',exact:true})).toBeVisible()
 await page.getByRole('button',{name:'Save and use provider'}).click()
 await expect(page.getByText('Enter a model ID.',{exact:true})).toBeVisible()
 await page.getByLabel('Model ID',{exact:true}).fill('test-model')
 await page.getByLabel('API key',{exact:true}).fill('TEST_ONLY_BROWSER_KEY')
 failed=true
 await page.getByRole('button',{name:'Save and use provider'}).click()
 await expect(page.getByRole('alert')).toContainText('could not be saved')
 await expect(page.getByLabel('API key',{exact:true})).toHaveValue('TEST_ONLY_BROWSER_KEY')
 failed=false
 await page.getByRole('button',{name:'Save and use provider'}).click()
 await expect(page.getByText('Provider saved and selected for new analyses.')).toBeVisible()
 await expect(page.getByLabel('Replace API key (optional)',{exact:true})).toHaveValue('')
 expect(posts).toHaveLength(2)
 await page.reload()
 await expect(page.getByLabel('Replace API key (optional)',{exact:true})).toHaveValue('')
 await page.getByRole('button',{name:'Check model catalog'}).click()
 await expect(page.getByText(/The model was found in the provider catalog/)).toBeVisible()
 expect(await page.evaluate(()=>JSON.stringify({local:{...localStorage},session:{...sessionStorage}}))).not.toContain('TEST_ONLY_BROWSER_KEY')
 expect((await new AxeBuilder({page}).include('main').analyze()).violations).toEqual([])
})
test('AI configuration supports mobile Arabic RTL and dark mode',async({page})=>{
 await page.setViewportSize({width:390,height:844})
 await page.route('**/api/health',r=>r.fulfill({json:{status:'ok'}}))
 await page.route('**/api/settings/ai',r=>r.fulfill({json:{activeProvider:'ollama',providers:['ollama','openai','google','anthropic','openrouter','deepseek'].map(id=>({id,name:id,model:'',configured:false,keyConfigured:false,keySource:'none',requiresKey:true,...(id==='ollama'?{ollamaHost:'https://ollama.com'}:{})}))}}))
 await page.goto('/app/settings/ai')
 await page.getByRole('button',{name:'Change language'}).click()
 await expect(page.getByRole('heading',{name:'واجهات الذكاء الاصطناعي'})).toBeVisible()
 await expect(page.locator('html')).toHaveAttribute('dir','rtl')
 await page.getByRole('button',{name:'تبديل السمة'}).click()
 await expect(page.locator('.root')).toHaveClass(/dark/)
 await expect(page.getByLabel('معرّف النموذج',{exact:true})).toHaveAttribute('dir','ltr')
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth)).toBe(true)
 expect((await new AxeBuilder({page}).include('main').analyze()).violations).toEqual([])
})
