import os
import json
import re

candidate_files = [
    "/Users/iacopoperuzzi/Library/Application Support/Google/Chrome/Default/Local Storage/leveldb/087655.ldb",
    "/Users/iacopoperuzzi/Library/Application Support/Google/Chrome/Default/Local Storage/leveldb/075772.ldb",
    "/Users/iacopoperuzzi/Library/Application Support/Google/Chrome/Default/Local Storage/leveldb/087527.ldb",
    "/Users/iacopoperuzzi/Library/Application Support/Google/Chrome/Default/Local Storage/leveldb/075767.ldb",
    "/Users/iacopoperuzzi/Library/Application Support/Google/Chrome/Default/Local Storage/leveldb/075771.ldb",
    "/Users/iacopoperuzzi/Library/Application Support/Google/Chrome/Default/Local Storage/leveldb/073857.ldb",
    "/Users/iacopoperuzzi/Library/Application Support/Google/Chrome/Default/Local Storage/leveldb/086270.ldb",
    "/Users/iacopoperuzzi/Library/Application Support/Google/Chrome/Default/Local Storage/leveldb/075768.ldb",
    "/Users/iacopoperuzzi/Library/Application Support/Google/Chrome/Default/Local Storage/leveldb/073858.ldb",
    "/Users/iacopoperuzzi/Library/Application Support/Google/Chrome/Default/Local Storage/leveldb/079781.ldb",
    "/Users/iacopoperuzzi/Library/Application Support/Google/Chrome/Default/Local Storage/leveldb/079780.ldb",
    "/Users/iacopoperuzzi/Library/Application Support/Google/Chrome/Default/Local Storage/leveldb/079779.ldb",
    "/Users/iacopoperuzzi/Library/Application Support/Google/Chrome/Default/Local Storage/leveldb/087538.ldb",
    "/Users/iacopoperuzzi/Library/Application Support/Google/Chrome/Profile 9/Local Storage/leveldb/041375.ldb",
    "/Users/iacopoperuzzi/Library/Application Support/Google/Chrome/Profile 9/Local Storage/leveldb/024377.ldb",
    "/Users/iacopoperuzzi/Library/Application Support/Google/Chrome/Profile 9/Local Storage/leveldb/021012.ldb",
]

# Cerchiamo blocchi di testo che assomigliano a JSON usando regex di caratteri stampabili
# Troviamo qualsiasi stringa che inizi con '[' e finisca con ']' e contenga 'M8' o 'm8'
print("Scansione avanzata dei file LevelDB...")

for file_path in candidate_files:
    if not os.path.exists(file_path):
        continue
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        
        # Troviamo tutti i caratteri stampabili per semplificare la ricerca
        # Sostituiamo i caratteri non stampabili con spazi o li usiamo come delimitatori
        text_segments = []
        current_segment = []
        for byte in data:
            if 32 <= byte <= 126 or byte in [9, 10, 13]: # ASCII stampabile, tab, newline
                current_segment.append(chr(byte))
            else:
                if len(current_segment) > 20: # Salviamo solo segmenti con un minimo di lunghezza
                    text_segments.append("".join(current_segment))
                current_segment = []
        if len(current_segment) > 20:
            text_segments.append("".join(current_segment))

        for seg in text_segments:
            # Cerchiamo se c'è "m8" o "M8" nel segmento
            if "m8" in seg.lower() and "workout" in seg.lower():
                print(f"\nTrovato segmento interessante in {os.path.basename(file_path)}:")
                # Proviamo a estrarre un JSON da questo segmento
                # Cerchiamo una parentesi quadra aperta e proviamo a trovare una chiusa
                start_indices = [m.start() for m in re.finditer(r'\[', seg)]
                for start in start_indices:
                    # Cerchiamo di bilanciare le parentesi quadre
                    count = 0
                    for i in range(start, len(seg)):
                        if seg[i] == '[':
                            count += 1
                        elif seg[i] == ']':
                            count -= 1
                            if count == 0:
                                candidate = seg[start:i+1]
                                try:
                                    parsed = json.loads(candidate)
                                    # Se è una lista di dizionari ed ha id
                                    if isinstance(parsed, list) and len(parsed) > 0 and 'id' in parsed[0]:
                                        print(f"-> ESTRATTO JSON VALIDO!")
                                        print(json.dumps(parsed, indent=2)[:300] + "...")
                                        
                                        # Salviamo subito
                                        out_file = ".tmp/recovered_from_raw.json"
                                        with open(out_file, 'w', encoding='utf-8') as out_f:
                                            json.dump(parsed, out_f, indent=4, ensure_ascii=False)
                                        import sys
                                        sys.exit(0)
                                except Exception:
                                    pass
    except Exception as e:
        print(f"Errore {file_path}: {e}")

print("Scansione completata.")
