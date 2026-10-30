# Strumenti di lavoro per Ghisa

Servono a Claude (e a chi lavora sull'app) per modificare, provare e pubblicare Ghisa.
Non fanno parte dell'app: GitHub Pages li pubblica ma l'app non li usa.

## Ripartire da zero in una chat nuova
1. Clonare il repo in `/home/claude/ghisa`.
2. `python3 tools/estrai-sorgente.py` ricrea il sorgente in `/home/claude/w/tracker-palestra.html`
   (in alternativa: leggere l'artifact «Ghisa» con l'azione `read` dello strumento Artifact).
3. Dopo ogni modifica:
   - `tools/check.sh` controlla la sintassi dell'ultimo `<script>` con `node --check`;
   - i test in `tools/test/` (Playwright + Chromium): `cd tools/test && python3 t5.py` prova tutte le sezioni;
   - `tools/sync-pwa.sh "messaggio"` rigenera `index.html` (manifest, icone, service worker) e fa commit e push;
   - ripubblicare l'artifact sullo stesso URL.

## Test
`t.py` è il banco di prova comune (dati di esempio + passi). Gli altri file provano una funzione ciascuno:
`t1` guida esercizi, `t2` esercizi palestra, `t3` grammi alimenti (vecchio flusso), `t4` riscaldamento,
`t5` tutte le sezioni, `t6` barra seduta, `t7` sesso fuori dalla dieta, `t8` modelli scheda, `t9` programmi,
`t11` storico, `t12` nuova Dieta, `tdb` IndexedDB e migrazione, `twipe` cancella tutto, `tbk` ripristino backup.
Il percorso del sorgente si cambia con la variabile `SRC`.

## Demo
`python3 tools/demo/make-demo.py` costruisce `tools/demo/ghisa-demo.html` (un anno di dati, non si salva)
da `demo_data.json`; con `--rigenera` ricrea anche i dati con `gen.js`. Si pubblica sull'artifact
«Ghisa – demo un anno» solo se lo chiede Edo.
