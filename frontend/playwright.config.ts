import {defineConfig} from '@playwright/test'
export default defineConfig({workers:2,testDir:'./e2e',testIgnore:'**/fixture-preview.spec.ts',use:{baseURL:'http://127.0.0.1:5191'},webServer:{command:'npm run dev -- --host 127.0.0.1 --port 5191 --strictPort',url:'http://127.0.0.1:5191',reuseExistingServer:false}})
