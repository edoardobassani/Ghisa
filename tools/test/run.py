#!/usr/bin/env python3
"""Esegue tutti i test di Gym-Bo e dice quali passano.

Uso:  python3 tools/test/run.py [nomi...] [-j N] [-v]
      SRC=/percorso/del/file.html python3 tools/test/run.py     (predefinito: index.html del repo)

Un test FALLISCE se: esce con errore, stampa un Traceback o «EXC» (eccezione in una pagina),
riporta errori JavaScript non vuoti («errori: [...]», «ERR [...]», «errs ... [...]»), oppure stampa «FAIL».
«SKIP:» lo segna come saltato. Tutto il resto dell'uscita sono osservazioni da leggere con -v.
"""
import os, re, subprocess, sys, time, glob
from concurrent.futures import ThreadPoolExecutor

T = os.path.dirname(os.path.abspath(__file__))
args = [a for a in sys.argv[1:] if not a.startswith('-')]
J = 4
if '-j' in sys.argv:
    J = int(sys.argv[sys.argv.index('-j') + 1]); args = [a for a in args if a != str(J)]
V = '-v' in sys.argv
NOT_TESTS = {'t.py', 'gb.py', 'run.py'}
files = sorted(f for f in glob.glob(os.path.join(T, '*.py')) if os.path.basename(f) not in NOT_TESTS
               and re.match(r'(t\d|u\d|tbk|tdb|twipe|qa-)', os.path.basename(f)))
if args:
    files = [f for f in files if any(os.path.basename(f).startswith(a if a.endswith('.py') else a + '.') or os.path.basename(f) == a for a in args)]
key = lambda f: (re.sub(r'\d+', lambda m: m.group().zfill(4), os.path.basename(f)))
files.sort(key=key)

BAD = [
    (re.compile(r'Traceback \(most recent call last\)'), 'eccezione Python'),
    (re.compile(r"(?:^|[\s'\"])EXC "), 'eccezione nella pagina'),
    (re.compile(r'errori:\s*\[(?!\])'), 'errori JavaScript'),
    (re.compile(r'ERR \[(?!\])'), 'errori JavaScript'),
    (re.compile(r"errs'?\]?:?\s*\[(?!\])"), 'errori JavaScript'),
    (re.compile(r'\bFAIL\b'), 'verifica fallita'),
]


def one(f):
    t0 = time.time()
    try:
        p = subprocess.run([sys.executable, f], capture_output=True, text=True, timeout=300, env=os.environ.copy())
        out = p.stdout + p.stderr; code = p.returncode
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or b'').decode() if isinstance(e.stdout, bytes) else (e.stdout or ''); code = 'timeout'
    out = '\n'.join(l for l in out.splitlines() if not re.search(r'agent-proxy|fonts\.googleapis|Allowed domains|For details: curl', l))
    why = []
    if code == 'timeout': why.append('oltre 5 minuti')
    elif code: why.append(f'uscita {code}')
    for rx, w in BAD:
        if rx.search(out) and w not in why: why.append(w)
    st = 'SKIP' if 'SKIP:' in out and not why else ('FAIL' if why else 'ok')
    return os.path.basename(f), st, why, out, time.time() - t0


res = []
with ThreadPoolExecutor(J) as ex:
    for name, st, why, out, dt in ex.map(one, files):
        res.append((name, st, why, out))
        print(f'{st:4} {name:12} {dt:5.1f}s  {"; ".join(why)}', flush=True)
        if V or st == 'FAIL':
            print('     ' + '\n     '.join(out.strip().splitlines()[-12:]))
n = {k: sum(1 for r in res if r[1] == k) for k in ('ok', 'FAIL', 'SKIP')}
print(f"\n{n['ok']} ok, {n['FAIL']} falliti, {n['SKIP']} saltati su {len(res)}")
sys.exit(1 if n['FAIL'] else 0)
