from flask import Flask, request, session, redirect, url_for, send_from_directory, render_template_string, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from dotenv import load_dotenv
import os

# Carica le variabili dal file .env se presente
load_dotenv()

app = Flask(__name__)
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
    <title>Pale App - Login</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #f0f4f8;
            --shadow-light: rgba(255, 255, 255, 0.9);
            --shadow-dark: rgba(163, 177, 198, 0.4);
            --accent-blue: #007aff;
            --text-main: #4a5568;
        }

        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; outline: none; }
        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            font-family: 'Outfit', sans-serif;
            margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100vh;
            position: relative; overflow: hidden;
        }

        .bg-blob {
            position: fixed; width: 500px; height: 500px; border-radius: 50%; z-index: -1;
            background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, transparent 70%);
            filter: blur(80px); opacity: 0.6; pointer-events: none;
            animation: float 15s infinite alternate ease-in-out;
        }
        @keyframes float {
            0% { transform: translate(-20%, -20%); }
            100% { transform: translate(20%, 20%); }
        }

        .login-box { 
            text-align: center; width: 100%; max-width: 340px; padding: 60px 30px; 
            background: var(--bg-color); border-radius: 45px;
            box-shadow: 20px 20px 40px var(--shadow-dark), -20px -20px 40px var(--shadow-light);
            position: relative;
        }
        
        .tag {
            font-size: 0.7rem; font-weight: 900; text-transform: uppercase; 
            letter-spacing: 2px; color: var(--accent-blue); margin-bottom: 30px; display: block;
        }

        .brand-title { 
            font-size: 3.5rem; font-weight: 900; margin: 0 0 40px 0; letter-spacing: -2px; 
            text-transform: uppercase; line-height: 0.85; color: var(--text-main);
        }
        
        .input-wrap {
            background: var(--bg-color); border-radius: 20px; padding: 8px;
            box-shadow: inset 8px 8px 16px var(--shadow-dark), inset -8px -8px 16px var(--shadow-light);
            margin-bottom: 35px;
        }

        input { 
            width: 100%; padding: 15px; border: none; background: transparent; 
            color: var(--text-main); font-family: inherit; font-size: 1.25rem; text-align: center; font-weight: 600; 
        }
        
        button { 
            width: 100%; padding: 22px; 
            background: var(--bg-color); color: var(--accent-blue); 
            border: none; border-radius: 25px;
            font-weight: 900; font-size: 1.1rem; 
            text-transform: uppercase; cursor: pointer; transition: 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); 
            box-shadow: 10px 10px 20px var(--shadow-dark), -10px -10px 20px var(--shadow-light);
        }
        button:active { box-shadow: inset 6px 6px 12px var(--shadow-dark), inset -6px -6px 12px var(--shadow-light); transform: scale(0.96); }
        
        .error { 
            color: #ff3b30; font-size: 0.75rem; font-weight: 900; 
            margin-top: 25px; text-transform: uppercase; display: block;
        }
    </style>
</head>
<body>
    <div class="bg-blob"></div>
    <div class="login-box">
        <span class="tag">M7 Core Node</span>
        <h1 class="brand-title">PALE<br><span style="font-weight:200; opacity:0.4;">APP</span></h1>
        <form method="post">
            <div class="input-wrap">
                <input type="password" name="password" placeholder="PASSWORD" required autofocus>
            </div>
            <button type="submit">Access Node</button>
        </form>
        {% if error %}<div class="error">{{ error }}</div>{% endif %}
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
