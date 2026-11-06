import {describe,it,expect} from 'vitest'
import {selectFiles,MAX_FILE_BYTES} from './files'
const file=(name:string,size=1)=>new File([new Uint8Array(size)],name,{lastModified:1}) as unknown as globalThis.File
describe('evidence selection',()=>{
it('rejects unsupported types without losing existing selections',()=>{const original=file('data.csv');const result=selectFiles([original],[file('script.exe')]);expect(result.files).toEqual([original]);expect(result.issues).toEqual(['type'])})
it('deduplicates files in the same batch',()=>{const result=selectFiles([],[file('data.csv'),file('data.csv')]);expect(result.files).toHaveLength(1);expect(result.issues).toEqual(['duplicate'])})
it('enforces the size limit and accepts the boundary',()=>{expect(selectFiles([],[file('chart.png',MAX_FILE_BYTES+1)]).issues).toEqual(['size']);expect(selectFiles([],[file('chart.png',MAX_FILE_BYTES)]).files).toHaveLength(1)})
})
