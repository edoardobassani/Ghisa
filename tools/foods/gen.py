import json,re
C={d['code']:d for d in json.load(open('/home/claude/dl/ciq.json'))}
U={d['code']:d for d in json.load(open('/home/claude/dl/usda.json'))}
def crea(code):
  M={'Energia (kcal)':'kcal','Proteine (g)':'p','Lipidi (g)':'f','Carboidrati disponibili (g)':'c','Fibra totale (g)':'fib','Zuccheri solubili (g)':'sug','Sodio (mg)':'na','Potassio (mg)':'k','Calcio (mg)':'ca','Magnesio (mg)':'mg','Ferro (mg)':'fe','Vitamina C (mg)':'vc','Zinco (mg)':'zn'}
  d={}
  for l in open('/home/claude/dl/mm/data/food_details/'+code):
    a=l.rstrip('\n').split('\t')
    if a[0] in M:
      try:d[M[a[0]]]=float(a[1])
      except:pass
  nm=[l.split('\t')[1].strip() for l in open('/home/claude/dl/mm/data/name_foodID_correspondence.tsv') if l.startswith(code+'\t')][0]
  d['name']=nm;return d
def r(v,nd=1):
  if v is None:return ''
  v=round(v,nd);return ('%g'%v)
rows=[];syn={};miss=[]
for l in open('/home/claude/dl/sel.txt'):
  l=l.rstrip('\n')
  if not l or l.startswith('#'):continue
  name,src,cat,pz,sy=l.split('|')
  t,code=src.split(':')
  d=C[code] if t=='C' else U[code] if t=='U' else crea(code)
  if d.get('kcal') is None:miss.append(name)
  orig=re.sub(r'\s+',' ',d['name']).strip()
  vals=[r(d.get('kcal'),0),r(d.get('p')),r(d.get('c')),r(d.get('f')),r(d.get('fib')),r(d.get('sug'))]
  mic=[r(d.get(k),2) for k in ['na','k','ca','mg','fe','vc','zn','b12','d']]
  rows.append('|'.join([name,t+code,orig.replace('|','/').replace(';',','),*vals,cat,*mic,pz]))
  for s in [x.strip() for x in sy.split(',') if x.strip()]:syn.setdefault(s,[]).append(name)
print('mancano kcal:',miss)
open('/home/claude/dl/rows.txt','w').write(';'.join(rows));json.dump(syn,open('/home/claude/dl/syn.json','w'),ensure_ascii=False)
print(len(rows),'righe;',len(syn),'sinonimi');print(rows[0]);print(rows[44])
