import {useEffect,useState} from 'react'
import {useQuery} from '@tanstack/react-query'
import {readResearchCapabilities} from './api'
export function useResearchCapabilities(){return useQuery({queryKey:['research-capabilities'],queryFn:({signal})=>readResearchCapabilities(signal),retry:false,staleTime:30000})}
export function useDebounced(value:string){const [result,setResult]=useState(value);useEffect(()=>{const timer=setTimeout(()=>setResult(value),250);return()=>clearTimeout(timer)},[value]);return result}
