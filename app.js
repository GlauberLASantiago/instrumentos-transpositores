import {instruments} from './data.js';
import {normalize,adjacent,matchVoice} from './navigation.js';
const $=id=>document.getElementById(id);
let selected=1,recognizer=null;
const voiceAliases={};
fetch('voice-aliases.json').then(r=>{if(!r.ok)throw new Error('aliases');return r.json();}).then(map=>{for(const [word,id] of Object.entries(map))voiceAliases[normalize(word)]=id;}).catch(()=>{});
function renderList(){const query=normalize($('search').value);const items=instruments.filter(i=>normalize(i.name).includes(query));$('list').replaceChildren(...items.map(i=>{const a=document.createElement('a');a.textContent=i.name;a.href='#instrumento-'+i.id;if(i.id===selected)a.setAttribute('aria-current','page');return a;}));$('count').textContent=items.length?items.length+(items.length===1?' instrumento':' instrumentos'):'Nenhum instrumento encontrado.';}
function route(){const match=location.hash.match(/^#instrumento-(\d+)$/);const id=match?Number(match[1]):(!location.hash?1:0);const instrument=instruments.find(i=>i.id===id);$('home').hidden=!!instrument;$('catalog').hidden=!instrument;if(!instrument){document.title='Instrumentos Transpositores';recognizer?.abort();return;}selected=id;$('instrument-name').textContent=instrument.name;$('position').textContent='INSTRUMENTO '+id+' DE '+instruments.length;document.title=instrument.name+' · Instrumentos Transpositores';$('image-error').hidden=true;$('card').alt='Ficha original de '+instrument.name+': transposição, tonalidade, escrita da partitura e clave';$('card').src='assets/'+id+'.jpg';$('prev').href='#instrumento-'+adjacent(id,-1);$('next').href='#instrumento-'+adjacent(id,1);renderList();}
$('search').addEventListener('input',renderList);window.addEventListener('hashchange',route);$('card').addEventListener('error',()=>{$('image-error').hidden=false;});
$('about-open').addEventListener('click',()=>$('about').showModal());$('about-close').addEventListener('click',()=>$('about').close());
$('fullscreen').addEventListener('click',()=>$('sheet').requestFullscreen().catch(()=>{$('card').scrollIntoView({block:'start'});}));$('exit-fullscreen').addEventListener('click',()=>document.exitFullscreen());route();
$('voice').addEventListener('click',()=>{
  const Recognition=window.SpeechRecognition||window.webkitSpeechRecognition;
  if(!Recognition){$('voice-status').textContent='Este navegador não oferece busca por voz. Digite o nome no campo de busca.';$('search').focus();return;}
  if(recognizer)return;
  recognizer=new Recognition();recognizer.lang='pt-BR';recognizer.continuous=false;recognizer.interimResults=false;
  $('voice').disabled=true;$('voice-status').textContent='Diga o nome do instrumento…';
  recognizer.onresult=event=>{
    const text=event.results[0][0].transcript,id=matchVoice(text,instruments,voiceAliases);
    $('voice-status').textContent='Você disse: '+text;
    if(id){$('search').value='';location.hash='instrumento-'+id;renderList();}
    else{$('search').value=text;renderList();$('voice-status').textContent+=' — escolha um resultado ou tente outro nome.';}
  };
  recognizer.onerror=event=>{$('voice-status').textContent=event.error==='not-allowed'?'Microfone não autorizado. Use a busca digitada.':'Não foi possível reconhecer a fala. Tente novamente ou use a busca digitada.';};
  recognizer.onend=()=>{recognizer=null;$('voice').disabled=false;};
  try{recognizer.start();}catch{$('voice-status').textContent='Busca por voz indisponível. Use a busca digitada.';recognizer=null;$('voice').disabled=false;}
});
