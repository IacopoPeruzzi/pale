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
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@200;400;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-canvas: #F8F8F8;
            --text-dark: #111111;
            --accent-lime: #BFFF00;
            --accent-pink: #FF0077;
            --accent-blue: #0055FF;
            --border-heavy: 2.5px;
            --border-light: 1px;
            --safe-top: env(safe-area-inset-top);
        }}

        @keyframes prop-pulse {{ 0% {{ background: transparent; }} 50% {{ background: var(--accent-lime); opacity: 0.3; }} 100% {{ background: transparent; }} }}

        * {{ box-sizing: border-box; -webkit-tap-highlight-color: transparent; outline: none; }}
        
        body {{
            background-color: var(--bg-canvas);
            background-image: 
                linear-gradient(rgba(0,0,0,0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0,0,0,0.03) 1px, transparent 1px);
            background-size: 25px 25px;
            color: var(--text-dark);
            font-family: 'Outfit', sans-serif;
            margin: 0; padding: 0; overflow-x: hidden;
        }}

        .ui-anchor {{
            position: fixed; top: calc(12px + var(--safe-top)); left: 12px; right: 12px;
            z-index: 5000; pointer-events: none;
            display: flex; justify-content: space-between; align-items: flex-start;
        }}

        .badge-core {{
            pointer-events: auto; background: #000; color: #fff;
            padding: 10px 18px; border: var(--border-heavy) solid #000;
            box-shadow: 5px 5px 0px var(--accent-lime);
            display: flex; flex-direction: column; cursor: pointer;
        }}
        .badge-core .t1 {{ font-size: 1.2rem; font-weight: 900; letter-spacing: -1.5px; line-height: 0.9; }}
        .badge-core .t2 {{ font-size: 0.45rem; font-family: 'JetBrains Mono', monospace; opacity: 0.6; margin-top: 4px; }}

        .ctrl-box {{
            pointer-events: auto; width: 48px; height: 48px; background: #fff;
            border: var(--border-heavy) solid #000; box-shadow: 5px 5px 0px #000;
            display: flex; align-items: center; justify-content: center;
            font-weight: 900; font-size: 0.6rem; cursor: pointer;
        }}
        .ctrl-box:active {{ transform: translate(3px, 3px); box-shadow: 0px 0px 0px #000; }}

        .view {{ display: none; padding: 12px; padding-top: 95px; min-height: 100vh; position: relative; z-index: 10; }}
        .view.active {{ display: block; animation: fade-in 0.25s ease-out; }}
        @keyframes fade-in {{ from {{ opacity: 0; transform: translateY(4px); }} to {{ opacity: 1; transform: translateY(0); }} }}

        .tech-card {{
            background: #fff; border: var(--border-heavy) solid #000;
            padding: 16px; margin-bottom: 25px; position: relative;
            box-shadow: 8px 8px 0px rgba(0,0,0,0.03);
        }}
        .tech-card::before {{ content: 'RE_SYS.04'; position: absolute; top: -11px; right: 12px; font-size: 0.5rem; font-family: 'JetBrains Mono', monospace; background: #000; color: #fff; padding: 2px 8px; }}
        .tech-card .label {{ font-size: 0.55rem; font-weight: 900; background: var(--accent-lime); color: #000; padding: 2px 8px; border: 1.5px solid #000; margin-bottom: 10px; display: inline-block; text-transform: uppercase; }}

        .heading-xl {{
            font-size: 1.7rem; font-weight: 900; line-height: 0.85; text-transform: uppercase;
            letter-spacing: -1.5px; margin: 0;
        }}
        .heading-xl span {{ color: var(--accent-blue); }}

        .shard-node {{ 
            background: #fff; color: #000; border: var(--border-light) solid #000; 
            padding: 14px 18px; margin-bottom: 10px; 
            display: flex; align-items: center; cursor: pointer;
            font-weight: 700; text-transform: uppercase; font-size: 0.9rem;
            transition: 0.1s;
        }}
        .shard-node:active {{ border-width: var(--border-heavy); background: var(--bg-canvas); }}
        .shard-node.done {{ border-left: 12px solid var(--accent-lime); background: #fff; font-weight: 900; }}

        .btn-tech {{
            background: #000; color: #fff;
            border: none; padding: 18px; font-weight: 900; 
            text-transform: uppercase; font-size: 1rem; cursor: pointer;
            width: 100%; box-shadow: 6px 6px 0px var(--accent-lime);
            transition: 0.1s;
        }}
        .btn-tech:active {{ transform: translate(3px, 3px); box-shadow: 0px 0px 0px #000; background: #222; }}
        .btn-tech.warning {{ background: var(--accent-pink); box-shadow: 6px 6px 0px #000; }}

        .selector-row {{ display: flex; gap: 8px; margin-bottom: 30px; overflow-x: auto; padding: 10px 5px; }}
        .selector-node {{ 
            flex: 0 0 55px; height: 55px; border: var(--border-light) solid #000;
            display: flex; align-items: center; justify-content: center;
            font-weight: 900; cursor: pointer; font-size: 0.85rem; background: #fff;
        }}
        .selector-node.active {{ background: #000; color: #fff; border-width: var(--border-heavy); transform: translateY(-5px); box-shadow: 6px 6px 0px var(--accent-lime); }}

        .data-strip {{ display: flex; gap: 10px; margin-top: 15px; }}
        .data-box {{ 
            background: #fff; border: var(--border-light) solid #000; padding: 10px; text-align: center; flex: 1;
        }}
        .data-box .v {{ font-size: 1.2rem; font-weight: 900; font-family: 'JetBrains Mono', monospace; display: block; }}
        .data-box .l {{ font-size: 0.45rem; opacity: 0.5; text-transform: uppercase; font-weight: 700; margin-top: 4px; display: block; }}

        .set-container {{ 
            background: #fff; border: var(--border-heavy) solid #000; 
            padding: 18px; margin-bottom: 25px; position: relative;
            scroll-margin-top: 110px;
        }}
        
        .badge-id {{ 
            width: 36px; height: 36px; border: var(--border-heavy) solid #000; 
            font-weight: 900; font-family: 'JetBrains Mono', monospace; font-size: 1rem;
            display: flex; align-items: center; justify-content: center; cursor: pointer;
            background: #fff; transition: 0.15s;
        }}
        .badge-id.active {{ background: var(--accent-lime); transform: scale(1.1); box-shadow: 4px 4px 0px #000; }}

        .input-tech {{ 
            border: none; border-bottom: 4px solid #000; 
            font-weight: 900; font-family: 'JetBrains Mono', monospace; font-size: 2.2rem; 
            width: 100px; text-align: center; background: transparent; color: #000; 
            transition: background 0.3s;
        }}
        .input-tech.pulse {{ animation: prop-pulse 0.6s ease-out; }}
        
        .prog-grid {{ height: 10px; display: flex; gap: 3px; margin-bottom: 35px; }}
        .prog-cell {{ flex: 1; background: #fff; border: 1px solid rgba(0,0,0,0.1); transition: 0.3s; }}
        .prog-cell.on {{ background: #000; border-color: #000; box-shadow: 0 0 5px rgba(0,0,0,0.2); }}

        #toast {{ 
            position: fixed; bottom: 25px; left: 15px; right: 15px;
            background: #000; color: #fff; padding: 15px; 
            font-weight: 900; font-family: 'JetBrains Mono', monospace; 
            border: var(--border-heavy) solid var(--accent-lime); z-index: 10000;
            display: none; text-align: center; text-transform: uppercase; font-size: 0.8rem;
        }}
        
        ::-webkit-scrollbar {{ display: none; }}
    </style>
</head>
<body>
    <div id="toast"></div>

    <div class="ui-anchor">
        <div class="badge-core" onclick="showView('view-home')">
            <div class="t1">PALE.SYSTEM</div>
            <div class="t2">ENGINE_V4.6_TRACK</div>
        </div>
        <div class="ctrl-box" onclick="showView('view-import')">
            SYNC
        </div>
    </div>

    <div id="view-home" class="view active">
        <div id="progress-grid" class="prog-grid"></div>
        <div id="resume-section"></div>
        <div style="font-weight:900; color:#000; font-size:0.5rem; margin:20px 0 10px 0; letter-spacing:1px; display:flex; align-items:center; gap:8px;">
            <div style="width:12px; height:2px; background:#000;"></div> DATA_CORE_ARCHIVE
        </div>
        <div id="workouts-list"></div>
    </div>

    <div id="view-import" class="view">
        <div class="tech-card" style="background:var(--accent-lime)">
            <span class="label">Kernel.Inbound</span>
            <h2 class="heading-xl">INJECT<span>SOURCE</span></h2>
            <textarea id="import-text" style="width:100%; height:260px; border:var(--border-heavy) solid #000; background:#fff; padding:18px; font-family:'JetBrains Mono', monospace; font-weight:700; font-size:0.8rem; margin:15px 0;"></textarea>
            <button id="import-btn" class="btn-tech" onclick="importAction()">EXECUTE_SYNC</button>
            <button class="btn-tech" style="margin-top:12px; background:transparent; border:none; box-shadow:none; color:#000; font-size:0.8rem;" onclick="showView('view-home')">CANCEL_SYSTEM</button>
        </div>
    </div>

    <div id="view-workout" class="view">
        <div id="workout-content"></div>
        <div style="margin-top:35px;"><button class="btn-tech" onclick="showView('view-home')">TERMINATE_SESSION</button></div>
    </div>

    <div id="view-session" class="view">
        <div id="session-header"></div>
        <div id="session-content"></div>
        <div style="margin-top:35px; display:flex; gap:12px;">
            <button class="btn-tech" style="flex:1; background:#fff; color:#000; border:var(--border-heavy) solid #000; box-shadow:none;" onclick="openWorkout(currentWorkoutIndex)">BACK</button>
            <button class="btn-tech" style="flex:2;" onclick="finishSession()">COMMIT_LOG_DATA</button>
        </div>
    </div>

    <div id="view-exercise" class="view">
        <div id="ex-header"></div>
        <div id="ex-content"></div>
        <div style="margin-top:35px; display:flex; gap:12px;" id="exercise-actions">
            <button class="btn-tech" style="padding:12px; flex:0.4; background:#fff; color:#000; border:var(--border-heavy) solid #000; box-shadow:none;" onclick="startSession(currentDayIdx)">LST</button>
            <button class="btn-tech warning" style="flex:1;" onclick="nextExercise()">SKIP</button>
            <button class="btn-tech" style="flex:2; background:var(--accent-lime); color:#000;" onclick="nextExercise()">NEXT_FORWARD</button>
        </div>
    </div>

    <script>
        let workouts = JSON.parse(localStorage.getItem('pale_workouts') || '[]');
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
            setTimeout(() => t.style.display = 'none', 1500);
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

        function renderHome() {{
            const res = document.getElementById('resume-section');
            const grid = document.getElementById('progress-grid');
            res.innerHTML = ''; grid.innerHTML = '';
            
            if (workouts.length > 0) {{
                const w = workouts[0];
                const n = getInc(w);
                let total = w.numWeeks * (w.days?w.days.length:0);
                let done = 0;
                if (w.progress) Object.values(w.progress).forEach(wk => done += Object.keys(wk).length);
                
                for(let i=0; i<20; i++) {{
                    const c = document.createElement('div');
                    c.className = `prog-cell ${{i < (done/total)*20 ? 'on' : ''}}`;
                    grid.appendChild(c);
                }}

                if (n) {{
                    res.innerHTML = `
                        <div class="tech-card" onclick="resumeWorkout(0)">
                            <span class="label">Session.Active</span>
                            <h2 class="heading-xl">${{sanitize(w.title)}}<span>_ONLINE</span></h2>
                            <p style="font-family:'JetBrains Mono', monospace; font-weight:700; margin-top:10px; font-size:0.85rem;">[ PHASE_0${{n.week}} // NODE_0${{n.day+1}} ]</p>
                        </div>`;
                }}
            }}
            const list = document.getElementById('workouts-list');
            list.innerHTML = '';
            workouts.forEach((w, i) => {{
                const card = document.createElement('div');
                card.className = `shard-node`;
                card.onclick = () => openWorkout(i);
                card.innerHTML = `<div style="flex:1">${{w.title}}</div><div style="font-size:0.45rem; border:1px solid #000; padding:2px 6px; font-family:'JetBrains Mono'">OPEN_ARCHIVE</div>`;
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
                <div class="tech-card">
                    <span class="label">Protocol.Info</span>
                    <h2 class="heading-xl">${{sanitize(w.title)}}<span>_V4</span></h2>
                    ${{weekInfo ? `<div style="background:var(--bg-canvas); border-left:6px solid var(--accent-blue); padding:15px; margin-top:12px; font-family:'JetBrains Mono'; font-size:0.75rem;">// LOG: ${{weekInfo.note || weekInfo.focus}}</div>` : ''}}
                </div>
                <div class="selector-row" id="week-selector"></div>
                <div id="day-list"></div>
            `;
            const sel = document.getElementById('week-selector');
            for(let i=1; i<=w.numWeeks; i++) {{
                const b = document.createElement('div');
                b.className = `selector-node ${{currentWeek === i ? 'active' : ''}}`;
                b.innerHTML = `W0${{i}}`;
                b.onclick = () => {{ currentWeek = i; openWorkout(idx); }};
                sel.appendChild(b);
            }}
            const dList = document.getElementById('day-list');
            w.days.forEach((d, dI) => {{
                const status = w.progress && w.progress[currentWeek] && w.progress[currentWeek][dI];
                const c = document.createElement('div');
                c.className = `shard-node ${{status ? 'done' : ''}}`;
                c.onclick = () => startSession(dI);
                c.innerHTML = `<div style="flex:1"><small style="opacity:0.4; font-size:0.45rem; font-family:'JetBrains Mono'">SYS_DATA.0${{dI+1}}</small><br>${{sanitize(d.name)}}</div>`;
                dList.appendChild(c);
            }});
            showView('view-workout');
        }}

        function startSession(dI) {{
            currentDayIdx = dI;
            const w = workouts[currentWorkoutIndex];
            const d = w.days[dI];
            document.getElementById('session-header').innerHTML = `
                <div class="tech-card" style="background:var(--accent-lime)">
                    <span class="label" style="background:#000; color:#fff;">Channel.Active</span>
                    <h2 class="heading-xl">${{sanitize(d.name)}}<span>_LOG</span></h2>
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-top:15px;">
                        <span style="font-weight:900; background:#000; color:#fff; padding:4px 12px; font-size:0.7rem; font-family:'JetBrains Mono'">PHASE_0${{currentWeek}}</span>
                        <button class="btn-tech" style="font-size:0.5rem; padding:8px 12px; width:auto; box-shadow:none; background:#fff; color:#000; border:2px solid #000;" onclick="resetDayAction()">RESET_CORE</button>
                    </div>
                </div>`;
            const content = document.getElementById('session-content');
            content.innerHTML = '';
            d.exercises.forEach((ex, eI) => {{
                // L'esercizio è completato se TUTTE le serie sono smarcate
                const isD = ex.sessionData && ex.sessionData[currentWeek] && 
                           ex.sessionData[currentWeek].rounds && 
                           ex.sessionData[currentWeek].rounds.length > 0 &&
                           ex.sessionData[currentWeek].rounds.every(r => r.done);
                
                const item = document.createElement('div');
                item.className = `shard-node ${{isD ? 'done' : ''}}`;
                item.onclick = () => openExercise(eI);
                item.innerHTML = `<div style="flex:1">${{sanitize(ex.name)}}</div><div style="font-size:0.65rem; opacity:0.6; font-family:'JetBrains Mono'">${{ex.sets}}S</div>`;
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
            
            if (currentWeek > 1) {{
                const prev = ex.sessionData[currentWeek - 1];
                if (prev && prev.rounds) {{
                    data.rounds.forEach((round, rI) => {{
                        if (prev.rounds[rI] && prev.rounds[rI].subLoads) {{
                            prev.rounds[rI].subLoads.forEach((sLoad, sI) => {{
                                if (round.subLoads[sI] === "" || round.subLoads[sI] === undefined) {{
                                    round.subLoads[sI] = sLoad;
                                }}
                            }});
                        }}
                    }});
                }}
            }}

            document.getElementById('ex-header').innerHTML = `
                <div class="tech-card" style="transform:none;">
                    <span class="label">Target.Dynamics</span>
                    <h2 class="heading-xl">${{sanitize(ex.name)}}<span>_DATA</span></h2>
                    <div class="data-strip">
                        <div class="data-box"><span class="v">${{ex.sets}}</span><span class="l">SETS</span></div>
                        <div class="data-box"><span class="v">${{subExs.length > 1 ? 'CIRC' : ex.reps}}</span><span class="l">REPS</span></div>
                        <div class="data-box" style="background:var(--accent-lime)"><span class="v">${{ex.rest}}</span><span class="l">REST</span></div>
                    </div>
                </div>`;
            const content = document.getElementById('ex-content');
            content.innerHTML = '';
            data.rounds.forEach((round, rI) => {{
                const block = document.createElement('div');
                block.className = 'set-container';
                block.id = 'set-block-' + rI;
                let subHtml = '';
                subExs.forEach((sx, sI) => {{
                    subHtml += `<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:18px;">
                        <div><b style="font-size:1.1rem; line-height:0.85;">${{sx.name}}</b><br><small style="font-family:'JetBrains Mono'; font-weight:700; font-size:0.5rem; color:#888;">// TGT: ${{sx.reps}}</small></div>
                        <div style="display:flex; align-items:center;">
                            <input type="number" class="input-tech subload-input" data-round="${{rI}}" data-sub="${{sI}}" value="${{round.subLoads[sI] || ""}}" oninput="updateSubLoad(${{rI}}, ${{sI}}, this.value)">
                            <small style="font-weight:900; font-family:'JetBrains Mono'; margin-left:8px; font-size:0.75rem;">KG</small>
                        </div>
                    </div>`;
                }});
                block.innerHTML = `
                    <div style="display:flex; align-items:center; gap:20px; margin-bottom:20px;">
                        <div class="badge-id ${{round.done ? 'active' : ''}}" data-round-badge="${{rI}}" onclick="toggleRound(${{rI}})">${{rI+1}}</div>
                        <div style="font-family:'JetBrains Mono'; font-weight:900; text-transform:uppercase; font-size:0.5rem; letter-spacing:1px; background:#000; color:#fff; padding:3px 10px;">CORE_NODE_0${{rI+1}}</div>
                    </div>
                    ${{subHtml}}`;
                content.appendChild(block);
            }});
            const notes = document.createElement('div');
            notes.className = 'tech-card';
            notes.style.background = 'var(--accent-pink)';
            notes.innerHTML = `<span class="label" style="background:#fff;">Log.Notes</span><textarea id="session-notes" oninput="updateSessionNotes()" style="width:100%; border:var(--border-heavy) solid #000; margin-top:12px; background:#fff; padding:15px; font-family:'JetBrains Mono'; font-weight:700; min-height:100px; font-size:0.85rem;">${{data.notes || ""}}</textarea>`;
            content.appendChild(notes);
            showView('view-exercise');
        }}

        function toggleRound(rI) {{ 
            const data = workouts[currentWorkoutIndex].days[currentDayIdx].exercises[currentExIdx].sessionData[currentWeek]; 
            data.rounds[rI].done = !data.rounds[rI].done; 
            save(); 
            
            const badge = document.querySelector(`[data-round-badge="${{rI}}"]`);
            if (badge) badge.classList.toggle('active');
            
            if (data.rounds[rI].done) {{
                const nextBlock = document.getElementById('set-block-' + (rI + 1));
                if (nextBlock) {{
                    nextBlock.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                }} else {{
                    document.getElementById('exercise-actions').scrollIntoView({{ behavior: 'smooth', block: 'end' }});
                }}
            }}
        }}
        
        function updateSubLoad(rI, sI, val) {{ 
            const data = workouts[currentWorkoutIndex].days[currentDayIdx].exercises[currentExIdx].sessionData[currentWeek]; 
            const oldVal = data.rounds[rI].subLoads[sI];
            data.rounds[rI].subLoads[sI] = val; 
            
            if (rI === 0) {{
                document.querySelectorAll(`.subload-input[data-sub="${{sI}}"]`).forEach(input => {{
                    const roundIdx = parseInt(input.dataset.round);
                    if (roundIdx > 0) {{
                        if (data.rounds[roundIdx].subLoads[sI] === "" || data.rounds[roundIdx].subLoads[sI] === undefined || data.rounds[roundIdx].subLoads[sI] === oldVal) {{
                            input.value = val;
                            input.classList.add('pulse');
                            setTimeout(() => input.classList.remove('pulse'), 600);
                            data.rounds[roundIdx].subLoads[sI] = val;
                        }}
                    }}
                }});
            }}
            save(); 
        }}
        
        function updateSessionNotes() {{ const val = document.getElementById('session-notes').value; const data = workouts[currentWorkoutIndex].days[currentDayIdx].exercises[currentExIdx].sessionData[currentWeek]; data.notes = val; save(); }}
        function nextExercise() {{ const d = workouts[currentWorkoutIndex].days[currentDayIdx]; if(currentExIdx < d.exercises.length - 1) openExercise(currentExIdx + 1); else startSession(currentDayIdx); }}
        function resetDayAction() {{ if(confirm('RESET?')) {{ const d = workouts[currentWorkoutIndex].days[currentDayIdx]; d.exercises.forEach(ex => {{ if(ex.sessionData) delete ex.sessionData[currentWeek]; }}); if(workouts[currentWorkoutIndex].progress && workouts[currentWorkoutIndex].progress[currentWeek]) delete workouts[currentWorkoutIndex].progress[currentWeek][currentDayIdx]; save(); startSession(currentDayIdx); }} }}
        function finishSession() {{ const w = workouts[currentWorkoutIndex]; if (!w.progress) w.progress = {{}}; if (!w.progress[currentWeek]) w.progress[currentWeek] = {{}}; w.progress[currentWeek][currentDayIdx] = true; save(); showToast("DATA_RECORD_COMMITTED"); openWorkout(currentWorkoutIndex); }}
        function save() {{
            localStorage.setItem('pale_workouts', JSON.stringify(workouts));
            if (currentWorkoutIndex !== null) {{
                fetch('/api/workouts', {{ method: 'POST', headers: {{ 'Content-Type': 'application/json' }}, body: JSON.stringify(workouts[currentWorkoutIndex]) }}).catch(e => console.error(e));
            }}
        }}
        function importAction() {{
            const raw = document.getElementById('import-text').value;
            if(!raw.trim()) return;
            const btn = document.getElementById('import-btn');
            btn.innerText = "INITIALIZING..."; btn.disabled = true;
            setTimeout(() => {{
                const w = {{ id: "p-" + Date.now(), title: "CORE_PROTOCOL", subtitle: "", days: [], numWeeks: 4, progress: {{}} }};
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
                btn.innerText = "EXECUTE_SYNC"; btn.disabled = false;
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
    print(f"Successo: UI Cyber-Industrial Track completion generata.")
