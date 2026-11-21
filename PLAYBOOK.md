# APExpress24 – Playbook social (@ape_express24)

Leggi questo file all'inizio di ogni sessione. Account Instagram: ape_express24, ds_id IGI, account_id 17841439178491368.
Sito: https://www.apexpress24.it · Preventivatore: https://www.apexpress24.it/configuratore (link in bio deve puntare lì).
Obiettivo: organico Instagram (NIENTE ads Meta/Instagram: le ads sono solo su SEO Google). Metriche da far crescere: reach, visite al profilo, clic sul link in bio (website_clicks), messaggi/richieste, clic sul configuratore.

## Fatti verificati (usabili nei contenuti)
- Servizio: APE (Attestato di Prestazione Energetica) in Lombardia; sopralluogo OBBLIGATORIO e incluso di un tecnico accreditato; APE firmato digitalmente (PDF e .p7m) e registrato al catasto energetico regionale. Tempi dal sopralluogo: standard 5 giorni lavorativi, priority 3, urgente 48 ore.
- Prezzi (+IVA 22%, più 10 € contributo CENED non soggetto a IVA): fino a 99 m² 99 €; 100-149 m² 119 €; 150-199 m² 139 €; 200-299 m² 169 €; 300-399 m² 199 €; 400-499 m² 239 €; oltre 500 m² preventivo. Esempio: 90 m² = 130,78 € totali. Il prezzo sale con superficie e urgenza.
- Zone servite: Varese e provincia (Gallarate, Busto Arsizio, Cassano Magnago, Cairate, Cardano al Campo, Samarate, Olgiate...), Milano (centro, ovest, est, hinterland: Rho, Lainate, Arese, Pero, Legnano, Canegrate, Parabiago, Rescaldina, Saronno), Como, Monza e Brianza (Carate Brianza), Pavia, tutta la Lombardia. Peso: 40% Varese+provincia, 40% Milano, 10% Como, 10% Monza.
- Normativa: APE necessario per vendita (al rogito), nuovi contratti di locazione, annunci (classe energetica indicata), nuove costruzioni, ristrutturazioni >25% involucro. Validità max 10 anni dalla registrazione; decade prima se lavori cambiano la prestazione. Il rinnovo tacito dell'affitto richiede APE valida (interpello MASE). Contratti senza APE non nulli ma sanzionabili. NON citare importi di sanzioni (fonti discordanti).
- CURIT: Catasto Unico Regionale Impianti Termici; targa impianto obbligatoria in Lombardia dal 15/10/2014; libretto di impianto.
- Prima di usare un fatto nuovo (legale/tecnico/prezzi) verificalo con WebSearch e fonti ufficiali. Non inventare offerte, sconti, convenzioni, recensioni, tempi o numeri.

## Tono e stile
Diretto, professionale, rassicurante, trasparente ("prezzo chiaro prima di pagare"). Frasi corte. Italiano. Ogni contenuto: testi NUOVI (mai ripetere headline già usate), stessa grafica.
Palette: sfondo verde petrolio #0F4D4D, crema #F6F3EA, ambra #F2B134, verde CTA #0B7A3B, scuro #10222B, scala classi A4 #0B7A3B / A3 #1F8A3C / A2-A1 #7DB93A / B #E8D93A / C #F4B73A / D-E #EE6B45 / F-G #B3262F. Font Inter (/usr/share/fonts/opentype/inter/). Brand testo "APExpress24" ambra in alto.
Ogni contenuto chiude con CTA verso il preventivatore ("link in bio" nei reel/post; nelle stories "apexpress24.it/configuratore").

## Strumenti (in tools/)
- tools/reels.py: reel 1080x1920 ~12 s con PIL+ffmpeg (4 esempi: rogito, agenzie, APE scaduta, sopralluogo). Copia e adatta: stessa struttura, scene diverse.
- tools/static.py: caroselli 1080x1350 (cover/statement/table/points/cta) e stories 1080x1920.
- Safe area reel/story: evita i primi 250 px e gli ultimi 350 px.
- Istagram accetta immagini JPEG (non PNG) e video MP4 H.264 yuv420p.

## Pipeline di pubblicazione
1. Genera i file in locale, guarda i fotogrammi/slide prima di caricarli.
2. Metti i file nel repo andresanarico-pixel/ape-express24-media (cartelle wNN/ per immagini JPEG, reels/ per mp4), commit e push.
3. URL pubblici: immagini https://raw.githubusercontent.com/andresanarico-pixel/ape-express24-media/main/<path>.jpg ; video https://andresanarico-pixel.github.io/ape-express24-media/<path>.mp4 (GitHub Pages: attendi 1-2 minuti dopo il push; i video via raw NON sono accettati).
4. Pubblica con manage_social_media (ds_id IGI; content_type VIDEO per reel, CAROUSEL, STORY, IMAGE), publish_at con timezone Europe/Rome. Distanzia i post dello stesso account di almeno 5 minuti.
5. OGNI scrittura richiede approvazione umana: restituisce un approval_url. NON aprirlo, NON cliccarlo, NON cercare scorciatoie: elenca i link all'utente (push notification + messaggio) con titolo e orario. Poi verifica con status(approval_ref).

## Rotazione temi (non ripetere a breve)
Vendi casa/rogito · affitto/locatore · APE scaduta · costi e fattori di prezzo · sopralluogo e tecnico · CURIT/caldaia · agenzie immobiliari · notaio · nuova costruzione/ristrutturazione · annuncio con classe energetica · come migliorare la classe (consigli generici) · FAQ tempi (5/3/48h) · post per zona (Varese prov., Milano ovest/centro, Como, Monza) · mini-casi "prima/dopo".
Formati: almeno 1 contenuto al giorno (reel/post/carosello e/o story); 3-4 reel a settimana, 2-3 caroselli, stories quasi ogni giorno.
