import {z} from 'zod'

export const structuredReview = z.object({
 claim_assessments:z.array(z.object({claim_id:z.string(),position:z.enum(['supports','partially_supports','contradicts','cannot_assess']),rationale:z.string(),evidence_refs:z.array(z.string())})),
 findings:z.array(z.object({finding_id:z.string(),title:z.string(),observation:z.string(),why_it_matters:z.string(),recommendation:z.string(),evidence_refs:z.array(z.string())}))
})
