from flask import Flask, request, session, redirect, url_for, send_from_directory, render_template_string, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from dotenv import load_dotenv
import os

# Carica le variabili dal file .env se presente
load_dotenv()

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# Per sicurezza, usa una chiave segreta dalle variabili d'ambiente
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'pale-secret-key-123')
PASSWORD_HASH = os.environ.get('APP_PASSWORD_HASH')

# Configurazione Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modello Workout
class WorkoutModel(db.Model):
    __tablename__ = 'workouts'
    id = db.Column(db.String(50), primary_key=True)
    data = db.Column(db.JSON, nullable=False)

# Crea le tabelle se non esistono
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"Errore creazione tabelle: {e}")

LOGIN_HTML = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>Pale App - Auth</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@200;400;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-canvas: #F8F8F8;
            --text-dark: #111111;
            --accent-lime: #BFFF00;
            --accent-pink: #FF0077;
            --accent-blue: #0055FF;
            --border-heavy: 2.5px;
        }

        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; outline: none; }
        
        body {
            background-color: var(--bg-canvas);
            background-image: 
                linear-gradient(rgba(0,0,0,0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0,0,0,0.03) 1px, transparent 1px);
            background-size: 25px 25px;
            color: var(--text-dark);
            font-family: 'Outfit', sans-serif;
            margin: 0; padding: 0; height: 100vh;
            display: flex; align-items: center; justify-content: center;
        }

        .login-node {
            width: 100%; max-width: 360px; padding: 15px;
        }

        .tech-card {
            background: #fff; border: var(--border-heavy) solid #000;
            padding: 30px; position: relative;
            box-shadow: 12px 12px 0px rgba(0,0,0,0.05);
        }
        .tech-card::before { content: 'AUTH_GATE.01'; position: absolute; top: -11px; right: 12px; font-size: 0.5rem; font-family: 'JetBrains Mono', monospace; background: #000; color: #fff; padding: 2px 10px; }
        
        .brand-logo { text-align: center; margin-bottom: 40px; }
        .brand-logo h1 { font-size: 3.5rem; font-weight: 900; line-height: 0.8; margin: 0; letter-spacing: -3px; }
        .brand-logo span { color: var(--accent-blue); opacity: 0.4; }

        .input-group { margin-bottom: 35px; text-align: center; }
        .input-group label { display: block; font-family: 'JetBrains Mono'; font-size: 0.5rem; font-weight: 900; text-transform: uppercase; margin-bottom: 8px; opacity: 0.6; }
        
        input { 
            width: 100%; border: none; border-bottom: 5px solid #000; 
            background: transparent; font-family: 'JetBrains Mono'; font-size: 2rem; 
            text-align: center; font-weight: 900; padding: 10px 0;
            transition: 0.3s;
        }
        input:focus { border-color: var(--accent-blue); }

        .btn-elite {
            position: relative; height: 68px; border: none; background: transparent;
            cursor: pointer; display: flex; align-items: center; justify-content: center;
            width: 100%; transition: 0.1s;
        }
        .btn-elite .body {
            position: absolute; inset: 0; background: var(--accent-lime); color: #000;
            border: var(--border-heavy) solid #000;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            z-index: 2; clip-path: polygon(0 0, 95% 0, 100% 15%, 100% 100%, 5% 100%, 0 85%);
        }
        .btn-elite .shadow {
            position: absolute; inset: 8px -8px -8px 8px; background: #000;
            z-index: 1; clip-path: polygon(0 0, 95% 0, 100% 15%, 100% 100%, 5% 100%, 0 85%);
        }
        .btn-elite .hatch {
            position: absolute; left: 0; top: 0; bottom: 0; width: 14px;
            background: repeating-linear-gradient(45deg, transparent, transparent 4px, rgba(0,0,0,0.05) 4px, rgba(0,0,0,0.05) 8px);
        }
        .btn-elite .main-txt { font-weight: 900; font-size: 1.2rem; text-transform: uppercase; letter-spacing: 2px; }
        .btn-elite .sub-txt { font-family: 'JetBrains Mono'; font-size: 0.45rem; opacity: 0.6; margin-top: 4px; }
        
        .btn-elite:active { transform: translate(4px, 4px); }
        .btn-elite:active .shadow { inset: 0; opacity: 0; }

        .error-node {
            background: var(--accent-pink); color: #fff; padding: 12px;
            font-family: 'JetBrains Mono'; font-size: 0.6rem; font-weight: 900;
            margin-top: 25px; text-align: center; border: 2px solid #000;
            text-transform: uppercase;
        }
    </style>
</head>
<body>
    <div class="login-node">
        <div class="tech-card">
            <div class="brand-logo">
                <h1>PALE<span>.SYS</span></h1>
            </div>
            <form method="post">
                <div class="input-group">
                    <label>CORE_AUTH_KEY_REQUIRED</label>
                    <input type="password" name="password" required autofocus>
                </div>
                <button type="submit" class="btn-elite">
                    <div class="body">
                        <div class="hatch"></div>
                        <span class="main-txt">INITIATE</span>
                        <span class="sub-txt">AUTH_SEQUENCE_START</span>
                    </div>
                    <div class="shadow"></div>
                </button>
            </form>
            {% if error %}<div class="error-node">ACCESS_DENIED: {{ error }}</div>{% endif %}
        </div>
    </div>
</body>
</html>
"""

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        password = request.form.get('password')
        if PASSWORD_HASH:
            if check_password_hash(PASSWORD_HASH, password):
                session['logged_in'] = True
                return redirect(url_for('index'))
        elif password == "admin": 
            session['logged_in'] = True
            return redirect(url_for('index'))
        error = "Accesso negato"
    return render_template_string(LOGIN_HTML, error=error)

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return send_from_directory('.', 'index.html')

# API Endpoints
@app.route('/api/workouts', methods=['GET'])
def get_workouts():
    if not session.get('logged_in'): return jsonify({"error": "Unauthorized"}), 401
    workouts = WorkoutModel.query.all()
    return jsonify([w.data for w in workouts])

@app.route('/api/workouts', methods=['POST'])
def save_workout():
    if not session.get('logged_in'): return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    workout_id = data.get('id')
    if not workout_id: return jsonify({"error": "Missing ID"}), 400
    
    workout = WorkoutModel.query.get(workout_id)
    if workout:
        workout.data = data
    else:
        workout = WorkoutModel(id=workout_id, data=data)
        db.session.add(workout)
    
    db.session.commit()
    return jsonify({"success": True})

@app.route('/api/workouts/<id>', methods=['DELETE'])
def delete_workout(id):
    if not session.get('logged_in'): return jsonify({"error": "Unauthorized"}), 401
    workout = WorkoutModel.query.get(id)
    if workout:
        db.session.delete(workout)
        db.session.commit()
    return jsonify({"success": True})

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/<path:path>')
def static_proxy(path):
    if not session.get('logged_in') and path != 'login':
        return redirect(url_for('login'))
    return send_from_directory('.', path)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
