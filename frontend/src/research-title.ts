/** A display prefix, never an inferred or generated research claim. */
export function researchTitle(value:string,limit=86){const text=value.replace(/\s+/gu,' ').trim();const points=Array.from(text);if(points.length<=limit)return text;const prefix=points.slice(0,limit).join('');const boundary=prefix.lastIndexOf(' ');return prefix.slice(0,boundary>limit*.6?boundary:undefined).trimEnd()+'…'}

/** Use a verbatim quoted claim or remove a recognized instruction wrapper for display only. */
export function researchSubjectTitle(value:string,limit=86) {
 const quoted=value.match(/[“"]([^”"]{12,})[”"]/u)?.[1]
 const subject=quoted||value.replace(/^(?:Investigate the following scientific claim|تحقق من الادعاء العلمي التالي)\s*[:：]\s*/iu,'')
 return researchTitle(subject,limit)
}
