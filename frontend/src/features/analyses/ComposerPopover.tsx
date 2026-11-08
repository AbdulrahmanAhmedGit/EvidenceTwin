import {useLayoutEffect, useRef} from 'react'
import type {ReactNode, RefObject} from 'react'

type Props = {
  open: boolean
  anchor: RefObject<HTMLElement | null>
  label: string
  menu: boolean
  focusKey: string
  initialFocus: string
  onDismiss: () => void
  children: ReactNode
}

/** Native top-layer dismissal, with positioning constrained to the visible viewport. */
export default function ComposerPopover({open, anchor, label, menu, focusKey, initialFocus, onDismiss, children}: Props) {
  const surface = useRef<HTMLDivElement>(null)
  const dismiss = useRef(onDismiss)
  useLayoutEffect(() => { dismiss.current = onDismiss }, [onDismiss])

  useLayoutEffect(() => {
    const element = surface.current
    if (!element) return
    if (!open) {
      if (element.matches(':popover-open')) element.hidePopover()
      return
    }
    if (!element.matches(':popover-open')) {
      if (anchor.current) element.showPopover({source: anchor.current})
      else element.showPopover()
    }

    function position() {
      const trigger = anchor.current
      if (!element || !trigger) return
      const viewport = window.visualViewport
      const leftBoundary = (viewport?.offsetLeft || 0) + 12
      const topBoundary = (viewport?.offsetTop || 0) + 12
      const viewportWidth = viewport?.width || window.innerWidth
      const bottomBoundary = topBoundary + (viewport?.height || window.innerHeight) - 24
      element.style.width = Math.min(320, viewportWidth - 24) + 'px'
      const rect = trigger.getBoundingClientRect()
      const below = Math.max(0, bottomBoundary - rect.bottom - 8)
      const above = Math.max(0, rect.top - topBoundary - 8)
      const preferBelow = below >= Math.min(420, element.scrollHeight) || below >= above
      element.style.maxHeight = Math.max(80, Math.min(420, preferBelow ? below : above)) + 'px'
      const size = element.getBoundingClientRect()
      const rtl = getComputedStyle(trigger).direction === 'rtl'
      const preferredLeft = rtl ? rect.right - size.width : rect.left
      element.style.left = Math.max(leftBoundary, Math.min(preferredLeft, leftBoundary + viewportWidth - 24 - size.width)) + 'px'
      const preferredTop = preferBelow ? rect.bottom + 8 : rect.top - size.height - 8
      element.style.top = Math.max(topBoundary, Math.min(preferredTop, bottomBoundary - size.height)) + 'px'
    }
    position()
    element.querySelector<HTMLElement>(initialFocus)?.focus({preventScroll: true})
    const observer = new ResizeObserver(position)
    observer.observe(element)
    window.addEventListener('resize', position)
    window.addEventListener('scroll', position, true)
    window.visualViewport?.addEventListener('resize', position)
    window.visualViewport?.addEventListener('scroll', position)
    return () => {
      observer.disconnect()
      window.removeEventListener('resize', position)
      window.removeEventListener('scroll', position, true)
      window.visualViewport?.removeEventListener('resize', position)
      window.visualViewport?.removeEventListener('scroll', position)
    }
  }, [open, anchor, focusKey, initialFocus])

  return <div id="research-composer-popover" ref={surface} popover="auto"
    className="composer-popover" role={menu ? 'menu' : 'dialog'} aria-label={label}
    onToggle={event => {
      if (event.newState === 'closed' && !event.currentTarget.matches(':popover-open')) dismiss.current()
    }}
    onKeyDown={event => {
      if (event.key === 'Escape') {
        event.preventDefault()
        event.stopPropagation()
        dismiss.current()
        anchor.current?.focus({preventScroll: true})
        return
      }
      if (!menu || !['ArrowDown', 'ArrowUp', 'Home', 'End'].includes(event.key)) return
      event.preventDefault()
      const items = Array.from(event.currentTarget.querySelectorAll<HTMLButtonElement>('button[role^="menuitem"]:not(:disabled)'))
      const current = items.indexOf(document.activeElement as HTMLButtonElement)
      let next = current + (event.key === 'ArrowUp' ? -1 : 1)
      if (event.key === 'Home') next = 0
      if (event.key === 'End') next = items.length - 1
      items[(next + items.length) % items.length]?.focus()
    }}>
    {children}
  </div>
}
