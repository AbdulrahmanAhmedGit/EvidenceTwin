export const previewEnabled=import.meta.env.DEV&&import.meta.env.VITE_ANALYSIS_FIXTURES==='true'
export function isFixtureAnalysis(id:string){return previewEnabled&&['sample-a1','sample-running','sample-failed'].includes(id)}
