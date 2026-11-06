import {Button} from './WorkspacePrimitives'

export default function Pagination({page,total,pageSize,onChange,ar,label}:{page:number;total:number;pageSize:number;onChange:(page:number)=>void;ar:boolean;label?:string}) {
 const pages=Math.max(1,Math.ceil(total/pageSize))
 const candidates=[1,page-1,page,page+1,pages].filter((p,i,all)=>p>=1&&p<=pages&&all.indexOf(p)===i).sort((a,b)=>a-b)
 const number=(v:number)=>new Intl.NumberFormat(ar?'ar':'en').format(v)
 return <nav className="pagination workspace-pagination" aria-label={label||(ar?'صفحات السجلات':'Record pages')}>
  <Button disabled={page<=1} onClick={()=>onChange(page-1)}>{ar?'السابق':'Previous'}</Button>
  <span className="pagination-summary" role="status">{ar?'الصفحة':'Page'} {number(page)} / {number(pages)}</span>
  <div className="pagination-numbers">{candidates.map((p,i)=><span key={p}>{i>0&&p-candidates[i-1]>1&&<span aria-hidden="true" className="page-gap">…</span>}<Button variant="quiet" aria-label={(ar?'الصفحة ':'Page ')+number(p)} aria-current={p===page?'page':undefined} onClick={()=>onChange(p)}>{number(p)}</Button></span>)}</div>
  <Button disabled={page>=pages} onClick={()=>onChange(page+1)}>{ar?'التالي':'Next'}</Button>
 </nav>
}
