import {describeCoverage} from './coverage'
import type {RecordedCheck} from './coverage'
export default function CoverageList({items,ar}:{items:RecordedCheck[];ar:boolean}){
 return <dl className="coverage-explanations">{items.map(item=>{const display=describeCoverage(item,ar);return <div key={item.check}><dt>{display.label}</dt><dd>{display.status}</dd><p>{display.explanation}</p></div>})}</dl>
}
