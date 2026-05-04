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
    <style>
        :root {{
            --bg-color: #050507;
            --card-bg: rgba(25, 25, 35, 0.8);
            --accent-color: #cfff04;
            --accent-glow: rgba(207, 255, 4, 0.3);
            --text-primary: #ffffff;
            --text-secondary: #8a8a93;
            --border-radius: 32px;
            --safe-area-top: env(safe-area-inset-top);
        }}

        * {{ box-sizing: border-box; -webkit-tap-highlight-color: transparent; outline: none; }}
        body {{
            background-color: var(--bg-color);
            background-image: radial-gradient(circle at 10% 10%, rgba(207, 255, 4, 0.05) 0%, transparent 40%);
            color: var(--text-primary);
            font-family: 'Outfit', sans-serif;
            margin: 0; padding: 0; overflow-x: hidden;
        }}

        .view {{ display: none; padding: calc(40px + var(--safe-area-top)) 24px 140px 24px; min-height: 100vh; position: relative; z-index: 10; }}
        .view.active {{ display: block; animation: fadeIn 0.3s ease; }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}

        h1 {{ font-size: 2.8rem; font-weight: 900; margin: 0; letter-spacing: -2px; text-transform: uppercase; line-height: 1; }}
        .subtitle {{ color: var(--text-secondary); font-size: 1rem; margin-top: 8px; }}

        .resume-card {{
            background: linear-gradient(135deg, #151518 0%, #1e1e24 100%);
            border-radius: 28px; padding: 25px; margin: 25px 0;
            border: 1px solid rgba(255,255,255,0.08);
            box-shadow: 0 15px 30px rgba(0,0,0,0.4);
            cursor: pointer;
        }}

        .progress-container {{ width: 100%; height: 6px; background: rgba(255,255,255,0.03); border-radius: 10px; margin: 20px 0; overflow: hidden; }}
        .progress-bar {{ height: 100%; background: var(--accent-color); transition: width 0.8s ease; }}

        .week-grid {{ display: flex; gap: 12px; margin-bottom: 25px; overflow-x: auto; padding-bottom: 10px; scrollbar-width: none; }}
        .week-btn {{ 
            flex: 0 0 100px; padding: 18px; background: var(--card-bg); 
            border-radius: 22px; text-align: center; cursor: pointer; opacity: 0.3;
            border: 1px solid rgba(255,255,255,0.05); transition: 0.3s;
        }}
        .week-btn.unlocked {{ opacity: 0.6; }}
        .week-btn.active {{ opacity: 1; background: var(--accent-color); color: #000; box-shadow: 0 8px 20px var(--accent-glow); }}

        .day-grid {{ display: grid; gap: 14px; }}
        .day-card {{ 
            background: var(--card-bg); border-radius: 28px; padding: 25px; 
            border: 1px solid rgba(255,255,255,0.05); backdrop-filter: blur(10px);
            display: flex; justify-content: space-between; align-items: center; cursor: pointer;
            transition: 0.2s;
        }}
        .day-card.locked {{ opacity: 0.2; filter: grayscale(1); }}
        .day-card.completed {{ border-left: 8px solid var(--accent-color); background: rgba(207, 255, 4, 0.03); }}
        .day-card.skipped {{ border-left: 8px solid #444; }}

        .status-tag {{ font-size: 0.7rem; font-weight: 900; padding: 6px 12px; border-radius: 12px; background: rgba(255,255,255,0.05); }}
        .completed .status-tag {{ background: var(--accent-color); color: #000; }}

        .exercise-card {{ background: var(--card-bg); border-radius: 28px; padding: 25px; margin-bottom: 16px; border: 1px solid rgba(255,255,255,0.05); }}
        .exercise-card.fully-done {{ opacity: 0.3; filter: grayscale(1); }}
        
        .sets-wrap {{ display: flex; gap: 8px; flex-wrap: wrap; margin-top: 15px; }}
        .set-btn {{ 
            width: 48px; height: 48px; border-radius: 14px; border: 2px solid rgba(255,255,255,0.1);
            display: flex; align-items: center; justify-content: center; font-weight: 800; cursor: pointer;
        }}
        .set-btn.checked {{ background: var(--accent-color); color: #000; border-color: transparent; }}

        .nav-dock {{ position: fixed; bottom: 0; left: 0; width: 100%; padding: 25px 25px 45px 25px; background: linear-gradient(to top, var(--bg-color) 80%, transparent); display: flex; gap: 12px; z-index: 100; }}
        .btn {{ flex: 1; border: none; padding: 22px; border-radius: 24px; font-weight: 800; cursor: pointer; text-transform: uppercase; font-size: 0.85rem; }}
        .btn-main {{ background: var(--accent-color); color: #000; box-shadow: 0 10px 25px var(--accent-glow); }}
        .btn-alt {{ background: rgba(255,255,255,0.08); color: #fff; }}

        #timer-screen {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.98); z-index: 3000; display: none; flex-direction: column; align-items: center; justify-content: center; }}
        #timer-clock {{ font-size: 10rem; font-weight: 900; color: var(--accent-color); }}
    </style>
</head>
<body>
    <div id="view-home" class="view active">
        <h1>Pale<br><span style="color:var(--accent-color)">App</span></h1>
        <p class="subtitle">Touch to start protocol.</p>
        <div id="resume-section"></div>
        <div id="workouts-list"></div>
        <div onclick="showView('view-import')" style="position: fixed; bottom: 40px; right: 25px; width: 75px; height: 75px; background: var(--accent-color); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; color: #000; box-shadow: 0 15px 30px var(--accent-glow); z-index: 1000; cursor: pointer;">+</div>
    </div>

    <div id="view-import" class="view">
        <div onclick="showView('view-home')" style="color:var(--text-secondary); font-weight:800; cursor:pointer; margin-bottom:25px;">← BACK</div>
        <h1>Import</h1>
        <textarea id="import-text" style="width: 100%; height: 300px; background: #111; color: #fff; border-radius: 24px; padding: 25px; border: 1px solid #333; margin: 20px 0;" placeholder="Paste text here..."></textarea>
        <button class="btn btn-main" style="width: 100%" onclick="importAction()">SAVE PLAN</button>
    </div>

    <div id="view-plan" class="view">
        <div onclick="showView('view-home')" style="color:var(--text-secondary); font-weight:800; cursor:pointer; margin-bottom:25px;">← DASHBOARD</div>
        <h1 id="plan-title">Protocol</h1>
        <div class="progress-container"><div class="progress-bar" id="total-progress-bar"></div></div>
        <div class="week-grid" id="week-selector"></div>
        <div class="day-grid" id="day-list"></div>
    </div>

    <div id="view-session" class="view">
        <div onclick="openWorkout(currentWorkoutIndex)" style="color:var(--text-secondary); font-weight:800; cursor:pointer; margin-bottom:25px;">← PIANO</div>
        <h1 id="session-title">Day X</h1>
        <p class="subtitle" id="session-subtitle">Week 1</p>
        <div id="session-content" style="margin-top:20px;"></div>
        <div class="nav-dock">
            <button id="restart-btn" class="btn btn-alt" style="display:none; color:#ff4444;" onclick="resetAction()">RESET</button>
            <button id="skip-btn" class="btn btn-alt" onclick="quickSkipAction()" style="flex: 0.3">SKIP</button>
            <button class="btn btn-main" id="timerBtn" onclick="startTimer()">REC</button>
            <button id="finish-btn" class="btn btn-alt" onclick="finishAction()">FINE</button>
        </div>
    </div>

    <div id="timer-screen" onclick="stopTimer()"><div id="timer-clock">90</div><p>READY?</p></div>

    <script>
        let workouts = JSON.parse(localStorage.getItem('pale_workouts') || '[]');
        let currentWorkoutIndex = null;
        let currentWeek = 1;
        let currentDayIdx = null;
        let activeRestTime = 90;

        function getInc(w) {{
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
            if(id === 'view-home') renderHome();
        }}

        function renderHome() {{
            const res = document.getElementById('resume-section');
            res.innerHTML = '';
            if (workouts.length > 0) {{
                const w = workouts[0];
                const n = getInc(w);
                if (n) res.innerHTML = `<div class="resume-card" onclick="openWorkout(0)"><h2>CONTINUA: ${{w.title}}</h2><small>Prossima: W${{n.week}} • Giorno ${{n.day+1}}</small></div>`;
            }}
            const list = document.getElementById('workouts-list');
            list.innerHTML = workouts.length === 0 ? '<p>Nessun piano.</p>' : '<h3>I tuoi Piani</h3>';
            workouts.forEach((w, i) => {{
                const c = document.createElement('div');
                c.className = 'day-card';
                c.style.opacity = '1'; c.style.marginBottom = '12px';
                c.onclick = () => openWorkout(i);
                c.innerHTML = `<div><b>${{w.title}}</b><br><small>${{w.numWeeks}} WEEKS</small></div>`;
                list.appendChild(c);
            }});
        }}

        function openWorkout(idx) {{
            currentWorkoutIndex = idx;
            const w = workouts[idx];
            const n = getInc(w);
            if(n && !currentWeek) currentWeek = n.week;
            else if(!currentWeek) currentWeek = 1;

            document.getElementById('plan-title').innerText = w.title;
            updateProg(w);

            const sel = document.getElementById('week-selector');
            sel.innerHTML = '';
            for(let i=1; i<=w.numWeeks; i++) {{
                const isU = n ? i <= n.week : true;
                const b = document.createElement('div');
                b.className = `week-btn ${{currentWeek === i ? 'active' : ''}} ${{isU ? 'unlocked' : ''}}`;
                b.innerHTML = `<span class="week-num">W${{i}}</span>`;
                b.onclick = () => {{ currentWeek = i; openWorkout(idx); }};
                sel.appendChild(b);
            }}

            const dList = document.getElementById('day-list');
            dList.innerHTML = '';
            w.days.forEach((d, dI) => {{
                const status = w.progress && w.progress[currentWeek] && w.progress[currentWeek][dI];
                const isU = n ? (currentWeek < n.week || (currentWeek === n.week && dI <= n.day)) : true;
                const c = document.createElement('div');
                c.className = `day-card ${{status === true ? 'completed' : ''}} ${{status === 'skipped' ? 'skipped' : ''}} ${{!isU ? 'locked' : ''}}`;
                c.onclick = () => {{ if(isU) startSession(dI); else alert('Giorno bloccato!'); }};
                let t = isU ? 'READY' : 'LOCKED';
                if(status === true) t = 'DONE';
                if(status === 'skipped') t = 'SKIP';
                c.innerHTML = `<div><h4>GIORNO ${{dI + 1}}</h4><small>${{d.name.split('-')[1] || d.name}}</small></div><div class="status-tag">${{t}}</div>`;
                dList.appendChild(c);
            }});
            showView('view-plan');
        }}

        function startSession(dI) {{
            currentDayIdx = dI;
            const w = workouts[currentWorkoutIndex];
            const d = w.days[dI];
            const status = w.progress && w.progress[currentWeek] && w.progress[currentWeek][dI];
            document.getElementById('session-title').innerText = `GIORNO ${{dI + 1}}`;
            document.getElementById('session-subtitle').innerText = `WEEK ${{currentWeek}} • ${{d.name.split('-')[1] || ''}}`;
            document.getElementById('restart-btn').style.display = status ? 'block' : 'none';
            document.getElementById('finish-btn').style.display = status ? 'none' : 'block';
            document.getElementById('skip-btn').style.display = status ? 'none' : 'block';

            const content = document.getElementById('session-content');
            content.innerHTML = '';
            d.exercises.forEach((ex, eI) => {{
                const nS = parseInt(ex.sets) || 1;
                if(!ex.setStates) ex.setStates = new Array(nS).fill(false);
                const isD = ex.setStates.every(s => s === true);
                const card = document.createElement('div');
                card.className = `exercise-card ${{isD ? 'fully-done' : ''}}`;
                let bs = '';
                for(let i=0; i<nS; i++) bs += `<div class="set-btn ${{ex.setStates[i] ? 'checked' : ''}}" onclick="toggleSetAction(${{eI}}, ${{i}})">${{i+1}}</div>`;
                card.innerHTML = `<b>${{ex.name}}</b><br><small>${{ex.sets}}x${{ex.reps}} • ${{ex.rest}}</small><div class="sets-wrap">${{bs}}</div>`;
                content.appendChild(card);
            }});
            showView('view-session');
        }}

        function toggleSetAction(eI, sI) {{
            const ex = workouts[currentWorkoutIndex].days[currentDayIdx].exercises[eI];
            ex.setStates[sI] = !ex.setStates[sI];
            if(ex.setStates[sI]) activeRestTime = parseRest(ex.rest);
            startSession(currentDayIdx);
            save();
        }}

        function resetAction() {{ if(confirm('RESET?')) {{ const w = workouts[currentWorkoutIndex]; delete w.progress[currentWeek][currentDayIdx]; w.days[currentDayIdx].exercises.forEach(ex => delete ex.setStates); save(); startSession(currentDayIdx); }} }}
        function finishAction() {{ const w = workouts[currentWorkoutIndex]; if (!w.progress[currentWeek]) w.progress[currentWeek] = {{}}; w.progress[currentWeek][currentDayIdx] = true; save(); openWorkout(currentWorkoutIndex); }}
        function quickSkipAction() {{ if(confirm('SKIP?')) {{ const w = workouts[currentWorkoutIndex]; if (!w.progress[currentWeek]) w.progress[currentWeek] = {{}}; w.progress[currentWeek][currentDayIdx] = 'skipped'; save(); openWorkout(currentWorkoutIndex); }} }}
        function updateProg(w) {{ let t = w.numWeeks * w.days.length; let d = 0; if (w.progress) Object.values(w.progress).forEach(wk => {{ d += Object.keys(wk).length; }}); document.getElementById('total-progress-bar').style.width = `${{(d / t) * 100}}%`; }}
        function parseRest(r) {{ const m = r.match(/(\\d+)/); if (!m) return 90; let v = parseInt(m[1]); return (r.includes("'") || r.toLowerCase().includes("m")) ? v * 60 : v; }}
        function save() {{ localStorage.setItem('pale_workouts', JSON.stringify(workouts)); }}
        let tInt;
        function startTimer() {{ stopTimer(); const s = document.getElementById('timer-screen'); const c = document.getElementById('timer-clock'); s.style.display = 'flex'; let l = activeRestTime; c.innerText = l; tInt = setInterval(() => {{ l--; c.innerText = l; if (l <= 0) {{ stopTimer(); if(navigator.vibrate) navigator.vibrate([400, 100, 400]); }} }}, 1000); }}
        function stopTimer() {{ clearInterval(tInt); document.getElementById('timer-screen').style.display = 'none'; }}
        function importAction() {{
            const t = document.getElementById('import-text').value;
            if(!t.trim()) return;
            const w = {{ id: "p-" + Date.now(), title: t.split('\\n')[0].substring(0,15).toUpperCase(), numWeeks: 4, days: [], progress: {{}} }};
            const lines = t.split('\\n'); let curD = null;
            lines.forEach(l => {{
                if(l.match(/Giorno|Day|Sessione/i)) {{ if(curD) w.days.push(curD); curD = {{ name: l.trim(), exercises: [] }}; }}
                else {{ const m = l.match(/(\\d+)\\s*[xX]\\s*(\\d+)/); if(m && curD) curD.exercises.push({{ name: l.split(m[0])[0].replace(/[-•*]/g, '').trim(), sets: m[1], reps: m[2], rest: "90s", notes: "" }}); }}
            }});
            if(curD) w.days.push(curD);
            if(w.days.length > 0) {{ workouts.unshift(w); save(); showView('view-home'); }}
        }}
        function deleteWorkout(i) {{ if(confirm('DELETE?')) {{ workouts.splice(i, 1); save(); renderHome(); }} }}
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
    print(f"Successo: Pale App ripristinata e cliccabile.")
