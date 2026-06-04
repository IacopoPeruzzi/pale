import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import json

# Carica l'ambiente
load_dotenv()

OLD_DB_URL = "postgresql://pale_postgres_user:12oRZWt5BtQWpM07k2r7CZj7fIGHa1Eq@dpg-d7su79gg4nts73e6n0g0-a.frankfurt-postgres.render.com/pale_postgres?sslmode=require"
NEW_DB_URL = "postgresql://postgres.kbcdxouxmgivxqsaahcf:12oRZWt5BtQWpM07k2r7CZj7fIGHa1Eq@aws-0-eu-west-1.pooler.supabase.com:6543/postgres?sslmode=require"

def migrate():
    print("Inizio migrazione database...")
    rows = []
    
    # 1. Estrazione dati dal vecchio database
    print(f"Tentativo di connessione al vecchio database Render...")
    try:
        conn_old = psycopg2.connect(OLD_DB_URL, connect_timeout=5)
        cursor_old = conn_old.cursor(cursor_factory=RealDictCursor)
        
        # Verifica se la tabella workouts esiste
        cursor_old.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'workouts'
            );
        """)
        exists = cursor_old.fetchone()['exists']
        if exists:
            cursor_old.execute("SELECT id, data FROM workouts;")
            rows = cursor_old.fetchall()
            print(f"Estratti {len(rows)} record dalla tabella 'workouts' di Render.")
        else:
            print("Tabella 'workouts' non trovata nel vecchio database.")
        conn_old.close()
    except Exception as e:
        print(f"Impossibile connettersi al vecchio database Render: {e}")
        print("Provo ad utilizzare il backup locale in .tmp/workout_data.json come fallback...")
        backup_path = ".tmp/workout_data.json"
        if os.path.exists(backup_path):
            try:
                with open(backup_path, 'r', encoding='utf-8') as f:
                    local_data = json.load(f)
                # Formattiamo nel formato id, data
                if isinstance(local_data, dict) and "id" in local_data:
                    rows = [{"id": local_data["id"], "data": local_data}]
                    print(f"Trovato record locale '{local_data['id']}' da ripristinare.")
                else:
                    print("Il file JSON locale non ha la struttura attesa.")
            except Exception as le:
                print(f"Errore lettura file locale: {le}")
        else:
            print("Nessun backup locale trovato in .tmp/workout_data.json.")

    if not rows:
        print("Nessun dato da migrare trovato. Verrà solo creata la tabella su Supabase.")

    # 2. Scrittura dati nel nuovo database su Supabase
    print(f"Connessione al nuovo database Supabase...")
    try:
        conn_new = psycopg2.connect(NEW_DB_URL)
        cursor_new = conn_new.cursor()
        
        # Crea la tabella se non esiste
        cursor_new.execute("""
            CREATE TABLE IF NOT EXISTS workouts (
                id VARCHAR(50) PRIMARY KEY,
                data JSON NOT NULL
            );
        """)
        conn_new.commit()
        print("Tabella 'workouts' creata o già esistente su Supabase.")
        
        # Inserimento/Aggiornamento dati
        inserted = 0
        for row in rows:
            data_json = json.dumps(row['data'])
            cursor_new.execute("""
                INSERT INTO workouts (id, data) 
                VALUES (%s, %s) 
                ON CONFLICT (id) 
                DO UPDATE SET data = EXCLUDED.data;
            """, (row['id'], data_json))
            inserted += 1
            
        conn_new.commit()
        print(f"Migrazione completata con successo! {inserted} record inseriti/aggiornati su Supabase.")
        conn_new.close()
    except Exception as e:
        print(f"Errore durante la scrittura dei dati su Supabase: {e}")
        return

if __name__ == "__main__":
    migrate()
