import json
import re
import os

def parse_workout(text):
    # 1. Estrazione Titolo (Cerca il codice tra asterischi o dopo 'Perfetto:')
    title_match = re.search(r'(?:#|\*\*|Perfetto:)\s*\*?\*?([A-Z0-9]+)\*?\*?', text)

    workout = {
        "id": re.sub(r'[^a-z0-9]', '', title_match.group(1).lower()) if title_match else str(int(os.path.getmtime(".tmp/raw_workout.txt"))),
        "title": title_match.group(1) if title_match else "Nuova Scheda",
        "numWeeks": 4,
        "weeklyStructure": [],
        "days": [],
        "totalEx": 0
    }
    
    if not title_match:
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        if lines: workout["title"] = lines[0][:30]

    # 2. Estrazione Durata
    weeks_match = re.search(r'(\d+)\s*settimane', text, re.IGNORECASE)
    if weeks_match:
        workout["numWeeks"] = int(weeks_match.group(1))

    # 3. Estrazione Struttura Settimanale
    struct_match = re.search(r'(\| Settimana \| Focus \|.*?\|)\s*\n\s*(\|[-:| ]+\|)\s*\n((?:\|.*\|\s*\n?)+)', text, re.DOTALL)
    if struct_match:
        rows = struct_match.group(3).strip().split('\n')
        for row in rows:
            cols = [c.strip() for c in row.strip('|').split('|')]
            if len(cols) >= 2:
                workout["weeklyStructure"].append({
                    "week": cols[0],
                    "focus": cols[1],
                    "note": cols[3] if len(cols) > 3 else ""
                })

    # 4. Divisione per Giorni
    day_pattern = r'(?i)(?:^|\n)(?:##\s*|#\s*)?(Giorno\s+[A-Z\d]+|Giorno\s+extra|Day\s+\d+|Sessione\s+\d+)(?:\s*[–-]\s*(.*))?'
    sections = re.split(day_pattern, text)
    
    i = 1
    while i < len(sections):
        day_name = sections[i].strip()
        day_subtitle = sections[i+1].strip() if sections[i+1] else ""
        day_content = sections[i+2].strip()
        
        full_day_name = f"{day_name} - {day_subtitle}" if day_subtitle else day_name
        day_data = {"name": full_day_name, "exercises": []}
        
        table_match = re.search(r'(\|.*\|)\s*\n\s*(\|[-:| ]+\|)\s*\n((?:\|.*\|\s*\n?)+)', day_content)
        
        if table_match:
            header_row = table_match.group(1)
            rows = table_match.group(3).strip().split('\n')
            headers = [h.strip().lower() for h in header_row.strip('|').split('|')]
            idx = {"name": -1, "sets": -1, "reps": -1, "rest": -1, "tech": -1}
            for h_idx, h in enumerate(headers):
                if 'esercizio' in h: idx["name"] = h_idx
                elif 'serie' in h: idx["sets"] = h_idx
                elif 'reps' in h or 'ripetizioni' in h: idx["reps"] = h_idx
                elif 'recupero' in h or 'rest' in h: idx["rest"] = h_idx
                elif 'tecnica' in h or 'note' in h: idx["tech"] = h_idx

            for row in rows:
                cols = [c.strip() for c in row.strip('|').split('|')]
                if len(cols) <= max(idx.values()): continue
                ex_name = cols[idx["name"]] if idx["name"] != -1 else "Esercizio"
                if not ex_name or ex_name.startswith('---'): continue
                
                day_data["exercises"].append({
                    "name": ex_name, "sets": cols[idx["sets"]], "reps": cols[idx["reps"]], "rest": cols[idx["rest"]], "notes": cols[idx["tech"]] if idx["tech"] != -1 else ""
                })
                workout["totalEx"] += 1
        else:
            lines = day_content.split('\n')
            for line in lines:
                m = re.search(r'(\d+)\s*[xX]\s*(\d+(?:-\d+)?)', line)
                if m:
                    exercise_name = re.sub(r'(\d+)\s*[xX]\s*(\d+(?:-\d+)?)', '', line).strip(' :-*•').strip()
                    day_data["exercises"].append({
                        "name": exercise_name, "sets": m.group(1), "reps": m.group(2), "rest": "90s", "notes": ""
                    })
                    workout["totalEx"] += 1

        if day_data["exercises"]:
            workout["days"].append(day_data)
        i += 3
    return workout

if __name__ == "__main__":
    input_path = ".tmp/raw_workout.txt"
    output_path = ".tmp/workout_data.json"
    if os.path.exists(input_path):
        with open(input_path, 'r', encoding='utf-8') as f: raw_text = f.read()
        data = parse_workout(raw_text)
        with open(output_path, 'w', encoding='utf-8') as f: json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Successo: Dati estratti in {output_path}")
