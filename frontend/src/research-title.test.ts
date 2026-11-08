import {describe,it,expect} from 'vitest'
import {researchSubjectTitle} from './research-title'

describe('research subject display titles',()=>{
 it('uses a verbatim quoted claim instead of an instruction wrapper',()=>{
  expect(researchSubjectTitle('Investigate the following scientific claim: "A supplied scientific claim with exact values 22.4 and 13.7."')).toBe('A supplied scientific claim with exact values 22.4 and 13.7.')
 })
 it('preserves the original Arabic subject wording',()=>{
  expect(researchSubjectTitle('تحقق من الادعاء العلمي التالي: هل تدعم البيانات هذا الادعاء؟')).toBe('هل تدعم البيانات هذا الادعاء؟')
 })
})
