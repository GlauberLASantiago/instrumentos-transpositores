import assert from 'node:assert/strict';import {readFile} from 'node:fs/promises';import {createHash} from 'node:crypto';import {instruments} from '../data.js';import {normalize,adjacent,matchVoice} from '../navigation.js';
const root=new URL('../',import.meta.url),manifest=JSON.parse(await readFile(new URL('docs/extracted-assets.json',root),'utf8'));
assert.equal(manifest.assets.length,44);assert.equal(instruments.length,43);
for(const asset of manifest.assets){const bytes=await readFile(new URL(asset.path,root));assert.equal(bytes.length,asset.bytes);assert.equal(createHash('sha256').update(bytes).digest('hex'),asset.sha256,asset.path);}
assert.equal(adjacent(1,-1),43);assert.equal(adjacent(42,1),43);assert.equal(adjacent(43,1),1);
const aliases=JSON.parse(await readFile(new URL('voice-aliases.json',root),'utf8')),normalized=Object.fromEntries(Object.entries(aliases).map(([w,id])=>[normalize(w),id]));
for(const [word,id] of Object.entries(aliases))assert.equal(matchVoice(word,instruments,normalized),id);
assert.equal(matchVoice('OBOE',instruments,normalized),7);assert.equal(matchVoice('instrumento inexistente',instruments,normalized),null);
console.log('PASS: 44 recursos idênticos ao APK; 43 fichas acessíveis; navegação circular e '+Object.keys(aliases).length+' aliases originais de voz.');
