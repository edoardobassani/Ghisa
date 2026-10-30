import openpyxl,json,re,sys
wb=openpyxl.load_workbook('/home/claude/dl/src/ciqual-2025_Table_Ciqual_2025_FR_2025_11_03.xlsx',read_only=True)
ws=wb.worksheets[0];R=list(ws.iter_rows(values_only=True));H=[str(h).replace('\n',' ') for h in R[0]]
def col(*pats):
  for i,h in enumerate(H):
    if all(p.lower() in h.lower() for p in pats):return i
  raise Exception(pats)
C=dict(code=col('alim_code'),name=col('alim_nom_fr'),grp=col('alim_ssgrp_nom_fr'),kcal=10,p=col('Protéines, N x facteur'),c=col('Glucides'),f=col('Lipides'),sug=col('Sucres'),fib=col('Fibres alimentaires'),
 na=col('Sodium (mg'),k=col('Potassium'),ca=col('Calcium'),mg=col('Magnésium'),fe=col('Fer (mg'),vc=col('Vitamine C'),zn=col('Zinc'),b12=col('B12'),d=col('Vitamine D (µg'))
print({k:H[v][:40] for k,v in C.items()},file=sys.stderr)
def num(v):
  if v is None:return None
  s=str(v).strip().replace(',','.')
  if s in ('-',''):return None
  if s.lower().startswith('traces'):return 0
  s=s.replace('<','').strip()
  try:return float(s)
  except:return None
out=[]
for r in R[1:]:
  d={k:(r[v] if k in('code','name','grp') else num(r[v])) for k,v in C.items()};d['code']=str(d['code']);out.append(d)
json.dump(out,open('/home/claude/dl/ciq.json','w'),ensure_ascii=False);print(len(out))
