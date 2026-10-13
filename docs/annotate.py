import json,re,pathlib,ast
import struct
p=pathlib.Path(__file__).parent
d=json.loads((p/'dex-evidence.json').read_text(encoding='utf8'))[0]
r=next(m for m in d['methods'] if m['method'].endswith('Screen1;.<clinit>'))['refs']
lits={}
code=next(m for m in d['methods'] if m['method'].endswith('Screen1;.<clinit>'))['code_offset']
b=pathlib.Path(d['dex']).read_bytes(); count=struct.unpack_from('<I',b,code+12)[0];w=struct.unpack_from('<'+'H'*count,b,code+16)
# Numeric make calls consume constant registers; this initializer is linear.
reg={}; makes={}
for i in next(m for m in d['methods'] if m['method'].endswith('Screen1;.<clinit>'))['instruction_offsets']:
 op=w[i]&255;a=w[i]>>8
 if op==0x12:reg[a&15]=((a>>4)-16 if a>>4>7 else a>>4)
 if op==0x13 and i+1<count:reg[a]=w[i+1]-65536 if w[i+1]>32767 else w[i+1]
 if op==0x14 and i+2<count:reg[a]=w[i+1]|w[i+2]<<16
 if op==0x15 and i+1<count:reg[a]=w[i+1]<<16
 # Only decode at verified instruction offsets, rather than operands that resemble opcodes.
 if any(off==i and 'IntNum;.make' in s for off,s in r):
  args=w[i+2];first=args&15;makes[i]=reg.get(first)
for i,(off,s) in enumerate(r):
 if 'field ' not in s or '.Lit' not in s:continue
 name=s.split('.Lit')[1].split(':')[0]
 if ':Lgnu/mapping/SimpleSymbol;' in s and i>=3 and 'readResolve' in r[i-1][1] and r[i-3][1].startswith('string '):lits[name]=ast.literal_eval(r[i-3][1][7:])
 if ':Lgnu/math/IntNum;' in s and i>=2 and 'IntNum;.make' in r[i-1][1] and r[i-2][1].startswith('const '):lits[name]=int(r[i-2][1][6:])
 if ':Lgnu/math/IntNum;' in s and name not in lits and i>=1 and 'IntNum;.make' in r[i-1][1] and makes.get(r[i-1][0]) is not None:lits[name]=makes[r[i-1][0]]
(p/'literal-map.json').write_text(json.dumps(lits,ensure_ascii=False,indent=2),encoding='utf8')
with (p/'annotated-methods.txt').open('w',encoding='utf8') as f:
 for m in d['methods']:
  if not ('Screen1;.' in m['method']) or m['method'].endswith('<clinit>'):continue
  f.write('\n'+m['method']+'\n')
  for off,s in m['refs']:
   match=re.search(r'\.Lit(\d+):',s)
   if match and match[1] in lits:s+=' = '+str(lits[match[1]])
   f.write(f'{off:04x} {s}\n')
print('mapped',len(lits),{k:lits.get(k) for k in ['4','46','59','66']})
voice=next(m for m in d['methods'] if m['method'].endswith('Screen1;.ReconhecedorDeVoz1$AfterGettingText'))['refs']
aliases={};last=None
for off,s in voice:
 if s.startswith('string '):
  value=ast.literal_eval(s[7:])
  if value not in ['The variable ',' is not bound in the current context','Unbound Variable','=']:last=value
 if 'IntNum;' in s and last:
  key=re.search(r'\.Lit(\d+):',s)[1];aliases[last]=lits.get(key);last=None
(p/'voice-aliases.json').write_text(json.dumps(aliases,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(aliases,ensure_ascii=False))
