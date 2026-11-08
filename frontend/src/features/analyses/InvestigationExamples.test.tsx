// @vitest-environment jsdom
import {afterEach,expect,it,vi} from 'vitest'
import {render,screen,fireEvent,cleanup} from '@testing-library/react'
import InvestigationExamples from './InvestigationExamples'

afterEach(cleanup)
it('selects an educational question without creating a case',()=>{
 const onSelect=vi.fn()
 render(<InvestigationExamples ar={false} question="" busy={false} onSelect={onSelect}/>)
 fireEvent.click(screen.getByRole('button',{name:/Health/}))
 expect(onSelect).toHaveBeenCalledWith('Do the axes exaggerate the difference in diabetes prevalence between these groups?')
 expect(screen.getByText(/Prompts only/)).toBeTruthy()
})
it('protects an existing question until replacement is explicitly chosen',()=>{
 const onSelect=vi.fn()
 render(<InvestigationExamples ar={false} question="My original research question" busy={false} onSelect={onSelect}/>)
 fireEvent.click(screen.getByRole('button',{name:/Public health/}))
 expect(onSelect).not.toHaveBeenCalled()
 fireEvent.click(screen.getByRole('button',{name:'Keep my question'}))
 expect(onSelect).not.toHaveBeenCalled()
 fireEvent.click(screen.getByRole('button',{name:/Public health/}))
 fireEvent.click(screen.getByRole('button',{name:'Use this question'}))
 expect(onSelect).toHaveBeenCalledTimes(1)
})
