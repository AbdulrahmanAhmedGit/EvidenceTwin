import {describe,it,expect} from 'vitest'
import {blankDraft,draftSchema,validateStep} from './draft-store'
describe('analysis draft validation',()=>{
it('requires a file or an explicitly selected educational case',()=>{expect(validateStep(0,blankDraft(),0)).toHaveProperty('files');expect(validateStep(0,{...blankDraft(),caseId:'a1'},0)).toEqual({})})
it('rejects non-http source links',()=>{expect(validateStep(1,{...blankDraft(),url:'javascript:alert(1)'},0)).toHaveProperty('url');expect(validateStep(1,{...blankDraft(),url:'https://example.org/study'},0)).toEqual({})})
it('requires each user-added claim',()=>{expect(validateStep(2,{...blankDraft(),claims:['Association is not causation.','  ']},0)).toHaveProperty('claim-1')})
it('strips files and unrelated fields from persisted draft shape',()=>{const result=draftSchema.parse({...blankDraft(),files:['sensitive.csv'],secret:'never persist'});expect(result).not.toHaveProperty('files');expect(result).not.toHaveProperty('secret')})
})
