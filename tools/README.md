# Strumenti di lavoro per Ghisa

Servono a Claude (e a chi lavora sull'app) per modificare, provare e pubblicare Ghisa.
Non fanno parte dell'app: GitHub Pages li pubblica ma l'app non li usa.

## Ripartire da zero in una chat nuova
1. Clonare il repo in `/home/claude/ghisa`.
2. `python3 tools/estrai-sorgente.py` ricrea il sorgente in `/home/claude/w/tracker-palestra.html`
   (in alternativa: leggere l'artifact «Ghisa» con l'azione `read` dello strumento Artifact).
3. Dopo ogni modifica:
   - `tools/check.sh` controlla la sintassi dell'ultimo `<script>` con `node --check`;
   - un test mirato sulla parte nuova (`python3 tools/test/run.py tNN`); la suite intera solo se richiesta;
   - `tools/sync-pwa.sh "messaggio"` rigenera `index.html` (manifest, icone, service worker) e fa commit e push;
   - ripubblicare l'artifact sullo stesso URL.

## Test
Tutti insieme: `python3 tools/test/run.py` (4 alla volta; `-j N` per cambiarlo, `-v` per vedere le osservazioni, `run.py t63 t68` per sceglierne alcuni).
Per provare il sorgente prima di sincronizzarlo: `SRC=/home/claude/w/tracker-palestra.html python3 tools/test/run.py`; senza `SRC` si prova `index.html` del repo.
- `gb.py` è l'ambiente comune: copia la pagina in una cartella temporanea con pdf.js e i file di prova (`pdft/`, `gxs/`, `hi/`), la serve su `localhost` con una porta libera e ci sposta la cartella di lavoro. Ogni test fa `import gb` e apre `gb.URL`; le schermate vanno in `gb.O` (con `OUT=cartella` restano dove vuoi, con `KEEP=1` non si cancella niente).
- Un test fallisce se esce con errore, stampa un Traceback o «EXC», ha errori JavaScript («errori: [...]», «ERR [...]») o stampa «FAIL». Il resto dell'uscita sono osservazioni da leggere con `-v`; i test nuovi controllano i risultati e stampano `ok`/`FAIL` riga per riga (vedi `t69`).
- `t.py` è il banco di prova comune dei test più vecchi (dati di esempio + passi), `u.py` quello a passi di `u7`/`u8`. `fix/dpm-v217.json`: i 9 piani alimentari di prima, per `t56`.
- Di regola si prova solo la parte nuova o cambiata con un test mirato; la suite intera solo se Edo lo chiede.
Gli altri file provano una funzione ciascuno: `t1` guida esercizi, `t2` esercizi palestra, `t3` grammi alimenti, `t4` riscaldamento,
`t5` tutte le sezioni, `t6` barra seduta, `t7` sesso fuori dalla dieta, `t8` modelli scheda, `t9` programmi,
`t11` storico, `t12` Dieta, `t19` ricerca alimenti, `t20` gruppi alimenti, `tdb` IndexedDB e migrazione, `twipe` cancella tutto, `tbk` ripristino backup.

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

## v206 – riepilogo dell’uscita cardio
`cdSumOpen(id)` apre un foglio con durata, distanza, passo (velocità per bici/cyclette, `cdBike`), kcal, battito, dislivello, tempo nelle zone (`hzBar`) e il confronto con l’uscita simile precedente (`cdPrev`: stesso tipo, distanza o durata entro ±25%). Si apre da solo dopo il salvataggio (dal vivo `lcSave`, timer guidato, a mano `cda`, import di un solo file in `gxSave`) e toccando una riga dello storico (`cdsum`). Prova: `test/t45.py`. Nota: `t24.py` cerca il vecchio tasto `[data-a=hrc]` e va aggiornato (falliva già dalla v179).

## v207 – lettura al tocco sui grafici piccoli
I grafici nel tempo della pagina Grafici (`plot`) avevano già la lettura al tocco. Ora ce l'hanno anche la curva del battito (`hrCurve(hs,h,dur)`: minuto · bpm), il profilo altimetrico (`gxElv(e,km)`: km · m) e la linea del peso nel Riepilogo della Home (settimana e mese: data · kg). Contenitore `.tsc` con `data-l` (etichette in ordine) e `data-p` (inizio e fine del tracciato in frazione della larghezza); `tsAt` mostra linea e etichetta (`.tsl`, `.tst`), che spariscono dopo 3,5 s. La mappa muscolare mostra già i valori in testo sotto il grafico. Prova: `test/t46.py`.
Attenzione: `tools/demo/make-demo.py` riscrive `tools/demo/gymbo-demo.html` nel repo; per i test copiarla altrove e fare `git checkout` del file (la demo si aggiorna solo se lo chiede Edo).

## v208 – lista della spesa condivisa come link
«Condividi la lista» apre un foglio (`spShare`) con «Link da spuntare» (`spshl`) e «Testo» (`spsht`, come prima). Il link è `shlBase()` (l'indirizzo della PWA se aperta da github.io, altrimenti `SHL_URL`) + `#spesa=` + `z` e i dati (`spData`: solo voci non prese, per reparto) in JSON compresso deflate-raw e base64url (`j` = senza compressione). All'avvio `shlParse(location.hash)` apre la vista `shl` (`vshl`): spunte salvate solo in localStorage `gymbo-shl`, «Azzera spunte», «Apri Gym-Bo» toglie l'hash. Non tocca `S`. Prova: `test/t47.py`.

## v209 – lista della spesa come immagine
Nel foglio «Condividi la lista» c'è «Immagine» (`spshi`): `spImg()` disegna su canvas un PNG largo 1080 px (titolo, periodo, reparti, una riga per voce con casella e quantità, nomi lunghi accorciati) dai dati di `spData` e lo condivide come file (API Share); se il telefono non condivide file, lo scarica. Prova: `test/t48.py` (salva `u/lista-spesa.png`).

## v210 – programmi pronti palestra e cardio insieme in Schede
Il tasto di Schede «Programmi pronti (PGM+BPM+CPM)» apre `pgView` con i tasti Palestra/Cardio (`pgSeg`, azione `pgk`; ultima scelta in localStorage `gymbo-pgk`). Su Cardio mostra l'elenco di `cpView(1)` (senza intestazione) con il filtro in `V.pg.cf`; aprendo un programma (`cpo`) il dettaglio resta nella sezione Cardio con `V.cp.from='s'`, e «indietro» (`cpb`) torna a Schede su Cardio. In Cardio il tasto «Programmi pronti» (`cpl`) apre la stessa pagina già su Cardio; la scorciatoia `bppr` apre Palestra con il filtro A blocchi. Prova: `test/t49.py`. I test t27/t28 vogliono `demo/demo_data.json` accanto al sorgente (`/home/claude/w/demo/`).

## v211 – grammi modificabili nel piano pasti
Tocco sulla voce singola del piano (`.ppgl`, azione `ppge`, stato `V.ppe`) apre `ppEdH`: grammi con −/+ (`ppgm`, passo 5 g, 10 g sopra i 200), porzioni note (`ppgz`), kcal aggiornate mentre si scrive (`ppEk`), casella «anche negli altri giorni con questa voce» (`#ppea`, voci uguali di `mpSwSame`). Salva (`ppgs`, con Annulla e `mpMat`) aggiorna anche la scelta corrispondente in `al`. Prova: `test/t50.py`.

## v212 – avvisi fuori dall'app (seduta e cardio guidato)
Nella seduta guidata e nel cardio guidato compare una striscia (`ntfBan`): «Attiva» (`ntfa`) chiede il permesso delle notifiche e salva `S.ntf=1`; «No grazie»/«Disattiva» (`ntfn`/`ntfo`) mettono `S.ntf=0`. Con gli avvisi attivi, a ogni tocco durante la sessione `bgOn()` avvia un suono quasi muto in WebAudio (rumore a 2e-4, non prende il focus audio della musica) che tiene vivi i timer quando l'app è in sottofondo; `bgOff()` lo spegne a fine sessione (in `render`). `ntf(t,b)` manda la notifica (via service worker, altrimenti `Notification`) solo se la pagina non è visibile: fine recupero (`tick`), cambio fase e fine del cardio guidato (`csTick`). `sw.js` (cache `ghisa-v4`): `notificationclick` riporta all'app. Prova: `test/t51.py` (notifiche e visibilità simulate). Da verificare sul telefono vero: comportamento in sottofondo dipende da Chrome/Android (risparmio energetico).

## v213 – striscia della settimana e scorrimento tra i giorni
- Dieta: sotto la data `dwkH()` disegna i 7 giorni della settimana di `V.nd` (anello kcal/obiettivo: giallo sotto il 90%, verde fino al 105%, rosso oltre); tocco = `ndw`.
- Scorrimento orizzontale (>70 px, poco verticale) su Dieta e Piano pasti › Giorno: `dayOk`/`dayStep` cliccano `ndp`, `ppd` o `ppw` (cambio settimana ai bordi). Non parte da campi, grafici, zone che scorrono di lato, menu aperto, dialoghi o riordino; i primi 30 px restano al menu.
- Avviso «Scorri col dito» finché non si scorre o lo si tocca (localStorage `gymbo-swd`). Animazione `dsl-n`/`dsl-p` (spenta con riduzione movimento).
- `test/t52.py`.

## v214 – dimensione del testo
- `S.ts` da −2 a +2 (Molto piccolo … Molto grande, passo 15%): `applyTs()` mette `zoom` su `<html>` e la variabile `--z`; si chiama in `applyTh()` e dopo `dataBoot()`. Voce in ☰ sotto Tema (`tszo`), foglio `tsOpen()` (`#cfm.sht.tsz`, escluso dal rinfresco del foglio Drive in `render`).
- Con lo zoom sulla radice le unità vw/vh crescono: nel CSS sono scritte `calc(Nvw / var(--z,1))`. Le coordinate dei puntatori sono in px dello schermo: il timer (`tmMenu`, `tmClamp`, `tmPos`, trascinamento), il riordino (`dragInit`) e la lettura al tocco (`tsAt`) dividono per `TZ`.
- `test/t53.py`.

## v215 – riepilogo di fine seduta più ricco
- `ssSum(sid,sc)` raccoglie i dati di una seduta conclusa: seduta precedente con la stessa scheda (`P`), per ogni esercizio serie di oggi e di allora (o dell'ultima volta che è stato fatto), badge ↑ ↓ = (prima il carico massimo, poi le ripetizioni totali; a corpo libero solo ripetizioni), consiglio `ssTip`, record con 1RM stimato, serie per gruppo oggi e nella settimana.
- `ssDoneH` disegna la vista; `ssTipsH` tace sui carichi con un programma a blocchi o in settimana di scarico. «Com'è andata» (`ssrt`, secondo tocco toglie) e la nota (`#ssnt`) finiscono nella seduta: `S.ses[].rt` (f/g/d) e `S.ses[].nt`; `ssEnd` li conserva se la seduta viene riaperta.
- `ssImg(sid)` crea il PNG del riepilogo (azione `sssh`, condivisione o download).
- `test/t54.py`.

## v216 – riquadro «La volta scorsa»
- All'inizio di una seduta con una scheda già fatta (`lsbH`, inserito da `vss()` sotto la barra in alto; il vecchio corpo è `vss0`): data, durata, com'è andata, record, nota, «Da ricordare oggi» (`ssTipsH`) e, aperto (`lsbt`, `V.o.lsb`), il confronto `ssCmpH` con la seduta prima. Sparisce dopo la prima serie; la × (`lsbx`) mette `V.ss.lsx`.
- `lsChip` mette sotto «Ultima volta» il promemoria dell'esercizio (solo i consigli «resta…», perché «prova X kg» c'è già nella riga). Dati in cache in `LSC` (`lsLast`).
- `test/t55.py`.

## v217 – riquadro «La volta scorsa» su una riga
- Chiuso di default: una sola riga (`.lsc`, «Volta scorsa · gio dd/mm · durata · com'è andata · 🏆») con ▾ e ×; toccandola (`lsbt`, `V.o.lsb`) si apre tutto: info, nota, «Da ricordare oggi», confronto. `test/t55.py` aggiornato.

## v218 – piani «Allenamento e riposo»
- 4 piani nuovi in `DPM` (`cym`, `cyp` onnivori, `cyv` vegetariano, `cyn` vegano) con un decimo elemento `{tr:1, st:[spuntini dei giorni di allenamento]}`; i 9 piani di prima restano identici (verificato in `t56`).
- Giorni di allenamento `td` (7 booleani): di partenza quelli del programma settimanale della palestra (`plId`), altrimenti `DPTD` (3 → Lun Mer Ven); stepper `dptn` (1–6) e tocco sul giorno `dptd`.
- `dpCyc(K,td)`: giorni di allenamento il 20% (`DPCR`) sopra quelli di riposo, media settimanale = obiettivo; `dpWeek` scala ogni giorno sul suo valore (proteine uguali). Solo «7 giorni diversi». `S.dpa.td` tiene i giorni per «Ricalcola dosi».
- L'obiettivo del diario resta la media della settimana.
- `test/t56.py`.

## v219 – Riepilogo Excel unico con ambiti a scelta
- In Esporta dati la scheda «Riepilogo Excel» (ambiti `V.xe`: peso, palestra, cardio, alimentazione; azioni `xesec`, `xmx`) crea un solo file `Gym-Bo_Riepilogo_<dal>_<al>.xlsx` con `xmBook(sel)`: Riepilogo (riquadri, settimana per settimana con barre e colori sull'obiettivo, progressi per esercizio), Allenamenti (un blocco per seduta, righe raggruppabili, confronto con la volta prima, nota e com'è andata), Progressi (esercizi × settimane, scala di colore), Serie, Cardio, Alimentazione (un giorno per riga), Calendario kcal, Alimenti, Micronutrienti, Peso e misure, Grafici (grafici veri di Excel).
- Scrittura `xmWrite(sheets)`: stili interni deduplicati, celle unite, formati condizionali (barre, scala, cellIs con dxf), outline, blocchi, filtri, disegni e grafici `xmChart` (barre o linea). I vecchi Excel per area sono sostituiti; resta il CSV per area dentro «Dati grezzi in CSV» (`xExport(k,'csv')`).
- `test/t57.py` (apre i file con openpyxl e controlla che gli XML siano ben formati).

## v220–v221 – giornate incomplete fuori dalle medie
- `kcOk(k)` / `kcIn(d)`: un giorno di diario entra nelle medie solo se le kcal sono almeno il 70% dell'obiettivo (`S.goal`); sopra l'obiettivo conta sempre (v221: tolto il limite superiore del 130%). Senza obiettivo, almeno 800 kcal.
- Applicato a: `moStat` e `vwk` (Riepilogo in Home, con «N giorni esclusi»), `av7` (Media ultimi 7 giorni in Dieta), `adEst` (stima del fabbisogno reale: i giorni fuori soglia contano come esclusi, come quelli con pasti non segnati), PDF (`xReport`), Excel (`xmBook`: riquadro, settimane, grafico, media del calendario, colonna «Nelle medie»), micronutrienti di `xFood`. Il grafico giorno per giorno delle calorie resta con tutti i giorni.
- `test/t58.py`.

## v222 – chiudere a mano una giornata
- `S.dcl[data]=1`: giornata con poche kcal chiusa a mano. `kcIn(d)` la conta nelle medie se ha almeno un pasto; `mSk` considera «non fatti» i pasti principali mancanti, quindi spariscono gli avvisi e la giornata entra anche in `adEst`.
- `dclH(d,home)`: in Dieta sotto il Riepilogo del giorno (riquadro giallo con «Chiudi la giornata» / «Completa il diario», oppure riga verde «Giornata chiusa · Riapri»), in Home nel riquadro «Ieri». Mai per oggi. Azioni `dcl`, `dclr`, `dclg`; ✓ nell'anello della striscia della settimana (`.dclm`).
- `test/t59.py`.

## v223 – licenza e «gratis per sempre»
- Licenza PolyForm Noncommercial 1.0.0: `LICENSE.md` (testo ufficiale dal repository polyformproject/polyform-licenses, con la riga «Required Notice» in cima), `NOTICE.md` (nome e logo non concessi, componenti e dati di terzi), `README.md`. Lo stesso avviso è in un commento in testa al sorgente.
- In app: voce ☰ › Dati › «Informazioni» (`inf`, `vinf`, costanti `GBV`, `GBSITE`, `GBREPO`), riga nel Benvenuto, sezione «Gratis per sempre» in cima alla Guida, «app gratuita» nei piè di pagina di PDF, Excel e immagini condivise.
- `decFix` salta i testi dentro `.nodec` (numeri di versione come «1.0.0»). `GBV` va aggiornato a ogni versione.
- `test/t60.py`.

## v224 – attrezzatura degli esercizi
- `ATX[nome]=[modi, zone]`: per ognuno dei 73 esercizi del catalogo i modi di farlo (stringhe di codici, servono tutti: `b` bilanciere e rack, `m` manubri, `p` panca, `s` sbarra e parallele, `c` cavi, `x` macchine, `e` elastici e piccoli attrezzi, `n` corpo libero) e le zone caricate (`sp` spalle, `sb` schiena bassa, `gi` ginocchia).
- `atOf(e)`: `e.eq` se l'utente l'ha scelta, poi catalogo (anche via `gdCat` per i nomi simili), poi dalle parole del nome; `atTxt`, `atOk(e,H)` (H = codici disponibili). Mostrata nella riga in Esercizi, nella guida «Come si esegue», nel Catalogo; scelta nel foglio dell'esercizio (`exat`, salva `eq` solo se diversa dal catalogo).
- `test/t61.py`.

## v225 – import dello storico da Strong e Hevy
- «Esporta dati» diventa «Importa ed esporta» con il riquadro «Arrivi da un'altra app?» (`#hif`); i CSV condivisi (Condividi › Gym-Bo, `share_target` accetta ora anche .csv) vanno all'import.
- `hiCsv` (CSV con virgolette e a capo nei campi, separatore , o ;), `hiParse` riconosce Strong (`Exercise Name`, `Set Order`, `W` = riscaldamento) e Hevy (`exercise_title`, `start_time`, `set_type`, `weight_kg`/`weight_lbs`); `hiDate` legge ISO, «13 Mar 2024, 07:12» e d/m/y. Unità: colonna se c'è, altrimenti dai valori (libbre convertite).
- `hiName`: dizionario `HIM` (≈90 nomi inglesi → catalogo, con l'attrezzo tra parentesi), `HIC` per il cardio; esito ✓ abbinato, ≈ da confermare, + nuovo, → cardio. `V.hi` = anteprima (`hiView`), scelta per esercizio (`.hims`: `x:Nome`, `n` nuovo, `-` salta, `c:Tipo` cardio), opzioni riscaldamento (`hiwu`) e schede ricorrenti (`hisc`, ≥3 sedute con lo stesso nome).
- `hiDo` (azione `hiok`, in `UD` per Annulla): salta le sedute con stessa data ed esercizio già presenti (`hiDupSet`), crea `S.ses` con `src`, `tn` (nome dell'allenamento, mostrato nello Storico), serie con RIR = 10 − RPE, cardio con kcal stimate. File di prova in `test/hi/`, `test/t62.py`.

## v226 – «Crea il programma per me»
- In Programmi pronti, scheda «✨ Crea il programma per me» (`pbo`) → `V.pb` con 5 passi: obiettivo (`PBG`: f forza, m massa, t tonificare, s salute) e livello (`pbLv`: <10 sedute in 90 giorni → principiante; ≥36 e 1RM panca ≥ 1,25 × peso → avanzato; `pblv` lo cambia), giorni (2–6), minuti (30–90), attrezzatura (palestra completa o codici `ATL`), zone da proteggere (`ATZ`).
- `pbAdapt(p,Q)`: sostituisce gli esercizi non fattibili con l'attrezzatura o che caricano una zona protetta con uno dello stesso gruppo del catalogo (`pbAlt`, ordinato per parole in comune); se non c'è, segna `miss` (manca l'attrezzo) o `zk` (carica la zona). Taglia al tempo: stima `pbEst` = 6 + Σ serie·(recupero+40)/60 min; toglie serie ai complementari (indice ≥ 2, minimo 2), poi l'ultimo complementare se si sfora di oltre 6′. Con `Q.vary` cambia i complementari (rinnovo).
- `pbScore(Q)`: giorni, obiettivo (`PBT`), livello, −50 per esercizio impossibile, −2 per sostituzione, −3 per zona caricata; i programmi a blocchi (`BPM`) entrano solo se i giorni coincidono e tutto è fattibile. Mostra i primi 3 con i motivi; anteprima con schede, ⇄ sostituzioni, serie tolte, carico di partenza da `rmOf` (1RM/(1+r/30)·0,9, arrotondato a 2,5 kg).
- `pbDo` (`pbok`, in `UD`): crea le schede (serie con `kg`), programma settimanale o rotazione sui giorni scelti, `S.prog.rn` = +70 giorni, `S.eqh` (attrezzatura, usata anche da `swAlt` per mettere prima ciò che si può fare) e `S.pbq` (risposte). In Schede, da `rn`, banner `pbRenew`: `pbrw` rinnova, `pbrl` rimanda di 14 giorni. Test `test/t63.py`.

## v227 – costruttore in Schede, Integratori
- «✨ Crea il programma per me» esce da Programmi pronti: `pbHero()` in cima alla pagina Schede (versione compatta se `S.prog.pb`); `pbx` e «‹ Schede» tornano a Schede.
- Nuova sezione **Integratori** (tab `it`, `vit()`, gruppo Alimentazione, link dal riquadro Micronutrienti). `itData()` legge le ultime 4 settimane: giorni completi (`kcIn`), media % LARN dei micronutrienti (`miRows`), proteine g/kg dall'ultimo peso, sedute pesi e cardio a settimana, uscite ≥75′, tipo di alimentazione (dai pasti; se <20 pasti dal piano `S.dpa`), porzioni di pesce grasso (`ITFISH`), sesso, età, stagione.
- `itList(D)` → gruppi: utili (`si`), prima un controllo (`chk`: vitamina D, ferro, B12 in alcuni casi), da valutare (`mb`: omega-3, caffeina, carboidrati nel cardio lungo), prima il cibo (`cibo`, con alimenti da `miSug` via `itFood`), servono dati, non servono (+ `ITNO`, poche prove). Obiettivo proteine 1,6 g/kg con ≥2 sedute pesi, 1,2 con ≥3 cardio, altrimenti 0,9. «Lo prendo già» (`itg`) → `S.itg`. Fonti AIS, ISSN, Morton 2018, LARN. Test `test/t64.py`.

## v228 – verifica delle fonti
- Formule controllate sulle fonti originali e confermate: Epley/Brzycki, Mifflin-St Jeor, Keytel 2005 (coefficienti), Tanaka 2001, Marina USA (Hodgdon e Beckett, formule metriche), fasce ACE, BMI OMS, ritmi Helms 2014 / Iraki 2019, ISSN 2017 proteine, ACSM 2009 progressione, Schoenfeld 2017 / Baz-Valle 2022 volume, 5/3/1 (percentuali e scarico), zone % FC massima, gruppi AIS (A: creatina, caffeina, proteine, vitamina D, ferro, bevande e gel; B: oli di pesce; C: BCAA; D: booster del testosterone e stimolanti).
- MET confrontati con la tabella ufficiale del Compendium 2024 (PDF pacompendium.com): corsa, attività sportive, circuiti ok. Corretti: camminata 2,5 mph = 3,0 e 2,8–3,4 mph = 3,8 (prima 3,5 a 4,8 km/h), punti della bici lenta (8,9 e 15,1 km/h), bici senza velocità 7,0 (01014).
- LARN V revisione (2024), confrontati con le tabelle SINU riportate da Smartfood IEO: K, Ca, Mg, Fe, Zn, vit. C, B12 ok; sodio: limite 1,6 g dai 65 anni (prima sempre 2 g). Proteine nella sezione Integratori: 1,1 g/kg dai 65 anni.
- 1RM: `rmEst` e lo storico mensile usavano solo Epley fino a 12 ripetizioni; ora `rm1` come dichiarato.
- Banca dati: controllo Atwater su tutti i 1.007 alimenti (nessun errore oltre alcolici e convenzioni CREA), valori anomali per categoria e colonne duplicate. Corretti: Sale senza sodio (ora USDA 02047, 38.758 mg), barretta al cocco calcio 1101 → 110 (CREA/INRAN), B12 del muesli (copiata dallo zinco), semi di girasole (sodio e vitamina C copiati da fibra e zuccheri; ora USDA 12036), sodio delle patate dolci (USDA 11507); fonti dichiarate onestamente per gallette, pesce spada, seitan, barretta ai cereali, bevanda di mandorla, whey. Blocco `correzioni dopo la verifica delle fonti` dopo le banche dati. Test `test/t65.py`.

## v229 – Cardio come Palestra, riordino del menu per gruppi
- Cardio (`vc`) con tre schede (`V.cv`: `a` Allenamento, `h` Storico, `r` Record, azione `cdv`), come Palestra.
  - Allenamento: `cdHero()` «Modalità uscita» con menu `#cdq` (`V.cq`, `cdQ()` sceglie la scheda di oggi, poi il programma, poi l'ultima attività): programma (`cpgo`, riga «Settimana X di N · Programma ›»), scheda cardio (`csgo`), uscita libera (`cdgo` = cronometro dal vivo con battito se collegato). Poi `wkCard('c')`, `cdOpts()` (orologio/fascia e zone, `#dCop`), `cdMan()` (`#dCdm`, A mano / Da file).
  - Storico: `cdHist()` con riquadri «Uscite ultimi 30 giorni» e «Minuti a settimana», una `details.hsx` per uscita con `cdSumH` dentro, percorso (`gxCard`), Modifica/Elimina; etichette `cdTag` (dal vivo, da file, programma, scheda). `cdmore` +15.
  - Record: `cdRecs()` per attività: 5 km, 10 km, mezza (solo Corsa e Tapis roulant, dal passo dell'uscita più veloce di almeno quella distanza), uscita più lunga, velocità media migliore (bici), battito più alto; «nuovo» se degli ultimi 14 giorni; tocco → `cdsum`.
  - Via la fila «Programmi pronti / Schede cardio / Grafici / Esercizi cardio» e il modulo sempre aperto.
- Schede: selettore Palestra / Cardio (`V.sk`, azione `skk`); in Cardio «Programmi cardio pronti», programma in corso (`cpCard`), `cscCard`, programma settimanale. Gli editor delle schede cardio impostano `V.sk='c'`. Esercizi aveva già Palestra/Cardio (`V.ek`), Grafici il gruppo Cardio.
- Menu: anche in riordino le voci restano divise in gruppi; ⠿ sulle voci le sposta dentro il gruppo, ⠿ sul titolo sposta il gruppo intero (`S.ngo`). `dragInit` ascolta il rilascio anche sulla finestra: prima, se il dito si alzava fuori dalla maniglia, il trascinamento restava appeso. Test `test/t66.py`, `test/t67.py`.

## v230 – Programmi pronti separati per Palestra e Cardio
- Schede › Palestra: «Programmi pronti (PGM+BPM)», lista «Programmi palestra pronti» senza il selettore `pgSeg`; `pgl` forza `k:'p'`.
- Schede › Cardio: stessa riga della palestra (`.mrow`: «Programmi pronti (12)» + «⋯ Altro» con «Importa sedute (PDF o Excel)», tolto da `cscCard`). Lista «Programmi cardio pronti»: filtri Tutti / A blocchi (più mesi) / Iniziare / Dimagrire / Prestazione / Basso impatto, prima i programmi a blocchi (`p[2]=='m'`) poi quelli a settimane, etichette come in palestra. `pgx` torna alla scheda giusta (`V.sk`).

## v231 – «Crea il programma cardio per me»
- Schede › Cardio: `qcHero()` (compatto se `S.cpr.pb`), azione `qco` → `V.qc` con 5 passi: obiettivo (`QCG`: i iniziare, d dimagrire, s fiato e cuore, p prestazione) e livello (`qcLv`: <6 uscite in 90 giorni → principiante; ≥24 e corsa ≥10 km o uscita ≥70′ → avanzato), giorni (2–6), minuti per uscita (20–90), cosa puoi usare (`QCE`: corsa all'aperto, tapis roulant, bici o cyclette, ellittica, vogatore, piscina; la camminata c'è sempre), zone da proteggere (`QCZ` ginocchia, schiena, caviglie).
- `qcAct(p,Q)`: attività tra quelle del programma e quelle disponibili; con ginocchia o caviglie evita corsa e tapis roulant, con la schiena anche il vogatore, in ordine di basso impatto (`QCLOW`). `qcScore`: giorni, obiettivo (`QCT`), livello («Tutti i livelli» va bene per tutti), −60 se si corre con zone da proteggere, penalità se le uscite vanno accorciate molto; «Cardio dopo i pesi» solo se hai schede palestra. Mostra i primi 3 con i motivi; anteprima settimana per settimana (`qcw`) con le uscite già accorciate.
- `cpCap(sp,mx)` accorcia un'uscita al tempo massimo: meno ripetizioni e parti continue scalate, riscaldamento e defaticamento al massimo 5′. `cpSes` lo applica al programma attivo se `S.cpr.mx` c'è.
- `qcDo` (`qcok`, in `UD`): `S.cpr` con attività scelta, giorni (al massimo quante uscite prevede il programma), `mx`, `pb:1`; salva le risposte in `S.cpq`. A fine programma `cpCard` propone «✨ Crea il prossimo per me» (`qcnx`): stesse risposte, livello +1. Test `test/t68.py`.

## v232 – scambio esercizio nei programmi a blocchi, test in ordine
- «⇄ Sostituisci › Anche nella scheda» in seduta: con un programma a blocchi attivo la scheda si rigenera ogni settimana da `S.bp.D` (`bpGen`), quindi l'esercizio vecchio tornava alla settimana dopo. Ora `swDo` lo cambia anche in `S.bp.D` (e prende il massimale di lavoro del nuovo esercizio, se c'è). Test `test/t69.py`.
- Test: ambiente comune `gb.py`, esecutore `run.py`, 18 test vecchi aggiornati alle schermate di oggi (Cardio a schede, Schede Palestra/Cardio, foglio di ricerca alimenti, eliminazione esercizi senza registrazioni al primo tocco, condivisione della spesa con il foglio), `t20d` tolto (confronto una tantum con la v170), `t56` confronta con `fix/dpm-v217.json`, `t46` costruisce la demo al volo (`make-demo.py` accetta `DEMO_OUT`). Tolte dal repo le schermate dei test finite per sbaglio nella cartella principale.

## v233 – lingua: italiano, inglese, francese
- Il codice resta in italiano. `LANG` (da `localStorage['gb-lang']`; se manca: italiano per chi ha già dati, altrimenti la lingua del browser, inglese di riserva) e `LOC` (formati di numeri e date) sono definiti all'inizio dello script; `S.lang` va nei backup e su un dispositivo nuovo viene ripreso.
- Dizionario nel tag `<script id="i18nd">`: righe `[italiano, inglese, francese]`, `\x01` dove il testo italiano ha un valore. `trS()` traduce: frase esatta → modello con valori (i valori vengono tradotti a loro volta) → frase con punteggiatura finale → frasi separate → frasi note dentro testi composti (`i18Sub`). Il MutationObserver che già metteva la virgola decimale (`decFix`) ora traduce prima testi e attributi (`placeholder`, `aria-label`, `title`, `alt`); in inglese la virgola decimale diventa punto. `.notr` e `[contenteditable]` restano come sono.
- Tradotti anche: canvas (immagini condivise), celle Excel e CSV, testi condivisi della spesa, formato data Excel (`XD`). La ricerca degli alimenti cerca anche nel nome tradotto; per cancellare tutto vanno bene CANCELLA, DELETE o SUPPRIMER.
- Scelta della lingua: riga «🌐 Lingua · Language · Langue» nel menu (sopra il tema) e nella scheda di benvenuto; azione `lng` salva e ricarica.
- Rigenerare il dizionario dopo nuovi testi: `tools/i18n/ex.js` estrae le frasi dallo script, `items.json` le numera, `traduzioni.tsv` (`id\tEN\tFR`, `-` = da non tradurre) le traduce, `build.py` + `mk.py` controllano i segnaposto e producono il JSON da mettere in `#i18nd`. Le frasi nuove non tradotte restano in italiano. Test `test/t70.py` (elenca le frasi italiane rimaste visibili in EN e FR).

## v234 – ricerca libera nel foglio «Scambia»
- Il foglio ⇄ Scambia (diario e piano pasti, `mpSwOpen`) ha in alto il campo `#swq` (`V.sw.q`): `mpSwRes()` usa `fMatch` (sinonimi, correzione, nome tradotto) e propone fino a 8 alimenti con i grammi che danno le stesse kcal dell'alimento attuale (`gR(k0/f.k*100)`). Le righe sono quelle di sempre (`mpSwRow`, prima interna a `mpSwOpen`): «⇄ Scambia» o «+ Salva» tra le alternative. L'input aggiorna solo `#swres`, così il campo non perde il fuoco.
- Frasi nuove per EN/FR in `tools/i18n/extra.json` (le legge `mk.py`). Test `test/t71.py`.

## v235 – età in un riquadro suo
- Obiettivi e misure: `agCard()` (classe `agc`, stesso campo `#tda` e stesso salvataggio in `S.pf.age`) subito prima di `sxCard()`. In `objBody` (Obiettivi dieta) al posto del campo c'è il richiamo «Età: N anni · cambia» (azione `agf`, porta al campo). Test `test/t72.py`.

## v236 – silhouette con richiami
- Grafici › Mappa muscolare › Silhouette: `mmBody(D)` disegna i muscoli con la loro forma (`MBF` davanti, `MBB` dietro: mezzo corpo, specchiato), colorati con `mmCol`, e una linea da ogni gruppo a numero e nome (a sinistra davanti, a destra dietro). Testo con contorno del colore della scheda (`paint-order:stroke`) per restare leggibile sopra i muscoli. Con la silhouette l'elenco dei numeri sotto è nascosto (sono già nei richiami). Test `test/t73.py`.

## v237 – tasto «indietro»
- `#nbb` accanto al ☰: «‹ nome della pagina precedente». `navTrack()` (all'inizio di `render`) registra un passo quando cambia `NAVK` (`tab`, `wv`, `cv`, `sk`, `ek`); ogni voce tiene `V.o` (pannelli aperti), scorrimento e sotto-scheda (`navSub`, per l'elenco). `navGo(i)` ripristina e scorre al punto di prima. Nascosto in Home, in seduta e nel cardio dal vivo.
- Pressione lunga (500 ms) su `#nbb` → foglio «Pagine recenti» (`navList`, fino a 8, senza doppioni).
- Gesto/tasto indietro del telefono: una voce di cronologia «trappola» (`history.pushState({gb:1})`); `popstate` chiude nell'ordine menu, foglio, menu +, poi torna indietro; in seduta non fa niente; in Home il secondo «indietro» entro 2,5 s esce. Test `test/t74.py`.

## v238 – calistenia
- Catalogo (`XB`) da 73 a 89 esercizi: 16 nuovi a corpo libero (piegamenti inclinati, archer, diamante, pike push-up, rematore australiano, trazioni negative e con elastico, scapular pull-up, squat a corpo libero, squat bulgaro a corpo libero, pistol squat assistito, hip thrust a una gamba, nordic curl assistito, calf raise a una gamba, hollow body e L-sit in secondi), ognuno con la guida in `XG`.
- `PGM`: «Calistenia base» (`ca1`, A/B), «Calistenia Upper / Lower» (`ca2`, 4 giorni), «Calistenia Push / Pull / Legs» (`ca3`, 3 o 6 giorni); filtro «Calistenia» (`pgf` `ca`) nei Programmi pronti.
- Progressioni `CGP` (esercizio → variante più difficile, soglia di ripetizioni o secondi): in seduta `cgBox` (dentro `xnBox`) propone «💪 Pronto per …» se nell'ultima seduta tutte le serie (almeno 2) hanno raggiunto la soglia; «Passa a …» (`cgup`) usa `swDo(…,'xb:'+nome,'sch')`, quindi aggiunge l'esercizio dal catalogo e lo sostituisce anche nella scheda. Guida aggiornata (89 esercizi, 19 programmi). Frasi EN/FR in `tools/i18n/extra.json`. Test `test/t75.py`.

## v239 – generatore di schede su misura
- «Crea il programma per me» ora costruisce le schede da zero (prima classificava e adattava i programmi pronti; quel percorso resta solo per il rinnovo dei vecchi programmi `pb:1`).
- Domande: le 5 di prima + 6 «muscoli in priorità» (`Q.pri`, max 3) + 7 «esercizi da tenere/evitare» (`Q.keep`, `Q.ban`, ricerca `#gkq`/`#gbq` → `gnFind`).
- `gnBuild(Q)`: divisione dai giorni (`gnSplit`: 2–3 full body, 4 Upper/Lower, 5 ibrido, 6 PPL ×2) con sedute a posti `[movimento, livello]` (`GNS`); movimento e livello di ogni esercizio in `GNM`; candidati `gnCand` (attrezzatura, zone, esclusi, da tenere, storico `gnHist`: progresso % e sedute dall'ultimo record, varietà, seme per «Rigenera»); ripetizioni/recuperi per obiettivo (`gnRx`); serie verso l'obiettivo per muscolo (`gnTarget`: livello, obiettivo, +30% priorità) con posti di isolamento aggiunti nelle sedute adatte; tempo (`gnEst`): superserie fra isolamenti, meno serie (prima ai muscoli più sopra obiettivo), fondamentali a 3, poi meno esercizi; ripieghi `GNF` se l'attrezzatura non basta. Ogni esercizio ha il suo motivo.
- Viste: `gnView` (schede, lucchetto `gnl` = `Q.lk`, ⇄ `gns` = `Q.alt`, «Rigenera il resto» `gnr` = `Q.seed`), `gnSum` (serie per muscolo, note su cosa è stato sacrificato, ciclo 5/6/7 settimane con scarico finale = `S.dlw`), `gnDo` (schede, programma settimanale, `S.prog.pb=2`, `rn` a fine ciclo, `S.pbq` con le nuove risposte). Attrezzatura degli esercizi di calistenia in `GNX` (unita ad `ATX`). Test `test/t76.py`.

## v240 – rinnovo a fine ciclo del programma su misura
- Quando `S.prog.pb==2` e `S.prog.rn` è passato, Home e Schede mostrano `gnRenew()`: «⇄ Il tuo ciclo è finito» con cosa cambierebbe (gruppi rimasti sotto la fascia nelle sedute del ciclo, esercizi fermi, esercizi che progrediscono, complementari cambiati). «Più tardi» = `pbrl` (+14 giorni).
- `gnRenQ()` riparte da `S.pbq`: tiene d'ufficio gli esercizi in progresso (`keep`), `Q.boost` alza l'obiettivo dei gruppi rimasti indietro, `seed` diverso per variare i complementari, motivo «nuovo, per variare lo stimolo». «Vedi il rinnovo» (`gnrw`) apre il generatore già sulle schede; le schede del ciclo finito restano. `gnHist`: un esercizio in progresso non conta come fermo. Test `test/t77.py`.

## v241 – generatore del piano pasti su misura
- Piano pasti › «✨ Crea il piano pasti per me» (`mgo`, `mgView`): 3 passi (obiettivo, dieta onnivoro/pescetariano/vegetariano/vegano, 3 o 4 pasti; allergie, alimenti da evitare/tenere con ricerca `mgFind`; tempo in cucina, varietà, più carboidrati nei giorni di allenamento con `dpCyc`).
- `MGF`: elenchi per ruolo (carboidrato, proteina con tipo, verdura, cereali, latte/yogurt, frutta, extra, spuntino, rinforzo proteico `pb`) con diete, allergeni (`MGA`) e tempo. `mgBuild(Q)` sceglie per ogni posto con `mgPick` (rotazione proteine: pesce ≥2, carne rossa ≤2, pranzo e cena di tipo diverso; varietà; seme), poi dosi con `dpScale`; se le proteine restano sotto il 93% aggiunge fino a 2 rinforzi. Varietà «Stessi pasti» = 3 giornate a rotazione (`DPS`).
- Settimana: giorni con 🏋, macro del giorno, perché di ogni scelta, lucchetto su alimento o pasto (`mgl`/`mglm`), ⇄ (`mgs`), «Rigenera il resto» (`mgr`). Riepilogo `mgSum`: medie contro obiettivi, micronutrienti (`microOf`/`miL`) con note, numero alimenti, settimana di destinazione; «Usa questo piano» (`mgDo`) scrive `S.mpw[w]` e salva le risposte in `S.mpg`.
- `mgRenew()`: a settimana nuova senza piano, propone la settimana successiva in base a quanto è stato seguito (`mgAdh` sul diario: tiene i pasti seguiti, cambia gli altri, adegua le calorie). Test `test/t78.py`.

## v242 – ricerca per gruppi di alimenti
- `FQG`: gruppi e sottogruppi (pesce › azzurro e grasso, bianco, crostacei e molluschi, in scatola; carne › rossa, bianca, maiale; salumi; latticini › latte e yogurt, formaggi › freschi, stagionati, spalmabili; uova; legumi; frutta secca; cereali con glutine; dolci; verdure; frutta), ognuno con le parole che lo richiamano e una regola (gruppo di `cat()` o espressione sul nome). `fgOf(q)` riconosce anche plurali, inizi di parola e frasi come «non mi piace il pesce»; `fgMem(id)` elenca gli alimenti.
- Generatore del piano pasti: la ricerca propone il gruppo intero, i sottogruppi e poi gli alimenti; il gruppo si salva come `g:<id>` in `ban`/`keep`, le eccezioni in `Q.bx`. Chip unico con pannello per togliere la spunta (`mggx`, `mgbe`). `mgBan`/`mgKeep` sostituiscono i controlli sui nomi.
- Cambio alimento: scrivendo un gruppo compaiono solo i suoi alimenti alle stesse kcal; gli alimenti esclusi nel piano su misura (`swBan`) non compaiono tra risultati ed equivalenti, con nota.
- Diario: scrivendo un gruppo, elenco diviso per sottogruppi (`flG`). Test `test/t79.py`.

## v243 – risultati della ricerca alimenti subito sotto la barra
- Nel foglio «Aggiungi a …» la parte iniziale (Recenti, Di solito, Copia un pasto) è in `#fpre` e si nasconde appena si scrive: i risultati compaiono sotto la barra, sopra la tastiera.
- `fqRow(f)`: riga compatta con kcal per 100 g; per gli alimenti già usati «già usato», «di solito N g» e il pulsante «+ N g» (`fqa`, aggiunge e svuota la barra), per gli altri «Scegli». Prima 4 risultati, poi «Altri N risultati» (40) e «Mostra tutti» (`fqall`, `V.fqAll` 1 e 2).
- Alimento scelto: resta solo lui con il riquadro dei grammi attivo e «‹ altri risultati» (`fsx`). Test `test/t80.py`.

## v244 – fogli sopra la tastiera
- Su Android la tastiera copre la parte bassa della pagina senza ridimensionarla: i fogli dal basso (`.sdov`) restavano dietro la tastiera. `kbFit()` legge `visualViewport` (eventi resize e scroll) e imposta `--kb` (altezza della tastiera, se oltre 60 px) e `--vvh` (altezza visibile): `.sdov` lascia `--kb` libero in basso e `.fsh` si accorcia allo spazio visibile, così barra e risultati restano sopra la tastiera. Test `test/t81.py` (spazio simulato).

## v245 – carico proposto senza cali ingiustificati
- Prima: se mancava anche una ripetizione, il carico tornava a quello scritto nella scheda alla creazione (il generatore scrive il 90% della stima e non lo aggiorna mai); senza carico nella scheda si ripartiva dall’ultima serie della seduta precedente, spesso quella scalata. I carichi quindi scendevano a gradini.
- Ora `tgNext(tg,ps,j,last,bw,id)`: base = serie di lavoro più pesante della seduta precedente (per serie se la scheda è a piramide, `ldPyr`); +2% (`sgP`) se tutte le ripetizioni fatte o RIR ≥ 3; uguale se no; −5% solo dopo due sedute di fila sotto l’85% delle ripetizioni previste (`ldLow`, `ldPrev`). Il carico della scheda vale senza storico o se la scheda è stata cambiata dopo l’ultima seduta (`tg.at`, scritto dall’editor solo quando cambiano ripetizioni/carichi, dal generatore e dalle azioni dello stallo). Programmi a percentuale (`tg.bp`) invariati. Nella seduta, dalla seconda serie segue il carico appena usato.
- Sotto il carico il motivo (`N.why`, `.ldw`); le serie previste mostrano il carico proposto (`ldSh`). Test `test/t82.py`.

## v246 – dispensa
- Piano pasti › Dispensa (`V.pv=='d'`, `vdsp`): alimenti in casa (`S.dsp.it[id]={q,q0,t,ex?}`), ricerca anche per gruppi (`dsRes`), sezioni «Da usare presto» (scadenza entro 3 giorni), Frigo, Dispensa; per ogni alimento quantità, scadenza o «basta per N pasti del piano» (`dsPlan`), modifica con Metà/Finito/Salva/Togli. Scadenza proposta per gruppo (`dsExp`).
- Le quantità sono calcolate dal diario (`dsCalc`): quantità impostata meno quanto mangiato a casa dopo quel momento (ora di creazione della voce da `uid`, `entTs`). Annullare, eliminare o spostare un pasto rimette tutto da solo. `dsUse`/`dsAdd`: stesso alimento, crudo dal cotto a parità di calorie (o `CR`), ingredienti delle ricette in proporzione; mai sotto zero, con avviso «finito» (`dsOver`: alla spesa o «Ne ho ancora»).
- Diario: «Casa | Fuori» su ogni pasto (`S.mfo['data|pasto']`, `mFuori`), scritta «Fuori casa», sotto ogni alimento cosa è stato tolto (`dsNote`). Avviso dopo un pasto a casa con «Annulla» (`x.nd`) ed «Era fuori casa» (`dsWatch`, `#dstst`). Abitudine: 4 pranzi feriali «Fuori» in 14 giorni → proposta di automatico (`S.dsp.af`, `dsHabitChk`).
- Impostazioni: togli in automatico / chiedi ogni volta (`x.dy`) / non togliere; controllo veloce settimanale (`dsCk`).
- Spesa: `dsSp` toglie quello che hai (riga «servono X · ne hai Y», riquadro «Già in casa»), anche nel testo e nel link condiviso; «Ho fatto la spesa» (`dsBought`) mette in dispensa gli spuntati.
- Generatore pasti: «Usa prima quello che ho in casa» (`Q.dsp`), precedenza agli alimenti in dispensa e in scadenza, con il motivo. Test `test/t83.py`.

## v247 – Spesa e dispensa come sezione a sé
- Nuova voce di menu «Spesa e dispensa» (`V.tab=='sp'`, `vspd`, gruppo Alimentazione) con le schede Spesa (con la settimana da scegliere) e Dispensa (`V.spv`). Piano pasti resta con Giorno e Settimana più il collegamento «Spesa e dispensa ›» (`spgo`); «Lista della spesa ›» e «Ne ho ancora» portano qui. Test `test/t84.py`.

## v248 – «Cosa cucino con quello che ho?» e alimento aperto
- `ccBuild(m,o)`: calorie e proteine che mancano oggi divise sui pasti vuoti (`ccNeed`, pesi `CCW`), alimenti in dispensa (rispettando dieta, allergie ed esclusi del piano su misura, `ccOk`) per ruolo (`ccRole`), schemi per pasto (pranzo/cena: carboidrato+proteina+verdura, varianti; colazione; spuntino), dosi su proteine e calorie (`ccDose`), olio sempre disponibile. Ordine: vicinanza a kcal/proteine, alimenti in scadenza o aperti, tempo (`ccMin`), varietà tra proposte consecutive. Filtri «Veloci» e «Senza fornelli», opzione con 1 alimento da comprare (va in spesa), «Come si fa» (`ccSteps`).
- Si apre dai pasti vuoti di oggi nel diario e da Spesa e dispensa › Dispensa («Cosa cucino adesso?», pasto da `ccNext`). Foglio `ccHtml` (`V.cq`); «Aggiungi» scrive il pasto, avviso con Annulla e «Salva come ricetta» (`rcStore`).
- Dispensa: «Aperto oggi» (`dsop`, `i.op`): scadenza = quella del prodotto aperto (`dsOpenD`: passata 4 giorni, latte 3, tonno 2…), annullabile. Scatolame e prodotti a lunga conservazione senza scadenza e, se chiusi, in «Dispensa» anziché «Frigo». Test `test/t85.py`.

## v249 – quantità della spesa modificabili, dispensa proiettata
- Ogni quantità della lista è un pulsante (`spqe`): riquadro con − e + di un pezzo o confezione (`spStep`, altrimenti 50 g), campo in grammi, confezioni pronte arrotondate per eccesso, «Salva» / «Torna al piano» (`spEd`). Salvate in `S.spq[settimana][alimento]={g,b}` (b = quanto diceva il piano), applicate da `spAdj` dentro `spAll()` usato da lista, testo, link condiviso e «Ho fatto la spesa». In viola con «modificato da te · dal piano X»; se il piano cambia oltre il 10% compare «Usa X / Tieni Y» (`spqr`/`spqk`). 0 = «Non serve» con «Rimetti».
- Articoli aggiunti a mano: quantità libera (`v.q`, `spxe`/`spxs`), anche nel testo condiviso.
- Settimane future: `dsProj(w)` toglie dalla dispensa quanto il piano prevede da oggi all’inizio di quella settimana (pasti di oggi non ancora registrati compresi), riga «ne avrai circa X». Test `test/t86.py`.
