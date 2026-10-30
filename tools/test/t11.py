import asyncio;from t import *
steps=["""()=>{const id=n=>S.ex.find(e=>e.name==n).id;xbAdd(['Plank (secondi)']);const d=dShift(today(),-1);S.ses.push({id:'h1',d,sc:'sA',t0:Date.now()-3600e3,t1:Date.now()-60e3});
 const L=[['Panca piana bilanciere',70,8],['Panca piana bilanciere',75,6],['Panca piana bilanciere',80,4],['Croci con manubri',16,12],['Croci con manubri',16,10],['Croci con manubri',16,9],['Piegamenti',0,15],['Piegamenti',0,12],['Lat machine',55,10],['Lat machine',55,10],['Plank (secondi)',0,30],['Plank (secondi)',0,30]];
 L.forEach(([n,kg,r])=>S.log.push({id:uid(),d,e:id(n),kg,r,ss:'h1'}));save();document.documentElement.dataset.theme='dark';V.tab='w';V.wv='h';render();
 const det=document.querySelector('details.hsx');if(det)det.open=true;return [...document.querySelectorAll('details.hsx')].length}""",
 "()=>[...document.querySelectorAll('details.hsx')][0].innerText",("h1.png",)]
r,e=asyncio.run(run(steps));print('\n'.join(map(str,r)));print('ERR',e)
