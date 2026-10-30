#!/bin/bash
# controllo sintassi dell'ultimo <script>
python3 -c "
s=open(''+__import__('os').environ.get('SRC','/home/claude/w/tracker-palestra.html')+'').read();i=s.rfind('<script>');j=s.rfind('</script>');open('/tmp/ghisa-last.js','w').write(s[i+8:j])"
node --check /tmp/ghisa-last.js && echo SINTASSI OK
