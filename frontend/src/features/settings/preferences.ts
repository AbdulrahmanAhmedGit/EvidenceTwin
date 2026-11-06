import {useSyncExternalStore} from 'react'
const session=new Map<string,string>()
export const preferenceDefaults:Record<string,string>={theme:'system',locale:'en',Motion:'System preference',Density:'Comfortable','Default mode':'Exploratory','Review depth':'Focused',Visualization:'Side by side'}
export function readPreference(key:string,fallback:string){if(session.has(key))return session.get(key)!;try{return localStorage.getItem(key)||fallback}catch{return fallback}}
export function writePreference(key:string,value:string){session.set(key,value);let saved=true;try{localStorage.setItem(key,value)}catch{saved=false}window.dispatchEvent(new Event('preferences-changed'));return saved}
function subscribe(callback:()=>void){const changed=(e:StorageEvent)=>{if(e.key)session.delete(e.key);else session.clear();callback()};window.addEventListener('preferences-changed',callback);window.addEventListener('storage',changed);return()=>{window.removeEventListener('preferences-changed',callback);window.removeEventListener('storage',changed)}}
export function usePreference(key:string,fallback=preferenceDefaults[key]||''){const value=useSyncExternalStore(subscribe,()=>readPreference(key,fallback));return [value,(next:string)=>writePreference(key,next)] as const}
export function useSystemDark(){return useSyncExternalStore(callback=>{const query=matchMedia('(prefers-color-scheme: dark)');query.addEventListener('change',callback);return()=>query.removeEventListener('change',callback)},()=>matchMedia('(prefers-color-scheme: dark)').matches)}
