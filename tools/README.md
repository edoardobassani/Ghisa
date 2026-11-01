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
