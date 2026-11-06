// @vitest-environment jsdom
import {it,expect,vi} from 'vitest'
import {render,screen,fireEvent,cleanup} from '@testing-library/react'
import AppErrorBoundary from './AppErrorBoundary'
it('offers recovery without presenting a render error as a scientific result',()=>{const log=vi.spyOn(console,'error').mockImplementation(()=>{});let broken=true;function View(){if(broken)throw new Error('Test render failure');return <p>Recovered view</p>}try{render(<AppErrorBoundary><View/></AppErrorBoundary>);expect(screen.getByRole('heading',{name:'This view could not be displayed'})).toBeTruthy();broken=false;fireEvent.click(screen.getByRole('button',{name:'Try displaying again'}));expect(screen.getByText('Recovered view')).toBeTruthy()}finally{cleanup();log.mockRestore()}})
