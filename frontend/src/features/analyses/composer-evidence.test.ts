import {describe,it,expect} from 'vitest'
import {selectFiles as selectComposerEvidence} from './files'
import {MAX_FILE_BYTES} from './files'

describe('local composer evidence boundary',()=>{
 it('rejects XLSX because there is no backend workbook support',()=>{
  const xlsx=new File(['local test bytes'],'data.xlsx')
  expect(selectComposerEvidence([],[xlsx])).toEqual({files:[],issues:['type']})
 })
 it('retains existing selections and rejects duplicate, oversized and unsupported additions',()=>{
  const original=new File(['x'],'data.csv',{lastModified:1})
  const duplicate=new File(['x'],'data.csv',{lastModified:1})
  const unsupported=new File(['x'],'code.exe')
  const oversized=new File([new Uint8Array(MAX_FILE_BYTES+1)],'chart.png')
  const result=selectComposerEvidence([original],[duplicate,unsupported,oversized])
  expect(result.files).toEqual([original])
  expect(result.issues).toEqual(['duplicate','type','size'])
 })
})
