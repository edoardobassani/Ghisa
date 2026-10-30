import asyncio;from t import *
steps=["()=>{V.tab='n';V.mm='Spuntino';V.o.dn_add=true;V.fq='yogurt';render();document.querySelector('#fq').scrollIntoView({block:'start'})}",
 "()=>{document.querySelector('[data-a=fsel][data-i=\"bYogurt greco 0%\"]').click()}",
 "()=>({box:!!document.querySelector('.fgi'),g:document.querySelector('#fg').value,focus:document.activeElement.id,k:document.querySelector('#fgk').textContent,chips:document.querySelectorAll('[data-a=fpz]').length})",
 ("f1.png",),
 "()=>{document.querySelector('#fg').value='200';document.querySelector('#fg').dispatchEvent(new Event('input',{bubbles:true}));return document.querySelector('#fgk').textContent}",
 "()=>{document.querySelector('[data-a=fpz]').click();return document.querySelector('#fg').value+'|'+document.querySelector('#fgk').textContent}",
 "()=>{const m=document.querySelector('#mm');m.value='Pranzo';m.dispatchEvent(new Event('change',{bubbles:true}));return document.querySelector('#fga').textContent}",
 "()=>{document.querySelector('#fga').click();return JSON.stringify({meal:S.meal.slice(-1)[0],sel:V.sel,fq:V.fq,box:!!document.querySelector('.fgi'),undo:document.querySelector('#undo').className,txt:document.querySelector('#undo span').textContent})}",
 ("f2.png",),
 "click:#undo button","()=>'dopo annulla pasti:'+S.meal.length",
 # grammi vuoti
 "()=>{document.querySelector('[data-a=fsel][data-i=\"bYogurt bianco intero\"]').click();document.querySelector('#fg').value='';document.querySelector('#fga').click();return 'vuoto -> pasti:'+S.meal.length+' box:'+!!document.querySelector('.fgi')}",
 # invio
 "()=>{const g=document.querySelector('#fg');g.value='150';g.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',bubbles:true}));return 'invio -> '+JSON.stringify(S.meal.slice(-1)[0])}",
 # tocco di nuovo chiude, annulla chiude
 "()=>{document.querySelector('[data-a=fsel][data-i=\"bYogurt caprino\"]').click();const a=!!document.querySelector('.fgi');document.querySelector('[data-a=fsx]').click();return 'apri '+a+' annulla '+!document.querySelector('.fgi')}",
 # recenti
 "()=>{const b=document.querySelector('[data-a=rc]');if(!b)return 'no recenti';b.click();return 'recente -> '+V.sel+' box '+!!document.querySelector('.fgi')+' g '+document.querySelector('#fg').value}",
 # ricerca chiude
 "()=>{const q=document.querySelector('#fq');q.value='pollo';q.dispatchEvent(new Event('input',{bubbles:true}));return 'cerca -> sel '+V.sel+' box '+!!document.querySelector('.fgi')}",
 "()=>{V.tab='h';render();return 'home ok'}"]
r,e=asyncio.run(run(steps));print('\n'.join(map(str,r)));print('ERR',e)
