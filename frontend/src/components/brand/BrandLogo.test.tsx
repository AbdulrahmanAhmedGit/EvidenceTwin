// @vitest-environment jsdom
import {afterEach,describe,it,expect} from 'vitest'
import {cleanup,render,screen} from '@testing-library/react'
import '@testing-library/jest-dom/vitest'
import BrandLogo from './BrandLogo'
afterEach(cleanup)
describe('official brand presentation',()=>{
 it('announces the application once and preserves supplied full-logo proportions',()=>{
  const {container}=render(<BrandLogo/>)
  expect(screen.getAllByRole('img')).toHaveLength(1)
  expect(screen.getByRole('img',{name:'EvidenceTwin'})).toHaveAttribute('dir','ltr')
  const images=container.querySelectorAll('img')
  expect(images[0]).toHaveAttribute('src','/brand/evidencetwin-logo.svg')
  expect(images[1]).toHaveAttribute('src','/brand/evidencetwin-logo-dark.svg')
  for(const image of images){expect(image).toHaveAttribute('alt','');expect(image).toHaveAttribute('width','1277');expect(image).toHaveAttribute('height','298')}
 })
 it('supports icon, explicit theme, custom sizing and a contextual label',()=>{
  const {container}=render(<BrandLogo variant="icon" theme="dark" width={36} label="EvidenceTwin workspace"/>)
  expect(screen.getByRole('img',{name:'EvidenceTwin workspace'})).toHaveAttribute('data-brand-theme','dark')
  expect(container.firstElementChild).toHaveStyle({'--brand-width':'36px'})
  expect(container.querySelector('img')).toHaveAttribute('width','317')
  expect(container.querySelector('img')).toHaveAttribute('height','339')
 })
 it('is decorative inside a labeled navigation link without duplicate announcements',()=>{
  render(<a href="/" aria-label="EvidenceTwin home"><BrandLogo decorative/></a>)
  expect(screen.getByRole('link',{name:'EvidenceTwin home'})).toHaveAttribute('href','/')
  expect(screen.queryByRole('img')).toBeNull()
 })
})
