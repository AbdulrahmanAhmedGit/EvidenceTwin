import {useEffect, useRef, useState} from 'react'
import type {FormEvent} from 'react'
import {useNavigate} from 'react-router-dom'
import {useQueryClient} from '@tanstack/react-query'
import {researchError} from './research-error'
import {ArrowUpRight, Paperclip, LinkIcon, FileText, DatasetIcon, SettingsIcon, FilePlus2, ChevronDown, X, FlaskConical, Gallery} from '../../components/ui/Icons'
import {
  useAnalysisDraft, updateDraft, setDraftFiles, setDraftPersistence, prepareDraft,
  acceptDraft, studyDesigns, setDraftPending, getDraftOwner,
} from './draft-store'
import type {AnalysisDraft} from './draft-store'
import {selectFiles, ACCEPTED_FILES} from './files'
import FilePreview from './FilePreview'
import InvestigationExamples from './InvestigationExamples'
import InvestigationAtmosphere from './InvestigationAtmosphere'
import ComposerPopover from './ComposerPopover'
import {saveCase, caseFilesUrl} from './cases-api'
import type {EvidenceFile, ResearchCase} from './cases-api'
import './research-entry.css'
import './investigation-reference.css'

export default function ResearchEntry({ar}: {ar: boolean}) {
  const {draft, files, persist, notice, pending} = useAnalysisDraft()
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const guard = useRef(false)
  const mounted = useRef(true)
  const navigate = useNavigate()
  const cache = useQueryClient()

  useEffect(() => {
    mounted.current = true
    prepareDraft()
    return () => { mounted.current = false }
  }, [])
  useEffect(() => {
    if (draft.mode !== 'exploratory') updateDraft({mode: 'exploratory'})
  }, [draft.mode])

  async function save() {
    if (guard.current || pending) return
    guard.current = true
    const submittedOwner = getDraftOwner()
    setDraftPending(true, submittedOwner)
    setBusy(true)
    setError('')
    try {
      const hasChart=files.some(file=>/\.(png|jpe?g|webp)$/i.test(file.name))
      const submittedDraft=hasChart&&!draft.claims[0]?.trim()
        ? {...draft,claims:[ar?'افحص الرسم المرفوع بحثاً عن خيارات عرض قد تكون مضللة، واشرح الأدلة والحدود.':'Inspect the uploaded chart for potentially misleading presentation choices, explaining the evidence and limitations.',...draft.claims.slice(1)]}
        : draft
      const record = await saveCase(submittedDraft, files)
      acceptDraft(record.id, submittedOwner)
      if (getDraftOwner() !== submittedOwner) return
      cache.setQueryData(['research-case', record.id], record)
      void cache.invalidateQueries({queryKey: ['research-cases']})
      if (mounted.current && getDraftOwner() === submittedOwner) {
        navigate('/app/cases/' + encodeURIComponent(record.id))
      }
    } catch (error) {
      setError(researchError(error, ar))
    } finally {
      guard.current = false
      setDraftPending(false, submittedOwner)
      setBusy(false)
    }
  }

  return <section className="research-entry">
    <InvestigationAtmosphere/>
    <div className="research-entry-content">
      <header className="investigation-introduction">
      <span className="investigation-context"><FlaskConical size={21}/>{ar?'فحص رسم علمي':'Chart investigation'}</span>
      <h1>{ar ? 'افحص رسماً علمياً بوضوح' : 'Inspect a scientific visualization'}</h1>
      <p className="research-entry-intro">{ar
        ? 'ارفع رسماً طبياً أو علمياً، وافحص خيارات العرض التي قد تضلل القارئ. قارن بإعادة بناء تستند إلى البيانات عند توفر منهج مدعوم.'
        : 'Upload a medical or scientific chart. Examine potentially misleading visual choices and compare with an evidence-grounded reconstruction when supported.'}</p>
      </header>
      <ResearchForm
        allowImageOnly ar={ar} draft={draft} update={updateDraft} files={files} setFiles={setDraftFiles}
        busy={busy || pending} save={save} error={error}
        dirty={files.length > 0 || draft.claims.some(claim => !!claim.trim()) ||
          !!(draft.url || draft.source || draft.context || draft.population || draft.uncertainty)}
        localDraft={{enabled: persist, change: setDraftPersistence, notice}}
      />
      <p className="investigation-save-note">{ar?'يُحفظ الرسم والسياق أولاً. دون سؤال مكتوب، سنطلب فحص خيارات عرض الرسم والأدلة والحدود. تبدأ مراجعة الذكاء الاصطناعي بعد موافقتك.':'Your chart and context are saved first. With no written question, the request is to inspect its presentation, evidence and limitations. AI review starts with your consent.'}</p>
      <div className="investigation-workflow" aria-label={ar?'مسار فحص الرسوم المقصود':'Intended chart investigation workflow'}>
        {(ar?['ارفع','حلّل','اكتشف','أعد البناء','قارن']:['Upload','Analyze','Detect','Reconstruct','Compare']).map((step,index)=><span key={step}>{index>0&&<span aria-hidden="true">{ar?'←':'→'}</span>}{step}</span>)}
      </div>
      <p className="investigation-method-status">{ar?'المتاح حالياً: فحص الصور ومراجعات الذكاء الاصطناعي. إعادة البناء المعماة تنتظر منهجاً معتمداً؛ لم تُنفذ لهذا البحث.':'Available now · original-chart inspection and AI review. Blind reconstruction awaits an approved method and is currently unavailable.'}</p>
      <InvestigationExamples ar={ar} question={draft.claims[0]||''} busy={busy||pending} onSelect={value=>{
        updateDraft({claims:[value,...draft.claims.slice(1)]})
        document.getElementById('research-question')?.focus({preventScroll:true})
      }}/>
    </div>
  </section>
}

type FormProps = {
  allowImageOnly?: boolean
  ar: boolean
  draft: AnalysisDraft
  update: (patch: Partial<AnalysisDraft>) => void
  files: File[]
  setFiles: (files: File[]) => void
  busy: boolean
  save: () => void
  error: string
  current?: ResearchCase
  retained?: EvidenceFile[]
  setRetained?: (files: EvidenceFile[]) => void
  dirty?: boolean
  localDraft?: {
    enabled: boolean
    change: (enabled: boolean) => void
    notice: 'restored' | 'storage_error' | null
  }
}
type ComposerPanel = 'add' | 'review' | 'source' | 'claims' | 'settings' | null
const designNames: Record<string, string> = {
  Unknown: 'غير معروف', 'Randomized experimental': 'تجريبية عشوائية',
  Observational: 'رصدية', 'Cross-sectional': 'مقطعية',
  'Repeated cross-sectional': 'مقطعية متكررة', Longitudinal: 'طولية',
  'Meta-analysis': 'تحليل تلوي', Other: 'أخرى',
}

export function ResearchForm({
  ar, draft, update, files, setFiles, busy, save, error, current, allowImageOnly = false,
  retained = [], setRetained, dirty = true, localDraft,
}: FormProps) {
  const t = (en: string, arabic: string) => ar ? arabic : en
  const question = useRef<HTMLTextAreaElement>(null)
  const picker = useRef<HTMLInputElement>(null)
  const plus = useRef<HTMLButtonElement>(null)
  const anchor = useRef<HTMLElement | null>(null)
  const [panel, setPanel] = useState<ComposerPanel>(null)
  const [expanded, setExpanded] = useState(false)
  const [activeClaim, setActiveClaim] = useState(1)
  const [contextField, setContextField] = useState<'context' | 'population' | 'uncertainty'>('context')
  const [validation, setValidation] = useState('')
  const [fileMessage, setFileMessage] = useState<'limit' | 'images' | 'table' | 'issues' | 'selected' | null>(null)
  const number = new Intl.NumberFormat(ar ? 'ar' : 'en')
  const fileSize = new Intl.NumberFormat(ar ? 'ar' : 'en', {maximumFractionDigits: 1})
  const total = files.length + retained.length
  const hasImage = files.some(file=>/\.(png|jpe?g|webp)$/i.test(file.name))||retained.some(file=>file.mediaType.startsWith('image/'))
  const claimIndex = Math.min(activeClaim, draft.claims.length - 1)
  const reviewName = draft.reviewDepth === 'council' ? t('Multi-perspective', 'متعددة التخصصات') : t('Visual review', 'مراجعة بصرية')
  const hasSource = !!(draft.url || draft.source || draft.studyDate)
  const hasContext = !!(draft.context || draft.population || draft.uncertainty || draft.studyDesign !== 'Unknown')
  const contextNames = {
    context: t('Research notes', 'ملاحظات البحث'),
    population: t('Population and scope', 'المجتمع والنطاق'),
    uncertainty: t('Uncertainty and limitations', 'عدم اليقين والحدود'),
  }
  const labels = {
    add: t('Add to investigation', 'إضافة إلى البحث'),
    review: t('Review mode', 'نوع المراجعة'),
    source: t('Source reference', 'مرجع المصدر'),
    claims: t('Additional claims', 'ادعاءات إضافية'),
    settings: t('Study settings', 'إعدادات الدراسة'),
  }
  const sizeLabel = (bytes: number) => bytes < 1024
    ? number.format(bytes) + ' ' + t('bytes', 'بايت') : fileSize.format(bytes / 1024) + ' KB'

  useEffect(() => {
    const input = question.current
    if (!input) return
    const resize = () => {
      input.style.height = 'auto'
      input.style.height = Math.min(expanded ? window.innerHeight * .65 : Math.min(340, window.innerHeight * (window.innerWidth < 600 ? .3 : .4)), Math.max(56, input.scrollHeight)) + 'px'
    }
    resize()
    window.addEventListener('resize', resize)
    return () => window.removeEventListener('resize', resize)
  }, [draft.claims, ar, expanded])
  useEffect(() => {
    if (!dirty) return
    const warn = (event: BeforeUnloadEvent) => event.preventDefault()
    window.addEventListener('beforeunload', warn)
    return () => window.removeEventListener('beforeunload', warn)
  }, [dirty])

  function openPanel(next: Exclude<ComposerPanel, null>, trigger?: HTMLElement) {
    if (trigger) anchor.current = trigger
    if (!anchor.current?.isConnected) anchor.current = plus.current
    setPanel(next)
  }
  function closePanel() {
    setPanel(null)
    const trigger = anchor.current?.isConnected ? anchor.current : plus.current
    trigger?.focus({preventScroll: true})
  }
  function addClaim() {
    if (draft.claims.length >= 10) return
    setActiveClaim(draft.claims.length)
    update({claims: [...draft.claims, '']})
    setValidation('')
    openPanel('claims')
  }
  function pickFiles(accept=ACCEPTED_FILES) {
    closePanel()
    if(picker.current){picker.current.accept=accept;picker.current.click()}
  }
  function attach(incoming: File[]) {
    if (busy) return
    const result = selectFiles(files, incoming)
    setPanel(null)
    if (result.files.length + retained.length > 10) { setFileMessage('limit'); return }
    const imageCount = retained.filter(file => file.mediaType.startsWith('image/')).length +
      result.files.filter(file => /\.(png|jpe?g|webp)$/i.test(file.name)).length
    const tableCount = retained.filter(file => ['text/csv', 'application/json'].includes(file.mediaType)).length +
      result.files.filter(file => /\.(csv|json)$/i.test(file.name)).length
    if (imageCount > 5) { setFileMessage('images'); return }
    if (tableCount > 1) { setFileMessage('table'); return }
    setFiles(result.files)
    setFileMessage(result.issues.length ? 'issues' : 'selected')
  }
  function sourceValid() {
    if (!draft.url) return true
    try {
      const url = new URL(draft.url)
      return ['http:', 'https:'].includes(url.protocol) && !url.username && !url.password
    } catch { return false }
  }
  function finishSource() {
    if (!sourceValid()) {
      setValidation('url')
      document.getElementById('research-source')?.focus()
      return
    }
    closePanel()
  }
  function submit(event?: FormEvent) {
    event?.preventDefault()
    if (busy) return
    const emptyClaim = draft.claims.findIndex((claim,index) => !claim.trim()&&!(allowImageOnly&&hasImage&&index===0))
    if (emptyClaim >= 0) {
      setValidation('claim')
      if (emptyClaim === 0) { setPanel(null); question.current?.focus() }
      else { setActiveClaim(emptyClaim); openPanel('claims', plus.current || undefined) }
      return
    }
    if (!sourceValid()) {
      setValidation('url')
      openPanel('source', plus.current || undefined)
      return
    }
    setValidation('')
    setPanel(null)
    save()
  }

  return <form className="research-form" onSubmit={submit} noValidate aria-busy={busy}
    onKeyDown={event => {
      if (event.key === 'Enter' && event.target instanceof HTMLInputElement && event.target.closest('.composer-popover')) {
        event.preventDefault()
        if (panel === 'source') finishSource()
        else closePanel()
      }
    }}>
    <fieldset disabled={busy} className={'research-composer'+(allowImageOnly?' chart-first-composer':'')}
      onDragOver={event => event.preventDefault()}
      onDrop={event => { event.preventDefault(); attach(Array.from(event.dataTransfer.files)) }}>
      <legend className="sr-only">{t('Research question and evidence', 'سؤال البحث والأدلة')}</legend>
      <div className={'composer-writing' + (expanded ? ' question-expanded' : '')}>
        {allowImageOnly&&!hasImage&&<div className="composer-upload-invitation"><button type="button" onClick={()=>pickFiles('.png,.jpg,.jpeg,.webp')}><Gallery size={22}/>{t('Upload a scientific chart','ارفع رسماً علمياً')}</button><span>{t('PNG, JPG or WebP · dataset and source optional','PNG أو JPG أو WebP · البيانات والمصدر اختياريان')}</span></div>}
        {total > 0 && <ul className="evidence-selection" aria-label={t('Evidence attachments', 'مرفقات الأدلة')}>
          {retained.map(file => <li key={file.id}>
            {file.mediaType.startsWith('image/')
              ? <img className="upload-preview" width={40} height={40} src={caseFilesUrl(current!.id, current!.currentRevision, file.id) + '?preview=1'} alt={t('Saved original ', 'الأصل المحفوظ ') + file.name}/>
              : <span className="attachment-file-icon">{['text/csv', 'application/json'].includes(file.mediaType) ? <DatasetIcon size={20}/> : <FileText size={20}/>}</span>}
            <div><a href={caseFilesUrl(current!.id, current!.currentRevision, file.id)} download><bdi title={file.name}>{file.name}</bdi></a><small>{t('Saved original', 'الأصل المحفوظ')} · {sizeLabel(file.size)}</small></div>
            <button type="button" aria-label={t('Remove from next revision ', 'إزالة من النسخة التالية ') + file.name} onClick={() => setRetained?.(retained.filter(item => item.id !== file.id))}><X size={16}/></button>
          </li>)}
          {files.map((file, index) => <li key={file.name + '-' + index}>
            <FilePreview file={file} ar={ar}/>
            <div><bdi title={file.name}>{file.name}</bdi><small>{t('Selected locally', 'مختار محلياً')} · {sizeLabel(file.size)}</small></div>
            <button type="button" aria-label={t('Remove attachment ', 'إزالة المرفق ') + file.name} onClick={() => setFiles(files.filter((_, itemIndex) => itemIndex !== index))}><X size={16}/></button>
          </li>)}
        </ul>}
        {(draft.claims[0]?.length || 0) > 240 && <button className="question-expand" type="button" aria-expanded={expanded} onClick={()=>setExpanded(!expanded)}>{expanded?t('Compact view','عرض مختصر'):t('Expand question','توسيع السؤال')}</button>}

        <label className="sr-only" htmlFor="research-question">{t('Scientific claim or research question', 'الادعاء العلمي أو سؤال البحث')}</label>
        <textarea ref={question} id="research-question" name="question" className="research-question"
          rows={1} dir="auto" maxLength={10000} value={draft.claims[0] || ''}
          placeholder={allowImageOnly?t('Add a question or chart context (optional with an image)…','أضف سؤالاً أو سياق الرسم (اختياري مع الصورة)…'):t('Ask a research question…','اطرح سؤالاً بحثياً…')}
          aria-invalid={validation === 'claim' && !draft.claims[0]?.trim()} aria-describedby="question-feedback"
          onChange={event => { update({claims: [event.target.value, ...draft.claims.slice(1)]}); setValidation('') }}
          onKeyDown={event => {
            if ((event.ctrlKey || event.metaKey) && event.key === 'Enter' && !event.nativeEvent.isComposing) {
              event.preventDefault(); submit()
            }
          }}/>
        <p id="question-feedback" className="form-feedback" role="alert">
          {validation === 'claim' && !draft.claims[0]?.trim() ? t('Write a research question first.', 'اكتب سؤال البحث أولاً.') : ''}
        </p>
        {(hasSource || draft.claims.length > 1 || hasContext) && <div className="composer-item-chips">
          {hasSource && <div className="composer-item-chip">
            <button type="button" aria-label={t('Edit source reference', 'تعديل مرجع المصدر')} onClick={event => openPanel('source', event.currentTarget)}><LinkIcon size={14}/><bdi>{draft.url || draft.source || t('Source reference', 'مرجع المصدر')}</bdi></button>
            <button type="button" aria-label={t('Remove source reference', 'إزالة مرجع المصدر')} onClick={() => update({url: '', source: '', studyDate: ''})}><X size={14}/></button>
          </div>}
          {draft.claims.slice(1).map((claim, index) => <div className="composer-item-chip" key={index}>
            <button type="button" aria-label={t('Edit claim ', 'تعديل الادعاء ') + number.format(index + 2)} onClick={event => { setActiveClaim(index + 1); openPanel('claims', event.currentTarget) }}><FileText size={14}/><bdi>{claim || t('Claim ', 'ادعاء ') + number.format(index + 2)}</bdi></button>
            <button type="button" aria-label={t('Remove claim ', 'إزالة الادعاء ') + number.format(index + 2)} onClick={() => { update({claims: draft.claims.filter((_, itemIndex) => itemIndex !== index + 1)}); setValidation('') }}><X size={14}/></button>
          </div>)}
          {hasContext && <button className="composer-context-chip" type="button" onClick={event => openPanel('settings', event.currentTarget)}><SettingsIcon size={14}/>{t('Study context', 'سياق الدراسة')}</button>}
        </div>}
      </div>

      <div className="composer-feedback">
        <p className={fileMessage === 'selected' ? 'sr-only' : 'form-feedback'} role="status">{fileMessage === 'limit'
          ? t('Attach up to ten files per revision.', 'أرفق عشرة ملفات كحد أقصى لكل نسخة.')
          : fileMessage === 'images' ? t('Attach up to five images per revision.', 'أرفق خمس صور كحد أقصى لكل نسخة.')
          : fileMessage === 'table' ? t('Attach one CSV or JSON table per revision.', 'أرفق جدول CSV أو JSON واحداً لكل نسخة.')
          : fileMessage === 'issues' ? t('Some files were skipped. Use supported files up to 20 MB. Duplicates are skipped.', 'تُجاوزت بعض الملفات. استخدم ملفات مدعومة بحد ٢٠ ميغابايت. تُتجاوز الملفات المكررة.')
          : fileMessage === 'selected' ? t('Files selected locally. They upload when you save.', 'اختيرت الملفات محلياً. تُرفع عند الحفظ.') : ''}</p>
        <p className="form-feedback error-text" role="alert">{error}</p>
        <p className="form-feedback" role="status">{localDraft?.notice === 'restored'
          ? t('Text restored. Reattach unsaved files.', 'استُعيد النص. أعد إرفاق الملفات غير المحفوظة.')
          : localDraft?.notice === 'storage_error' ? t('Browser storage is unavailable. Keep this tab open.', 'تخزين المتصفح غير متاح. أبقِ هذه النافذة مفتوحة.') : ''}</p>
      </div>
      <div className="composer-action-row">
        <div className="composer-tools" role="group" aria-label={t('Investigation inputs', 'مدخلات البحث')}>
          <button ref={plus} type="button" className="composer-add" aria-label={t('Add evidence or supporting information', 'إضافة أدلة أو معلومات داعمة')}
            aria-haspopup={panel === 'source' || panel === 'claims' ? 'dialog' : 'menu'} aria-expanded={panel === 'add' || panel === 'source' || panel === 'claims'} aria-controls="research-composer-popover"
            onClick={event => panel === 'add' ? closePanel() : openPanel('add', event.currentTarget)}><FilePlus2 size={20}/><span>{t('Add evidence','إضافة أدلة')}</span></button>
          <button type="button" className="composer-source-trigger" aria-label={t('Add source link','إضافة رابط مصدر')} aria-haspopup="dialog" aria-expanded={panel==='source'} aria-controls="research-composer-popover" onClick={event=>panel==='source'?closePanel():openPanel('source',event.currentTarget)}><LinkIcon size={18}/><span>{t('Add link','إضافة رابط')}</span></button>
          <button type="button" className="composer-review-trigger" aria-haspopup={panel==='settings'?'dialog':'menu'} aria-expanded={panel === 'review' || panel === 'settings'} aria-controls="research-composer-popover"
            onClick={event => panel === 'review' ? closePanel() : openPanel('review', event.currentTarget)}>{reviewName}<ChevronDown size={14}/></button>
        </div>
        <button type="submit" className="primary composer-start" aria-describedby="composer-save-note" disabled={busy || (!!current && !dirty)}>
          <span className="composer-submit-long">{busy ? t('Saving…', 'جارٍ الحفظ…') : current ? t('Save revision', 'حفظ نسخة جديدة') : t('Create investigation', 'إنشاء بحث')}</span>
          <span className="composer-submit-short" aria-hidden="true">{busy ? t('Saving…', 'جارٍ الحفظ…') : current ? t('Save', 'حفظ') : t('Create', 'إنشاء')}</span><ArrowUpRight size={18}/>
        </button>
      </div>
      <p id="composer-save-note" className="sr-only">{t('Creates a saved case. AI review is requested separately.', 'ينشئ بحثاً محفوظاً. تُطلب مراجعة الذكاء الاصطناعي بصورة منفصلة.')}</p>
      <input ref={picker} type="file" className="sr-only" multiple tabIndex={-1} aria-label={t('Attach evidence files', 'إرفاق ملفات الأدلة')} accept={ACCEPTED_FILES}
        onChange={event => { attach(Array.from(event.target.files || [])); event.target.value = '' }}/>

      <ComposerPopover open={!!panel && !busy} anchor={anchor} label={panel ? labels[panel] : ''}
        menu={panel === 'add' || panel === 'review'} focusKey={panel + '-' + claimIndex}
        initialFocus={panel === 'review' ? '[aria-checked=true]' : panel === 'add' ? '[role=menuitem]' : panel === 'claims' ? 'textarea, button.composer-done' : 'input, select, textarea'}
        onDismiss={() => setPanel(null)}>
        {panel === 'add' && <>
          <button role="menuitem" type="button" tabIndex={-1} onClick={() => pickFiles('.png,.jpg,.jpeg,.webp')}><Gallery size={18}/>{t('Add images','إضافة صور')}</button>
          <button role="menuitem" type="button" tabIndex={-1} onClick={() => pickFiles()}><Paperclip size={18}/><span>{t('Add evidence', 'إضافة أدلة')}<small>{t('Images, tables and PDF files', 'صور وجداول وملفات PDF')}</small></span></button>
          <button role="menuitem" type="button" tabIndex={-1} onClick={() => pickFiles('.csv,.json')}><DatasetIcon size={18}/>{t('Add dataset','إضافة بيانات')}</button>
          <button role="menuitem" type="button" tabIndex={-1} onClick={() => openPanel('source')}><LinkIcon size={18}/>{t('Add source link', 'إضافة رابط مصدر')}</button>
          <button role="menuitem" type="button" tabIndex={-1} disabled={draft.claims.length >= 10} onClick={addClaim}><FileText size={18}/>{t('Add another claim', 'إضافة ادعاء آخر')}</button>
          <p className="popover-help">{t('PNG, JPG, WebP, CSV, JSON, PDF · 20 MB per file. Up to 5 images, 1 table and 10 files total.', 'PNG وJPG وWebP وCSV وJSON وPDF · ٢٠ ميغابايت للملف. حتى ٥ صور وجدول واحد و١٠ ملفات إجمالاً.')}</p>
        </>}
        {panel === 'review' && <>
          <button type="button" role="menuitemradio" tabIndex={-1} aria-checked={draft.reviewDepth === 'focused'} onClick={() => { update({reviewDepth: 'focused'}); closePanel() }}><span><strong>{t('Visual review', 'مراجعة بصرية')}</strong><small>{t('Focused review of chart presentation', 'مراجعة مركزة لطريقة عرض الرسوم')}</small></span></button>
          <button type="button" role="menuitemradio" tabIndex={-1} aria-checked={draft.reviewDepth === 'council'} onClick={() => { update({reviewDepth: 'council'}); closePanel() }}><span><strong>{t('Multi-perspective review', 'مراجعة متعددة التخصصات')}</strong><small>{t('Specialist perspectives and cross-review', 'آراء متخصصة ومراجعة متبادلة')}</small></span></button>
          <button type="button" role="menuitem" tabIndex={-1} className="popover-settings" onClick={() => openPanel('settings')}><SettingsIcon size={17}/>{t('Study settings…', 'إعدادات الدراسة…')}</button>
        </>}
        {(panel === 'source' || panel === 'claims' || panel === 'settings') && <>
          <div className="popover-heading"><h2>{labels[panel]}</h2><button type="button" aria-label={t('Close editor', 'إغلاق المحرر')} onClick={closePanel}><X size={16}/></button></div>
          {panel === 'source' && <div className="popover-fields">
            <label htmlFor="research-source">{t('Source link', 'رابط المصدر')}<input id="research-source" name="source_url" type="url" dir="ltr" maxLength={2000} value={draft.url} autoComplete="off" placeholder="https://…"
              aria-invalid={validation === 'url'} aria-describedby="source-feedback" onChange={event => { update({url: event.target.value}); setValidation('') }}/></label>
            <p id="source-feedback" role="alert" className="form-feedback">{validation === 'url' ? t('Use an http or https link without credentials.', 'استخدم رابط http أو https دون بيانات تسجيل دخول.') : ''}</p>
            <details open={!!(draft.source || draft.studyDate)}><summary>{t('Source details', 'تفاصيل المصدر')}</summary><div className="popover-fields">
              <label>{t('Source title', 'عنوان المصدر')}<input name="source_title" dir="auto" maxLength={500} value={draft.source} onChange={event => update({source: event.target.value})}/></label>
              <label>{t('Publication date', 'تاريخ النشر')}<input name="publication_date" type="date" value={draft.studyDate} onChange={event => update({studyDate: event.target.value})}/></label>
            </div></details>
            <p className="popover-help">{t('A reference link does not authenticate its contents.', 'رابط المرجع لا يثبت أصالة محتواه.')}</p>
            <button className="composer-done" type="button" onClick={finishSource}>{t('Done', 'تم')}</button>
          </div>}
          {panel === 'claims' && <div className="popover-fields">
            {claimIndex > 0 && <>
              {draft.claims.length > 2 && <label>{t('Choose claim', 'اختيار ادعاء')}<select aria-label={t('Choose claim', 'اختيار ادعاء')} value={claimIndex} onChange={event => setActiveClaim(Number(event.target.value))}>{draft.claims.slice(1).map((_, index) => <option key={index} value={index + 1}>{t('Claim ', 'ادعاء ') + number.format(index + 2)}</option>)}</select></label>}
              <label htmlFor={'research-claim-' + claimIndex}>{t('Claim ', 'ادعاء ') + number.format(claimIndex + 1)}<textarea id={'research-claim-' + claimIndex} dir="auto" rows={4} maxLength={10000} value={draft.claims[claimIndex]}
                aria-invalid={validation === 'claim' && !draft.claims[claimIndex].trim()} onChange={event => { update({claims: draft.claims.map((claim, index) => index === claimIndex ? event.target.value : claim)}); setValidation('') }}/></label>
              {validation === 'claim' && <p className="form-feedback" role="alert">{t('Write the claim or remove it before saving.', 'اكتب الادعاء أو أزله قبل الحفظ.')}</p>}
            </>}
            <div className="popover-editor-actions"><button type="button" disabled={draft.claims.length >= 10} onClick={addClaim}>{t('Add claim', 'إضافة ادعاء')}</button><button className="composer-done" type="button" onClick={closePanel}>{t('Done', 'تم')}</button></div>
          </div>}
          {panel === 'settings' && <div className="popover-fields">
            <label>{t('Study design', 'تصميم الدراسة')}<select aria-label={t('Study design', 'تصميم الدراسة')} value={draft.studyDesign} onChange={event => update({studyDesign: event.target.value as AnalysisDraft['studyDesign']})}>{studyDesigns.map(name => <option key={name} value={name}>{ar ? designNames[name] : name}</option>)}</select></label>
            <label htmlFor="context-kind">{t('Research context', 'سياق البحث')}</label><select id="context-kind" value={contextField} onChange={event => setContextField(event.target.value as typeof contextField)}>{Object.entries(contextNames).map(([key, value]) => <option key={key} value={key}>{value}{draft[key as typeof contextField] ? ' · ' + t('added', 'مضاف') : ''}</option>)}</select>
            <textarea aria-label={contextNames[contextField]} name={contextField} rows={3} dir="auto" maxLength={contextField === 'context' ? 5000 : 3000} value={draft[contextField]} onChange={event => update({[contextField]: event.target.value})}/>
            {localDraft && <label className="check popover-draft"><input type="checkbox" checked={localDraft.enabled} onChange={event => localDraft.change(event.target.checked)}/>{t('Keep unsaved text on this device', 'احتفظ بالنص غير المحفوظ على هذا الجهاز')}</label>}
            <p className="popover-help">{t('Text only. Save the case to preserve files.', 'النص فقط. احفظ البحث للاحتفاظ بالملفات.')}</p>
            <button className="composer-done" type="button" onClick={closePanel}>{t('Done', 'تم')}</button>
          </div>}
        </>}
      </ComposerPopover>
    </fieldset>
  </form>
}
