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
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@900&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-black: #000000;
            --accent-yellow: #FFEA00;
            --accent-lime: #B8FF00;
            --accent-white: #FFFFFF;
            --border-thick: 3px;
        }

        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; outline: none; }
        body {
            background-color: var(--bg-black);
            color: var(--accent-white);
            font-family: 'Outfit', sans-serif;
            margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100vh;
            overflow: hidden;
        }

        .login-card { 
            text-align: center; width: 100%; max-width: 340px; padding: 50px 30px; 
            background: var(--accent-yellow); border: var(--border-thick) solid var(--bg-black);
            box-shadow: 12px 12px 0px var(--accent-lime);
            position: relative;
        }
        
        .meta-strip {
            background: var(--bg-black); color: var(--accent-white);
            padding: 5px 12px; font-weight: 900; text-transform: uppercase; 
            font-size: 0.7rem; margin-bottom: 25px; display: inline-block;
        }

        .brand-title { 
            font-size: 4rem; font-weight: 900; margin: 0 0 40px 0; letter-spacing: -2px; 
            text-transform: uppercase; line-height: 0.85; color: var(--bg-black);
        }
        
        input { 
            width: 100%; padding: 20px; 
            border: var(--border-thick) solid var(--bg-black); 
            background: var(--accent-white); border-radius: 0;
            color: var(--bg-black); font-family: inherit; font-size: 1.2rem; text-align: center; font-weight: 900; 
            margin-bottom: 25px;
        }
        
        button { 
            width: 100%; padding: 22px; 
            background: var(--bg-black); color: var(--accent-lime); 
            border: none; font-weight: 900; font-size: 1.1rem; 
            text-transform: uppercase; cursor: pointer; transition: 0.1s; 
            box-shadow: 8px 8px 0px var(--accent-white);
        }
        button:active { transform: translate(4px, 4px); box-shadow: 4px 4px 0px var(--accent-white); }
        
        .error { 
            background: #ff3b30; color: #fff; font-size: 0.75rem; font-weight: 900; 
            margin-top: 25px; padding: 10px; border: var(--border-thick) solid var(--bg-black);
            text-transform: uppercase; display: block;
        }
    </style>
</head>
<body>
    <div class="login-card">
        <div class="meta-strip">Secure Gateway</div>
        <h1 class="brand-title">PALE<br><span style="color:var(--accent-white)">APP</span></h1>
        <form method="post">
            <input type="password" name="password" placeholder="PASSWORD" required autofocus>
            <button type="submit">ACCESS NODE</button>
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
