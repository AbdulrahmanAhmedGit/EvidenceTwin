import {useEffect, useState} from 'react'
import {DatasetIcon, FileText} from '../../components/ui/Icons'

/** Only complete CSV records from a bounded local preview, including quoted cells. */
function previewRows(text:string) {
  const rows:string[][]=[]
  let row:string[]=[], cell='', quoted=false
  for(let index=0;index<text.length && rows.length<6;index++) {
    const char=text[index]
    if(char==='"') {
      if(quoted && text[index+1]==='"') {cell+='"';index++}
      else if(!quoted && cell.length>0) cell+='"'
      else quoted=!quoted
    } else if(char===',' && !quoted) {row.push(cell);cell=''}
    else if(char==='\n' && !quoted) {row.push(cell.replace(/\r$/,''));rows.push(row);row=[];cell=''}
    else cell+=char
  }
  return rows
}
export default function FilePreview({file, ar}: {file: File; ar: boolean}) {
  const [preview,setPreview] = useState<{file:File;url:string}|null>(null)
  const [rows,setRows] = useState<string[][]>([])
  const supported = /^image\/(png|jpeg|webp)$/.test(file.type) || /\.(png|jpe?g|webp)$/i.test(file.name)
  useEffect(() => {
    if (!supported) return
    const object = URL.createObjectURL(file)
    const loader = new Image()
    loader.onload = () => setPreview({file,url:object})
    loader.src = object
    return () => {
      loader.onload = null
      URL.revokeObjectURL(object)
    }
  }, [file, supported])
  useEffect(()=>{
    let active=true
    if(/\.csv$/i.test(file.name)) file.slice(0,32768).text().then(text=>{if(active)setRows(previewRows(text))}).catch(()=>{if(active)setRows([])})
    return()=>{active=false}
  },[file])
  if (supported && preview?.file===file) return <img src={preview.url} width={120} height={80} className="upload-preview"
    alt={(ar ? 'معاينة محلية ' : 'Local preview ') + file.name}/>
  if(rows.length) return <span className="attachment-dataset-preview" aria-label={ar?'معاينة محلية لأول صفوف CSV؛ الملف الكامل محفوظ عند الإرسال':'Local preview of the first CSV records. The complete file is retained on submission.'}>
    <span aria-hidden="true">{rows.map((row,i)=><span className="preview-table-row" key={i}>{row.slice(0,4).map((cell,j)=><span key={j}>{cell}</span>)}</span>)}</span>
    <DatasetIcon size={16}/>
  </span>
  return <span className="attachment-file-icon">
    {/\.(csv|json)$/i.test(file.name) ? <DatasetIcon size={22}/> : <FileText size={22}/>}
  </span>
}
