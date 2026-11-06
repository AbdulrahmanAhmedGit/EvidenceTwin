"""Optional real HTTP transport check with the unchanged React TypeScript adapters.

Uses a temporary WSGI test server and Vite's installed TS loader. No science runs.
Skipped only when this independent backend checkout lacks frontend dependencies.
"""
from pathlib import Path
import json
import shutil
import subprocess
import threading
import pytest
from werkzeug.serving import make_server

SCRIPT = r'''
import assert from 'node:assert/strict';
process.env.VITE_API_BASE_URL=process.argv[1];
process.env.VITE_ANALYSIS_FIXTURES='false';
const {createServer}=await import('vite');
const server=await createServer({server:{middlewareMode:true},appType:'custom'});
try {
 const {api}=await server.ssrLoadModule('/src/api.ts');
 const workspace=await server.ssrLoadModule('/src/workspace-api.ts');
 const research=await server.ssrLoadModule('/src/features/research/api.ts');
 const inspection=await server.ssrLoadModule('/src/research-api.ts');
 const signal=new AbortController().signal;
 const health=await api.health();assert.equal(health.status,'ok');
 const caps=await workspace.getCapabilities(signal);assert.equal(caps.analyses.create,false);assert.deepEqual(caps.analyses.modes,[]);
 assert.deepEqual((await research.readResearchCapabilities(signal)).benchmarks,{read:false,create:false});
 const unavailable=[()=>workspace.getAnalyses({search:'',status:'',mode:'',verdict:'',sort:'createdAt:desc',page:1},signal),()=>inspection.readAnalysis('owner-record',signal),()=>inspection.readAnalysisSection('owner-record','evidence',signal),()=>research.readReports({search:'',status:'',sort:'createdAt:desc',page:1},signal)];
 for(const call of unavailable)await assert.rejects(call,error=>error.status===501);
 console.log(JSON.stringify({health:'reachable',scientificCapabilities:false,unavailableAdapterReads:unavailable.length}));
} finally {await server.close();}
'''

def test_existing_frontend_adapters_parse_real_infrastructure_and_reject_stubs(app):
    frontend=Path(__file__).resolve().parents[2]/'frontend'
    if not shutil.which('node') or not (frontend/'node_modules/vite').exists():
        pytest.skip('Optional bridge requires installed existing frontend Node/Vite dependencies')
    server=make_server('127.0.0.1',0,app)
    worker=threading.Thread(target=server.serve_forever,daemon=True)
    worker.start()
    try:
        result=subprocess.run(['node','--input-type=module','-e',SCRIPT,f'http://127.0.0.1:{server.server_port}/api'],cwd=frontend,capture_output=True,text=True,timeout=45)
        assert result.returncode==0,result.stderr
        assert '"scientificCapabilities":false' in result.stdout
    finally:
        server.shutdown();worker.join(timeout=5);server.server_close()
