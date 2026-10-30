import asyncio;from t import *
DATA=r"""()=>{const F=q=>{const f=allF().find(x=>x.name.toLowerCase().includes(q));return f?f.id:null};
 [['Colazione','fette biscottate',30],['Colazione','marmellata',20],['Pranzo','riso basmati',80],['Pranzo','olio extra',10]].forEach(([m,q,g])=>S.meal.push({id:uid(),d:today(),m,f:F(q),g}));
 S.meal.push({id:'y1',d:hvAdd(today(),-1),m:'Cena',f:F('yogurt greco 0%'),g:125});
 S.goal=2200;S.ord={n:['scan','add','meals','tot','kc']};save()}"""
cl=lambda sel:f"()=>{{const b=document.querySelector({sel!r});if(!b)return 'MANCA '+{sel!r};b.click()}}"
steps=[DATA,"()=>{V.tab='n';V.nd=today();render();window.scrollTo(0,0);return {ring:document.querySelector('.dring b').textContent,tag:document.querySelector('.dtag').textContent,diario:document.querySelector('#dn_meals').open,pasti:document.querySelectorAll('.dml').length,blk:[...document.querySelectorAll('[data-blk]')].map(x=>x.dataset.blk).join(',')}}",("n1.png",),
 cl('[data-a=mad][data-pm=Pranzo]'),"()=>({sheet:!!document.querySelector('#fshov'),title:document.querySelector('.fsh .xph b').textContent,rec:document.querySelectorAll('.fsh [data-a=rc]').length,body:document.body.classList.contains('fsh-on')})",("n2.png",),
 "()=>{const q=document.querySelector('#fq');q.value='pollo';q.dispatchEvent(new Event('input',{bubbles:true}));return document.querySelectorAll('#fl .fr').length}",
 cl('[data-a=fsel][data-i=\"bPetto di pollo (crudo)\"]'),"()=>{const g=document.querySelector('#fg');g.value='150';return null}",
 "()=>{const l=document.querySelector('#fshl');l.scrollTop=200;document.querySelector('#fga').click();const l2=document.querySelector('#fshl');return {pasto:JSON.stringify(S.meal.slice(-1)[0].m),g:S.meal.slice(-1)[0].g,ancora:!!document.querySelector('#fshov'),scroll:l2&&l2.scrollTop,fq:V.fq}}",("n3.png",),
 cl('[data-a=fshx]'),"()=>({chiuso:!document.querySelector('#fshov'),body:document.body.classList.contains('fsh-on'),pranzo:[...document.querySelectorAll('.dml')][1].innerText})",
 # modifica alimento
 "()=>{const b=document.querySelector('.dit');b.click();return !!document.querySelector('#mig')}",
 "()=>{document.querySelector('#mig').value='40';document.querySelector('[data-a=mis]').click();return S.meal.find(x=>x.m=='Colazione').g}",
 "()=>{document.querySelector('.dit').click();const n=S.meal.length;document.querySelector('#v [data-a=md]').click();return 'eliminato:'+(n-S.meal.length)}",
 # preferiti
 cl('[data-a=mfx][data-pm=Pranzo]'),"()=>{document.querySelector('#smn2').value='Pranzo riso';document.querySelector('[data-a=sms2]').click();return S.sm.map(x=>x.name+':'+x.items.length)}",
 # copia ieri
 "()=>{const n=S.meal.length;document.querySelector('[data-a=cp]').click();return 'copiati:'+(S.meal.length-n)}",
 # sfondo ed esc
 cl('[data-a=mad][data-pm=Cena]'),"()=>{document.querySelector('#fshov').click();return 'sfondo chiude:'+!document.querySelector('#fshov')}",
 cl('[data-a=mad][data-pm=Cena]'),"()=>{document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape'}));return 'esc chiude:'+!document.querySelector('#fshov')}",
 # copia da altro giorno nel pannello
 cl('[data-a=mad][data-pm=Cena]'),cl('[data-a=cpmo]'),"()=>!!document.querySelector('[data-a=cpmg]')",
 # cambio tab chiude
 "()=>{document.querySelector('nav [data-t=h]').click();document.querySelector('nav [data-t=n]').click();return 'tab chiude:'+!document.querySelector('#fshov')}",
 # barcode pick
 "()=>{V.mm='Spuntino';bcPick(fo('bBanana')||allF()[5]);return {sheet:!!document.querySelector('#fshov'),box:!!document.querySelector('.fgi'),t:document.querySelector('.fsh .xph b').textContent}}",
 cl('[data-a=fshx]'),
 # home ogx
 "()=>{V.tab='h';render();const b=document.querySelector('[data-a=ogx]');if(!b)return 'no ogx in home';b.click();return {tab:V.tab,sheet:!!document.querySelector('#fshov')}}",
 cl('[data-a=fshx]'),
 # giorno successivo e data
 "()=>{document.querySelector('[data-a=ndp][data-d=\"-1\"]').click();return document.querySelector('.dtt').innerText}",
 # riordino menu
 "()=>{V.nd=today();render();const g=document.querySelector('[data-a=ordq]');if(g){g.click();const y=[...document.querySelectorAll('#cfm button,[data-a]')].find(b=>/Sì, sposta/.test(b.textContent));if(y)y.click()}return 'riordino barre:'+document.querySelectorAll('.ordbar').length}",
 "()=>{document.documentElement.dataset.theme='dark';V.nvm=0;V.ordu=0;V.tab='n';render();window.scrollTo(0,0)}",("n4.png",),
 "()=>{S.goal=1000;render();return document.querySelector('.dtag').textContent+' '+document.querySelector('.dring span').textContent}"]
r,e=asyncio.run(run(steps));print('\n'.join(map(str,r)));print('ERR',e)
