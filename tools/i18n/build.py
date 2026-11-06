import json,glob,re,sys
it=json.load(open('items.json'))
T={}
bad=[]
for f in sorted(glob.glob('t/*.txt')):
  for ln in open(f,encoding='utf8'):
    ln=ln.rstrip('\n')
    if not ln.strip():continue
    p=ln.split('\t')
    i=int(p[0])
    if len(p)==2 and p[1].strip()=='-':continue
    if len(p)!=3:bad.append((f,ln[:80]));continue
    T[i]=(p[1].strip(),p[2].strip())
miss=[i for i in range(len(it)) if i not in T]
print('items',len(it),'trad',len(T),'bad',len(bad))
for b in bad[:20]:print(b)
ph=lambda s:len(re.findall(r'\{(_|\d)\}',s))
pc=[]
for i,(e,f) in T.items():
  n=it[i].count('\x01')
  if ph(e)!=n or ph(f)!=n:pc.append((i,it[i][:60],e[:60],f[:60]))
print('placeholder mismatch',len(pc))
for x in pc[:40]:print(x)
json.dump({str(k):v for k,v in T.items()},open('tr.json','w'),ensure_ascii=False)
