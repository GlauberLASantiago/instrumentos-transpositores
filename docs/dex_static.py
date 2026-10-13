import struct,json,pathlib
ROOT=pathlib.Path(r'C:\Users\Principal\AppData\Local\Temp\rea-extracted-a358cf1e-7453-40ed-9d23-a207610ce6d4')
OUT=pathlib.Path(__file__).parent
def parse(path):
 b=path.read_bytes(); u=lambda off:struct.unpack_from('<I',b,off)[0]
 def leb(off):
  n=0;s=0
  while True:
   x=b[off];off+=1;n|=(x&127)<<s;s+=7
   if x<128:return n,off
 ns,so=u(56),u(60); strings=[]
 for i in range(ns):
  off=u(so+i*4); _,off=leb(off);end=b.index(0,off);strings.append(b[off:end].decode('utf8','replace'))
 nt,to=u(64),u(68);types=[strings[u(to+i*4)] for i in range(nt)]
 nf,fo=u(80),u(84);fields=[]
 for i in range(nf):
  c,t,n=struct.unpack_from('<HHI',b,fo+i*8);fields.append(types[c]+'.'+strings[n]+':'+types[t])
 nm,mo=u(88),u(92);methods=[]
 for i in range(nm):
  c,p,n=struct.unpack_from('<HHI',b,mo+i*8);methods.append(types[c]+'.'+strings[n])
 nc,co=u(96),u(100); result=[]
 for i in range(nc):
  cls=types[u(co+i*32)];off=u(co+i*32+24)
  if 'appinventor/ai_glauber' not in cls or not off:continue
  counts=[]
  for _ in range(4):v,off=leb(off);counts.append(v)
  for count in counts[:2]:
   idx=0
   for _ in range(count):delta,off=leb(off);flags,off=leb(off);idx+=delta
  for count in counts[2:]:
   idx=0
   for _ in range(count):
    delta,off=leb(off);flags,off=leb(off);code,off=leb(off);idx+=delta
    row={'method':methods[idx],'flags':flags,'code_offset':code,'refs':[],'instruction_offsets':[]}
    if code:
     size=u(code+12); words=struct.unpack_from('<'+'H'*size,b,code+16);j=0
     while j<size:
      w=words[j];op=w&255;ref=None
      if op==0 and w:
       typ=w>>8
       if typ==1: width=4+words[j+1]*2
       elif typ==2:width=2+words[j+1]*4
       elif typ==3:width=4+(words[j+1]*(words[j+2]|words[j+3]<<16)+1)//2
       else:width=1
      elif op in [0x18]:width=5
      elif op in [0x03,0x06,0x09,0x14,0x17,0x1b,0x24,0x25,0x26,0x2a,0x2b,0x2c] or 0x6e<=op<=0x72 or 0x74<=op<=0x78:width=3
      elif op in [0x02,0x05,0x08,0x13,0x15,0x16,0x19,0x1a,0x1c,0x1f,0x20,0x22,0x23,0x29] or 0x2d<=op<=0x3d or 0x44<=op<=0x6d or 0x90<=op<=0xaf or 0xd0<=op<=0xe2:width=2
      else:width=1
      if j+width>size:break
      row['instruction_offsets'].append(j)
      if op==0x1a:ref='string '+repr(strings[words[j+1]])
      elif op==0x1b:ref='string '+repr(strings[words[j+1]|words[j+2]<<16])
      elif 0x52<=op<=0x6d:ref='field '+fields[words[j+1]]
      elif 0x6e<=op<=0x72 or 0x74<=op<=0x78:ref='invoke '+methods[words[j+1]]
      elif op==0x12:ref='const '+str((w>>12)-16 if w>>12>7 else w>>12)
      elif op in [0x13,0x14]:ref='const '+str(words[j+1] if op==0x13 else words[j+1]|words[j+2]<<16)
      if ref:row['refs'].append([j,ref])
      j+=width
    result.append(row)
 return {'dex':str(path),'classes':[x for x in types if 'appinventor/ai_glauber' in x],'methods':result,'strings':[x for x in strings if '.jpg' in x or 'Click' in x]}
results=[parse(p) for p in ROOT.glob('classes*.dex')]
(OUT/'dex-evidence.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf8')
with (OUT/'dex-methods.txt').open('w',encoding='utf8') as f:
 for r in results:
  for m in r['methods']:
   f.write('\n'+m['method']+'\n');f.write('\n'.join(f'{o:04x} {s}' for o,s in m['refs'])+'\n')
print([(r['dex'],len(r['methods']),r['classes']) for r in results])

