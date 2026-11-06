import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import AppErrorBoundary from './AppErrorBoundary'
import '@fontsource-variable/alan-sans/wght.css'
import './styles/workspace.css'
import './styles/precision.css'
import './styles/observatory.css'
import './styles/accessibility.css'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <AppErrorBoundary><App /></AppErrorBoundary>
  </StrictMode>,
)
