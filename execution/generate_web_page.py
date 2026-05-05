import json
import os

def generate_html():
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
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;600;900&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #f2f5f9;
            --shadow-light: rgba(255, 255, 255, 0.95);
            --shadow-dark: rgba(163, 177, 198, 0.35);
            --accent-blue: #007aff;
            --accent-red: #ff3b30;
            --text-main: #4a5568;
            --text-dim: #94a3b8;
            --safe-area-top: env(safe-area-inset-top);
        }}

        * {{ box-sizing: border-box; -webkit-tap-highlight-color: transparent; outline: none; }}
        
        body {{
            background-color: var(--bg-color);
            color: var(--text-main);
            font-family: 'Outfit', sans-serif;
            margin: 0; padding: 0; overflow-x: hidden;
            min-height: 100vh;
        }}

        .bg-blob {{
            position: fixed; width: 500px; height: 500px; border-radius: 50%; z-index: -1;
            background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, transparent 70%);
            filter: blur(80px); opacity: 0.5; pointer-events: none;
            animation: float 20s infinite alternate ease-in-out;
        }}
        @keyframes float {{ 0% {{ transform: translate(-10%, -10%); }} 100% {{ transform: translate(10%, 10%); }} }}

        .view {{ display: none; padding: 12px; padding-top: 85px; min-height: 100vh; position: relative; z-index: 10; }}
        .view.active {{ display: block; }}

        /* Slim Sticky Header */
        .glass-header {{
            position: fixed; top: 0; left: 0; right: 0;
            background: var(--bg-color);
            padding: calc(10px + var(--safe-area-top)) 15px 10px 15px;
            z-index: 2000;
            display: flex; justify-content: space-between; align-items: center;
            box-shadow: 0 4px 15px var(--shadow-dark);
        }}

        .brand-logo {{ font-size: 1rem; font-weight: 900; letter-spacing: 1px; color: var(--text-main); }}
        .brand-logo::after {{ content: ''; width: 6px; height: 6px; background: var(--accent-blue); border-radius: 50%; margin-left: 5px; display: inline-block; }}

        /* Optimized Neo Panels */
        .neo-panel {{
            background: var(--bg-color);
            border-radius: 20px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 8px 8px 16px var(--shadow-dark), -8px -8px 16px var(--shadow-light);
        }}

        .neo-inset {{
            background: var(--bg-color);
            box-shadow: inset 5px 5px 10px var(--shadow-dark), inset -5px -5px 10px var(--shadow-light);
            border-radius: 15px;
        }}

        h2 {{ font-size: 1.3rem; font-weight: 900; margin: 0; letter-spacing: -0.5px; color: var(--text-main); }}
        h3 {{ font-size: 0.6rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; color: var(--text-dim); margin: 25px 0 10px 0; }}

        .tag {{
            display: inline-block; font-size: 0.55rem; font-weight: 900; text-transform: uppercase; 
            letter-spacing: 1.2px; color: var(--accent-blue); margin-bottom: 5px;
        }}

        .resume-card {{
            background: var(--bg-color);
            border-radius: 24px; padding: 18px; margin-bottom: 25px; cursor: pointer;
            box-shadow: 10px 10px 20px var(--shadow-dark), -10px -10px 20px var(--shadow-light);
            transition: 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }}
        .resume-card:active {{ box-shadow: inset 6px 6px 12px var(--shadow-dark), inset -6px -6px 12px var(--shadow-light); transform: scale(0.97); }}

        .list-card {{ 
            background: var(--bg-color); 
            border-radius: 18px; padding: 14px 18px; 
            margin-bottom: 12px; display: flex; align-items: center; cursor: pointer;
            box-shadow: 6px 6px 12px var(--shadow-dark), -6px -6px 12px var(--shadow-light);
            transition: 0.3s ease;
        }}
        .list-card:active {{ box-shadow: inset 4px 4px 8px var(--shadow-dark), inset -4px -4px 8px var(--shadow-light); }}
        .list-card.completed {{ color: var(--accent-blue); }}

        .nav-btn {{
            background: var(--bg-color); color: var(--text-main);
            border: none; border-radius: 10px; padding: 8px 14px;
            font-weight: 900; font-size: 0.65rem; text-transform: uppercase; cursor: pointer;
            box-shadow: 4px 4px 8px var(--shadow-dark), -4px -4px 8px var(--shadow-light);
        }}
        .nav-btn:active {{ box-shadow: inset 2px 2px 4px var(--shadow-dark), inset -2px -2px 4px var(--shadow-light); }}

        .week-grid {{ display: flex; gap: 10px; margin-bottom: 15px; overflow-x: auto; padding: 10px 2px; }}
        .week-btn {{ 
            flex: 0 0 50px; padding: 12px; background: var(--bg-color); 
            border-radius: 15px; color: var(--text-dim); font-weight: 800; text-align: center; cursor: pointer; font-size: 0.7rem;
            box-shadow: 4px 4px 8px var(--shadow-dark), -4px -4px 8px var(--shadow-light);
        }}
        .week-btn.active {{ box-shadow: inset 3px 3px 6px var(--shadow-dark), inset -3px -3px 6px var(--shadow-light); color: var(--accent-blue); }}

        .ex-item {{ 
            background: var(--bg-color); border-radius: 18px; padding: 14px 18px; margin-bottom: 10px; 
            display: flex; align-items: center; cursor: pointer;
            box-shadow: 6px 6px 12px var(--shadow-dark), -6px -6px 12px var(--shadow-light);
        }}
        .ex-item.done {{ opacity: 0.4; box-shadow: inset 3px 3px 6px var(--shadow-dark), inset -3px -3px 6px var(--shadow-light); }}

        .metric-box {{ 
            background: var(--bg-color); border-radius: 15px; padding: 10px; text-align: center; flex: 1;
            box-shadow: inset 4px 4px 8px var(--shadow-dark), inset -4px -4px 8px var(--shadow-light);
        }}
        .metric-label {{ font-size: 0.5rem; font-weight: 600; color: var(--text-dim); text-transform: uppercase; }}
        .metric-value {{ font-size: 0.9rem; font-weight: 900; margin-top: 2px; color: var(--text-main); }}

        .set-block {{ 
            background: var(--bg-color); border-radius: 20px; padding: 15px; margin-bottom: 15px; 
            box-shadow: 8px 8px 16px var(--shadow-dark), -8px -8px 16px var(--shadow-light);
        }}
        .set-circle {{ 
            width: 44px; height: 44px; border-radius: 50%; 
            display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 0.9rem; cursor: pointer;
            box-shadow: 5px 5px 10px var(--shadow-dark), -5px -5px 10px var(--shadow-light);
            background: var(--bg-color); transition: 0.2s;
        }}
        .set-circle.active {{ box-shadow: inset 4px 4px 8px var(--shadow-dark), inset -4px -4px 8px var(--shadow-light); color: var(--accent-blue); transform: scale(0.94); }}

        .load-input {{ 
            border: none; border-bottom: 1.5px solid var(--accent-blue); font-weight: 900; font-size: 1.3rem; 
            width: 70px; text-align: center; background: transparent; color: var(--text-main); 
        }}
        
        .progress-monitor {{ 
            height: 10px; background: var(--bg-color); border-radius: 20px; margin-bottom: 25px; 
            box-shadow: inset 4px 4px 8px var(--shadow-dark), inset -4px -4px 8px var(--shadow-light);
            padding: 3px;
        }}
        .progress-fill {{ height: 100%; background: var(--accent-blue); border-radius: 20px; transition: 0.6s ease; }}

        .action-btn {{ 
            padding: 6px 12px; border-radius: 12px; background: var(--bg-color); border: none; 
            color: var(--text-dim); font-weight: 800; font-size: 0.55rem; text-transform: uppercase; cursor: pointer;
            box-shadow: 3px 3px 6px var(--shadow-dark), -3px -3px 6px var(--shadow-light);
        }}
        .action-btn.danger {{ color: var(--accent-red); }}

        .btn-floating {{ 
            background: var(--bg-color); color: var(--accent-blue); border: none; border-radius: 18px; 
            padding: 16px 25px; font-weight: 900; text-transform: uppercase; font-size: 0.75rem; cursor: pointer; 
            box-shadow: 8px 8px 16px var(--shadow-dark), -8px -8px 16px var(--shadow-light);
            transition: 0.2s;
        }}
        .btn-floating:active {{ box-shadow: inset 4px 4px 8px var(--shadow-dark), inset -4px -4px 8px var(--shadow-light); }}

        #toast {{ 
            position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%); 
            background: var(--bg-color); color: var(--accent-blue); padding: 12px 25px; 
            font-weight: 900; border-radius: 15px; z-index: 9999; display: none; 
            box-shadow: 8px 8px 16px var(--shadow-dark), -8px -8px 16px var(--shadow-light);
            font-size: 0.65rem;
        }}
        
        ::-webkit-scrollbar {{ display: none; }}
    </style>
</head>
<body>
    <div class="bg-blob"></div>
    <div id="toast"></div>

    <div class="glass-header">
        <div class="brand-logo" onclick="showView('view-home')" style="cursor:pointer">PALE APP</div>
        <div id="header-actions">
            <button class="nav-btn" onclick="showView('view-import')">Nuovo</button>
        </div>
    </div>

    <div id="view-home" class="view active">
        <div class="progress-monitor"><div id="progress-bar" class="progress-fill" style="width:0%"></div></div>
        <div id="resume-section"></div>
        <h3>I tuoi Piani <button id="manage-btn" class="action-btn" style="float:right" onclick="toggleManageMode()">Edit</button></h3>
        <div id="workouts-list"></div>
    </div>

    <div id="view-import" class="view">
        <div class="neo-panel">
            <div class="tag">M7 Core</div>
            <h2 style="margin-bottom:15px;">IMPORTA <span>DATI</span></h2>
            <div class="neo-inset" style="padding:15px; margin:15px 0;">
                <textarea id="import-text" style="width:100%; height:280px; border:none; background:transparent; color:var(--text-main); font-family:monospace; font-size:0.85rem;"></textarea>
            </div>
            <button id="import-btn" class="btn-floating" style="width:100%;" onclick="importAction()">Sincronizza</button>
            <button class="action-btn" style="width:100%; margin-top:15px; box-shadow:none; opacity:0.5;" onclick="showView('view-home')">Torna Indietro</button>
        </div>
    </div>

    <div id="view-workout" class="view">
        <div id="workout-content"></div>
        <div style="margin-top:25px;"><button class="btn-floating" style="width:100%; color:var(--text-dim); background:transparent; box-shadow:none;" onclick="showView('view-home')">Chiudi</button></div>
    </div>

    <div id="view-session" class="view">
        <div id="session-header"></div>
        <div id="session-content"></div>
        <div style="margin-top:25px; display:flex; gap:12px;">
            <button class="btn-floating" style="flex:1; color:var(--text-dim); padding:16px 10px; background:transparent; box-shadow:none;" onclick="openWorkout(currentWorkoutIndex)">Esci</button>
            <button class="btn-floating" style="flex:2;" onclick="finishSession()">Salva</button>
        </div>
    </div>

    <div id="view-exercise" class="view">
        <div id="ex-header"></div>
        <div id="ex-content"></div>
        <div style="margin-top:25px; display:flex; gap:10px;">
            <button class="btn-floating" style="padding:16px 12px; color:var(--text-dim); background:transparent; box-shadow:none;" onclick="startSession(currentDayIdx)">List</button>
            <button class="btn-floating" style="flex:1; color:var(--accent-red); background:transparent; box-shadow:none;" onclick="nextExercise()">Salta</button>
            <button class="btn-floating" style="flex:2;" onclick="nextExercise()">Avanti</button>
        </div>
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
            document.getElementById('manage-btn').innerText = manageMode ? 'Fine' : 'Edit';
            renderHome();
        }}

        function renderHome() {{
            const res = document.getElementById('resume-section');
            const progBar = document.getElementById('progress-bar');
            res.innerHTML = '';
            if (workouts.length > 0) {{
                const w = workouts[0];
                const n = getInc(w);
                let t = w.numWeeks * (w.days?w.days.length:0);
                let d = 0;
                if (w.progress) Object.values(w.progress).forEach(wk => d += Object.keys(wk).length);
                progBar.style.width = (t ? Math.round((d/t)*100) : 0) + '%';
                if (n) {{
                    res.innerHTML = `
                        <div class="resume-card" onclick="resumeWorkout(0)">
                            <div class="tag">In Corso</div>
                            <h2 style="color:var(--accent-blue); font-size:1.1rem;">${{sanitize(w.title)}}</h2>
                            <p style="font-weight:600; opacity:0.4; margin-top:5px; font-size:0.8rem;">W${{n.week}} • Giorno ${{n.day+1}}</p>
                        </div>`;
                }}
            }}
            const list = document.getElementById('workouts-list');
            list.innerHTML = workouts.length === 0 ? '<div class="neo-panel" style="font-size:0.75rem; text-align:center;">Vuoto.</div>' : '';
            workouts.forEach((w, i) => {{
                const card = document.createElement('div');
                card.className = `list-card`;
                card.onclick = () => {{ if(!manageMode) openWorkout(i); }};
                card.innerHTML = `
                    <div style="flex:1">
                        <b style="font-size:0.95rem;">${{w.title}}</b><br>
                        <small style="opacity:0.3; text-transform:uppercase; font-weight:900; font-size:0.55rem;">${{w.subtitle || "Standard"}}</small>
                    </div>
                    ${{manageMode ? `<div class="action-btn danger" onclick="event.stopPropagation(); deleteWorkout(${{i}})">Elimina</div>` : ''}}
                `;
                list.appendChild(card);
            }});
        }}

        function resumeWorkout(idx) {{ const w = workouts[idx]; const n = getInc(w); currentWorkoutIndex = idx; if(n) {{ currentWeek = n.week; startSession(n.day); }} else openWorkout(idx); }}
        function sanitize(str) {{ return str ? str.replace(/^[#\\*\\s\\-\\–\\—]+/g, '').replace(/[#\\*\\-\\–\\—\\s]+$/g, '').trim() : ""; }}
        
        function openWorkout(idx) {{ 
            currentWorkoutIndex = idx; 
            const w = workouts[idx]; 
            const n = getInc(w); 
            if(!currentWeek) currentWeek = n ? n.week : 1;
            const weekInfo = w.weeklyStructure?.find(s => s.week === 'W' + currentWeek);
            const content = document.getElementById('workout-content');
            content.innerHTML = `
                <div class="neo-panel" style="padding:12px 15px;">
                    <div class="tag">Dettaglio</div>
                    <h2 style="font-size:1.1rem;">${{sanitize(w.title)}}</h2>
                    ${{weekInfo ? `<div class="neo-inset" style="padding:10px; margin-top:8px;">
                        <small style="font-weight:900; color:var(--accent-blue); font-size:0.5rem; text-transform:uppercase;">Focus W${{currentWeek}}</small>
                        <p style="margin:2px 0 0 0; font-size:0.75rem; font-weight:600; opacity:0.8;">${{weekInfo.note || weekInfo.focus}}</p>
                    </div>` : ''}}
                </div>
                <div class="week-grid" id="week-selector"></div>
                <div id="day-list"></div>
            `;
            const sel = document.getElementById('week-selector');
            for(let i=1; i<=w.numWeeks; i++) {{
                const b = document.createElement('div');
                b.className = `week-btn ${{currentWeek === i ? 'active' : ''}}`;
                b.innerHTML = `W${{i}}`;
                b.onclick = () => {{ currentWeek = i; openWorkout(idx); }};
                sel.appendChild(b);
            }}
            const dList = document.getElementById('day-list');
            w.days.forEach((d, dI) => {{
                const status = w.progress && w.progress[currentWeek] && w.progress[currentWeek][dI];
                const c = document.createElement('div');
                c.className = `list-card ${{status ? 'completed' : ''}}`;
                c.onclick = () => startSession(dI);
                c.innerHTML = `<div style="flex:1"><small style="opacity:0.3; font-weight:900; font-size:0.55rem;">GIORNO ${{dI+1}}</small><br><b style="font-size:0.95rem;">${{sanitize(d.name)}}</b></div>`;
                dList.appendChild(c);
            }});
            showView('view-workout');
        }}

        function startSession(dI) {{
            currentDayIdx = dI;
            const w = workouts[currentWorkoutIndex];
            const d = w.days[dI];
            document.getElementById('session-header').innerHTML = `
                <div class="neo-panel" style="padding:12px 15px;">
                    <div class="tag">Sessione</div>
                    <h2 style="font-size:1.1rem;">${{sanitize(d.name)}}</h2>
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-top:10px;">
                        <small style="opacity:0.4; font-weight:900; font-size:0.55rem;">W${{currentWeek}}</small>
                        <button class="action-btn danger" onclick="resetDayAction()">Reset</button>
                    </div>
                </div>`;
            const content = document.getElementById('session-content');
            content.innerHTML = '';
            d.exercises.forEach((ex, eI) => {{
                const isD = ex.sessionData && ex.sessionData[currentWeek] && ex.sessionData[currentWeek].completed;
                const item = document.createElement('div');
                item.className = `ex-item ${{isD ? 'done' : ''}}`;
                item.onclick = () => openExercise(eI);
                item.innerHTML = `<div style="flex:1; font-size:0.95rem;"><b>${{sanitize(ex.name)}}</b></div><div style="font-weight:900; font-size:0.65rem; color:var(--accent-blue)">${{ex.sets}}S</div>`;
                content.appendChild(item);
            }});
            showView('view-session');
        }}

        function openExercise(eI) {{
            currentExIdx = eI;
            const w = workouts[currentWorkoutIndex];
            const ex = w.days[currentDayIdx].exercises[eI];
            if (!ex.sessionData) ex.sessionData = {{}};
            if (!ex.sessionData[currentWeek]) ex.sessionData[currentWeek] = {{ completed: false, rounds: [], notes: "" }};
            const data = ex.sessionData[currentWeek];
            let subExs = [];
            if (ex.notes && (ex.notes.includes('+') || ex.name.toLowerCase().includes('circuito'))) {{
                subExs = ex.notes.split('+').map(s => {{
                    const m = s.trim().match(/(.*?)\s*(\d+.*)/);
                    return {{ name: m ? m[1].trim() : s.trim(), reps: m ? m[2].trim() : "" }};
                }}).filter(x => x.name);
            }}
            if (subExs.length === 0) subExs = [{{ name: sanitize(ex.name), reps: ex.reps }}];
            const nR = parseInt(ex.sets) || 1;
            while (data.rounds.length < nR) data.rounds.push({{ done: false, subLoads: new Array(subExs.length).fill("") }});
            
            document.getElementById('ex-header').innerHTML = `
                <div class="neo-panel" style="padding:12px 15px;">
                    <div class="tag">Dettaglio</div>
                    <h2 style="font-size:1.1rem;">${{sanitize(ex.name)}}</h2>
                    <div style="display:flex; gap:10px; margin-top:12px;">
                        <div class="metric-box"><div class="metric-label">SETS</div><div class="metric-value">${{ex.sets}}</div></div>
                        <div class="metric-box"><div class="metric-label">REPS</div><div class="metric-value">${{subExs.length > 1 ? 'CIRC' : ex.reps}}</div></div>
                        <div class="metric-box"><div class="metric-label">REST</div><div class="metric-value">${{ex.rest}}</div></div>
                    </div>
                </div>`;
            const content = document.getElementById('ex-content');
            content.innerHTML = '';
            data.rounds.forEach((round, rI) => {{
                const block = document.createElement('div');
                block.className = 'set-block';
                let subHtml = '';
                subExs.forEach((sx, sI) => {{
                    subHtml += `<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                        <div><b style="font-size:0.85rem">${{sx.name}}</b><br><small style="opacity:0.4; font-size:0.7rem;">${{sx.reps}}</small></div>
                        <div style="display:flex; align-items:center;">
                            <input type="number" class="load-input" value="${{round.subLoads[sI] || ""}}" oninput="updateSubLoad(${{rI}}, ${{sI}}, this.value)">
                            <small style="font-weight:900; margin-left:8px; color:var(--accent-blue); font-size:0.75rem;">KG</small>
                        </div>
                    </div>`;
                }});
                block.innerHTML = `
                    <div style="display:flex; align-items:center; gap:15px; margin-bottom:15px;">
                        <div class="set-circle ${{round.done ? 'active' : ''}}" onclick="toggleRound(${{rI}})">${{rI+1}}</div>
                        <div style="font-weight:900; font-size:0.6rem; opacity:0.35;">${{subExs.length > 1 ? 'GIRO' : 'SERIE'}}</div>
                    </div>
                    ${{subHtml}}`;
                content.appendChild(block);
            }});
            const notes = document.createElement('div');
            notes.className = 'neo-panel';
            notes.innerHTML = `<small style="font-weight:900; opacity:0.35; font-size:0.55rem;">NOTE</small><div class="neo-inset" style="padding:10px; margin-top:8px;"><textarea id="session-notes" oninput="updateSessionNotes()" style="width:100%; border:none; background:transparent; color:var(--text-main); font-family:inherit; min-height:60px; font-size:0.8rem;">${{data.notes || ""}}</textarea></div>`;
            content.appendChild(notes);
            showView('view-exercise');
        }}

        function toggleRound(rI) {{ const data = workouts[currentWorkoutIndex].days[currentDayIdx].exercises[currentExIdx].sessionData[currentWeek]; data.rounds[rI].done = !data.rounds[rI].done; save(); openExercise(currentExIdx); }}
        function updateSubLoad(rI, sI, val) {{ const data = workouts[currentWorkoutIndex].days[currentDayIdx].exercises[currentExIdx].sessionData[currentWeek]; data.rounds[rI].subLoads[sI] = val; save(); }}
        function updateSessionNotes() {{ const val = document.getElementById('session-notes').value; const data = workouts[currentWorkoutIndex].days[currentDayIdx].exercises[currentExIdx].sessionData[currentWeek]; data.notes = val; save(); }}
        function nextExercise() {{ const d = workouts[currentWorkoutIndex].days[currentDayIdx]; if(currentExIdx < d.exercises.length - 1) openExercise(currentExIdx + 1); else startSession(currentDayIdx); }}
        function resetDayAction() {{ if(confirm('RESET?')) {{ const d = workouts[currentWorkoutIndex].days[currentDayIdx]; d.exercises.forEach(ex => {{ if(ex.sessionData) delete ex.sessionData[currentWeek]; }}); if(workouts[currentWorkoutIndex].progress && workouts[currentWorkoutIndex].progress[currentWeek]) delete workouts[currentWorkoutIndex].progress[currentWeek][currentDayIdx]; save(); startSession(currentDayIdx); }} }}
        function finishSession() {{ const w = workouts[currentWorkoutIndex]; if (!w.progress) w.progress = {{}}; if (!w.progress[currentWeek]) w.progress[currentWeek] = {{}}; w.progress[currentWeek][currentDayIdx] = true; save(); showToast("SESSIONE SALVATA"); openWorkout(currentWorkoutIndex); }}
        function save() {{
            localStorage.setItem('pale_workouts', JSON.stringify(workouts));
            if (currentWorkoutIndex !== null) {{
                fetch('/api/workouts', {{ method: 'POST', headers: {{ 'Content-Type': 'application/json' }}, body: JSON.stringify(workouts[currentWorkoutIndex]) }}).catch(e => console.error(e));
            }}
        }}
        function deleteWorkout(i) {{ if(confirm('ELIMINA?')) {{ const id = workouts[i].id; workouts.splice(i, 1); localStorage.setItem('pale_workouts', JSON.stringify(workouts)); renderHome(); fetch(`/api/workouts/${{id}}`, {{ method: 'DELETE' }}).catch(e => console.error(e)); }} }}
        function importAction() {{
            const raw = document.getElementById('import-text').value;
            if(!raw.trim()) return;
            const btn = document.getElementById('import-btn');
            btn.innerText = "Sincronizzazione..."; btn.disabled = true;
            setTimeout(() => {{
                const w = {{ id: "p-" + Date.now(), title: "NUOVO PIANO", subtitle: "", days: [], numWeeks: 4, progress: {{}} }};
                const lines = raw.split('\\n');
                let curD = null;
                lines.forEach(l => {{
                    if(l.startsWith('## ') && (l.toLowerCase().includes('giorno') || l.toLowerCase().includes('sessione'))) {{
                        if(curD) w.days.push(curD);
                        curD = {{ name: l.replace('##', '').trim(), exercises: [] }};
                    }} else if(curD && l.includes('|') && !l.includes('Esercizio') && !l.includes('---')) {{
                        const cols = l.split('|').map(c => c.trim());
                        if(cols.length >= 4) curD.exercises.push({{ name: cols[1], sets: cols[2], reps: cols[3], rest: cols[4] || "90s", notes: cols[5] || "" }});
                    }}
                }});
                if(curD) w.days.push(curD);
                if(w.days.length > 0) {{ workouts.unshift(w); save(); showView('view-home'); renderHome(); }}
                btn.innerText = "Sincronizza"; btn.disabled = false;
            }}, 800);
        }}
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
    print(f"Successo: UI Neomorphism Compatta generata.")
