// Solar by 480 Design, CC BY 4.0. Bundled Iconify data; no remote icon requests.
// See docs/FRONTEND_MOTION_REFINEMENT.md for attribution and license links.
import {Icon} from '@iconify/react/offline'
import type {IconProps,IconifyIcon} from '@iconify/react/offline'
import arrow from '@iconify-icons/solar/arrow-right-up-linear'
import menu from '@iconify-icons/solar/hamburger-menu-linear'
import sun from '@iconify-icons/solar/sun-linear'
import moon from '@iconify-icons/solar/moon-linear'
import chevron from '@iconify-icons/solar/alt-arrow-right-linear'
import close from '@iconify-icons/solar/close-square-linear'
import dashboard from '@iconify-icons/solar/widget-2-linear'
import add from '@iconify-icons/solar/add-square-linear'
import files from '@iconify-icons/solar/documents-linear'
import library from '@iconify-icons/solar/library-linear'
import columns from '@iconify-icons/solar/sidebar-minimalistic-linear'
import flask from '@iconify-icons/solar/test-tube-linear'
import document from '@iconify-icons/solar/document-text-linear'
import plug from '@iconify-icons/solar/plug-circle-linear'
import collapse from '@iconify-icons/solar/sidebar-close-linear'
import expand from '@iconify-icons/solar/sidebar-open-linear'
import settings from '@iconify-icons/solar/settings-linear'
import down from '@iconify-icons/solar/alt-arrow-down-linear'
import paperclip from '@iconify-icons/solar/paperclip-linear'
import link from '@iconify-icons/solar/link-linear'
import database from '@iconify-icons/solar/database-linear'
import heart from '@iconify-icons/solar/heart-pulse-linear'
import leaf from '@iconify-icons/solar/leaf-linear'
import pills from '@iconify-icons/solar/pills-linear'
import chartSquare from '@iconify-icons/solar/chart-square-linear'
import gallery from '@iconify-icons/solar/gallery-linear'
import book from '@iconify-icons/solar/book-linear'

type Props=Omit<IconProps,'icon'> & {size?:number;strokeWidth?:number}
function Glyph({data,size=20,strokeWidth,...props}:Props & {data:IconifyIcon}) {
 return <Icon icon={data} width={size} height={size} aria-hidden="true" focusable="false" strokeWidth={strokeWidth} {...props}/>
}
export function ArrowUpRight({className='',...props}:Props){return <Glyph data={arrow} className={`directional-icon ${className}`} {...props}/>}
export function Menu(props:Props){return <Glyph data={menu} {...props}/>}
export function Sun(props:Props){return <Glyph data={sun} {...props}/>}
export function Moon(props:Props){return <Glyph data={moon} {...props}/>}
export function ChevronRight({className='',...props}:Props){return <Glyph data={chevron} className={`directional-icon ${className}`} {...props}/>}
export function X(props:Props){return <Glyph data={close} {...props}/>}
export function LayoutDashboard(props:Props){return <Glyph data={dashboard} {...props}/>}
export function FilePlus2(props:Props){return <Glyph data={add} {...props}/>}
export function Files(props:Props){return <Glyph data={files} {...props}/>}
export function LibraryBig(props:Props){return <Glyph data={library} {...props}/>}
export function Columns2(props:Props){return <Glyph data={columns} {...props}/>}
export function FlaskConical(props:Props){return <Glyph data={flask} {...props}/>}
export function FileText(props:Props){return <Glyph data={document} {...props}/>}
export function Plug(props:Props){return <Glyph data={plug} {...props}/>}
export function PanelLeftClose({className='',...props}:Props){return <Glyph data={collapse} className={`directional-icon ${className}`} {...props}/>}
export function PanelLeftOpen({className='',...props}:Props){return <Glyph data={expand} className={`directional-icon ${className}`} {...props}/>}
export function BookOpen(props:Props){return <Glyph data={book} {...props}/>}

export function SettingsIcon(props:Props){return <Glyph data={settings} {...props}/>}

export function Paperclip(props:Props){return <Glyph data={paperclip} {...props}/>}
export function LinkIcon(props:Props){return <Glyph data={link} {...props}/>}
export function DatasetIcon(props:Props){return <Glyph data={database} {...props}/>}

export function ChevronDown(props:Props){return <Glyph data={down} {...props}/>}

export function HeartPulse(props:Props){return <Glyph data={heart} {...props}/>}
export function Leaf(props:Props){return <Glyph data={leaf} {...props}/>}
export function Pills(props:Props){return <Glyph data={pills} {...props}/>}
export function ChartSquare(props:Props){return <Glyph data={chartSquare} {...props}/>}
export function Gallery(props:Props){return <Glyph data={gallery} {...props}/>}
