export const MAX_FILE_BYTES=20*1024*1024
export const ACCEPTED_FILES='.png,.jpg,.jpeg,.webp,.csv,.json,.pdf'
export function selectFiles(existing:File[],incoming:File[]){const files=[...existing];const issues:('type'|'size'|'duplicate')[]=[];for(const file of incoming){if(!/\.(png|jpe?g|webp|csv|json|pdf)$/i.test(file.name)){issues.push('type');continue}if(file.size>MAX_FILE_BYTES){issues.push('size');continue}if(files.some(f=>f.name===file.name&&f.size===file.size&&f.lastModified===file.lastModified)){issues.push('duplicate');continue}files.push(file)}return {files,issues}}
