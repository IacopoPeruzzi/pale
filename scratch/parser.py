import re
import json
import time
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv('/Users/iacopoperuzzi/Documents/projects/pale/.env')

markdown_path = "/Users/iacopoperuzzi/Documents/projects/pale/scratch/fase12.md"
with open(markdown_path, 'r', encoding='utf-8') as f:
    raw = f.read()

lines = raw.split('\n')
titleStr = "FASE 12 (ACCUMULO FUNZIONALE)"

w = {
    "id": f"p-{int(time.time()*1000)}",
    "title": titleStr,
    "subtitle": "**Periodo:** 5 settimane\n**Obiettivo:** accumulare volume ipertrofico di qualità su schiena, deltoidi, braccia e petto...",
    "days": [],
    "numWeeks": 5,
    "progress": {},
    "weeklyStructure": []
}

structMatch = re.search(r'\|\s*Settimana\s*\|.*?\n\|\s*[-:| ]+\s*\|\n((?:\|.*\|\s*\n?)+)', raw, re.IGNORECASE)
if structMatch:
    rows = structMatch.group(1).strip().split('\n')
    for r in rows:
        cols = [c.strip() for c in r.split('|') if c.strip()]
        if len(cols) >= 2:
            week_num = int(re.sub(r'\D', '', cols[0]) or 1)
            w["weeklyStructure"].append({
                "week": week_num,
                "focus": cols[1],
                "note": cols[3] if len(cols) > 3 else (cols[2] if len(cols) > 2 else "")
            })

curD = None
readingDays = True

for l in lines:
    l = l.strip()
    dayMatch = re.match(r'^##\s*Giorno\s*\d+\s*[—\-]\s*(.*)', l, re.IGNORECASE)
    if dayMatch:
        if curD:
            w["days"].append(curD)
        curD = {"name": dayMatch.group(1).strip(), "exercises": []}
        readingDays = True
        continue
    
    if curD and readingDays and l.startswith('|') and 'Esercizio' not in l and not re.match(r'^\|\s*[-:| ]+\s*\|$', l):
        cols = [c.strip() for c in l.split('|') if c.strip()]
        if len(cols) >= 4:
            reps = cols[1]
            sets = "1"
            setRepMatch = re.match(r'(\d+)\s*[xX]\s*(.*)', reps)
            if setRepMatch:
                sets = setRepMatch.group(1).strip()
                reps = setRepMatch.group(2).strip()
            
            rpeList = []
            if len(cols) >= 5:
                for k in range(4, len(cols)):
                    if re.search(r'[\d\.\-\–]+', cols[k]):
                        rpeList.append(cols[k])
            
            curD["exercises"].append({
                "name": cols[0],
                "sets": sets,
                "reps": reps,
                "rest": cols[2],
                "tecnica": cols[3],
                "rpe": rpeList[0] if rpeList else "",
                "rpeList": rpeList,
                "sessionData": {}
            })

if curD:
    w["days"].append(curD)

if not w["weeklyStructure"] and w["days"] and w["days"][0]["exercises"]:
    w["numWeeks"] = len(w["days"][0]["exercises"][0]["rpeList"]) or 5

db_url = os.environ.get('DATABASE_URL')
if not db_url:
    print("No DATABASE_URL in .env")
else:
    engine = create_engine(db_url)
    with engine.connect() as conn:
        conn.execute(text("INSERT INTO workouts (id, data) VALUES (:id, :data)"), {"id": w["id"], "data": json.dumps(w)})
        conn.commit()
    print(f"Successfully inserted workout {w['id']} into Supabase DB.")
