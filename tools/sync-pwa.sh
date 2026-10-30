#!/bin/bash
# Rigenera index.html della PWA da tracker-palestra.html, poi commit e push.
# Uso: tools/sync-pwa.sh "messaggio"   (SRC=percorso del sorgente, predefinito /home/claude/w/tracker-palestra.html)
set -e
SRC=${SRC:-/home/claude/w/tracker-palestra.html}; REPO=${REPO:-$(cd "$(dirname "$0")/.." && pwd)}
python3 - "$SRC" "$REPO/index.html" <<'P'
import sys
s=open(sys.argv[1]).read()
head='<link rel="manifest" href="manifest.webmanifest">\n<meta name="theme-color" content="#1c262b">\n<meta name="mobile-web-app-capable" content="yes">\n<meta name="apple-mobile-web-app-capable" content="yes">\n<meta name="apple-mobile-web-app-title" content="Ghisa">\n<link rel="apple-touch-icon" href="icon-192.png">\n<link rel="icon" href="icon-192.png">\n'
sw="if('serviceWorker' in navigator&&location.protocol.startsWith('http'))addEventListener('load',()=>navigator.serviceWorker.register('sw.js').catch(()=>{}));\n"
anchor='</title>\n';assert s.count(anchor)==1;s=s.replace(anchor,anchor+head)
a2='dataBoot().then(';assert s.count(a2)==1;s=s.replace(a2,sw+a2)
open(sys.argv[2],'w').write(s)
P
cd $REPO && git add -A && git commit -q -m "$1" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01J1sGSPronNQehVaLG4kM1G" && git push -q origin main && git log --oneline -1
