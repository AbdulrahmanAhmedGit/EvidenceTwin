import {useState} from 'react'
import {HeartPulse,Leaf,Pills,ChartSquare} from '../../components/ui/Icons'

const prompts=[
  {id:'health',icon:HeartPulse,label:['Health','الصحة'],question:['Do the axes exaggerate the difference in diabetes prevalence between these groups?','هل تبالغ المحاور في الفرق بين المجموعات في رسم انتشار السكري؟']},
  {id:'environment',icon:Leaf,label:['Public health','الصحة العامة'],question:['Does the time range in this public-health chart hide changes in the trend?','هل تخفي الفترة الزمنية المختارة في رسم الصحة العامة تغيرات في الاتجاه؟']},
  {id:'medicine',icon:Pills,label:['Medicine','الطب'],question:['Does this treatment-benefit chart distinguish absolute from relative risk?','هل يميّز رسم فوائد العلاج بين المخاطر المطلقة والنسبية؟']},
  {id:'data',icon:ChartSquare,label:['Data analysis','تحليل البيانات'],question:['Does this chart faithfully represent the supplied data, units and uncertainty?','هل يمثل الرسم البيانات المقدمة والوحدات وعدم اليقين بصورة أمينة؟']},
]

export default function InvestigationExamples({ar,question,busy,onSelect}:{ar:boolean;question:string;busy:boolean;onSelect:(question:string)=>void}) {
  const [pending,setPending]=useState<string|null>(null)
  function choose(value:string) {
    if(question.trim()&&question!==value){setPending(value);return}
    onSelect(value)
    setPending(null)
  }
  return <section className="investigation-examples" aria-labelledby="investigation-examples-title">
    <div className="investigation-examples-heading"><h2 id="investigation-examples-title">{ar?'جرّب سؤالاً عن رسم':'Try a chart investigation'}</h2><span>{ar?'أسئلة تعليمية قابلة للتعديل':'Editable educational prompts'}</span></div>
    <div className="investigation-prompt-grid">{prompts.map(prompt=>{
      const Icon=prompt.icon
      return <button type="button" className={'investigation-prompt prompt-'+prompt.id} key={prompt.id} disabled={busy} onClick={()=>choose(prompt.question[ar?1:0])}>
        <span className="investigation-prompt-icon"><Icon size={25}/></span><span><strong>{prompt.label[ar?1:0]}</strong><span>{prompt.question[ar?1:0]}</span></span>
      </button>
    })}</div>
    {pending&&<div className="example-replacement" role="group" aria-label={ar?'استبدال السؤال الحالي':'Replace the current question'}>
      <p>{ar?'هل تريد استبدال سؤالك الحالي بهذا السؤال التعليمي؟':'Replace your current question with this educational prompt?'}</p>
      <button type="button" disabled={busy} onClick={()=>{onSelect(pending);setPending(null)}}>{ar?'استخدم هذا السؤال':'Use this question'}</button><button type="button" onClick={()=>setPending(null)}>{ar?'الاحتفاظ بسؤالي':'Keep my question'}</button>
    </div>}
    <p className="investigation-example-note">{ar?'هذه أسئلة مقترحة، وليست أبحاثاً محفوظة أو نتائج. أضف مصادرك أو بياناتك قبل طلب المراجعة.':'Prompts only, with no saved research or results. Add your own sources or data before requesting a review.'}</p>
  </section>
}
