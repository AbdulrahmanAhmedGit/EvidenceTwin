// @vitest-environment jsdom
import {afterEach,expect,it,vi} from 'vitest'
import {cleanup,fireEvent,render,screen} from '@testing-library/react'
import {MemoryRouter} from 'react-router-dom'
import Pagination from '../../components/ui/Pagination'
import {Stat} from '../../components/ui/WorkspacePrimitives'
import {AnalysisTable} from './AnalysisRecords'
import type {AnalysisRecord} from '../../workspace-api'
afterEach(cleanup)
it('bounds pagination, exposes the current page and selects a distant page',()=>{
 const change=vi.fn()
 render(<Pagination page={1} total={95} pageSize={10} onChange={change} ar={false}/>)
 expect((screen.getByRole('button',{name:'Previous'}) as HTMLButtonElement).disabled).toBe(true)
 expect(screen.getByRole('button',{name:'Page 1'}).getAttribute('aria-current')).toBe('page')
 fireEvent.click(screen.getByRole('button',{name:'Page 10'}))
 expect(change).toHaveBeenCalledWith(10)
})
it('keeps empty pagination on one page without an enabled next action',()=>{
 render(<Pagination page={1} total={0} pageSize={10} onChange={vi.fn()} ar={false}/>)
 expect((screen.getByRole('button',{name:'Next'}) as HTMLButtonElement).disabled).toBe(true)
 expect(screen.getByRole('status').textContent).toBe('Page 1 / 1')
})
it('keeps summary descriptions inside valid definition-list groups',()=>{
 const {container}=render(<dl><Stat label="Analyses" value="Unavailable">No valid records received</Stat></dl>)
 expect(container.querySelectorAll('dl>div>dd')).toHaveLength(2)
 expect(container.querySelector('dl>div>p')).toBeNull()
 expect(screen.getByText('Unavailable')).toBeTruthy()
})
it('preserves full record titles and capability-gates destructive actions',()=>{
 const record:AnalysisRecord={id:'record-1',title:'A full research title',status:'failed',mode:'exploratory',createdAt:'2026-11-03T00:00:00Z',reportAvailable:false,summary:'Source context is incomplete'}
 const controls={selected:[],pending:false,permissions:{delete:false,retry:false},toggle:vi.fn(),requestDelete:vi.fn(),retry:vi.fn()}
 render(<MemoryRouter><AnalysisTable items={[record]} controls={controls} ar={false}/></MemoryRouter>)
 expect(screen.getByRole('link',{name:'A full research title →'}).getAttribute('href')).toBe('/app/analyses/record-1')
 expect((screen.getByRole('button',{name:'Delete'}) as HTMLButtonElement).disabled).toBe(true)
 expect((screen.getByRole('button',{name:'Retry analysis'}) as HTMLButtonElement).disabled).toBe(true)
 fireEvent.click(screen.getByRole('checkbox',{name:'Select A full research title'}))
 expect(controls.toggle).toHaveBeenCalledWith('record-1')
 expect(screen.getByText('Source & context')).toBeTruthy()
})
