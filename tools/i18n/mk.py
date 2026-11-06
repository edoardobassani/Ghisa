import json,html
it=json.load(open('items.json'));T={int(k):v for k,v in json.load(open('tr.json')).items()}
import os
X=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'extra.json')))
D=[]
u=lambda s:html.unescape(s).replace('\xa0',' ')
for i,s in enumerate(it):
  if i in T:
    e,f=T[i]; a=u(s)
    if e==a and f==a and ' ' in a: continue
    D.append([a,u(e),u(f)])
D+= [list(x) for x in X]
js=json.dumps(D,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
open('i18nd.json','w').write(js);print(len(D),len(js.encode()))
