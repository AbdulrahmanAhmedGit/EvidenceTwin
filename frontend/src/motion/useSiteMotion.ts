import {useEffect} from 'react'

/** Load enhancements after content; never make route rendering depend on motion. */
export function useSiteMotion(path:string,locale:string,reduced:boolean,workspace:boolean) {
 useEffect(()=>{
  const preference=matchMedia('(prefers-reduced-motion: reduce)')
  let disposed=false
  let generation=0
  let destroy:undefined|(()=>void)
  const update=()=>{
   const version=++generation
   destroy?.();destroy=undefined
   if(workspace||reduced||preference.matches)return
   void import('./siteMotion').then(({mountSiteMotion})=>{
    if(disposed||version!==generation)return
    destroy=mountSiteMotion({workspace})
   }).catch(()=>{/* Motion is optional. Static content and native scrolling remain available. */})
  }
  update();preference.addEventListener('change',update)
  return ()=>{disposed=true;generation++;preference.removeEventListener('change',update);destroy?.()}
 },[path,locale,reduced,workspace])
}
