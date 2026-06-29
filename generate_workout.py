import json
import re

markdown = """
## Blocco

**Periodo:** 29 giugno 2026 → 26 luglio 2026.   
**Funzione:** pivot / resensitization upper-focused con reinserimento progressivo del petto.
**Struttura:** 4 giorni upper-focused, nessun giorno solo gambe, lower trekking integrato in ogni seduta.
**Priorità:** schiena, spalle, braccia, petto, addome; lower sempre secondario rispetto alla qualità dell’upper.

## Regole pratiche di progressione
- Se chiudi tutte le serie nel top del range con tecnica stabile e RPE in linea, la settimana dopo alzi leggermente il carico.
- Se non conviene alzare il carico, provi prima a migliorare reps, controllo o qualità delle pause tecniche.
- Se un esercizio peggiora nettamente già dalla seconda serie, non forzi la progressione: mantieni o riduci leggermente per stare dentro il target del blocco.
- Negli esercizi trekking/lower l’obiettivo non è la progressione aggressiva, ma stabilità, tolleranza locale e trasferibilità.
- Il petto progredisce con logica conservativa: prima tolleranza, poi stabilità, poi intensificazione moderata.

## Giorno 1 — Pull priority + trekking

| Esercizio | Serie | Reps | Rest | Tecnica | RPE W1 | RPE W2 | RPE W3 | RPE W4 |
|---|---:|---:|---:|---|---:|---:|---:|---:|
| Rematore bilanciere o T-bar row | 4 | 6–8 | 2:00 | Torace stabile, chiusura controllata, no cheating | 7.5 | 8 | 8.5 | 7.5 |
| Lat machine presa neutra | 3 | 8–10 | 1:45 | Eccentrica controllata, pausa 1″ in allungamento | 7.5 | 8 | 8 | 7.5 |
| Pullover ai cavi | 3 | 12–15 | 1:15 | Pausa 1″ in picco, ROM pieno | 7 | 7.5 | 8 | 7 |
| Face pull | 3 | 15 | 1:00 | Tecnico, rotazione esterna, ROM pulito | 7 | 7.5 | 8 | 7 |
| Hollow hold | 3 | 30–40″ | 1:00 | Retroversione costante, niente compensi | 7 | 7 | 7.5 | 7 |
| Step-up trekking | 3 | 8/lato | 1:00 | Spinta controllata, focus stabilità e piede | 6.5 | 7 | 7.5 | 6.5 |
| Calf raise in piedi o pressa | 2 | 15–20 | 1:00 | Pausa breve in allungo e accorcio | 7 | 7.5 | 7.5 | 7 |

## Giorno 2 — Push + chest re-entry + trekking

| Esercizio | Serie | Reps | Rest | Tecnica | RPE W1 | RPE W2 | RPE W3 | RPE W4 |
|---|---:|---:|---:|---|---:|---:|---:|---:|
| Chest press convergente o inclinata guidata | 3 | 6–8 | 2:00 | Scapole stabili, fermo breve in allungamento, traiettoria pulita | 7.5 | 8 | 8.5 | 7.5 |
| Military press seduta | 3 | 6–8 | 2:00 | Buffer 2, traiettoria pulita, niente grind | 7.5 | 8 | 8 | 7.5 |
| Alzate laterali | 4 | 12 | 1:00 | Pausa 1″ in alto, no slancio | 8 | 8 | 8.5 | 7.5 |
| Behind-the-back rear delt raise | 3 | 12–15 | 1:00 | Eccentrica 2–3″, pausa 1″ in picco | 7.5 | 8 | 8 | 7.5 |
| Pushdown corda | 2 | 10–12 | 1:15 | Pausa 1″ in contrazione | 7.5 | 8 | 8 | 7.5 |
| Dead bug | 3 | 10/lato | 1:00 | Movimento lento, lombare neutra | 7 | 7 | 7.5 | 7 |
| Split squat | 2 | 8/lato | 1:15 | Discesa controllata, assetto stabile | 7 | 7.5 | 7.5 | 6.5 |

## Giorno 3 — Upper spessore + trekking

| Esercizio | Serie | Reps | Rest | Tecnica | RPE W1 | RPE W2 | RPE W3 | RPE W4 |
|---|---:|---:|---:|---|---:|---:|---:|---:|
| Rematore cavo seduto | 4 | 8–10 | 1:45 | Pausa 1″ in chiusura | 7.5 | 8 | 8.5 | 7.5 |
| Lat machine supina o neutra | 3 | 10 | 1:30 | Tensione continua, ROM pulito | 7.5 | 8 | 8 | 7.5 |
| Kelso shrug | 3 | 12 | 1:15 | Pausa 1–2″ in retrazione scapole | 7.5 | 8 | 8 | 7.5 |
| Rear delt cable fly | 3 | 15 | 1:00 | Tensione continua, pompaggio pulito | 7.5 | 7.5 | 8 | 7 |
| Curl bilanciere | 3 | 6–8 | 2:00 | Tecnico, niente slancio | 8 | 8 | 8.5 | 7.5 |
| Pallof press | 3 | 12/lato | 1:00 | Pausa 1″ in massima tensione | 7 | 7 | 7.5 | 7 |
| Walking lunges | 2 | 10/lato | 1:00 | Passo medio, controllo ginocchio e bacino | 6.5 | 7 | 7.5 | 6.5 |
| Calf raise | 2 | 15–20 | 1:00 | Escursione piena, ritmo costante | 7 | 7.5 | 7.5 | 7 |

## Giorno 4 — Chest richiamo + arms + delts + trekking

| Esercizio | Serie | Reps | Rest | Tecnica | RPE W1 | RPE W2 | RPE W3 | RPE W4 |
|---|---:|---:|---:|---|---:|---:|---:|---:|
| Fly ai cavi basso-alto o macchina | 3 | 12–15 | 1:15 | Stretch controllato, chiusura attiva, nessun compenso di spalla | 7 | 7.5 | 8 | 7 |
| Curl inclinato manubri | 3 | 10–12 | 1:15 | Eccentrica 2–3″, ROM pulito | 8 | 8 | 8.5 | 7.5 |
| Hammer curl | 2 | 10–12 | 1:15 | Tecnico, niente slancio | 7.5 | 8 | 8 | 7.5 |
| French press EZ o cavo | 2 | 8–10 | 1:30 | Pausa 1″ in allungamento, controllo gomiti | 7.5 | 8 | 8 | 7.5 |
| Estensioni cavo singolo | 2 | 12–15 | 1:15 | Pausa 1″ in allungamento | 7.5 | 8 | 8 | 7.5 |
| Alzate laterali | 3 | 15 | 1:00 | Tensione continua, no cheating | 8 | 8 | 8.5 | 7.5 |
| Hollow hold | 3 | 30–40″ | 1:00 | Qualità prima della durata | 7 | 7 | 7.5 | 7 |
| Step-up basso o box | 2 | 10/lato | 1:00 | Ritmo costante, enfasi su stabilità | 6.5 | 7 | 7.5 | 6.5 |

## Progressioni settimanali

### Settimana 1
Settimana di **ingresso e taratura**: usi i carichi per costruire tecnica, ritmo e percezione dello sforzo, senza cercare il limite.
Sugli esercizi base di schiena e sulle spinte tieni 1–3 reps in riserva reali; sugli isolamenti cerchi soprattutto tensione continua, controllo e qualità dell’allungamento.
Il petto rientra con un obiettivo preciso: tollerare bene lo stimolo, non dimostrare subito performance.

### Settimana 2
Settimana di **progressione lineare controllata**: dove possibile aumenti leggermente il carico; se il carico non sale in modo pulito, aggiungi 1 ripetizione restando nel range previsto.
Sui multiarticolari l’obiettivo è battere W1 di poco, non stravolgere il profilo di fatica.
Sugli esercizi di isolamento puoi spingere un po’ di più la contrazione e la densità del lavoro, ma senza perdere standard tecnico.

### Settimana 3
Settimana di **picco del blocco**: qui provi a ottenere il miglior compromesso tra carico, reps e qualità, arrivando al punto più alto di stimolo del mesociclo.
Non significa grindare tutto, ma rendere produttive le serie target: sui fondamentali ti avvicini di più al limite tecnico, sugli isolamenti cerchi il massimo output controllabile.
Il petto qui dovrebbe sentirsi ormai integrato, soprattutto nel giorno 2, mentre il giorno 4 resta un richiamo utile ma meno tassante.

### Settimana 4
Settimana di **consolidamento e resensitization**: il carico può anche restare simile a W3 in alcuni esercizi, ma abbassi la percezione di sforzo effettiva e tagli l’aggressività esecutiva.
L’obiettivo non è fare un vero deload passivo, ma uscire dal blocco con buona freschezza sistemica, articolazioni tranquille e tecnica ancora pulita.
In pratica, confermi gli adattamenti ottenuti senza accumulare fatica che ti sporchi il blocco successivo.

"""

def extract(pattern, text):
    m = re.search(pattern, text, re.IGNORECASE)
    return m.group(1).strip() if m else ""

periodo = extract(r'\*\*Periodo:\*\*\s*(.*?)\n', markdown)
funzione = extract(r'\*\*Funzione:\*\*\s*(.*?)\n', markdown)
struttura = extract(r'\*\*Struttura:\*\*\s*(.*?)\n', markdown)
priorita = extract(r'\*\*Priorit[aà]:\*\*\s*(.*?)\n', markdown)

title = f"{funzione.upper().split('CON')[0].strip()} ({periodo.replace('.', '')})"
subtitle = []
if periodo: subtitle.append(f"**Periodo:** {periodo}")
if funzione: subtitle.append(f"**Funzione:** {funzione}")
if struttura: subtitle.append(f"**Struttura:** {struttura}")
if priorita: subtitle.append(f"**Priorità:** {priorita}")
subtitle.append("\n**Regole pratiche di progressione**\n" + markdown.split("## Regole pratiche di progressione")[1].split("## Giorno 1")[0].strip())
subtitle = "\n".join(subtitle)

workout = {
    "id": "pale-embedded-block-1",
    "title": title,
    "subtitle": subtitle,
    "numWeeks": 4,
    "weeklyStructure": [],
    "days": [],
    "progress": {}
}

week_blocks = re.split(r'### Settimana \d+', markdown)
if len(week_blocks) > 1:
    for i, block in enumerate(week_blocks[1:], 1):
        lines = block.strip().split('\n')
        focus = ""
        note_lines = []
        for l in lines:
            if l.startswith('Settimana di **'):
                focus = l.split('**')[1].strip() + ": " + l.split('**:')[1].strip() if '**:' in l else l
            elif l.startswith('Settimana di'):
                focus = l
            else:
                note_lines.append(l)
        
        workout["weeklyStructure"].append({
            "week": i,
            "focus": focus,
            "note": "\n".join(note_lines).strip()
        })

day_blocks = re.split(r'## Giorno \d+ — ', markdown)
if len(day_blocks) > 1:
    for block in day_blocks[1:]:
        day_name_line = block.split('\n')[0].strip()
        day = {
            "name": day_name_line,
            "exercises": []
        }
        table_lines = [l for l in block.split('\n') if l.strip().startswith('|')]
        if len(table_lines) > 2:
            headers = [h.strip().lower() for h in table_lines[0].split('|')[1:-1]]
            for row in table_lines[2:]:
                cols = [c.strip() for c in row.split('|')[1:-1]]
                if len(cols) >= 5:
                    rpe_list = []
                    for i, h in enumerate(headers):
                        if h.startswith('rpe w'):
                            rpe_list.append(cols[i])
                    
                    day["exercises"].append({
                        "name": cols[0],
                        "sets": cols[1],
                        "reps": cols[2],
                        "rest": cols[3],
                        "tecnica": cols[4],
                        "notes": cols[4],
                        "rpe": rpe_list[0] if rpe_list else "",
                        "rpeList": rpe_list,
                        "sessionData": {}
                    })
        workout["days"].append(day)

with open('default_workout.js', 'w') as f:
    f.write("const PALE_DEFAULT_WORKOUT = " + json.dumps(workout, indent=2) + ";\n")

print("Generated default_workout.js successfully!")
