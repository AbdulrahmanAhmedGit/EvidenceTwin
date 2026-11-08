/** Decorative mathematical curves. These do not represent measurements or findings. */
export default function InvestigationAtmosphere() {
  return <svg className="investigation-atmosphere" viewBox="0 0 1440 500" preserveAspectRatio="none" fill="none" aria-hidden="true" focusable="false">
    {Array.from({length:22},(_,index)=><g key={index}>
      <path d={`M -100 ${140+index*5} C 210 ${65+index*6}, 240 ${355+index*2}, 580 ${370+index*2}`}/>
      <path d={`M 880 ${370+index*2} C 1200 ${355-index*2}, 1210 ${5+index*7}, 1530 ${105+index*5}`}/>
    </g>)}
  </svg>
}
