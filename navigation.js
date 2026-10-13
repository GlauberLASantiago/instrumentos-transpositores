export const normalize=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().trim();
export const adjacent=(id,offset,total=43)=>((id-1+offset)%total+total)%total+1;
export function matchVoice(text,instruments,aliases={}){const word=normalize(text);if(aliases[word])return aliases[word];return instruments.find(i=>normalize(i.name)===word)?.id||null;}
