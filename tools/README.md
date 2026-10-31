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

## Massimali e programmi a blocchi (v180)
- `S.rm[id]={kg,src:'t'|'m',d,h:[]}` (1RM scritto o testato); senza voce il 1RM è stimato (`rmEst`: miglior Epley ≤12 rip., ultimi 120 giorni). `S.tmp` = TM in % (default 90).
- `S.bp` = programma attivo: `B` blocchi `{n,w}`, `D` giorni `{n,it:[{e,ty:'p'|'i'|'t'|'k',W:[[set]]]}]}` con set `{r,p|rir|rel|kg,am}`; runtime `wk, ws, cyc, tm, amf, sch, pl0`. I giorni del programma settimanale valgono `'bp'` (`bpToday`). `bpGen` scrive gli obiettivi (con `bp:1`) nelle schede; `bpTick` (in `render`) fa avanzare la settimana quando tutte le sedute sono concluse dopo `ws`.
- `S.bpl` = programmi salvati dal costruttore. Pronti: `BPM` (5/3/1+BBB, lineare 12 sett., DUP 8 sett.).
- `test/t27.py` (massimali, avvio, schede, Home, seduta, costruttore) e `test/t28.py` (5/3/1: AMRAP, fine ciclo, modifica, termina).

## Demo (v185)
- `demo/gen.js` simula anche: programma «Forza lineare a blocchi» da settembre (lun/mer/ven, settimana 9), 1RM testato dello stacco, programma cardio «Fondo e VO2max», uscite GPX con percorso e due corse dal vivo con battito. Pagina: `demo/gymbo-demo.html`.
- `test/qa-demo.py`: apre ogni sezione della demo e segnala errori, testo «undefined/NaN» e pagine più larghe dello schermo.
- `test/t29.py`: riapertura sull’ultima schermata (localStorage `gymbo-view`, 12 ore) con campi e scorrimento; stato vecchio o rotto → Home; la seduta in corso ha la precedenza.

## v190 – banca dati alimenti ampliata
82 alimenti nuovi (1007 in totale). Priorità fonti: CREA 2019 → Ciqual 2025 (ANSES, Licence Ouverte 2.0) → USDA FoodData Central SR Legacy (CC0).
File sorgente scaricati dalla release `sources-2026-10-05` di github.com/raddatzk/sous (ridistribuiti invariati); valori Ciqual 2025 confrontati con Ciqual 2020: 63/67 identici, 4 revisioni.
`tools/foods/selezione-v190.txt` = elenco nome app | fonte:codice | categoria | porzione | sinonimi. Script: ciq.py, usda.py, gen.py.

## v191 – import da PDF (palestra, dieta, cardio)
pdf.js 6.2.108 legacy build (Mozilla, Apache 2.0, vedi LICENSE-pdfjs.txt) in `pdf.min.mjs` + `pdf.worker.min.mjs`, caricato solo quando si apre un PDF.
PDF → griglia (colonne dall'intestazione) → stessi parser di Excel; se non ci sono tabelle, parser del testo libero (imTxt, ipTxt, ccTxt/ccParse).
Cardio: nuova importazione sedute (PDF/Excel/CSV) → schede cardio a blocchi, opzionale nel programma settimanale. Test: t32–t34, PDF di prova in test/pdft.

## v192–v193 – piano del nutrizionista (formato Nutrium)
- v192: `ipDay` legge «Giorno N» come N-esimo giorno della settimana (prima «Giorno 1» diventava giovedì).
- v193: `nuTxt(lines)` riconosce il formato Nutrium (pasti «07:00 COLAZIONE», sottosezioni Antipasto/Primo/Secondo, punti elenco, alternative separate da «○», da «o» seguito da una quantità o da uno spazio largo) e produce una griglia con le colonne in più `Gruppo` (stesso punto elenco = porzione a scelta) e `Porzione` («5 fette»). `ipPrep` la prova prima di `ipTxt`.
- `nuItem` legge quantità e unità, «da 150g», grammi tra parentesi, e tiene la prima voce di «carne bianca o pesce magro» (il resto va nelle note). `ipUnitG` converte le unità con le porzioni di `PZ` o la tabella `NUD`; `IPGEN` abbina le voci generiche (frutta, verdura, carne bianca, legumi…) a un alimento rappresentativo da confermare (≈).
- Nel piano la voce attiva è la prima; tutte le scelte sono in `al:[{f,g}]` della voce di `S.mpw`.
- `test/t35.py`: importa `pdft/nutrium_circ.pdf`, `nutrium_o.pdf`, `nutrium_gap.pdf` (stesso piano con «○» scritto, «o» e cerchio disegnato; si rigenerano con `pdft/mk-nutrium.py`) e il vecchio `diet_text.pdf`.

## v194 – piano pronto «A scelta, stile nutrizionista»
Nuovo elemento di `DPM` (id `sce`, onnivoro, equilibrato) ricavato dallo schema Nutrium di Edo, senza nomi: ogni giorno un carboidrato + una proteina dalle scelte equivalenti, verdura libera, olio misurato, due spuntini uniti in Spuntino. Generato da `test/pdft/mk-dpm-sce.py`. Prova: `test/t36.py`.

## v195 – alimenti equivalenti
`eqOf(f,g,N)`: stessa famiglia (`EQG`: proteici, carboidrati, grassi; altrimenti stessa categoria), ripartizione delle kcal tra P/C/G simile (distanza < 0,3), grammi ricalcolati per le stesse kcal. Esclude farine e ingredienti, sciroppati e canditi, secchi se l'originale non lo è, crudo↔cotto, piatti pronti; penalizza nomi lunghi da banca dati e categorie diverse, favorisce `CMN`. Nel pannello «+ Alimento» del piano pasti: menu chiuso «Vedi equivalenti» (`#ppeq`, `ppEqH`), si aggiorna con i grammi; «Usa» (`ppeu`) sostituisce l'alimento scelto. Prova: `test/t37.py`.

## v196 – tasto ⇄ sulle voci del piano
Ogni voce singola del piano (non i preferiti) ha ⇄ (`mpSwB`), con il numero di scelte se ha `al`; c'è anche in Home nel prossimo pasto. Il foglio (`mpSwOpen`, `#cfm.sht`) mostra «Alternative del piano» (`al`, la prima è l'originale) ed «Equivalenti per macro» (`eqOf`), con kcal e differenza. Tocco = scambia (`mpsw`, con Annulla); «+ ⇄» (`mpsa`) aggiunge l'equivalente ad `al` senza scambiare. «Solo [giorno]» o «Tutti i giorni (n)»: le voci della settimana nello stesso pasto con stesso alimento, grammi e alternative (`mpSwSame`). Le voci cambiate mostrano «scambiato» (`mpSwd`). Se la settimana è ereditata viene materializzata in `S.mpw` al primo scambio. Prova: `test/t38.py`.

## v197 – scelta alimento compatta nel piano pasti
Dopo la scelta il pannello «+ Alimento» mostra solo il riquadro `.pps` (nome, kcal e macro per 100 g) al posto di ricerca ed elenco; «Cambia» (`ppch`) svuota la scelta e riapre la ricerca con la stessa parola. Prova in `test/t37.py`.

## v198 – Svuota la settimana
Tasto «Svuota la settimana» (`ppsv0` apre la conferma, `ppsv` svuota, con Annulla) accanto a «Svuota il giorno». La settimana vuota resta in `S.mpw` e viene segnata in `S.mpe`, così `mpSrc` la fa ereditare alle settimane dopo senza piano proprio. La casella `#ppsvf` toglie anche le settimane successive già pianificate. Toglie `S.dpa` se riguarda le settimane svuotate. Prova: `test/t39.py`.

## v199 – codice a barre: fotocamera sempre visibile
Il riquadro `.bcf` non viene più nascosto: in `bcStart` i messaggi (`m`) non toccano il video; senza fotocamera o senza BarcodeDetector la cornice prende la classe `off` e mostra il motivo in `#bcph`. Dopo una lettura (`bcGot`) la fotocamera resta accesa in pausa (`BC.pause`) e compare «Scansiona di nuovo» (`#bcr`, riparte con `BC.tick`). `bcClose` spegne tutto. Prova: `test/t40.py` (fotocamera finta di Chromium, BarcodeDetector e Open Food Facts simulati).

## v200 – foglio ⇄ con tasti separati
Nel foglio di scambio le righe (`.swr`, info in `.swi`) non sono più toccabili: ogni riga ha «⇄ Scambia» (`mpsw`) e, per gli equivalenti, «+ Salva» (`mpsa`, aggiunge ad `al`) nella colonna `.swbx`; la voce attuale mostra «✓ In uso». Attenzione: `.swb` è già usato per un altro tasto.

## v201 – equivalenti per sottofamiglia
`eqSub` assegna una sottofamiglia dal nome (`EQS`: primo, patate, pane, snack, colaz, dolce, ripiena, salumi, cbianca, lfresco, vprot, oli, grassi, semi; altrimenti la categoria). `eqOf` propone prima la stessa sottofamiglia (macro fino a 0,6 di distanza), poi le affini di `EQA` (fino a 0,2, penalità 0,2); premia `CMN`, gli alimenti base `EQB` e quelli usati di recente; una sola variante per tipo (`stem`); scarta grammi oltre 3× (tranne verdure).

## v202 – ⇄ nel diario
Ogni voce del diario Dieta ha ⇄ (`.dirw`, `mpso` con `data-k="d"`): stesso foglio del piano (`V.sw.k=="d"`, niente «tutti i giorni»), scambia `f`/`g` della voce in `S.meal` e tiene le scelte in `al`. Quando il piano viene segnato nel diario (`ogm`, «Segna tutti», «Applica al diario») le voci portano anche `al`. Prova: `test/t41.py`.

## v203 – codice a barre: grammi e pasto subito
Nel lettore (`bcGot`) la scheda chiede grammi e pasto (`bcQty`: ultimi grammi usati o prima porzione, pasto da `V.fsh`/`V.mm`/fascia oraria, giorno del diario aperto o oggi). Prodotto nuovo: «Salva e aggiungi al diario» (salva l’limento e aggiunge con `bcAdd`) o «Salva soltanto» (comportamento di prima). Prodotto già salvato: scheda con «Aggiungi al diario» e «Apri nella ricerca alimenti». Prova: `test/t42.py`.

## v204 – lista della spesa per reparto
`vsp` raggruppa per reparto del supermercato (`SPR`, `spGroups`: frutta e verdura con le patate, pane pasta e cereali, carne e pesce, salumi, latticini e uova, legumi, dispensa, altro), con conteggio «presi», barra di avanzamento, «Nascondi presi» (`V.psh`) e i presi in fondo al reparto. Voci aggiunte a mano in `S.spx` ({id,t,on}; `spxa`, `spxd`, `.spxc`). «Condividi la lista» (`spsh`, API Share o copia) e «Copia come testo» usano `spText`: solo le voci non ancora prese. «Azzera spunte» toglie anche quelle delle voci a mano. Prova: `test/t43.py`.

## v205 – vista Settimana del piano
Terzo interruttore nel piano pasti: Giorno / Settimana / Spesa (`V.pv`=p/w/s). `vpw()`: tabella giorni × pasti con le kcal, totale colorato rispetto a `S.goal` (entro 5%, 12%, oltre), riga Media, media dei macro e il menu chiuso «Cosa c’\è in ogni giorno» (`pw_det`). Tocco su un giorno (`ppwd`) apre la vista Giorno su quel giorno. Prova: `test/t44.py`.
