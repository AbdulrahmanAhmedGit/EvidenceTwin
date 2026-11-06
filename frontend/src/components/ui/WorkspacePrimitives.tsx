import type {ButtonHTMLAttributes,HTMLAttributes,ReactNode} from 'react'
import {Link} from 'react-router-dom'
import type {LinkProps} from 'react-router-dom'

export function Button({variant='secondary',className='',type='button',...props}:ButtonHTMLAttributes<HTMLButtonElement> & {variant?:'primary'|'secondary'|'quiet'|'danger'}) {
 return <button type={type} className={`ui-button ${variant} ${className}`} {...props}/>
}
export function ActionLink({variant='secondary',className='',...props}:LinkProps & {variant?:'primary'|'secondary'|'quiet'}) {
 return <Link className={`button ui-button ${variant} ${className}`} {...props}/>
}
export function PageHeader({className='',...props}:HTMLAttributes<HTMLElement>) {
 return <header className={`page-heading workspace-page-header ${className}`} {...props}/>
}
export function PageHeading({children,...props}:HTMLAttributes<HTMLHeadingElement>) {return <h1 {...props}>{children}</h1>}
export function PageDescription(props:HTMLAttributes<HTMLParagraphElement>) {return <p className="page-description" {...props}/>}
export function PageActions(props:HTMLAttributes<HTMLDivElement>) {return <div className="actions page-actions" {...props}/>}
export function SectionHeader({children,...props}:HTMLAttributes<HTMLDivElement>){return <div className="section-heading" {...props}>{children}</div>}
export function StatePanel({state,children,...props}:HTMLAttributes<HTMLDivElement> & {state:'empty'|'error'|'pending'}) {
 return <div className="workspace-state" data-state={state} {...props}>{children}</div>
}
export function Stat({label,value,children}:{label:string;value:ReactNode;children:ReactNode}) {
 return <div className="workspace-stat"><dt>{label}</dt><dd className="stat-value">{value}</dd><dd className="stat-context">{children}</dd></div>
}
