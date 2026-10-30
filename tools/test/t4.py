import asyncio;from t import *
st="(i)=>{V.ss={sid:'ssN',sc:'sA',fr:0,L:[],i,t0:Date.now()-60000,d:today(),done:false};V.tab='ss';render();const w=document.querySelector('.wuc');return i+':'+(w?(w.open?'APERTO ':'chiuso ')+w.querySelector('summary').textContent:'nessuno')}"
steps=[st.replace('(i)','()').replace(',i,',',i:0,').replace('return i+','return 0+')]
steps=[]
for i in range(6):
  steps.append(st.replace("(i)=>","()=>").replace(",i,",f",i:{i},").replace("return i+",f"return {i}+"))
steps+=[st.replace("(i)=>","()=>").replace(",i,",",i:2,").replace("return i+","return 'lat'+"),
 "()=>{const w=document.querySelector('.wuc');w.open=true;return V.o[w.id]}",
 "()=>{document.querySelector('.wur').click();const w=document.querySelector('.wuc');return 'dopo spunta: '+(w&&w.open)}",("w1.png",),
 "()=>{V.ss.i=3;render();V.ss.i=2;render();const w=document.querySelector('.wuc');return 'torno: '+(w&&w.open)}",
 # dopo una serie vera sparisce
 "()=>{const x=S.ex.find(e=>e.name=='Lat machine').id;S.log.push({id:uid(),d:today(),e:x,kg:55,r:8,ss:'ssN'});render();return 'dopo serie: '+!!document.querySelector('.wuc')}",
 # opzione spenta
 "()=>{S.wuOff=1;V.ss.i=0;render();return 'spento: '+!!document.querySelector('.wuc')}",
 # seduta libera con esercizio cardio in testa
 "()=>{S.wuOff=0;const c=cxAll().find(x=>x.m=='t');V.ss={sid:'ssF',sc:'',fr:1,L:[c.id,S.ex.find(e=>e.name=='Squat').id],i:1,t0:Date.now(),d:today(),done:false};S.log.push({id:uid(),d:dShift(today(),-2),e:S.ex.find(e=>e.name=='Squat').id,kg:80,r:5,ss:'o9'});render();const w=document.querySelector('.wuc');return 'libera squat: '+(w?w.querySelector('summary').textContent:'nessuno')}",
 "()=>{V.ss.i=0;render();return 'cardio ok'}"]
r,e=asyncio.run(run(steps));print('\n'.join(map(str,r)));print('ERR',e)
