import asyncio;from t import *
st=lambda i:f"()=>{{const sc=S.sch[0];const p=S.ex.find(e=>e.name=='Panca piana bilanciere').id;sc.t[p]={{s:3,r:8,sets:[{{r:8}}]}};V.ss={{sid:'ssN',sc:'sA',fr:0,L:[],i:{i},t0:Date.now()-60000,d:today(),done:false}};V.tab='ss';render();window.scrollTo(0,0)}}"
info="()=>({bar:[...document.querySelectorAll('.ssb button')].map(b=>b.textContent),inl:[...document.querySelectorAll('#v [data-a=ssa]:not(.ssab)')].map(b=>b.textContent),fx:!!document.querySelector('.hint.fx'),fxi:!!document.querySelector('[data-a=fxi]'),ssq:!!document.querySelector('.ssq')})"
steps=[st(0),info,"()=>{document.querySelector('[data-a=fxi]').click();return document.querySelector('#cfm h2').textContent}",("q1.png",),
 "()=>{document.querySelector('#cfm [data-a=cfx]').click();return 'chiusa:'+document.querySelector('#cfm').hidden}",
 "()=>{document.querySelector('.ssab').click();return 'serie:'+S.log.filter(l=>l.ss=='ssN').length}",info,
 "()=>{document.querySelector('.ssab').click();document.querySelector('.ssab').click();return 'serie:'+S.log.filter(l=>l.ss=='ssN').length}",info,
 "()=>{document.querySelector('#v [data-a=ssa]').click();return 'extra:'+S.log.filter(l=>l.ss=='ssN').length}",
 st(2),info,("q2.png",),"()=>{document.querySelector('.ssab').click();return 'serie lat:'+S.log.filter(l=>l.ss=='ssN').length}",
 "()=>{document.querySelector('.ssnv:last-child').click();return 'avanti -> i='+V.ss.i}",
 st(5),info,
 "()=>{V.ss={sid:'ssF',sc:'',fr:1,L:[S.ex.find(e=>e.name=='Squat').id],i:0,t0:Date.now(),d:today(),done:false};render();return null}",info,
 "()=>{document.querySelector('.ssab').click();return 'libera serie:'+S.log.filter(l=>l.ss=='ssF').length}",
 "()=>{V.ss=null;V.tab='s';render();return 'schede ok'}"]
r,e=asyncio.run(run(steps));print('\n'.join(map(str,r)));print('ERR',e)
