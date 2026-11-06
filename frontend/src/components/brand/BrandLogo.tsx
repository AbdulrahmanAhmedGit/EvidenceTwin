import type {CSSProperties} from 'react'
import {brandAssets} from './assets'
import './brand.css'
export type BrandLogoProps={
 variant?:'full'|'icon'
 theme?:'light'|'dark'|'auto'
 size?:'sm'|'md'|'lg'
 width?:number
 label?:string
 decorative?:boolean
 className?:string
}
/** Artwork stays untouched; auto follows the application's .root.dark surface. */
export default function BrandLogo({variant='full',theme='auto',size='md',width,label='EvidenceTwin',decorative=false,className=''}:BrandLogoProps){
 const asset=brandAssets[variant]
 const style=width===undefined?undefined:{'--brand-width':`${width}px`} as CSSProperties
 return <span className={`brand-logo brand-logo--${variant} brand-logo--${size} ${className}`.trim()} data-brand-theme={theme} role={decorative?undefined:'img'} aria-label={decorative?undefined:label} aria-hidden={decorative?true:undefined} dir="ltr" translate="no" style={style}>
  <img className="brand-logo__light" src={asset.light} width={asset.width} height={asset.height} alt="" aria-hidden="true" draggable={false}/>
  <img className="brand-logo__dark" src={asset.dark} width={asset.width} height={asset.height} alt="" aria-hidden="true" draggable={false}/>
 </span>
}
