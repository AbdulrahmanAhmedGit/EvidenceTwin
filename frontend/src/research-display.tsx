/** Preserve supplied wording and paragraph boundaries; never interpret model output. */
export function ResearchText({text,className=''}:{text:string;className?:string}){return <div className={'research-prose '+className}>{text.split(/\n\s*\n/u).filter(Boolean).map((paragraph,index)=><p key={index} dir="auto">{paragraph}</p>)}</div>}
