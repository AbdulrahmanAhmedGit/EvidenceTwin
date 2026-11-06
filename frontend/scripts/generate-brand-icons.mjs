// Deterministic rasterization of official source SVGs; no artwork changes.
import {chromium} from 'playwright'
import {readFile,writeFile} from 'node:fs/promises'
const base=new URL('../public/brand/',import.meta.url)
const browser=await chromium.launch({headless:true})
try{
 const page=await browser.newPage()
 for(const theme of ['light','dark']){
  const suffix=theme==='dark'?'-dark':''
  const source=await readFile(new URL(`evidencetwin-icon${suffix}.svg`,base),'utf8')
  await page.setContent(source)
  const bounds=await page.locator('svg').evaluate(svg=>{const b=svg.getBBox();const v=svg.viewBox.baseVal;return{x:b.x,y:b.y,width:b.width,height:b.height,vw:v.width,vh:v.height}})
  for(const size of theme==='light'?[16,32,180]:[16,32]){
   const data=await page.evaluate(async({source,bounds,size})=>{
    const image=new Image();image.src='data:image/svg+xml;base64,'+btoa(source);await image.decode()
    const canvas=document.createElement('canvas');canvas.width=size;canvas.height=size
    const context=canvas.getContext('2d');if(size===180){context.fillStyle='#f7f7f1';context.fillRect(0,0,size,size)}
    const padding=size===180?18:size===16?1:3
    const scale=(size-2*padding)/Math.max(bounds.width,bounds.height)
    const x=(size-bounds.width*scale)/2-bounds.x*scale
    const y=(size-bounds.height*scale)/2-bounds.y*scale
    context.drawImage(image,x,y,bounds.vw*scale,bounds.vh*scale)
    return canvas.toDataURL('image/png').split(',')[1]
   },{source,bounds,size})
   const name=size===180?'apple-touch-icon.png':`favicon-${size}${suffix}.png`
   await writeFile(new URL(name,base),Buffer.from(data,'base64'))
   console.log(name)
  }
 }
}finally{await browser.close()}
