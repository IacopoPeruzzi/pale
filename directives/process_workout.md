# Direttiva: Gestione Multi-Scheda e Importazione

## Obiettivo
Gestire un catalogo di schede di allenamento e permettere l'importazione rapida di nuovi piani da Perplexity tramite l'interfaccia web.

## Flusso UX
1. **Dashboard**: Visualizza l'elenco delle schede salvate come card interattive.
2. **Importazione**: Pulsante "+" che apre un'area di testo per incollare l'output di Perplexity direttamente nella Web App.
3. **Allenamento**: Visualizzazione della scheda selezionata con tracking dei progressi e persistenza.

## Strumenti di Esecuzione
1. `execution/parse_workout.py`: Motore di parsing che trasforma il testo in JSON.
2. `execution/generate_web_page.py`: Genera un'interfaccia SPA (Single Page Application) che integra Dashboard, Import e Dettaglio.

## Struttura Dati
- Le schede predefinite possono risiedere in `data/workouts/*.json`.
- Le nuove schede importate dall'utente vengono salvate nel `localStorage` del browser per immediatezza d'uso su smartphone.
