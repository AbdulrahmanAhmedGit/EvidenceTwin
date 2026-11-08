import {useState} from 'react'
import type {ReactNode} from 'react'
import {Link} from 'react-router-dom'
import {ArrowUpRight, ChevronRight} from './components/ui/Icons'
import './styles/landing.css'

export default function LandingPage({ar,chart}:{ar:boolean;chart:(neutral:boolean)=>ReactNode}) {
 const [neutral,setNeutral]=useState(false)
 const t=(en:string,arabic:string)=>ar?arabic:en
 const roles=[
  ['Visual Analyst','المحلل البصري','Axes, cropping, labels and visual emphasis.','المحاور والقص والتسميات والتأكيد البصري.'],
  ['Statistical Auditor','المدقق الإحصائي','Arithmetic, denominators and uncertainty.','الحسابات والمقامات وعدم اليقين.'],
  ['Scientific Skeptic','المراجع العلمي','Study design, confounding and causal claims.','تصميم الدراسة والإرباك والادعاءات السببية.'],
  ['Counterfactual Analyst','محلل السيناريو البديل','How framing changes an interpretation.','كيف يغير التأطير تفسير النتائج.'],
 ]
 return <div className="et-landing">
  <section className="et-hero" aria-labelledby="landing-title">
   <div className="et-hero-copy">
    
    <h1 id="landing-title">{t('Same data.','نفس البيانات.')}<span>{t('Different story.','قصة مختلفة.')}</span></h1>
    <p className="et-intro">{t('Inspect scientific charts for potentially misleading presentation, starting with healthcare and public-health data. Compare with an evidence-grounded reconstruction when a supported method is available.','افحص الرسوم العلمية بحثاً عن عرض قد يضلل القارئ، بدءاً ببيانات الطب والصحة العامة. قارن بإعادة بناء تستند إلى الأدلة عند توفر منهج مدعوم.')}</p>
    <p className="et-availability">{t('Exploratory AI review is available when configured. Source verification and Neutral Twin generation are not yet available.','تتوفر المراجعة الاستكشافية بالذكاء الاصطناعي عند إعدادها. التحقق من المصادر وإنشاء التوأم المحايد غير متاحين بعد.')}</p><div className="et-actions"><Link className="button primary" to="/app/analyses/new">{t('Inspect a chart','افحص رسماً')}<ArrowUpRight size={18}/></Link><Link className="et-link" to="/methodology">{t('Methodology','المنهجية')}<ChevronRight className="directional-icon" size={16}/></Link></div>
   </div>
   <div className="et-optics"><img src="/evidence-optics.webp" srcSet="/evidence-optics-600.webp 600w, /evidence-optics.webp 1200w" sizes="(max-width: 767px) calc(100vw - 40px), 46vw" width="1200" height="800" fetchPriority="high" alt={t('Two optical glass prisms refract the same green line differently.','منشوران من الزجاج البصري يكسران الخط الأخضر نفسه بطريقتين مختلفتين.')}/></div>
  </section>

  <section className="et-principles" aria-label={t('Research principles','مبادئ البحث')}>
   <p>{t('Evidence before agreement.','الأدلة قبل الاتفاق.')}<span>{t('A clearer basis for every conclusion.','أساس أوضح لكل استنتاج.')}</span></p>
   <div>{t('Trace the source','تتبع المصدر')}</div><div>{t('Inspect the framing','افحص التأطير')}</div><div>{t('Keep uncertainty visible','أظهر عدم اليقين')}</div>
  </section>

  <section className="et-comparison" aria-labelledby="framing-title">
   <div className="et-comparison-copy"><h2 id="framing-title">{t('A different axis.','محور مختلف.')}<span>{t('A different impression.','انطباع مختلف.')}</span></h2><p>{t('A chart can change the story without changing the data. Compare the framing yourself.','يمكن للرسم تغيير القصة دون تغيير البيانات. قارن التأطير بنفسك.')}</p>
    <div className="et-toggle" role="group" aria-label={t('Comparison focus','تركيز المقارنة')}><button aria-pressed={!neutral} onClick={()=>setNeutral(false)}>{t('Original framing','الإطار الأصلي')}</button><button aria-pressed={neutral} onClick={()=>setNeutral(true)}>{t('Neutral baseline','خط الأساس المحايد')}</button></div>
    <div className="et-observation" aria-live="polite"><strong dir="ltr">42% → 40%</strong><p>{neutral?t('The baseline starts at zero. The difference remains two percentage points.','يبدأ خط الأساس من الصفر. يبقى الفرق نقطتين مئويتين.'):t('The baseline starts at 38%. The same difference appears much larger.','يبدأ خط الأساس من ٣٨٪. يبدو الفرق نفسه أكبر بكثير.')}</p></div>
   </div>
   <div className="et-chart"><div className="et-chart-heading"><span>{t('Same values. Different framing.','القيم نفسها. تأطير مختلف.')}</span><span>{t('Educational example','مثال تعليمي')}</span></div>{chart(neutral)}<p className="et-chart-note">{t('Visual emphasis does not establish statistical significance. Original source not supplied.','التأكيد البصري لا يثبت الدلالة الإحصائية. المصدر الأصلي غير مقدم.')}</p></div>
  </section>

  <section className="et-process" aria-labelledby="process-title"><div className="et-process-heading"><h2 id="process-title">{t('Follow the evidence.','اتبع الأدلة.')}<span>{t('Question the interpretation.','راجع التفسير.')}</span></h2><p>{t('From the original claim to an evidence-linked audit, keep each decision open to inspection.','من الادعاء الأصلي إلى تدقيق مرتبط بالأدلة، اجعل كل قرار قابلاً للفحص.')}</p><Link className="et-link" to="/how-it-works">{t('How It Works','كيف يعمل')}<ArrowUpRight size={18}/></Link><p className="et-process-scope">{t('The intended workflow is shown below. Verification and neutral generation require scientific services that are not yet enabled.','يعرض ما يلي سير العمل المستهدف. يتطلب التحقق وإنشاء العرض المحايد خدمات علمية لم تُفعّل بعد.')}</p></div><ol className="et-process-list">{[
    ['Submit evidence','قدم الأدلة','Bring the chart, underlying data, source and claim.','أضف الرسم والبيانات الأساسية والمصدر والادعاء.'],
    ['Verify the data','افحص البيانات','Separate supplied values, calculations and missing context.','ميّز بين القيم المقدمة والحسابات والسياق المفقود.'],
    ['Generate a neutral twin','أنشئ توأماً محايداً','Hold the values fixed. Make framing changes explicit.','ثبّت القيم وأظهر تغييرات التأطير بوضوح.'],
    ['Review independently','راجع باستقلالية','Compare evidence references, limitations and disagreements.','قارن مراجع الأدلة والحدود والخلافات.'],
    ['Produce an audit','أنتج تدقيقاً','Trace findings back to their evidence and recorded checks.','تتبع النتائج وصولاً إلى أدلتها وفحوصها المسجلة.'],
   ].map(([en,arabic,body,bodyAr])=><li key={en}><h3>{t(en,arabic)}</h3><p>{t(body,bodyAr)}</p></li>)}</ol>
  </section>

  <section className="et-council" aria-labelledby="council-title"><div className="et-council-title"><h2 id="council-title">{t('Four perspectives.','أربع زوايا للنظر.')}<span>{t('Evidence decides.','الأدلة هي المرجع.')}</span></h2><p>{t('Independent reviews examine different failure modes. The evidence judge assesses support, rather than counting votes.','تفحص المراجعات المستقلة جوانب مختلفة للإخفاق. يقيّم حكم الأدلة الدعم المتاح بدلاً من عد الأصوات.')}</p></div><div className="et-roles">{roles.map(([en,arabic,body,bodyAr])=><article key={en}><h3>{t(en,arabic)}</h3><p>{t(body,bodyAr)}</p></article>)}</div><div className="et-proof"><p>{t('Agreement is not scientific proof.','اتفاق النماذج لا يثبت الحقيقة العلمية.')}</p><Link className="et-link" to="/methodology">{t('Methodology','المنهجية')}<ArrowUpRight size={18}/></Link></div></section>

  <section className="et-library" aria-labelledby="library-title"><h2 id="library-title">{t('Put an interpretation to the test.','اختبر تفسيراً للبيانات.')}</h2><p>{t('Explore educational cases with supplied values and explicit limitations. These are examples, not live verification results.','استكشف حالات تعليمية بقيم مقدمة وحدود واضحة. هذه أمثلة وليست نتائج تحقق حية.')}</p><div className="et-case-links">{[
   ['a1','Misleading axes','محاور مضللة','How a baseline changes the visual story.','كيف يغير خط الأساس القصة البصرية.'],
   ['a2','Correlation and causation','الارتباط والسببية','What an observed association cannot establish.','ما الذي لا يثبته الارتباط المرصود.'],
   ['a3','Missing uncertainty','عدم اليقين المفقود','What the chart leaves out of the picture.','ما الذي يغفله الرسم عن الصورة الكاملة.'],
  ].map(([id,en,arabic,body,bodyAr])=><Link to={'/app/library/'+id} key={id}><div><h3>{t(en,arabic)}</h3><p>{t(body,bodyAr)}</p></div><ArrowUpRight size={24}/></Link>)}</div></section>

  <section className="et-integrations"><div><h2>{t('Verification, where research happens.','التحقق حيث يجري البحث.')}</h2><p>{t('Work directly in the workspace. Explore planned interfaces for assistants, MCP and reusable skills.','اعمل مباشرة في مساحة العمل. استكشف واجهات مخططة للمساعدين وMCP والمهارات القابلة لإعادة الاستخدام.')}</p></div><Link className="et-link" to="/integrations">{t('Connection requirements','متطلبات الاتصال')}<ArrowUpRight size={18}/></Link><p className="et-capability-note">{t('Scientific execution requires a compatible backend and enabled capabilities.','يتطلب التنفيذ العلمي خادماً متوافقاً وقدرات مفعّلة.')}</p></section>

  <section className="et-end"><h2>{t('Better conclusions begin','استنتاجات أفضل تبدأ')}<span>{t('with better evidence.','بأدلة أفضل.')}</span></h2><Link className="button primary" to="/app">{t('Open Workspace','افتح مساحة العمل')}<ArrowUpRight size={18}/></Link></section>
 </div>
}
