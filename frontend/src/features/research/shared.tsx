import {useState} from 'react'
import './research.css'
export {default as Pager} from '../../components/ui/Pagination'
export function CapabilityNote({ar}:{ar:boolean}){return <p className="notice">{ar?'لم يؤكد الخادم دعم هذا الإجراء. تبقى المدخلات متاحة دون تشغيل وهمي.':'The backend has not confirmed support for this action. Your inputs remain available; no execution is simulated.'}</p>}
export function CopyButton({value,ar,label}:{value:string;ar:boolean;label?:string}){const [message,setMessage]=useState('');return <><button onClick={async()=>{try{await navigator.clipboard.writeText(value);setMessage(ar?'تم النسخ':'Copied')}catch{setMessage(ar?'تعذر النسخ':'Copy unavailable')}}}>{label||(ar?'نسخ':'Copy')}</button><span className="caption" role="status">{message}</span></>}
