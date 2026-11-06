import {readdir,readFile} from 'node:fs/promises'
import {join} from 'node:path'
import {fileURLToPath} from 'node:url'
const markers=['EVIDENCETWIN_DEVELOPMENT_ONLY_SENTINEL','TEST_ONLY_REDACT_ME','EDUCATIONAL RENDERING · BASELINE']
async function check(dir){for(const entry of await readdir(dir,{withFileTypes:true})){const path=join(dir,entry.name);if(entry.isDirectory())await check(path);else if(/\.(js|svg|html|json)$/.test(entry.name)){const text=await readFile(path,'utf8');if(markers.some(marker=>text.includes(marker)))throw new Error('Development fixture content found in production artifact: '+path)}}}
await check(fileURLToPath(new URL('../dist',import.meta.url)))
console.log('Production artifacts exclude development scientific fixtures.')
