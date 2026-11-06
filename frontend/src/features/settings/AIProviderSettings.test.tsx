// @vitest-environment jsdom
import {afterEach,beforeEach,expect,it,vi} from 'vitest'
import {cleanup,fireEvent,render,screen} from '@testing-library/react'
import '@testing-library/jest-dom/vitest'
import {MemoryRouter} from 'react-router-dom'
import {QueryClient,QueryClientProvider} from '@tanstack/react-query'
import AIProviderSettings from './AIProviderSettings'
import {readAISettings,saveAISettings,testAISettings} from './ai-api'
import type {AISettings} from './ai-api'
vi.mock('./ai-api',()=>({readAISettings:vi.fn(),saveAISettings:vi.fn(),testAISettings:vi.fn()}))
function fixture():AISettings{return {activeProvider:'ollama',providers:[{id:'ollama',name:'Ollama',model:'',configured:false,keyConfigured:false,keySource:'none',requiresKey:true,ollamaHost:'https://ollama.com'},{id:'openai',name:'OpenAI',model:'',configured:false,keyConfigured:false,keySource:'none',requiresKey:true}]}}
function mount(ar=false){return render(<MemoryRouter><QueryClientProvider client={new QueryClient({defaultOptions:{queries:{retry:false}}})}><AIProviderSettings ar={ar}/></QueryClientProvider></MemoryRouter>)}
beforeEach(()=>{vi.resetAllMocks();vi.mocked(readAISettings).mockResolvedValue(fixture())})
afterEach(cleanup)
it('validates before transmitting a key',async()=>{
 mount();await screen.findByLabelText('Model ID')
 fireEvent.click(screen.getByRole('button',{name:'Save and use provider'}))
 expect(await screen.findByText('Enter a model ID.')).toBeVisible()
 expect(saveAISettings).not.toHaveBeenCalled()
})
it('saves explicitly and clears the entered key',async()=>{
 const state=fixture();state.providers[0]={...state.providers[0],model:'test-model',configured:true,keyConfigured:true,keySource:'server'}
 vi.mocked(saveAISettings).mockResolvedValue(state)
 mount();fireEvent.change(await screen.findByLabelText('Model ID'),{target:{value:'test-model'}})
 fireEvent.change(screen.getByLabelText('API key'),{target:{value:'TEST_ONLY_KEY'}})
 fireEvent.click(screen.getByRole('button',{name:'Save and use provider'}))
 await screen.findByText('Provider saved and selected for new analyses.')
 expect(saveAISettings).toHaveBeenCalledWith({provider:'ollama',model:'test-model',apiKey:'TEST_ONLY_KEY',ollamaHost:'https://ollama.com'})
 expect(screen.getByLabelText('Replace API key (optional)')).toHaveValue('')
 expect(screen.getByLabelText('Replace API key (optional)')).toHaveAttribute('type','password')
})
it('preserves input when saving fails',async()=>{
 vi.mocked(saveAISettings).mockRejectedValue(new Error('Offline'))
 mount();fireEvent.change(await screen.findByLabelText('Model ID'),{target:{value:'test-model'}})
 fireEvent.change(screen.getByLabelText('API key'),{target:{value:'TEST_ONLY_KEY'}})
 fireEvent.click(screen.getByRole('button',{name:'Save and use provider'}))
 await screen.findByRole('alert')
 expect(screen.getByLabelText('API key')).toHaveValue('TEST_ONLY_KEY')
 expect(screen.getByRole('button',{name:'Save and use provider'})).toBeEnabled()
})
it('clears unsaved credentials when selecting another provider',async()=>{
 mount();fireEvent.change(await screen.findByLabelText('API key'),{target:{value:'TEST_ONLY_KEY'}})
 fireEvent.click(screen.getByRole('radio',{name:/OpenAI/}))
 expect(screen.getByLabelText('API key')).toHaveValue('')
 expect(screen.queryByLabelText('Ollama endpoint')).not.toBeInTheDocument()
})
it('checks saved models without permitting checks of unsaved input',async()=>{
 const state=fixture();state.providers[0]={...state.providers[0],model:'saved-model',configured:true,keyConfigured:true,keySource:'server'}
 vi.mocked(readAISettings).mockResolvedValue(state)
 vi.mocked(testAISettings).mockResolvedValue({status:'reachable',message:'model_found',checkedAt:'2026-11-05T10:00:00Z'})
 mount();const check=await screen.findByRole('button',{name:'Check model catalog'})
 expect(check).toBeEnabled();fireEvent.click(check)
 await screen.findByText(/The model was found in the provider catalog/)
 expect(testAISettings).toHaveBeenCalledTimes(1)
 fireEvent.change(screen.getByLabelText('Model ID'),{target:{value:'changed'}})
 expect(check).toBeDisabled()
})
it('renders Arabic labels with LTR identifiers',async()=>{
 mount(true)
 expect(await screen.findByLabelText('معرّف النموذج')).toHaveAttribute('dir','ltr')
 expect(screen.getByLabelText('مفتاح API')).toHaveAttribute('dir','ltr')
 expect(screen.getByRole('button',{name:'حفظ المزود واستخدامه'})).toBeVisible()
})
