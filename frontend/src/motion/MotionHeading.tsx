import type {HTMLAttributes} from 'react'

/** Words remain visible without the motion runtime. The heading has one accessible name. */
export function MotionWords({text}:{text:string}) {
 return <span aria-hidden="true">{text.split(/(\s+)/u).map((part,index)=>/\s/u.test(part)?part:<span className="motion-word" key={index}>{part}</span>)}</span>
}
export default function MotionHeading({as:Tag='h2',children,...props}:Omit<HTMLAttributes<HTMLHeadingElement>,'children'> & {as?:'h1'|'h2'|'h3';children:string}) {
 return <Tag {...props} aria-label={children}><MotionWords text={children}/></Tag>
}
