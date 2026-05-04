# Direttiva: Utilizzo dell'App Pale

## Workflow Quotidiano
1. **Input**: Incolla il testo di Perplexity in `.tmp/raw_workout.txt`.
2. **Generazione**: Esegui `python3 execution/parse_workout.py && python3 execution/generate_web_page.py`.
3. **Sincronizzazione**: La pagina `index.html` viene aggiornata istantaneamente.

## Accesso da Mobile
- **Server Locale**: `python3 -m http.server 8000`
- **Indirizzo**: `http://<IP-DEL-MAC>:8000`

## Note Tecniche
- Il design è ottimizzato per Safari/Chrome su iOS e Android.
- I dati intermedi sono salvati in `.tmp/workout_data.json` per facilitare eventuali modifiche manuali.
