import json
from sqlalchemy import create_engine, text

engine = create_engine('postgresql://postgres.kbcdxouxmgivxqsaahcf:12oRZWt5BtQWpM07k2r7CZj7fIGHa1Eq@aws-0-eu-west-1.pooler.supabase.com:6543/postgres?sslmode=require')
with engine.connect() as conn:
    res = conn.execute(text("SELECT data FROM workouts WHERE id='p-1779905883419'")).fetchone()
    if res:
        data = res[0]
        if isinstance(data, str): data = json.loads(data)
        
        # Aggiungiamo la weeklyStructure
        data['weeklyStructure'] = [
            {"week": "W1", "focus": "Entrata", "note": "Familiarizzazione"},
            {"week": "W2", "focus": "Progressione", "note": "+1-2 reps o piccolo incremento"},
            {"week": "W3", "focus": "Picco", "note": "Settimana più densa"},
            {"week": "W4", "focus": "Deload", "note": "-40% serie, no tecniche"}
        ]
        
        # Aggiorniamo il db
        conn.execute(text("UPDATE workouts SET data = :data WHERE id='p-1779905883419'"), {"data": json.dumps(data)})
        conn.commit()
        print("Success: DB patched!")
    else:
        print("Workout not found.")
