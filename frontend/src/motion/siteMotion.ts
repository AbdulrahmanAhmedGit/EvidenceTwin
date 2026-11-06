import {gsap} from 'gsap'
import {ScrollTrigger} from 'gsap/ScrollTrigger'
import Lenis from 'lenis'
import 'lenis/dist/lenis.css'

gsap.registerPlugin(ScrollTrigger)

/** One scoped motion owner per route. Never animates scientific values or original assets. */
export function mountSiteMotion({workspace}:{workspace:boolean}) {
 const root=document.querySelector<HTMLElement>('.root')
 const content=root?.querySelector<HTMLElement>('.route-content')
 if(!root||!content)return ()=>{}
 let active=true
 let frame=0
 const seen=new WeakSet<Element>()
 const context=gsap.context(()=>{},root)
 const lenis=!workspace?new Lenis({autoRaf:false,smoothWheel:true,syncTouch:false,anchors:false,lerp:.12,
  prevent:node=>!!node.closest('dialog,pre,textarea,select,.public-nav,.chart-window,.table-scroll,[data-native-scroll]')
 }):undefined
 const tick=(seconds:number)=>{if(!document.hidden)lenis?.raf(seconds*1000)}
 const refresh=()=>{if(active){lenis?.resize();ScrollTrigger.refresh()}}
 if(lenis){
  root.dataset.scrollEngine='lenis'
  lenis.on('scroll',ScrollTrigger.update)
  gsap.ticker.add(tick)
 }
 root.dataset.motionEngine='gsap'
 const animate=(heading:HTMLElement)=>{
  if(seen.has(heading)||heading.closest('dialog,.notice,[role=alert],.chart-window,.report-document'))return
  seen.add(heading)
  // Search results and linked headings are navigation content, not split-text canvases.
  const words=heading.querySelectorAll<HTMLElement>('.motion-word')
  const targets=words.length?words:heading
  const below=heading.getBoundingClientRect().top>innerHeight*.9
  context.add(()=>{
   const sequence=gsap.timeline({defaults:{ease:'power3.out',clearProps:'transform'},
    ...(below?{scrollTrigger:{trigger:heading,start:'top 94%',once:true,toggleActions:'play none none none'}}:{})})
   sequence.from(targets,{y:workspace?4:12,duration:workspace?.32:.65,stagger:words.length?.035:0})
   const copy=!workspace?heading.parentElement?.querySelector(':scope>p'):undefined
   if(copy)sequence.from(copy,{y:5,duration:.5},.12)
  })
 }
 const scan=()=>{
  frame=0
  content.querySelectorAll<HTMLElement>('h1,h2').forEach(animate)
  refresh()
 }
 context.add(()=>{
  const landing=content.querySelector('.et-hero')
  if(landing){
   const heading=landing.querySelector<HTMLElement>('h1')
   if(heading)seen.add(heading)
   // Reveal the value proposition before its physical illustration, then the action.
   gsap.timeline({defaults:{ease:'power3.out',clearProps:'transform,opacity'}})
    .from('.et-hero-copy h1',{y:8,duration:.45},0)
    .from('.et-hero-copy .et-intro',{y:4,duration:.4},.12)
    .from('.et-hero-copy .et-actions',{y:3,duration:.35},.22)
    .from('.et-optics',{x:document.dir==='rtl'?-12:12,duration:.8},.08)
  }
  const hero=content.querySelector('.hero-instrument')
  if(hero){
   const heading=content.querySelector<HTMLElement>('.hero-copy h1')
   if(heading)seen.add(heading)
   const intro=gsap.timeline({defaults:{ease:'power3.out',clearProps:'transform'}})
   if(heading)intro.from(heading.querySelectorAll('.motion-word'),{y:14,stagger:.055,duration:.75},0)
   intro.from(hero,{x:document.dir==='rtl'?-14:14,duration:.85},.08)
    .from('.hero-copy .lede',{y:8,duration:.6},.16)
    .from('.hero-copy .actions',{y:5,duration:.5},.24)
   // Frame movement guides comparison; data marks, axis labels and values stay immutable.
  }
 })
 scan()
 // Lazy routes and asynchronous result sections get the same bounded treatment.
 const observer=new MutationObserver(()=>{if(!frame)frame=requestAnimationFrame(scan)})
 observer.observe(content,{childList:true,subtree:true})
 const resize=new ResizeObserver(()=>{if(!frame)frame=requestAnimationFrame(scan)})
 resize.observe(content)
 void document.fonts.ready.then(()=>{if(active)refresh()})
 root.addEventListener('load',refresh,true)
 window.addEventListener('focus',refresh)
 window.addEventListener('pageshow',refresh)
 const print=()=>{context.revert();if(lenis)gsap.ticker.remove(tick)}
 const afterPrint=()=>{if(lenis)gsap.ticker.add(tick);refresh()}
 window.addEventListener('beforeprint',print)
 window.addEventListener('afterprint',afterPrint)
 return ()=>{
  active=false
  observer.disconnect();resize.disconnect();cancelAnimationFrame(frame)
  root.removeEventListener('load',refresh,true)
  window.removeEventListener('focus',refresh);window.removeEventListener('pageshow',refresh)
  window.removeEventListener('beforeprint',print);window.removeEventListener('afterprint',afterPrint)
  context.revert()
  if(lenis){lenis.off('scroll',ScrollTrigger.update);gsap.ticker.remove(tick);lenis.destroy()}
  delete root.dataset.scrollEngine;delete root.dataset.motionEngine
 }
}
