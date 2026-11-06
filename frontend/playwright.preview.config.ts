import {defineConfig} from '@playwright/test'
export default defineConfig({workers:1,testDir:'./e2e',testMatch:'fixture-preview.spec.ts',use:{baseURL:'http://127.0.0.1:5193'},webServer:{command:'VITE_ANALYSIS_FIXTURES=true npm run dev -- --host 127.0.0.1 --port 5193 --strictPort',url:'http://127.0.0.1:5193',reuseExistingServer:false}})
