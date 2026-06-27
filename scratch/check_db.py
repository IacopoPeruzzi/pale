import os
import sys
from sqlalchemy import create_engine, text
engine = create_engine('postgresql://postgres.kbcdxouxmgivxqsaahcf:12oRZWt5BtQWpM07k2r7CZj7fIGHa1Eq@aws-0-eu-west-1.pooler.supabase.com:6543/postgres?sslmode=require')
with engine.connect() as conn:
    res = conn.execute(text("SELECT data FROM workouts LIMIT 1")).fetchone()
    if res:
        import json
        data = res[0]
        if isinstance(data, str): data = json.loads(data)
        print(json.dumps(data.get('weeklyStructure'), indent=2))
    else:
        print("No workouts found.")
