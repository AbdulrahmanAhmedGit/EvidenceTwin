import type {Page} from '@playwright/test'

/** The desktop source index and mobile select expose the same existing categories. */
export async function selectEvidenceCategory(page:Page,category:'dataset'|'contract') {
 await page.getByLabel('Evidence category',{exact:true}).waitFor({state:'attached'})
 const name=category==='dataset'?'Data values':'Evidence Contract'
 const index=page.getByRole('navigation',{name:'Evidence categories'})
 if(await index.isVisible())await index.getByRole('button',{name,exact:true}).click()
 else await page.getByLabel('Evidence category',{exact:true}).selectOption(category)
}
