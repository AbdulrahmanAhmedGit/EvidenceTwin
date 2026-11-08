import react from '@vitejs/plugin-react'
import {defineConfig,loadEnv} from 'vite'

export default defineConfig(({mode})=>{
  const origin=process.env.FLASK_DEV_ORIGIN||loadEnv(mode,process.cwd(),'FLASK_').FLASK_DEV_ORIGIN
  if(origin){const url=new URL(origin);if(!['http:','https:'].includes(url.protocol)||url.username||url.password||url.search||url.hash||url.pathname!=='/')throw new Error('FLASK_DEV_ORIGIN must be a public HTTP(S) origin without credentials, path or query.')}
  // Preserve the browser-facing host so Flask can validate same-origin writes.
  return {plugins:[react()],server:origin?{proxy:{'/api':{target:origin,changeOrigin:false}}}:undefined}
})
