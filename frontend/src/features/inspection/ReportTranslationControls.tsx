import {downloadJson} from './utils'
import type {useReportTranslation} from './report-translations'
type State=ReturnType<typeof useReportTranslation>
export default function ReportTranslationControls({state,ar}:{state:State;ar:boolean}){
 const t=(en:string,arabic:string)=>ar?arabic:en
 const pending=state.requesting||!!state.selected&&['queued','running'].includes(state.selected.status)
 const busy=state.requesting||pending
 return <section className="report-translation-controls" aria-label={t('Report translation','ترجمة التقرير')}>
  <div className="translation-actions"><label>{t('Translate report to','ترجمة التقرير إلى')}<select value={state.target} onChange={event=>state.setTarget(event.target.value as 'ar'|'en')} disabled={busy}><option value="ar">العربية</option><option value="en">English</option></select></label>
  <button onClick={state.start} disabled={busy||!state.availability.data?.available||!state.availability.data.targets.includes(state.target)}>{busy?t('Translating…','جارٍ الترجمة…'):state.selected?.status==='failed'?t('Retry translation','إعادة محاولة الترجمة'):t('Translate','ترجمة')}</button>
  {state.selectedId&&<button onClick={()=>state.setSelectedId(null)}>{t('Read original','قراءة الأصل')}</button>}
  {state.translated&&<button onClick={()=>downloadJson(state.translated,state.translated!.analysisId+'-'+state.translated!.targetLanguage+'-translation.json')}>{t('Download translation JSON','تنزيل الترجمة JSON')}</button>}</div>
  <p className="caption">{t('LibreTranslate creates a labeled derivative. Check scientific terminology against the original. Numbers and references are protected.','ينشئ LibreTranslate نسخة مشتقة موسومة. راجع المصطلحات العلمية مع الأصل. تُحمى الأرقام والمراجع أثناء الترجمة.')}</p>
  {state.availability.isPending&&<p role="status">{t('Checking translation availability…','جارٍ التحقق من توفر الترجمة…')}</p>}
  {(state.availability.error||state.availability.data&&!state.availability.data.available)&&<div><p>{t('The translation service is unavailable. The original report is available.','خدمة الترجمة غير متاحة. التقرير الأصلي متاح.')}</p><button onClick={()=>state.availability.refetch()} disabled={state.availability.isFetching}>{t('Check again','التحقق مجدداً')}</button></div>}
  {state.availability.data?.translations.filter(item=>item.status==='completed').map(item=><button key={item.id} onClick={()=>state.setSelectedId(item.id)} aria-pressed={state.selectedId===item.id}>{item.targetLanguage==='ar'?t('Read Arabic translation','قراءة الترجمة العربية'):t('Read English translation','قراءة الترجمة الإنجليزية')}</button>)}
  {state.selected&&pending&&<p role="status">{t('Processed text blocks','كتل النص المعالجة')} <bdi>{state.selected.completedBlocks} / {state.selected.totalBlocks}</bdi></p>}
  {(state.error||state.job.error||state.selected?.status==='failed')&&<p role="alert">{state.error||t('Translation could not be completed or loaded. The original report remains available.','تعذر إكمال الترجمة أو تحميلها. يظل التقرير الأصلي متاحاً.')}</p>}
  {state.translated&&<p className="translation-notice" role="status">{state.translated.retainedOriginalBlocks.length?t('Partial machine translation','ترجمة آلية جزئية'):t('Machine-translated report','تقرير مترجم آلياً')} · {state.translated.targetLanguage==='ar'?'العربية':'English'}{state.translated.finishedAt?' · '+new Date(state.translated.finishedAt).toLocaleString(ar?'ar':'en'):''}</p>}
  {state.translated&&state.translated.retainedOriginalBlocks.length>0&&<p role="note">{t('Some passages retain their original wording because safe preservation of numbers or references could not be confirmed.','تبقى بعض المقاطع بلغتها الأصلية لتعذر تأكيد الحفاظ الآمن على الأرقام أو المراجع.')} <bdi>{state.translated.retainedOriginalBlocks.length}</bdi></p>}
 </section>
}
