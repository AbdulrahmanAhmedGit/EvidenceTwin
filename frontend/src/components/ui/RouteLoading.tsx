/** A content-shaped loading state. Contains no fictional records or values. */
export default function RouteLoading({ar=false,compact=false}:{ar?:boolean;compact?:boolean}) {
  return <div className={compact?'loading-folio compact':'loading-folio'} role="status" aria-live="polite">
    <span className="sr-only">{ar?'جارٍ التحميل':'Loading…'}</span>
    <div aria-hidden="true" className="skeleton-heading"/>
    {[0,1,2].map(index=><div aria-hidden="true" className="skeleton-row" key={index}><span/><span/><span/></div>)}
  </div>
}
