#!/usr/bin/env python3
"""Ricrea il sorgente dell'app (tracker-palestra.html) dall'index.html della PWA,
togliendo le righe aggiunte da sync-pwa.sh. Uso: python3 tools/estrai-sorgente.py [destinazione]"""
import os,sys
R=os.path.dirname(os.path.abspath(__file__))
s=open(os.path.join(R,'..','index.html')).read()
head='<link rel="manifest" href="manifest.webmanifest">\n<meta name="theme-color" content="#1c262b">\n<meta name="mobile-web-app-capable" content="yes">\n<meta name="apple-mobile-web-app-capable" content="yes">\n<meta name="apple-mobile-web-app-title" content="Gym-Bo">\n<link rel="apple-touch-icon" href="icon-192.png">\n<link rel="icon" href="icon-192.png">\n'
sw="if('serviceWorker' in navigator&&location.protocol.startsWith('http'))addEventListener('load',()=>navigator.serviceWorker.register('sw.js').catch(()=>{}));\n"
assert s.count(head)==1 and s.count(sw)==1,'index.html non riconosciuto'
out=sys.argv[1] if len(sys.argv)>1 else '/home/claude/w/tracker-palestra.html'
os.makedirs(os.path.dirname(out),exist_ok=True)
open(out,'w').write(s.replace(head,'').replace(sw,''));print('Sorgente scritto in',out)
