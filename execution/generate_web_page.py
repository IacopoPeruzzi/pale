import json
import os

def generate_html():
    parsed_workout = None
    json_path = ".tmp/workout_data.json"
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            parsed_workout = json.load(f)
    
    title = "Pale App"
    
    html_template = f"""
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/sortablejs@1.15.0/Sortable.min.js"></script>
    <style>
        :root {{
            --bg-color: #ffffff;
            --accent-color: #000000;
            --highlight-yellow: #FFE600;
            --highlight-purple: #DDB8FF;
            --highlight-pink: #FF85C0;
            --text-primary: #000000;
            --text-secondary: #444;
            --border-thickness: 3px;
            --hard-shadow: 4px 4px 0px var(--accent-color);
            --hard-shadow-active: 0px 0px 0px var(--accent-color);
            --safe-area-top: env(safe-area-inset-top);
        }}

        * {{ box-sizing: border-box; -webkit-tap-highlight-color: transparent; outline: none; }}
        body {{
            background-color: var(--bg-color);
            background-image: 
                linear-gradient(rgba(0,0,0,0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0,0,0,0.05) 1px, transparent 1px);
            background-size: 20px 20px;
            color: var(--text-primary);
            font-family: 'Outfit', sans-serif;
            margin: 0; padding: 0; overflow-x: hidden;
        }}

        .view {{ display: none; padding: 0 20px 140px 20px; min-height: 100vh; position: relative; z-index: 10; }}
        .view.active {{ display: block; }}

        .sticky-header {{
            position: sticky; top: 0; 
            padding: calc(30px + var(--safe-area-top)) 0px 15px 0px;
            margin: 0 0 20px 0;
            background: var(--bg-color);
            border-bottom: var(--border-thickness) solid var(--accent-color);
            z-index: 1000;
        }}

        h1 {{ font-size: 3rem; font-weight: 900; margin: 0; letter-spacing: -1.5px; text-transform: uppercase; line-height: 0.85; }}
        h1 .highlight {{ background: var(--highlight-yellow); padding: 0 8px; border: var(--border-thickness) solid #000; border-radius: 8px; display: inline-block; transform: rotate(-2deg); margin-left: 5px; }}
        
        h2 {{ font-size: 1.8rem; font-weight: 900; margin: 0; letter-spacing: -1px; text-transform: uppercase; }}
        h3 {{ font-size: 0.8rem; font-weight: 900; text-transform: uppercase; letter-spacing: 1.5px; color: var(--text-primary); margin: 30px 0 15px 0; display: flex; align-items: center; justify-content: space-between; }}

        .subtitle {{ font-weight: 800; text-transform: uppercase; font-size: 0.75rem; margin-top: 10px; color: #444; }}

        .resume-card {{
            background: var(--highlight-yellow);
            border: var(--border-thickness) solid var(--accent-color);
            border-radius: 15px; padding: 24px; margin: 0 0 25px 0;
            box-shadow: 6px 6px 0px #000;
            cursor: pointer; color: #000; position: relative;
            transition: 0.1s;
        }}
        .resume-card:active {{ transform: translate(4px, 4px); box-shadow: 2px 2px 0px #000; }}
        .resume-card h2 {{ font-size: 1.5rem; margin-bottom: 8px; }}
        .resume-card p {{ font-size: 0.9rem; font-weight: 700; margin: 0; }}

        .list-card {{ 
            background: #fff; 
            border: var(--border-thickness) solid var(--accent-color); 
            border-radius: 12px; 
            padding: 16px; 
            margin-bottom: 12px; 
            box-shadow: var(--hard-shadow); 
            display: flex; align-items: center; cursor: pointer; transition: 0.1s;
        }}
        .list-card:active {{ transform: translate(2px, 2px); box-shadow: 2px 2px 0px #000; }}
        .list-card.completed {{ background: var(--highlight-purple); }}

        .week-grid {{ display: flex; gap: 8px; margin-bottom: 20px; overflow-x: auto; padding-bottom: 10px; }}
        .week-btn {{ 
            flex: 0 0 70px; padding: 12px; 
            background: #fff; border: 2px solid #000; border-radius: 12px; 
            font-weight: 900; text-align: center; cursor: pointer;
            box-shadow: 3px 3px 0px #000;
        }}
        .week-btn.active {{ background: var(--highlight-yellow); transform: translate(2px, 2px); box-shadow: 1px 1px 0px #000; }}

        .ex-item {{ 
            background: #fff; border: var(--border-thickness) solid #000; 
            border-radius: 12px; padding: 15px; margin-bottom: 10px; 
            box-shadow: var(--hard-shadow); display: flex; align-items: center; cursor: pointer;
        }}
        .ex-item.done {{ background: #eee; box-shadow: none; transform: translate(4px, 4px); opacity: 0.7; }}
        
        .metric-box {{ background: #fff; border: 2px solid #000; padding: 12px; border-radius: 12px; box-shadow: 3px 3px 0px #000; }}
        
        .set-block {{ background: #fff; border: var(--border-thickness) solid #000; border-radius: 15px; padding: 15px; margin-bottom: 15px; box-shadow: var(--hard-shadow); }}
        .set-circle {{ 
            width: 40px; height: 40px; border: 2px solid #000; border-radius: 50%; 
            display: flex; align-items: center; justify-content: center; font-weight: 900;
            box-shadow: 2px 2px 0px #000; cursor: pointer;
        }}
        .set-circle.active {{ background: var(--highlight-purple); transform: translate(2px, 2px); box-shadow: none; }}

        .load-input {{ border: none; border-bottom: 3px solid #000; font-weight: 900; font-size: 1.1rem; width: 60px; text-align: center; }}
        
        .nav-dock {{ position: fixed; bottom: 0; left: 0; width: 100%; padding: 20px; background: rgba(255,255,255,0.9); border-top: var(--border-thickness) solid #000; display: flex; gap: 10px; z-index: 1000; }}
        .btn {{ 
            flex: 1; border: var(--border-thickness) solid #000; padding: 16px; border-radius: 50px; 
            font-weight: 900; text-transform: uppercase; font-size: 0.9rem; cursor: pointer; 
            box-shadow: var(--hard-shadow); transition: 0.1s;
        }}
        .btn:active {{ transform: translate(4px, 4px); box-shadow: none; }}
        .btn-main {{ background: var(--highlight-purple); }}
        .btn-alt {{ background: #fff; }}

        .progress-container {{ width: 100%; height: 12px; background: #fff; border: 2px solid #000; border-radius: 10px; margin: 15px 0; overflow: hidden; box-shadow: 2px 2px 0px #000; }}
        .progress-bar {{ height: 100%; background: var(--highlight-yellow); transition: width 0.8s ease; }}
        .action-btn {{ position: absolute; top: calc(35px + var(--safe-area-top)); right: 0px; padding: 6px 12px; border: 2px solid #000; border-radius: 8px; background: #fff; font-weight: 900; font-size: 0.6rem; text-transform: uppercase; cursor: pointer; box-shadow: 2px 2px 0px #000; }}
        .action-btn.danger {{ background: var(--highlight-pink); }}
        
        #toast {{ 
            position: fixed; top: 20px; left: 50%; transform: translateX(-50%); 
            background: var(--highlight-pink); border: 2px solid #000; padding: 10px 20px; 
            font-weight: 900; border-radius: 10px; box-shadow: 4px 4px 0px #000; z-index: 9999; display: none;
        }}
        .floating-add {{ position: fixed; bottom: 40px; right: 25px; width: 70px; height: 70px; background: var(--highlight-yellow); border: var(--border-thickness) solid #000; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; color: #000; box-shadow: 4px 4px 0px #000; z-index: 1000; cursor: pointer; transition: 0.1s; }}
        .floating-add:active {{ transform: translate(2px, 2px); box-shadow: 2px 2px 0px #000; }}
    </style>
</head>
<body>
    <div id="toast"></div>

    <div id="view-home" class="view active">
        <div class="sticky-header"><h1>PALE<br><span class="highlight">APP</span></h1><p class="subtitle">Peak Performance Hub.</p></div>
        
        <div id="progress-info" class="progress-monitor"></div>
        <div id="resume-section"></div>
        
        <h3>I TUOI PIANI <div id="manage-btn" class="manage-toggle" onclick="toggleManageMode()">GESTISCI</div></h3>
        <div id="workouts-list"></div>
        
        <div onclick="showView('view-import')" class="floating-add">+</div>
    </div>

    <!-- Resto delle View invariate... -->
    <div id="view-import" class="view">
        <div class="sticky-header"><div onclick="showView('view-home')" style="font-weight:900; cursor:pointer; margin-bottom:8px; text-transform:uppercase; font-size:0.7rem;">← BACK</div><h1>Import</h1></div>
        <textarea id="import-text" style="width: 100%; height: 300px; background: #fff; color: #000; border-radius: 12px; padding: 20px; border: var(--border-thickness) solid #000; margin: 15px 0; font-weight: 800; font-family:inherit;" placeholder="Paste protocol..."></textarea>
        <button id="import-btn" class="btn btn-main" style="width: 100%" onclick="importAction()">INITIALIZE</button>
    </div>

    <div id="view-plan" class="view">
        <div class="sticky-header">
            <div onclick="showView('view-home')" style="font-weight:900; cursor:pointer; margin-bottom:8px; text-transform:uppercase; font-size:0.7rem;">← DASHBOARD</div>
            <h2 id="plan-title">Protocol</h2>
            <div class="progress-container"><div class="progress-bar" id="total-progress-bar"></div></div>
            <div class="week-grid" id="week-selector"></div>
        </div>
        <div class="day-grid" id="day-list"></div>
    </div>

    <div id="view-session" class="view">
        <div class="sticky-header">
            <div onclick="openWorkout(currentWorkoutIndex)" style="font-weight:900; cursor:pointer; margin-bottom:8px; text-transform:uppercase; font-size:0.7rem;">← PIANO</div>
            <h2 id="session-title">Day X</h2>
            <div class="action-btn danger" onclick="resetDayAction()">Reset</div>
            <p class="subtitle" id="session-subtitle">Week 1</p>
            <div id="session-focus-container" style="margin-top:12px;"></div>
        </div>
        <div id="exercise-list"></div>
        <div class="nav-dock"><button class="btn btn-main" onclick="finishSession()">CONCLUDI SESSIONE</button></div>
    </div>

    <div id="view-exercise" class="view">
        <div class="sticky-header">
            <div onclick="startSession(currentDayIdx)" style="font-weight:900; cursor:pointer; margin-bottom:8px; text-transform:uppercase; font-size:0.7rem;">← LISTA</div>
            <h2 id="ex-detail-name">Exercise Name</h2>
            <div class="action-btn danger" onclick="resetExAction()">Reset</div>
            <p class="subtitle" id="ex-detail-meta">Serie 1 di 4</p>
        </div>
        <div class="metrics-grid">
            <div class="metric-box"><div class="metric-label">Serie</div><div class="metric-value" id="val-sets">4</div></div>
            <div class="metric-box"><div class="metric-label">Reps</div><div class="metric-value" id="val-reps">---</div></div>
            <div class="metric-box"><div class="metric-label">Rest</div><div class="metric-value" id="val-rest">90"</div></div>
        </div>
        <div id="sets-blocks-container"></div>
        <div class="session-notes-box" style="background:#fff; border:var(--border-thickness) solid #000; border-radius:12px; padding:20px; box-shadow:var(--hard-shadow); margin-top:20px;">
            <label style="font-weight:900; font-size:0.7rem; color:#000; display:block; margin-bottom:10px;">NOTE DI SESSIONE</label>
            <textarea class="session-notes-textarea" id="session-notes" placeholder="Com'è andata oggi?" oninput="updateSessionNotes()" style="width:100%; border:none; background:transparent; font-weight:700; font-family:inherit; min-height:80px;"></textarea>
        </div>
        <div class="nav-dock"><button class="btn btn-main" onclick="nextExercise()">PROSSIMO</button></div>
    </div>

    <script>
        let workouts = JSON.parse(localStorage.getItem('pale_workouts') || '[]');
        let manageMode = false;
        let currentWorkoutIndex = null;
        let currentWeek = 1;
        let currentDayIdx = null;
        let currentExIdx = null;

        async function init() {{
            try {{
                const res = await fetch('/api/workouts');
                if (res.ok) {{
                    const data = await res.json();
                    if (data && data.length > 0) {{
                        workouts = data;
                        localStorage.setItem('pale_workouts', JSON.stringify(workouts));
                        renderHome();
                    }}
                }}
            }} catch(e) {{ console.error("Load error:", e); }}
        }}
        init();

        function showToast(msg) {{
            const t = document.getElementById('toast');
            t.innerText = msg; t.style.display = 'block';
            setTimeout(() => t.style.display = 'none', 3000);
        }}

        function getInc(w) {{
            if(!w.days) return null;
            for(let w_i=1; w_i<=w.numWeeks; w_i++) {{
                for(let d_i=0; d_i<w.days.length; d_i++) {{
                    if(!w.progress || !w.progress[w_i] || !w.progress[w_i][d_i]) return {{ week: w_i, day: d_i }};
                }}
            }}
            return null;
        }}

        function showView(id) {{
            document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
            document.getElementById(id).classList.add('active');
            window.scrollTo(0,0);
        }}

        function toggleManageMode() {{
            manageMode = !manageMode;
            const btn = document.getElementById('manage-btn');
            btn.innerText = manageMode ? 'FINE' : 'GESTISCI';
            btn.classList.toggle('active', manageMode);
            renderHome();
        }}

        function renderHome() {{
            const progInfo = document.getElementById('progress-info');
            progInfo.innerHTML = '';
            
            const res = document.getElementById('resume-section');
            res.innerHTML = '';

            if (workouts.length > 0) {{
                const w = workouts[0];
                const n = getInc(w);
                
                // Calcolo progressi semplici
                let t = w.numWeeks * (w.days?w.days.length:0);
                let d = 0;
                if (w.progress) Object.values(w.progress).forEach(wk => d += Object.keys(wk).length);
                let perc = t ? Math.round((d/t)*100) : 0;
                let left = t - d;

                progInfo.innerHTML = `COMPLETATO: ${{perc}}% • MANCANO ${{left}} SESSIONI`;

                if (n) {{
                    let titleStr = sanitize(w.title);
                    if(w.subtitle) titleStr += " - " + sanitize(w.subtitle);
                    res.innerHTML = `
                        <div class="resume-card" onclick="resumeWorkout(0)">
                            <small>Continua</small>
                            <h2>${{titleStr}}</h2>
                            ${{w.goal ? `<p>${{w.goal}}</p>` : ''}}
                            <div style="margin-top:15px; font-weight:900; font-size:0.65rem; opacity:0.5;">W${{n.week}} • GIORNO ${{n.day+1}}</div>
                            <div class="play-icon">▶</div>
                        </div>`;
                }}
            }}

            const list = document.getElementById('workouts-list');
            list.innerHTML = workouts.length === 0 ? '<p style="opacity:0.3; text-align:center; padding:20px;">Nessun piano caricato.</p>' : '';
            workouts.forEach((w, i) => {{
                const card = document.createElement('div');
                card.className = `list-card ${{manageMode ? 'manage-mode' : ''}}`;
                card.onclick = () => {{ if(!manageMode) openWorkout(i); }};
                card.innerHTML = `
                    <div style="flex:1">
                        <b>${{w.title}}</b><br>
                        <small style="opacity:0.5">${{w.subtitle || "Senza sottotitolo"}}</small>
                    </div>
                    <div class="delete-btn" onclick="event.stopPropagation(); deleteWorkout(${{i}})">🗑️</div>
                `;
                list.appendChild(card);
            }});
        }}

        function resumeWorkout(idx) {{ const w = workouts[idx]; const n = getInc(w); currentWorkoutIndex = idx; if(n) {{ currentWeek = n.week; startSession(n.day); }} else openWorkout(idx); }}
        function sanitize(str) {{ return str ? str.replace(/^[#\\*\\s\\-\\–\\—]+/g, '').replace(/[#\\*\\-\\–\\—\\s]+$/g, '').trim() : ""; }}
        function cleanMD(str) {{ return str ? str.replace(/\\*\\*/g, '').trim() : ""; }}
        function cleanSources(str) {{ return str ? str.replace(/\\[[\\d,\\s]+\\]/g, '').trim() : ""; }}
        function openWorkout(idx) {{ currentWorkoutIndex = idx; const w = workouts[idx]; const n = getInc(w); if(!currentWeek) currentWeek = n ? n.week : 1; document.getElementById('plan-title').innerText = sanitize(w.title); updateProg(w); const sel = document.getElementById('week-selector'); sel.innerHTML = ''; for(let i=1; i<=w.numWeeks; i++) {{ const b = document.createElement('div'); b.className = `week-btn ${{currentWeek === i ? 'active' : ''}}`; b.innerHTML = `W${{i}}`; b.onclick = () => {{ currentWeek = i; openWorkout(idx); }}; sel.appendChild(b); }} const dList = document.getElementById('day-list'); dList.innerHTML = ''; w.days.forEach((d, dI) => {{ const status = w.progress && w.progress[currentWeek] && w.progress[currentWeek][dI]; const c = document.createElement('div'); c.className = `list-card ${{status ? 'completed' : ''}}`; c.onclick = () => startSession(dI); c.innerHTML = `<div style="flex:1"><small style="color:var(--accent-color)">GIORNO ${{dI+1}}</small><br><b>${{sanitize(d.name)}}</b></div>`; dList.appendChild(c); }}); showView('view-plan'); }}
        function startSession(dI) {{
            currentDayIdx = dI;
            const w = workouts[currentWorkoutIndex];
            const d = w.days[dI];
            document.getElementById('session-title').innerText = `GIORNO ${{dI + 1}}`;
            document.getElementById('session-subtitle').innerText = `WEEK ${{currentWeek}} • ${{sanitize(d.name)}}`;
            const focus = document.getElementById('session-focus-container');
            const str = w.weeklyStructure?.find(s => s.week === 'W' + currentWeek);
            focus.innerHTML = str ? `<div style="background:rgba(207,255,4,0.08); padding:12px; border-radius:15px; border:1px solid var(--accent-color); font-size:0.8rem;"><b>FOCUS</b>: ${{str.note || str.focus}}</div>` : '';
            const list = document.getElementById('exercise-list');
            list.innerHTML = '';
            d.exercises.forEach((ex, eI) => {{
                const isD = ex.sessionData && ex.sessionData[currentWeek] && ex.sessionData[currentWeek].completed;
                const item = document.createElement('div');
                item.className = `ex-item ${{isD ? 'done' : ''}}`;
                item.onclick = () => openExercise(eI);
                item.innerHTML = `<div class="ex-item-name">${{sanitize(ex.name)}}</div><div style="font-size:0.8rem; opacity:0.5">${{ex.sets}} SETS</div>`;
                list.appendChild(item);
            }});
            showView('view-session');
        }}

        function openExercise(eI) {{
            try {{
                currentExIdx = eI;
                const w = workouts[currentWorkoutIndex];
                const ex = w.days[currentDayIdx].exercises[eI];
                if (!ex.sessionData) ex.sessionData = {{}};
                if (!ex.sessionData[currentWeek]) ex.sessionData[currentWeek] = {{ completed: false, rounds: [], notes: "" }};
                
                const data = ex.sessionData[currentWeek];
                if (!data.rounds) data.rounds = [];
                
                let subExs = [];
                const hasPlus = ex.notes && ex.notes.includes('+');
                const isCircuit = ex.name.toLowerCase().includes('circuito') || ex.name.toLowerCase().includes('superserie');
                
                if (ex.notes && (hasPlus || isCircuit)) {{
                    subExs = ex.notes.split('+').map(s => {{
                        const clean = s.trim();
                        if (!clean) return null;
                        const m = clean.match(/(.*?)\s*(\d+.*)/);
                        return {{ name: m ? m[1].trim() : clean, reps: m ? m[2].trim() : "" }};
                    }}).filter(x => x !== null);
                }}
                if (subExs.length === 0) {{
                    subExs = [{{ name: sanitize(ex.name), reps: ex.reps }}];
                }}
                
                const nR = parseInt(ex.sets) || 1;
                while (data.rounds.length < nR) {{
                    data.rounds.push({{ done: false, subLoads: new Array(subExs.length).fill("") }});
                }}
                
                data.rounds.forEach(r => {{
                    if (r.subLoads.length < subExs.length) {{
                        while (r.subLoads.length < subExs.length) r.subLoads.push("");
                    }}
                }});

                // Weight Suggestion Logic
                const numWeeks = w.numWeeks;
                const isLastWeek = (currentWeek === numWeeks && numWeeks > 1);
                
                data.rounds.forEach((round, rIdx) => {{
                    round.subLoads.forEach((load, sI) => {{
                        if (load === "") {{
                            let suggested = "";
                            if (currentWeek > 1) {{
                                const prevData = ex.sessionData[currentWeek - 1];
                                if (prevData && prevData.rounds && prevData.rounds[rIdx] && prevData.rounds[rIdx].subLoads[sI]) {{
                                    suggested = prevData.rounds[rIdx].subLoads[sI];
                                }}
                            }}
                            if (suggested !== "") {{
                                if (isLastWeek) {{
                                    let val = parseFloat(suggested);
                                    if (!isNaN(val)) {{
                                        suggested = (val * 0.8).toFixed(1).replace(/\.0$/, "");
                                    }}
                                }}
                                round.subLoads[sI] = suggested;
                            }}
                        }}
                    }});
                }});

                document.getElementById('ex-detail-name').innerText = sanitize(ex.name);
                document.getElementById('val-sets').innerText = ex.sets;
                document.getElementById('val-reps').innerText = subExs.length > 1 ? "Circuito" : ex.reps;
                document.getElementById('val-rest').innerText = ex.rest;
                document.getElementById('session-notes').value = data.notes || "";
                
                const container = document.getElementById('sets-blocks-container');
                container.innerHTML = '';
                
                data.rounds.forEach((round, rI) => {{
                    const block = document.createElement('div');
                    block.className = 'set-block';
                    let subHtml = '';
                    subExs.forEach((sx, sI) => {{
                        subHtml += `<div class="sub-ex-row">
                            <div class="sub-ex-info">
                                <div class="sub-ex-name">${{sx.name}}</div>
                                <div class="sub-ex-reps">${{sx.reps}}</div>
                            </div>
                            <div class="load-input-wrap">
                                <input type="number" class="load-input" value="${{round.subLoads[sI] || ""}}" placeholder="---" oninput="updateSubLoad(${{rI}}, ${{sI}}, this.value)">
                                <span class="load-unit">KG</span>
                            </div>
                        </div>`;
                    }});
                    block.innerHTML = `<div class="set-header">
                        <div class="set-circle ${{round.done ? 'active' : ''}}" onclick="toggleRound(${{rI}})">${{rI + 1}}</div>
                        <div style="font-weight:800; font-size:0.8rem; color:var(--text-secondary)">${{subExs.length > 1 ? 'GIRO COMPLETO' : 'SERIE'}}</div>
                    </div>
                    <div class="sub-ex-list">${{subHtml}}</div>`;
                    container.appendChild(block);
                }});
                
                updateExMeta();
                showView('view-exercise');
            }} catch (e) {{
                console.error(e);
                showToast("Errore apertura esercizio.");
            }}
        }}
        function toggleRound(rI) {{ const data = workouts[currentWorkoutIndex].days[currentDayIdx].exercises[currentExIdx].sessionData[currentWeek]; data.rounds[rI].done = !data.rounds[rI].done; save(); openExercise(currentExIdx); }}
        function updateSubLoad(rI, sI, val) {{ const data = workouts[currentWorkoutIndex].days[currentDayIdx].exercises[currentExIdx].sessionData[currentWeek]; data.rounds[rI].subLoads[sI] = val; save(); }}
        function updateSessionNotes() {{ const val = document.getElementById('session-notes').value; const data = workouts[currentWorkoutIndex].days[currentDayIdx].exercises[currentExIdx].sessionData[currentWeek]; data.notes = val; save(); }}
        function updateExMeta() {{ const data = workouts[currentWorkoutIndex].days[currentDayIdx].exercises[currentExIdx].sessionData[currentWeek]; const done = data.rounds.filter(r => r.done).length; document.getElementById('ex-detail-meta').innerText = `${{done}} di ${{data.rounds.length}} completati`; data.completed = (done === data.rounds.length); save(); }}
        function nextExercise() {{ const d = workouts[currentWorkoutIndex].days[currentDayIdx]; if(currentExIdx < d.exercises.length - 1) openExercise(currentExIdx + 1); else startSession(currentDayIdx); }}
        function resetDayAction() {{ if(confirm('Resettare il giorno?')) {{ const d = workouts[currentWorkoutIndex].days[currentDayIdx]; d.exercises.forEach(ex => {{ if(ex.sessionData) delete ex.sessionData[currentWeek]; }}); if(workouts[currentWorkoutIndex].progress && workouts[currentWorkoutIndex].progress[currentWeek]) delete workouts[currentWorkoutIndex].progress[currentWeek][currentDayIdx]; save(); startSession(currentDayIdx); }} }}
        function resetExAction() {{ if(confirm('Resettare esercizio?')) {{ const ex = workouts[currentWorkoutIndex].days[currentDayIdx].exercises[currentExIdx]; if(ex.sessionData) delete ex.sessionData[currentWeek]; save(); openExercise(currentExIdx); }} }}
        function finishSession() {{ const w = workouts[currentWorkoutIndex]; if (!w.progress) w.progress = {{}}; if (!w.progress[currentWeek]) w.progress[currentWeek] = {{}}; w.progress[currentWeek][currentDayIdx] = true; save(); exportToCSV(); showToast("SALVATA!"); openWorkout(currentWorkoutIndex); }}
        function exportToCSV() {{ const w = workouts[currentWorkoutIndex]; const d = w.days[currentDayIdx]; let csv = "Data,Piano,Settimana,Giorno,Esercizio,SottoEsercizio,Giro,Carico,Note\\n"; const date = new Date().toLocaleDateString(); d.exercises.forEach(ex => {{ const data = ex.sessionData && ex.sessionData[currentWeek]; if(data) {{ data.rounds.forEach((round, rI) => {{ round.subLoads.forEach((load, sI) => {{ csv += `"${{date}}","${{w.title}}","W${{currentWeek}}","${{sanitize(d.name)}}","${{sanitize(ex.name)}}","Set ${{sI+1}}",${{rI+1}},"${{load}}","${{(data.notes||'').replace(/"/g, '""')}}"\\n`; }}); }}); }} }}); const blob = new Blob([csv], {{ type: 'text/csv' }}); const url = window.URL.createObjectURL(blob); const a = document.createElement('a'); a.setAttribute('hidden', ''); a.setAttribute('href', url); a.setAttribute('download', `workout_log_${{new Date().getTime()}}.csv`); document.body.appendChild(a); a.click(); document.body.removeChild(a); }}
        function save() {{
            localStorage.setItem('pale_workouts', JSON.stringify(workouts));
            if (currentWorkoutIndex !== null) {{
                const w = workouts[currentWorkoutIndex];
                fetch('/api/workouts', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify(w)
                }}).catch(err => console.error("Sync error:", err));
            }}
        }}

        function deleteWorkout(i) {{
            if(confirm('ELIMINARE IL PIANO?')) {{
                const id = workouts[i].id;
                workouts.splice(i, 1);
                localStorage.setItem('pale_workouts', JSON.stringify(workouts));
                renderHome();
                fetch(`/api/workouts/${{id}}`, {{ method: 'DELETE' }}).catch(err => console.error("Delete error:", err));
            }}
        }}

        function importAction() {{
            const raw = document.getElementById('import-text').value;
            if(!raw.trim()) return;
            const btn = document.getElementById('import-btn');
            btn.innerText = "IMPORTING..."; btn.disabled = true;
            setTimeout(() => {{
                const w = {{ id: "p-" + Date.now(), title: "", subtitle: "", goal: "", numWeeks: 4, weeklyStructure: [], days: [], progress: {{}} }};
                let cleanText = raw;
                const fontiIdx = raw.toLowerCase().lastIndexOf('fonti');
                if(fontiIdx !== -1) cleanText = raw.substring(0, fontiIdx);
                const lines = cleanText.split('\\n');
                let inMesociclo = false;
                for(let i = 0; i < lines.length; i++) {{
                    const line = lines[i].trim();
                    if(line.toLowerCase().includes('mesociclo')) {{ inMesociclo = true; continue; }}
                    if(inMesociclo) {{
                        if(line.startsWith('##')) {{ inMesociclo = false; continue; }}
                        if(line.includes('**') && (line.includes('–') || line.includes('-')) && !line.toLowerCase().includes('obiettivo')) {{
                            const clean = line.replace(/^[-•\\*\\s]+/, '').replace(/[\\*\\s]+$/, '').trim();
                            const parts = clean.split(/[–-]/);
                            if(parts.length >= 1) w.title = cleanMD(parts[0]);
                            if(parts.length >= 2) w.subtitle = cleanMD(parts.slice(1).join('-'));
                        }}
                        if(line.toLowerCase().includes('obiettivo:')) {{
                            let fullGoal = line.replace(/^[-•\\*\\s]+/, '').replace(/obiettivo:/i, '').replace(/[\\*\\s]+$/, '').trim();
                            let next = i + 1;
                            while(next < lines.length && !lines[next].trim().startsWith('-') && !lines[next].trim().startsWith('•') && !lines[next].trim().startsWith('##')) {{
                                let nextLine = lines[next].trim();
                                if(nextLine !== "") fullGoal += " " + nextLine;
                                next++;
                            }}
                            w.goal = cleanMD(cleanSources(fullGoal));
                            i = next - 1;
                        }}
                    }}
                }}
                if(!w.title) w.title = "M7 PROTOCOL";
                const wMatch = cleanText.match(/(\\d+)\\s*settimane/i);
                if(wMatch) w.numWeeks = parseInt(wMatch[1]);
                let structureTable = []; let inStructureTable = false;
                lines.forEach(l => {{ if(l.includes('| Settimana |')) inStructureTable = true; else if(inStructureTable && l.includes('| W')) structureTable.push(l); else if(inStructureTable && l.trim() === "") inStructureTable = false; }});
                structureTable.forEach(l => {{ const cols = l.split('|').map(c => c.trim()); if(cols.length >= 3 && cols[1].startsWith('W')) w.weeklyStructure.push({{ week: cols[1], focus: cols[2], note: cols[4] || "" }}); }});
                let inRules = false;
                lines.forEach(l => {{ const cleanL = l.trim(); if(cleanL.toLowerCase().includes('## progressione')) {{ inRules = true; return; }} if(inRules && cleanL.startsWith('##')) {{ inRules = false; return; }} if(inRules) {{ const ruleMatch = cleanL.match(/(?:-|\\*)\\s*\\**W(\\d+)\\**\\s*:?\\s*(.*)/i); if(ruleMatch) {{ const wkNum = 'W' + ruleMatch[1]; const content = ruleMatch[2].trim(); let existing = w.weeklyStructure.find(s => s.week === wkNum); if(existing) existing.note = content; else w.weeklyStructure.push({{ week: wkNum, focus: "Regola", note: content }}); }} }} }});
                let curD = null;
                lines.forEach(l => {{ if(l.startsWith('## ') && (l.toLowerCase().includes('giorno') || l.toLowerCase().includes('sessione') || l.toLowerCase().includes('giorno extra'))) {{ if(curD && curD.exercises.length > 0) w.days.push(curD); curD = {{ name: sanitize(l), exercises: [] }}; }} else if(curD) {{ if(l.includes('|') && !l.includes('Esercizio') && !l.includes('---')) {{ const cols = l.split('|').map(c => c.trim()); if(cols.length >= 4 && cols[1] !== "") {{ curD.exercises.push({{ name: sanitize(cols[1]), sets: cols[2], reps: cols[3], rest: cols[4] || "90s", notes: cols[5] || "" }}); }} }} }} }});
                if(curD && curD.exercises.length > 0) w.days.push(curD);
                if(w.days.length > 0) {{ 
                    workouts.unshift(w); 
                    localStorage.setItem('pale_workouts', JSON.stringify(workouts));
                    fetch('/api/workouts', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify(w)
                    }}).then(() => {{
                        showToast("IMPORTED & SYNCED");
                        renderHome();
                        showView('view-home');
                    }}).catch(err => {{
                        showToast("IMPORTED (Local only)");
                        renderHome();
                        showView('view-home');
                    }});
                }}
                btn.innerText = "INITIALIZE"; btn.disabled = false;
            }}, 800);
        }}
        function updateProg(w) {{ let t = w.numWeeks * (w.days?w.days.length:0); let d = 0; if (w.progress) Object.values(w.progress).forEach(wk => d += Object.keys(wk).length); document.getElementById('total-progress-bar').style.width = `${{t?(d / t) * 100:0}}%`; }}
        renderHome();
    </script>
</body>
</html>
    """
    return html_template

if __name__ == "__main__":
    output_path = "index.html"
    html_content = generate_html()
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Successo: Semplificata Dashboard con monitor progressi minimale.")
