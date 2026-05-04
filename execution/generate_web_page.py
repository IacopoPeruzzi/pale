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
            --bg-color: #050507;
            --card-bg: rgba(25, 25, 35, 0.85);
            --accent-color: #cfff04;
            --accent-glow: rgba(207, 255, 4, 0.35);
            --text-primary: #ffffff;
            --text-secondary: #8a8a93;
            --border-radius: 24px;
            --safe-area-top: env(safe-area-inset-top);
            --edit-mode-bg: rgba(255, 68, 68, 0.05);
        }}

        * {{ box-sizing: border-box; -webkit-tap-highlight-color: transparent; outline: none; }}
        body {{
            background-color: var(--bg-color);
            background-image: radial-gradient(circle at 10% 10%, rgba(207, 255, 4, 0.05) 0%, transparent 40%);
            color: var(--text-primary);
            font-family: 'Outfit', sans-serif;
            margin: 0; padding: 0; overflow-x: hidden;
        }}

        .view {{ display: none; padding: 0 20px 140px 20px; min-height: 100vh; position: relative; z-index: 10; }}
        .view.active {{ display: block; animation: fadeIn 0.3s ease; }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}

        .sticky-header {{
            position: sticky; top: 0; 
            padding: calc(30px + var(--safe-area-top)) 20px 15px 20px;
            margin: 0 -20px 15px -20px;
            background: linear-gradient(to bottom, var(--bg-color) 80%, transparent);
            backdrop-filter: blur(25px);
            z-index: 1000;
        }}

        h1 {{ font-size: 2.4rem; font-weight: 900; margin: 0; letter-spacing: -1.5px; text-transform: uppercase; line-height: 1; }}
        h2 {{ font-size: 1.8rem; font-weight: 800; margin: 0; letter-spacing: -1px; }}
        .subtitle {{ color: var(--text-secondary); font-size: 0.9rem; margin-top: 6px; }}

        .setup-toggle {{
            position: absolute; top: calc(35px + var(--safe-area-top)); right: 20px;
            padding: 8px 16px; border-radius: 15px; background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1); font-weight: 800; font-size: 0.65rem;
            text-transform: uppercase; letter-spacing: 1px; color: var(--text-secondary); cursor: pointer;
            transition: 0.3s; z-index: 1100;
        }}
        .setup-toggle.active {{ background: var(--accent-color); color: #000; box-shadow: 0 0 20px var(--accent-glow); border-color: transparent; }}

        .resume-card {{
            background: linear-gradient(135deg, #151518 0%, #1e1e24 100%);
            border-radius: 20px; padding: 18px; margin: 20px 0;
            border: 1px solid rgba(255,255,255,0.08);
            box-shadow: 0 10px 20px rgba(0,0,0,0.4);
            cursor: pointer;
        }}

        .progress-container {{ width: 100%; height: 4px; background: rgba(255,255,255,0.03); border-radius: 10px; margin: 15px 0; overflow: hidden; }}
        .progress-bar {{ height: 100%; background: var(--accent-color); transition: width 0.8s ease; }}

        .week-grid {{ display: flex; gap: 10px; margin-bottom: 20px; overflow-x: auto; padding-bottom: 8px; scrollbar-width: none; }}
        .week-btn {{ 
            flex: 0 0 85px; padding: 14px; background: var(--card-bg); 
            border-radius: 18px; text-align: center; cursor: pointer; opacity: 0.4;
            border: 1px solid rgba(255,255,255,0.05); transition: 0.3s;
        }}
        .week-btn.active {{ opacity: 1; background: var(--accent-color); color: #000; box-shadow: 0 5px 15px var(--accent-glow); }}

        .day-grid {{ display: grid; gap: 10px; }}
        .list-card {{ 
            background: var(--card-bg); border-radius: 20px; padding: 16px; 
            border: 1px solid rgba(255,255,255,0.05); backdrop-filter: blur(10px);
            display: flex; align-items: center; cursor: pointer;
            transition: 0.3s;
        }}
        .list-card.completed {{ border-left: 6px solid var(--accent-color); background: rgba(207, 255, 4, 0.03); }}
        
        .drag-handle {{ opacity: 0.3; font-size: 1.2rem; margin-right: 15px; display: none; min-width: 20px; }}
        .edit-mode .drag-handle {{ display: block; }}

        .card-content {{ flex: 1; }}
        .delete-btn {{ 
            width: 32px; height: 32px; border-radius: 50%; background: rgba(255, 68, 68, 0.15); 
            display: none; align-items: center; justify-content: center; color: #ff4444; font-size: 0.85rem; margin-left: 10px;
        }}
        .edit-mode .delete-btn {{ display: flex; }}

        .ex-item {{ 
            background: var(--card-bg); border-radius: 20px; padding: 16px; margin-bottom: 10px;
            display: flex; align-items: center; cursor: pointer; border: 1px solid rgba(255,255,255,0.05);
        }}
        .ex-item.done {{ opacity: 0.4; border-left: 4px solid var(--accent-color); }}
        .ex-item-name {{ font-weight: 700; flex: 1; font-size: 1rem; }}
        .ex-item-meta {{ font-size: 0.75rem; color: var(--text-secondary); }}

        .exercise-detail-view {{ padding-top: 20px; }}
        .metrics-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 20px 0; }}
        .metric-box {{ 
            background: rgba(255,255,255,0.03); padding: 15px 10px; border-radius: 18px; 
            text-align: center; border: 1px solid rgba(255,255,255,0.05);
        }}
        .metric-label {{ font-size: 0.65rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }}
        .metric-value {{ font-size: 1.1rem; font-weight: 800; color: var(--accent-color); }}

        .sets-main-wrap {{ display: flex; justify-content: center; gap: 15px; flex-wrap: wrap; margin: 30px 0; }}
        .set-circle {{ 
            width: 65px; height: 65px; border-radius: 50%; border: 3px solid rgba(255,255,255,0.1);
            display: flex; align-items: center; justify-content: center; font-size: 1.4rem; font-weight: 900;
            transition: 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); cursor: pointer;
        }}
        .set-circle.active {{ background: var(--accent-color); color: #000; border-color: transparent; transform: scale(1.1); box-shadow: 0 0 30px var(--accent-glow); }}

        .notes-area {{ 
            background: rgba(255,255,255,0.02); border-radius: 20px; padding: 20px; margin-top: 30px;
            border: 1px solid rgba(255,255,255,0.05); position: relative;
        }}
        .notes-area::before {{ content: 'TECHNICAL NOTES'; position: absolute; top: -10px; left: 20px; background: var(--bg-color); padding: 0 10px; font-size: 0.65rem; font-weight: 900; color: var(--accent-color); letter-spacing: 1px; }}
        .notes-content {{ font-size: 0.95rem; line-height: 1.6; color: #ccc; }}

        .nav-dock {{ position: fixed; bottom: 0; left: 0; width: 100%; padding: 20px 20px 40px 20px; background: linear-gradient(to top, var(--bg-color) 80%, transparent); display: flex; gap: 10px; z-index: 1000; }}
        .btn {{ flex: 1; border: none; padding: 18px; border-radius: 20px; font-weight: 800; cursor: pointer; text-transform: uppercase; font-size: 0.8rem; transition: 0.2s; }}
        .btn-main {{ background: var(--accent-color); color: #000; box-shadow: 0 8px 20px var(--accent-glow); }}
        .btn-alt {{ background: rgba(255,255,255,0.08); color: #fff; }}
        .btn:active {{ transform: scale(0.95); }}

        #timer-screen {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.98); z-index: 3000; display: none; flex-direction: column; align-items: center; justify-content: center; }}
        #timer-clock {{ font-size: 10rem; font-weight: 900; color: var(--accent-color); }}
        #toast {{ position: fixed; top: 30px; left: 50%; transform: translateX(-50%); background: var(--accent-color); color: #000; padding: 10px 20px; border-radius: 50px; font-weight: 800; z-index: 5000; display: none; font-size: 0.8rem; }}
    </style>
</head>
<body>
    <div id="toast"></div>

    <!-- HOME VIEW -->
    <div id="view-home" class="view active">
        <div class="sticky-header">
            <h1>Pale<br><span style="color:var(--accent-color)">App</span></h1>
            <p class="subtitle">Peak Performance Hub.</p>
        </div>
        <div id="resume-section"></div>
        <div id="workouts-list"></div>
        <div onclick="showView('view-import')" style="position: fixed; bottom: 40px; right: 25px; width: 70px; height: 70px; background: var(--accent-color); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 2rem; color: #000; box-shadow: 0 10px 20px var(--accent-glow); z-index: 1000; cursor: pointer;">+</div>
    </div>

    <!-- IMPORT VIEW -->
    <div id="view-import" class="view">
        <div class="sticky-header">
            <div onclick="showView('view-home')" style="color:var(--text-secondary); font-weight:800; cursor:pointer; margin-bottom:8px;">← BACK</div>
            <h1>Import</h1>
        </div>
        <textarea id="import-text" style="width: 100%; height: 300px; background: #111; color: #fff; border-radius: 20px; padding: 20px; border: 1px solid #333; margin: 15px 0;" placeholder="Paste protocol..."></textarea>
        <button id="import-btn" class="btn btn-main" style="width: 100%" onclick="importAction()">INITIALIZE</button>
    </div>

    <!-- PLAN VIEW (Weeks & Days) -->
    <div id="view-plan" class="view">
        <div class="sticky-header">
            <div onclick="showView('view-home')" style="color:var(--text-secondary); font-weight:800; cursor:pointer; margin-bottom:8px;">← DASHBOARD</div>
            <h1 id="plan-title">Protocol</h1>
            <div class="setup-toggle" id="plan-setup-btn" onclick="toggleSetup('plan')">Setup</div>
            <div class="progress-container"><div class="progress-bar" id="total-progress-bar"></div></div>
            <div class="week-grid" id="week-selector"></div>
        </div>
        <div class="day-grid" id="day-list"></div>
    </div>

    <!-- SESSION VIEW (Exercise List) -->
    <div id="view-session" class="view">
        <div class="sticky-header">
            <div onclick="openWorkout(currentWorkoutIndex)" style="color:var(--text-secondary); font-weight:800; cursor:pointer; margin-bottom:8px;">← PIANO</div>
            <h1 id="session-title">Day X</h1>
            <div class="setup-toggle" id="session-setup-btn" onclick="toggleSetup('session')">Setup</div>
            <p class="subtitle" id="session-subtitle">Week 1</p>
            <div id="session-focus-container" style="margin-top:12px;"></div>
        </div>
        <div id="exercise-list"></div>
        <div class="nav-dock">
            <button id="finish-btn" class="btn btn-main" onclick="finishSession()">CONCLUDI SESSIONE</button>
        </div>
    </div>

    <!-- EXERCISE VIEW (Detail Focus) -->
    <div id="view-exercise" class="view">
        <div class="sticky-header">
            <div onclick="startSession(currentDayIdx)" style="color:var(--text-secondary); font-weight:800; cursor:pointer; margin-bottom:8px;">← LISTA</div>
            <h2 id="ex-detail-name">Exercise Name</h2>
            <p class="subtitle" id="ex-detail-meta">Set 1 di 4</p>
        </div>
        <div class="exercise-detail-view">
            <div class="metrics-grid">
                <div class="metric-box"><div class="metric-label">Serie</div><div class="metric-value" id="val-sets">4</div></div>
                <div class="metric-box"><div class="metric-label">Reps</div><div class="metric-value" id="val-reps">10-12</div></div>
                <div class="metric-box"><div class="metric-label">Rest</div><div class="metric-value" id="val-rest">90"</div></div>
            </div>
            
            <div class="sets-main-wrap" id="sets-container"></div>
            
            <div id="ex-notes-container"></div>
        </div>
        <div class="nav-dock">
            <button class="btn btn-alt" id="timerBtn" onclick="startTimer()" style="flex: 0.4">TIMER</button>
            <button class="btn btn-main" id="nextExBtn" onclick="nextExercise()">PROSSIMO</button>
        </div>
    </div>

    <div id="timer-screen" onclick="stopTimer()"><div id="timer-clock">90</div><p>READY?</p></div>

    <script>
        let workouts = JSON.parse(localStorage.getItem('pale_workouts') || '[]');
        let currentWorkoutIndex = null;
        let currentWeek = 1;
        let currentDayIdx = null;
        let currentExIdx = null;
        let activeRestTime = 90;
        let isEditMode = false;

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
            if(id === 'view-home') {{ renderHome(); isEditMode = false; }}
        }}

        function toggleSetup(view) {{
            isEditMode = !isEditMode;
            const btn = document.getElementById(view + '-setup-btn');
            btn.innerText = isEditMode ? 'Done' : 'Setup';
            btn.classList.toggle('active');
            if(view === 'plan') openWorkout(currentWorkoutIndex);
            else if(view === 'session') startSession(currentDayIdx);
        }}

        function renderHome() {{
            const res = document.getElementById('resume-section');
            res.innerHTML = '';
            if (workouts.length > 0) {{
                const w = workouts[0];
                const n = getInc(w);
                if (n) res.innerHTML = `<div class="resume-card" onclick="openWorkout(0)"><h2>CONTINUA: ${{w.title}}</h2><small>W${{n.week}} • Giorno ${{n.day+1}}</small></div>`;
            }}
            const list = document.getElementById('workouts-list');
            list.innerHTML = workouts.length === 0 ? '<p>Nessun piano.</p>' : '<h3>I tuoi Piani</h3>';
            workouts.forEach((w, i) => {{
                const card = document.createElement('div');
                card.className = 'list-card';
                card.style.marginBottom = '10px';
                card.onclick = () => openWorkout(i);
                card.innerHTML = `<div class="card-content"><b>${{w.title}}</b><br><small>${{w.numWeeks}} WEEKS</small></div><div style="opacity:0.2" onclick="event.stopPropagation(); deleteWorkout(${{i}})">🗑️</div>`;
                list.appendChild(card);
            }});
        }}

        function sanitize(str) {{
            if(!str) return "";
            return str.replace(/^[#\\*\\s\\-\\–\\—]+/g, '').replace(/[#\\*\\-\\–\\—\\s]+$/g, '').trim();
        }}

        function openWorkout(idx) {{
            currentWorkoutIndex = idx;
            const w = workouts[idx];
            const n = getInc(w);
            if(!currentWeek) currentWeek = n ? n.week : 1;

            document.getElementById('plan-title').innerText = sanitize(w.title);
            updateProg(w);

            const sel = document.getElementById('week-selector');
            sel.innerHTML = '';
            for(let i=1; i<=w.numWeeks; i++) {{
                const b = document.createElement('div');
                b.className = `week-btn ${{currentWeek === i ? 'active' : ''}}`;
                b.innerHTML = `<span class="week-num">W${{i}}</span>`;
                b.onclick = () => {{ currentWeek = i; openWorkout(idx); }};
                sel.appendChild(b);
            }}

            const dList = document.getElementById('day-list');
            dList.innerHTML = '';
            w.days.forEach((d, dI) => {{
                const status = w.progress && w.progress[currentWeek] && w.progress[currentWeek][dI];
                const c = document.createElement('div');
                c.className = `list-card ${{status === true ? 'completed' : ''}}`;
                c.onclick = () => {{ if(isEditMode) return; startSession(dI); }};
                
                let dayName = sanitize(d.name.includes(' – ') ? d.name.split(' – ')[1] : (d.name.includes(' - ') ? d.name.split(' - ')[1] : d.name));
                if(!dayName || dayName.toLowerCase().startsWith('giorno')) dayName = sanitize(d.name);

                c.innerHTML = `
                    <div class="drag-handle">☰</div>
                    <div class="card-content">
                        <h4 style="margin:0; font-size:0.8rem; color:var(--accent-color)">GIORNO ${{dI + 1}}</h4>
                        <b style="font-size:1.1rem">${{dayName}}</b>
                    </div>
                    <div class="delete-btn" onclick="event.stopPropagation(); deleteDay(${{dI}})">🗑️</div>
                `;
                dList.appendChild(c);
            }});
            
            if(isEditMode) dList.classList.add('edit-mode'); else dList.classList.remove('edit-mode');
            new Sortable(dList, {{
                animation: 500, disabled: !isEditMode, handle: '.drag-handle', ghostClass: 'sortable-ghost', dragClass: 'sortable-drag', forceFallback: true,
                onEnd: function(evt) {{
                    const w = workouts[currentWorkoutIndex];
                    const movedItem = w.days.splice(evt.oldIndex, 1)[0];
                    w.days.splice(evt.newIndex, 0, movedItem);
                    save(); openWorkout(currentWorkoutIndex);
                }}
            }});
            showView('view-plan');
        }}

        function startSession(dI) {{
            currentDayIdx = dI;
            const w = workouts[currentWorkoutIndex];
            const d = w.days[dI];
            
            let dayName = sanitize(d.name.includes(' – ') ? d.name.split(' – ')[1] : (d.name.includes(' - ') ? d.name.split(' - ')[1] : d.name));
            if(!dayName || dayName.toLowerCase().startsWith('giorno')) dayName = sanitize(d.name);

            document.getElementById('session-title').innerText = `GIORNO ${{dI + 1}}`;
            document.getElementById('session-subtitle').innerText = `WEEK ${{currentWeek}} • ${{dayName}}`;

            const focus = document.getElementById('session-focus-container');
            const str = w.weeklyStructure?.find(s => s.week === 'W' + currentWeek) || (w.weeklyStructure ? w.weeklyStructure[currentWeek-1] : null);
            focus.innerHTML = str ? `<div style="background:rgba(207,255,4,0.08); padding:12px; border-radius:15px; border:1px solid var(--accent-color); font-size:0.8rem;"><b>${{str.focus}}</b>: ${{str.note}}</div>` : '';

            const list = document.getElementById('exercise-list');
            list.innerHTML = '';
            d.exercises.forEach((ex, eI) => {{
                const isD = ex.setStates && ex.setStates.every(s => s === true);
                const item = document.createElement('div');
                item.className = `ex-item ${{isD ? 'done' : ''}}`;
                item.onclick = () => {{ if(isEditMode) return; openExercise(eI); }};
                item.innerHTML = `
                    <div class="drag-handle">☰</div>
                    <div class="ex-item-name">${{sanitize(ex.name)}}</div>
                    <div class="ex-item-meta">${{ex.sets}} SETS</div>
                    <div class="delete-btn" onclick="event.stopPropagation(); deleteEx(${{eI}})">🗑️</div>
                `;
                list.appendChild(item);
            }});

            if(isEditMode) list.classList.add('edit-mode'); else list.classList.remove('edit-mode');
            new Sortable(list, {{
                animation: 500, disabled: !isEditMode, handle: '.drag-handle', ghostClass: 'sortable-ghost', dragClass: 'sortable-drag', forceFallback: true,
                onEnd: function(evt) {{
                    const d = workouts[currentWorkoutIndex].days[currentDayIdx];
                    const movedItem = d.exercises.splice(evt.oldIndex, 1)[0];
                    d.exercises.splice(evt.newIndex, 0, movedItem);
                    save();
                }}
            }});
            showView('view-session');
        }}

        function openExercise(eI) {{
            currentExIdx = eI;
            const ex = workouts[currentWorkoutIndex].days[currentDayIdx].exercises[eI];
            
            document.getElementById('ex-detail-name').innerText = sanitize(ex.name);
            document.getElementById('val-sets').innerText = ex.sets;
            document.getElementById('val-reps').innerText = ex.reps;
            document.getElementById('val-rest').innerText = ex.rest;
            
            const nS = parseInt(ex.sets) || 1;
            if(!ex.setStates) ex.setStates = new Array(nS).fill(false);
            
            const container = document.getElementById('sets-container');
            container.innerHTML = '';
            for(let i=0; i<nS; i++) {{
                const c = document.createElement('div');
                c.className = `set-circle ${{ex.setStates[i] ? 'active' : ''}}`;
                c.innerText = i+1;
                c.onclick = () => toggleSet(i);
                container.appendChild(c);
            }}

            const notes = document.getElementById('ex-notes-container');
            notes.innerHTML = ex.notes ? `<div class="notes-area"><div class="notes-content">${{sanitize(ex.notes)}}</div></div>` : '';
            
            updateExMeta();
            activeRestTime = parseRest(ex.rest);
            showView('view-exercise');
        }}

        function toggleSet(sI) {{
            const ex = workouts[currentWorkoutIndex].days[currentDayIdx].exercises[currentExIdx];
            ex.setStates[sI] = !ex.setStates[sI];
            const circles = document.querySelectorAll('.set-circle');
            if(ex.setStates[sI]) circles[sI].classList.add('active'); else circles[sI].classList.remove('active');
            if(ex.setStates[sI]) startTimer();
            save();
            updateExMeta();
        }}

        function updateExMeta() {{
            const ex = workouts[currentWorkoutIndex].days[currentDayIdx].exercises[currentExIdx];
            const done = ex.setStates.filter(s => s).length;
            document.getElementById('ex-detail-meta').innerText = `Serie ${{done}} di ${{ex.sets}} completate`;
        }}

        function nextExercise() {{
            const d = workouts[currentWorkoutIndex].days[currentDayIdx];
            if(currentExIdx < d.exercises.length - 1) openExercise(currentExIdx + 1);
            else startSession(currentDayIdx);
        }}

        async function finishSession() {{
            const w = workouts[currentWorkoutIndex];
            if (!w.progress[currentWeek]) w.progress[currentWeek] = {{}};
            w.progress[currentWeek][currentDayIdx] = true;
            save(); showToast("SESSIONE COMPLETATA!"); openWorkout(currentWorkoutIndex);
        }}

        function deleteDay(idx) {{ if(confirm('DELETE DAY?')) {{ workouts[currentWorkoutIndex].days.splice(idx, 1); save(); openWorkout(currentWorkoutIndex); }} }}
        function deleteEx(idx) {{ if(confirm('DELETE EXERCISE?')) {{ workouts[currentWorkoutIndex].days[currentDayIdx].exercises.splice(idx, 1); save(); startSession(currentDayIdx); }} }}
        function parseRest(r) {{ const m = r.match(/(\\d+)/); if (!m) return 90; let v = parseInt(m[1]); return (r.includes("'") || r.toLowerCase().includes("m")) ? v * 60 : v; }}
        function save() {{ localStorage.setItem('pale_workouts', JSON.stringify(workouts)); }}
        
        let tInt;
        function startTimer() {{ stopTimer(); const s = document.getElementById('timer-screen'); const c = document.getElementById('timer-clock'); s.style.display = 'flex'; let l = activeRestTime; c.innerText = l; tInt = setInterval(() => {{ l--; c.innerText = l; if (l <= 0) {{ stopTimer(); if(navigator.vibrate) navigator.vibrate([400, 100, 400]); }} }}, 1000); }}
        function stopTimer() {{ clearInterval(tInt); document.getElementById('timer-screen').style.display = 'none'; }}
        
        function importAction() {{
            const t = document.getElementById('import-text').value;
            if(!t.trim()) return;
            const btn = document.getElementById('import-btn');
            btn.innerText = "IMPORTING..."; btn.disabled = true;
            setTimeout(() => {{
                const w = {{ id: "p-" + Date.now(), title: "NEW PROTOCOL", numWeeks: 4, weeklyStructure: [], days: [], progress: {{}} }};
                const lines = t.split('\\n');
                const tMatch = t.match(/(?:#|\\*\\*|Perfetto:)\\s*\\*?\\*?([A-Z0-9 ]+)\\b/i);
                if(tMatch) w.title = sanitize(tMatch[1]);
                const wMatch = t.match(/(\\d+)\\s*settimane/i);
                if(wMatch) w.numWeeks = parseInt(wMatch[1]);
                
                let structureTable = [];
                let inStructureTable = false;
                lines.forEach(l => {{
                    if(l.includes('| Settimana |')) inStructureTable = true;
                    else if(inStructureTable && l.includes('| W')) structureTable.push(l);
                    else if(inStructureTable && l.trim() === "") inStructureTable = false;
                }});
                structureTable.forEach(l => {{
                    const cols = l.split('|').map(c => c.trim());
                    if(cols.length >= 3 && cols[1].startsWith('W')) 
                        w.weeklyStructure.push({{ week: cols[1], focus: cols[2], note: cols[4] || "" }});
                }});

                let inRules = false;
                lines.forEach(l => {{
                    const cleanL = l.trim();
                    if(cleanL.toLowerCase().includes('## regole')) {{ inRules = true; return; }}
                    if(inRules && cleanL.startsWith('##')) {{ inRules = false; return; }}
                    if(inRules) {{
                        const ruleMatch = cleanL.match(/(?:-|\\*)\\s*\\**W(\\d+)\\**\\s*:?\\s*(.*)/i);
                        if(ruleMatch) {{
                            const wkNum = 'W' + ruleMatch[1];
                            const content = ruleMatch[2].trim();
                            let existing = w.weeklyStructure.find(s => s.week === wkNum);
                            if(existing) existing.note = content;
                            else w.weeklyStructure.push({{ week: wkNum, focus: "Regola", note: content }});
                        }}
                    }}
                }});

                let curD = null;
                lines.forEach(l => {{
                    if(l.startsWith('## ') && (l.toLowerCase().includes('giorno') || l.toLowerCase().includes('sessione') || l.toLowerCase().includes('giorno extra'))) {{
                        if(curD && curD.exercises.length > 0) w.days.push(curD);
                        curD = {{ name: sanitize(l), exercises: [] }};
                    }} else if(curD) {{
                        if(l.includes('|') && !l.includes('Esercizio') && !l.includes('---')) {{
                            const cols = l.split('|').map(c => c.trim());
                            if(cols.length >= 4 && cols[1] !== "") {{
                                curD.exercises.push({{ name: sanitize(cols[1]), sets: cols[2], reps: cols[3], rest: cols[4] || "90s", notes: cols[5] || "" }});
                            }}
                        }}
                    }}
                }});
                if(curD && curD.exercises.length > 0) w.days.push(curD);
                if(w.days.length > 0) {{ workouts.unshift(w); save(); showToast("IMPORTED"); showView('view-home'); }}
                btn.innerText = "INITIALIZE"; btn.disabled = false;
            }}, 800);
        }}
        function deleteWorkout(i) {{ if(confirm('DELETE?')) {{ workouts.splice(i, 1); save(); renderHome(); }} }}
        function updateProg(w) {{ let t = w.numWeeks * w.days.length; let d = 0; if (w.progress) Object.values(w.progress).forEach(wk => {{ d += Object.keys(wk).length; }}); document.getElementById('total-progress-bar').style.width = `${{(d / t) * 100}}%`; }}
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
    print(f"Successo: Implementata navigazione a 4 livelli con dettaglio esercizio dedicato.")
