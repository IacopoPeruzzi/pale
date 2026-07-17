import os
import json
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv('/Users/iacopoperuzzi/Documents/projects/pale/.env')

db_url = os.environ.get('DATABASE_URL')
engine = create_engine(db_url)
with engine.connect() as conn:
    # Aggiorna il workout Fase 12
    w_id = 'p-1784324567492'
    result = conn.execute(text("SELECT data FROM workouts WHERE id = :id"), {"id": w_id})
    row = result.fetchone()
    if row:
        data_str = row[0]
        data = json.loads(data_str) if isinstance(data_str, str) else data_str

        new_subtitle = """**Periodo:** 5 settimane
**Obiettivo:** Accumulare volume ipertrofico di qualità su schiena, deltoidi, braccia e petto; costruire al tempo stesso forza-resistenza, controllo unilaterale e capacità aerobica in salita per il trekking.

**Regole Definitive:**
- Nessun cedimento tecnico: il picco massimo è RPE 8-8.5 in W3, non il fallimento.
- Niente Myo-reps, cluster, drop set, FST-7 o rest-pause.
- Se chiudi tutte le serie al top del range, con tecnica stabile e RPE sotto target, aumenti il minimo carico disponibile la settimana successiva.
- Se una serie peggiora molto rispetto alla precedente, non forzi la progressione: ripeti il carico oppure togli 1-2 reps.
- W5 non è negoziabile: nessuna serie tagliata viene recuperata, nessun cardio extra.

**Distribuzione Settimanale:**
Giorno 1: Pull spessore
Giorno 2: Push - petto e spalle
Giorno 3: Riposo
Giorno 4: Trekking specifico
Giorno 5: Riposo
Giorno 6: Braccia e deltoidi
Giorno 7: Upper richiamo selettivo
*(Il quinto allenamento è un richiamo, nessuna fatica ridondante)*"""
        
        data["subtitle"] = new_subtitle
        conn.execute(text("UPDATE workouts SET data = :data WHERE id = :id"), {"data": json.dumps(data), "id": w_id})
        print(f"Updated subtitle for {w_id}")
    
    # Ripristina pale-embedded-block-1 (parziale)
    w_id_2 = 'pale-embedded-block-1'
    result2 = conn.execute(text("SELECT data FROM workouts WHERE id = :id"), {"id": w_id_2})
    row2 = result2.fetchone()
    if row2:
        data_str2 = row2[0]
        data2 = json.loads(data_str2) if isinstance(data_str2, str) else data_str2
        data2["subtitle"] = "**Periodo:** 5 settimane\n**Obiettivo:** Desensibilizzare il lower body"
        conn.execute(text("UPDATE workouts SET data = :data WHERE id = :id"), {"data": json.dumps(data2), "id": w_id_2})
        print(f"Restored subtitle for {w_id_2}")

    conn.commit()
