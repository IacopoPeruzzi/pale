import json
from sqlalchemy import create_engine, text
engine = create_engine('postgresql://postgres.kbcdxouxmgivxqsaahcf:12oRZWt5BtQWpM07k2r7CZj7fIGHa1Eq@aws-0-eu-west-1.pooler.supabase.com:6543/postgres?sslmode=require')
with engine.connect() as conn:
    res = conn.execute(text("SELECT id, data FROM workouts")).fetchall()
    for row in res:
        id = row[0]
        data = row[1]
        if isinstance(data, str): data = json.loads(data)
        has_ws = 'weeklyStructure' in data and bool(data['weeklyStructure'])
        print(f"ID: {id}, has weeklyStructure: {has_ws}")
