// @vitest-environment jsdom
import {beforeEach,expect,it,vi} from 'vitest'
beforeEach(()=>{localStorage.clear();vi.resetModules()})
it('restores only the selected account draft and retains the old local draft separately',async()=>{
 const store=await import('./draft-store')
 store.setDraftOwner('local');store.updateDraft({claims:['Local private draft']});store.setDraftPersistence(true)
 store.setDraftOwner('first');store.updateDraft({claims:['First account private draft']});store.setDraftPersistence(true)
 store.setDraftOwner(null)
 store.setDraftOwner('second');store.updateDraft({claims:['Second account draft']});store.setDraftPersistence(true)
 expect(localStorage.getItem(store.DRAFT_KEY)).toContain('Local private draft')
 expect(localStorage.getItem(store.DRAFT_KEY+'.account.second')).not.toContain('First account')
 store.setDraftOwner('first');store.updateDraft({context:'First only'});store.setDraftOwner('second')
 expect(localStorage.getItem(store.DRAFT_KEY+'.account.second')).not.toContain('First only')
 // A newly loaded tab never selects an account before authentication.
 vi.resetModules();const fresh=await import('./draft-store');expect(fresh.getDraftOwner()).toBeNull()
 fresh.setDraftOwner('second');fresh.setDraftPersistence(true)
 expect(localStorage.getItem(store.DRAFT_KEY+'.account.second')).toContain('Second account draft')
})
it('a late save acknowledgement cannot clear a different account draft',async()=>{
 const store=await import('./draft-store')
 store.setDraftOwner('first');store.updateDraft({claims:['First draft']});store.setDraftPersistence(true);store.setDraftPending(true,'first')
 store.setDraftOwner('second');store.updateDraft({claims:['Second draft']});store.setDraftPersistence(true)
 store.acceptDraft('accepted-first','first');store.setDraftPending(false,'first')
 expect(store.getDraftOwner()).toBe('second')
 expect(localStorage.getItem(store.DRAFT_KEY+'.account.second')).toContain('Second draft')
 expect(localStorage.getItem(store.DRAFT_KEY+'.account.first')).toBeNull()
})
