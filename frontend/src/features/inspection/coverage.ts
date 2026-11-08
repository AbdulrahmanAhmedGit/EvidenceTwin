export type RecordedCheck={check:string;status:string;label?:string;statusLabel?:string;explanation?:string}
const names:Record<string,[string,string]>={
 complete_dataset_queries:['Structured data inspection','فحص البيانات المنظمة'],descriptive_comparison:['Reported value comparison','مقارنة القيم المبلغ عنها'],
 source_retrieval:['Source reading','قراءة المصادر'],source_authenticity:['Independent source authentication','التحقق المستقل من أصالة المصدر'],
 statistical_inference:['Statistical inference','الاستدلال الإحصائي'],blind_optics:['Blind plot reconstruction','إعادة بناء الرسوم المعماة'],
}
const states:Record<string,[string,string]>={performed:['Performed','أُجري'],not_performed:['Not performed','لم يُجرَ'],no_dataset:['No structured table','لا يوجد جدول منظم'],
 retrieved:['Retrieved','تم الاسترجاع'],partially_retrieved:['Some sources retrieved','استُرجعت بعض المصادر'],unavailable:['Unavailable','غير متاح'],
 not_requested:['Awaiting a new review','بانتظار مراجعة جديدة'],not_requested_limit:['Retrieval limit reached','بُلغ حد الاسترجاع'],no_url:['No supported source link','لا يوجد رابط مصدر مدعوم']}
export function coverageStatus(status:string,ar:boolean){return states[status]?.[ar?1:0]||(ar?'حالة مسجلة أخرى':'Other recorded state')}
export function describeCoverage(item:RecordedCheck,ar:boolean){
 let explanation:[string,string]
 switch(item.check){
 case 'complete_dataset_queries':explanation=item.status==='no_dataset'?['No structured numerical table was processed. Images remain available as evidence. Supply a CSV, structured JSON or a supported dataset link for exact calculations.','لم يُعالج جدول رقمي منظم. تظل الصور أدلة متاحة. قدم CSV أو JSON منظماً أو رابط بيانات مدعوماً للحسابات الدقيقة.']:['Parsed tables are available for bounded queries. Inspect the selected rows and their provenance.','الجداول المحللة متاحة للاستعلامات المحدودة. افحص الصفوف المختارة وتتبعها.'];break
 case 'descriptive_comparison':explanation=item.status==='performed'?['Exact observations and arithmetic are recorded above.','الملاحظات الدقيقة والحسابات مسجلة أعلاه.']:['No reproducible comparison was established. It requires structured observations and an unambiguous compatible selection. Inspect the selection limits.','لم تثبت مقارنة قابلة للتكرار. تتطلب ملاحظات منظمة واختياراً متوافقاً غير ملتبس. افحص حدود اختيار البيانات.'];break
 case 'source_retrieval':explanation=item.status==='no_url'?['No supported URL was recorded for this run. New reviews also detect links in questions and research notes.','لم يُسجل رابط مدعوم لهذه المراجعة. تكشف المراجعات الجديدة أيضاً الروابط داخل الأسئلة وملاحظات البحث.']:item.status==='not_requested'?['Source links were detected. Reading starts when you authorize a new review.','كُشفت روابط المصادر. تبدأ قراءتها عند التصريح بمراجعة جديدة.']:['Inspect each source outcome below. Successful reading and independent verification have separate states.','افحص نتيجة كل مصدر أدناه. قراءة المحتوى والتحقق المستقل لهما حالتان منفصلتان.'];break
 case 'source_authenticity':explanation=['Independent source authentication is unavailable in this pipeline. Source provenance remains unverified.','التحقق المستقل من أصالة المصادر غير متاح في هذه المعالجة. يظل أصل المصادر غير متحقق منه.'];break
 case 'statistical_inference':explanation=['Validated inferential procedures are unavailable. Descriptive calculations are reported separately.','الإجراءات الاستدلالية المعتمدة غير متاحة. تُعرض الحسابات الوصفية بشكل منفصل.'];break
 case 'blind_optics':explanation=['Blind reconstruction awaits a specified and accepted blinding/rendering protocol. Original charts remain inspectable.','تنتظر إعادة البناء المعماة تحديد بروتوكول التعمية والرسم وقبوله. تظل الرسوم الأصلية متاحة للفحص.'];break
 default:explanation=['Inspect the preserved structured record for this check.','افحص السجل المنظم المحفوظ لهذا الفحص.']
 }
 return {label:ar?names[item.check]?.[1]||'فحص مسجل إضافي':item.label||names[item.check]?.[0]||'Additional recorded check',
  status:ar?coverageStatus(item.status,true):item.statusLabel||coverageStatus(item.status,false),explanation:!ar&&item.explanation?item.explanation:explanation[ar?1:0]}
}
export function parseLegacyCoverage(body:string):RecordedCheck[]|null {
 const lines=body.split('\n').map(line=>line.trim()).filter(Boolean)
 const items=lines.map(line=>{const [check,status]=line.split(' — ');return names[check]&&states[status]?{check,status}:null})
 return items.length&&items.every((item):item is RecordedCheck=>item!==null)?items:null
}
