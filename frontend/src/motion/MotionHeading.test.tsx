// @vitest-environment jsdom
import {render,screen,cleanup} from '@testing-library/react'
import {afterEach,describe,expect,it} from 'vitest'
import MotionHeading,{MotionWords} from './MotionHeading'
afterEach(cleanup)
describe('accessible motion headings',()=>{
 it('keeps one full accessible name while words remain visible text',()=>{
  const {container}=render(<MotionHeading as="h1">Same data. Different story.</MotionHeading>)
  expect(screen.getByRole('heading',{level:1,name:'Same data. Different story.'})).toBeTruthy()
  expect(container.textContent).toBe('Same data. Different story.')
  expect(container.querySelectorAll('.motion-word')).toHaveLength(4)
  expect(container.querySelector('h1>span')?.getAttribute('aria-hidden')).toBe('true')
 })
 it('preserves Arabic word shaping boundaries, punctuation and whitespace',()=>{
  const text='نفس البيانات. قصة مختلفة.'
  const {container}=render(<MotionHeading>{text}</MotionHeading>)
  expect(screen.getByRole('heading',{name:text})).toBeTruthy()
  expect(container.textContent).toBe(text)
  expect([...container.querySelectorAll('.motion-word')].map(node=>node.textContent)).toEqual(['نفس','البيانات.','قصة','مختلفة.'])
 })
 it('leaves hero emphasis outside the decorative word fragments',()=>{
  render(<h1 aria-label="Same data. Different story."><MotionWords text="Same data."/><br/><em><MotionWords text="Different story."/></em></h1>)
  expect(screen.getAllByRole('heading',{name:'Same data. Different story.'})).toHaveLength(1)
 })
})
