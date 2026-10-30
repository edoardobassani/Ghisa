import asyncio;from t import *
op="()=>{V.tab='o';render();const d=[...document.querySelectorAll('details')].find(x=>/Obiettivi dieta/.test(x.querySelector('summary').textContent));d.open=true;return {tds:!!document.querySelector('#tds'),warn:/Indica il sesso in alto/.test(d.innerHTML),f:(d.querySelector('.obt b')||{}).textContent,sxCard:!!document.querySelector('[data-a=sxb]')}}"
steps=["()=>{S.pf={age:38,act:1.55};S.h=178;S.wt=[{id:'w1',d:today(),kg:82}];save()}",op,
 "()=>{document.querySelector('[data-a=sxb][data-v=f]').click();return S.pf.sx}",op,
 "()=>{const t=document.querySelector('#tda');t.value='40';t.dispatchEvent(new Event('change',{bubbles:true}));return S.pf.age}",op,("x1.png",)]
r,e=asyncio.run(run(steps));print('\n'.join(map(str,r)));print('ERR',e)
