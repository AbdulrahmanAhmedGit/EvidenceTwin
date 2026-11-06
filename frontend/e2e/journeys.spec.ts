import {test,expect} from '@playwright/test'
test('homepage framing controls and case navigation',async({page})=>{await page.goto('/');await expect(page.getByRole('heading',{name:'Same data. Different story.'})).toBeVisible();await page.getByRole('button',{name:'Neutral baseline',exact:true}).click();await expect(page.getByText('Neutral display · zero baseline').first()).toBeVisible();await page.goto('/app/library/a1');await expect(page.getByRole('heading',{name:'Truncated axis'})).toBeVisible();await page.getByRole('link',{name:'New Analysis',exact:true}).last().click();await expect(page.getByRole('heading',{name:'Evidence',exact:true})).toBeVisible()})
test('wizard prevents empty evidence',async({page})=>{await page.goto('/app/analyses/new');await page.getByRole('button',{name:'Continue',exact:true}).click();await expect(page.getByRole('alert')).toContainText('Add evidence')})
test('mobile navigation, language and theme',async({page})=>{await page.setViewportSize({width:390,height:844});await page.goto('/');await page.getByRole('button',{name:'Toggle navigation'}).click();await page.getByRole('link',{name:'Methodology',exact:true}).first().click();await expect(page).toHaveURL(/methodology/);await page.getByRole('button',{name:'Change language'}).click();await expect(page.locator('.root')).toHaveAttribute('dir','rtl');await page.getByRole('button',{name:'تبديل السمة'}).click();await expect(page.locator('.root')).toHaveClass(/dark/)})
test('mobile menu supports focus, Escape, dismissal and route focus',async({page})=>{
 await page.setViewportSize({width:390,height:844});await page.goto('/');
 const toggle=page.getByRole('button',{name:'Toggle navigation'});
 await toggle.click();await expect(page.getByRole('navigation',{name:'Main navigation'}).getByRole('link',{name:'Features',exact:true})).toBeFocused();
 await page.keyboard.press('Escape');await expect(toggle).toBeFocused();await expect(toggle).toHaveAttribute('aria-expanded','false');
 await toggle.click();await page.getByRole('link',{name:'Methodology',exact:true}).first().click();
 await expect(page.locator('#main')).toBeFocused();await expect(toggle).toHaveAttribute('aria-expanded','false');
 await toggle.click();await page.getByRole('heading',{name:'Planned evaluation',exact:true}).click();await expect(toggle).toHaveAttribute('aria-expanded','false');
 await page.goto('/app');await page.getByRole('link',{name:'Settings',exact:true}).first().click();await expect(page).toHaveURL(/settings/);
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
