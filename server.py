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
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #ffffff;
            --accent-color: #000000;
            --highlight-yellow: #FFE600;
            --highlight-purple: #DDB8FF;
            --highlight-pink: #FF85C0;
            --text-primary: #000000;
            --btn-radius: 50px;
            --border-thickness: 3px;
            --hard-shadow: 4px 4px 0px var(--accent-color);
            --hard-shadow-active: 0px 0px 0px var(--accent-color);
        }

        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; outline: none; }
        body {
            background-color: var(--bg-color);
            color: var(--text-primary);
            font-family: 'Outfit', sans-serif;
            margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100vh;
            background-image: 
                linear-gradient(rgba(0,0,0,0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0,0,0,0.05) 1px, transparent 1px);
            background-size: 20px 20px;
        }
        
        .login-box { text-align: center; width: 100%; max-width: 320px; padding: 20px; }
        
        .brand-title { font-size: 3.5rem; font-weight: 900; margin: 0 0 40px 0; letter-spacing: -1px; text-transform: uppercase; line-height: 0.9; position: relative; display: inline-block; }
        .brand-title::before { content: ''; position: absolute; bottom: 5px; left: -5px; right: -5px; height: 15px; background: var(--highlight-yellow); z-index: -1; transform: rotate(-2deg); border: 2px solid #000; border-radius: 5px; }
        .brand-title span.outline { color: var(--text-primary); }
        .brand-title span.solid { color: var(--highlight-purple); -webkit-text-stroke: 2px #000; }
        
        input { 
            width: 100%; padding: 18px; 
            border: var(--border-thickness) solid var(--accent-color); 
            background: #fff; border-radius: 15px; 
            font-family: inherit; font-size: 1.1rem; text-align: center; font-weight: 800; 
            margin-bottom: 20px; box-sizing: border-box; 
            box-shadow: inset 2px 2px 0px rgba(0,0,0,0.1); 
        }
        
        button { 
            width: 100%; padding: 18px; 
            background: var(--highlight-purple); color: #000; 
            border: var(--border-thickness) solid var(--accent-color); 
            border-radius: var(--btn-radius); font-weight: 900; font-size: 1.1rem; 
            text-transform: uppercase; letter-spacing: 1px; cursor: pointer; transition: 0.15s; 
            box-shadow: var(--hard-shadow); 
        }
        button:active { transform: translate(4px, 4px); box-shadow: var(--hard-shadow-active); }
        
        .error { 
            background: var(--highlight-pink); color: #000; font-size: 0.8rem; font-weight: 900; 
            margin-top: 20px; padding: 10px; border: 2px solid #000; border-radius: 10px; 
            text-transform: uppercase; display: inline-block; box-shadow: 2px 2px 0px #000; transform: rotate(-2deg); 
        }
    </style>
</head>
<body>
    <div class="login-box">
        <h1 class="brand-title"><span class="outline">PALE</span><span class="solid">APP</span></h1>
        <form method="post">
            <input type="password" name="password" placeholder="PASSWORD" required autofocus>
            <button type="submit">ENTRA</button>
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
