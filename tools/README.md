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
`t11` storico, `t12` nuova Dieta, `t19` ricerca alimenti, `t20` gruppi alimenti, `t20d` verdure dei piani pronti uguali alla versione precedente (PRIMA=file), `tdb` IndexedDB e migrazione, `twipe` cancella tutto, `tbk` ripristino backup.
Il percorso del sorgente si cambia con la variabile `SRC`.

## Demo
`python3 tools/demo/make-demo.py` costruisce `tools/demo/ghisa-demo.html` (un anno di dati, non si salva)
da `demo_data.json`; con `--rigenera` ricrea anche i dati con `gen.js`. Si pubblica sull'artifact
«Ghisa – demo un anno» solo se lo chiede Edo.

## Import allenamenti (v173)
- `test/t23.py`: importa i file di esempio in `test/gxs/` (GPX Strava con battito, GPX tipo Huawei con sosta, percorso Komoot senza orari, TCX Garmin con kcal, KML gx:Track, ZIP con .gpx.gz e un .fit non supportato, file rotto), controlla doppioni, salvataggio e storico. Screenshot in `/home/claude/w/out3/`.
- Condividi › Ghisa: `share_target` in `manifest.webmanifest`; `sw.js` (cache `ghisa-v2`) mette i file nella cache `ghisa-share` e apre `./?gximp=N`; l'app li legge con `gxShared()`.

## Battito dal vivo (v174)
- `test/t24.py`: finto orologio Bluetooth (navigator.bluetooth simulato): collegamento, cardio dal vivo con pausa, ripresa dopo il riavvio, salvataggio, GPX della stessa corsa unito alla sessione, seduta in palestra con battito e kcal, ricollegamento dopo la perdita. Screenshot in `/home/claude/w/out4/`.
- Il battito va nel buffer `HRB` (localStorage `ghisa-hrb`, ultime 6 ore); cardio dal vivo in `ghisa-lc`. Campi nuovi: cd `hr{a,m}`, `hs` (≤240 valori), `hz` (minuti per zona), `src:'live'`, `st`, `el`; sedute `hr`, `hs`, `hz`, `kc`.
- Il percorso importato ora è nel campo `rte` (`rt` è la valutazione dei programmi cardio); `hrBoot()` sposta i vecchi `rt` con coordinate.

## v176
- `test/t25.py`: duplica scheda (nome «(copia)», apre la modifica, Annulla) e storico cardio con «Mostra altre» a blocchi di 120.

## Google Drive (v177)
- Nessuna chiave nel codice: ogni utente crea il suo ID client OAuth (guida dentro l'app, foglio «Backup e dati») e lo incolla; resta in localStorage `gymbo-drv` (`cid`, `on`, `em`, `last`, `svd`, `phs`). Token in `gymbo-drt` (circa 1 ora).
- Su Drive (appDataFolder): `d-AAAA-MM-GG.json` (dati del giorno, appProperties `svd`,`dev`; tenuti 10) e `p-<id>.json` (una per foto).
- Salvataggio 5 s dopo ogni `save()` o cambio foto, se il permesso è valido; altrimenti barra in Home e «Salva ora». Al collegamento confronta `svd` e chiede quale versione tenere; prima di ripristinare copia i dati in IndexedDB chiave `prev`.
- `test/t26.py`: Drive finto (route di Playwright) e Google Identity finto: chiave, collegamento, salvataggio automatico, foto cancellata, permesso scaduto, secondo dispositivo con conflitto.
