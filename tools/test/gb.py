"""Ambiente comune dei test di Gym-Bo.

Ogni test fa `import gb` e apre la pagina con `pg.goto(gb.URL)`.
- SRC: il file da provare (variabile d'ambiente SRC; se manca, index.html del repo).
- Serve una cartella temporanea (gb.D) con la pagina, pdf.js e i file di prova (pdft, gxs, hi),
  su una porta libera: i test possono girare uno dopo l'altro senza scontrarsi.
- La cartella di lavoro diventa gb.D, così i percorsi relativi ('pdft/x.pdf') funzionano
  e le schermate non finiscono nel repo. gb.O è la cartella delle schermate.
"""
import os, sys, shutil, socket, subprocess, tempfile, time, atexit

T = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(T))
SRC = os.path.abspath(os.environ.get('SRC') or os.path.join(REPO, 'index.html'))
D = tempfile.mkdtemp(prefix='gymbo-test-')
O = os.environ.get('OUT') or os.path.join(D, 'u')
os.makedirs(O, exist_ok=True)
if not O.endswith('/'):
    O += '/'

shutil.copy(SRC, os.path.join(D, 'app.html'))
for f in ('pdf.min.mjs', 'pdf.worker.min.mjs'):
    for base in (os.path.dirname(SRC), REPO):
        if os.path.exists(os.path.join(base, f)):
            shutil.copy(os.path.join(base, f), os.path.join(D, f))
            break
for d in ('pdft', 'gxs', 'hi'):
    os.symlink(os.path.join(T, d), os.path.join(D, d))
for f in ('demo_data.json',):
    p = os.path.join(REPO, 'tools', 'demo', f)
    if os.path.exists(p):
        os.makedirs(os.path.join(D, 'demo'), exist_ok=True)
        shutil.copy(p, os.path.join(D, 'demo', f))


def _port():
    s = socket.socket()
    s.bind(('127.0.0.1', 0))
    p = s.getsockname()[1]
    s.close()
    return p


PORT = _port()
BASE = f'http://localhost:{PORT}/'  # localhost: Google Drive nell'app funziona solo da qui, da file:// o da github.io
URL = BASE + 'app.html'
FILE = os.path.join(D, 'app.html')
_srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT), '--bind', '127.0.0.1'],
                        cwd=D, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
for _ in range(50):
    try:
        socket.create_connection(('127.0.0.1', PORT), timeout=0.2).close()
        break
    except OSError:
        time.sleep(0.1)


def _stop():
    _srv.terminate()
    shutil.rmtree(D, ignore_errors=True) if not os.environ.get('KEEP') else None


atexit.register(_stop)
os.chdir(D)


def skip(why):
    """Test che non si può eseguire in questo ambiente: lo dice e termina senza errore."""
    print('SKIP:', why)
    sys.exit(0)
