import asyncio;from t import *
steps=["()=>{const out=[];for(const t of ['h','w','c','n','pp','s','e','g','p','o','r','x']){try{V.tab=t;render()}catch(e){out.push(t+':'+e.message)}}V.tab='e';V.ek='c';render();V.ek='p';render();document.documentElement.dataset.theme='dark';render();return out.length?out:'tutte le sezioni ok'}"]
r,e=asyncio.run(run(steps));print(r,'ERR',e)
