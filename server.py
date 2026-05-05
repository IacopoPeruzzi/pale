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
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pale App - Login</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;900&display=swap" rel="stylesheet">
    <style>
        :root { --bg: #e8e6e1; --accent: #ff3300; --text: #111; }
        body { background: var(--bg); color: var(--text); font-family: 'Outfit', sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .login-box { text-align: center; width: 100%; max-width: 300px; padding: 20px; }
        h1 { font-size: 3rem; font-weight: 900; margin: 0 0 30px 0; letter-spacing: -2px; }
        h1 span { color: transparent; -webkit-text-stroke: 1.5px var(--accent); }
        input { width: 100%; padding: 15px; border: 1px solid var(--text); background: transparent; border-radius: 50px; font-family: inherit; font-size: 1rem; text-align: center; margin-bottom: 15px; box-sizing: border-box; }
        button { width: 100%; padding: 15px; background: var(--accent); color: #fff; border: none; border-radius: 50px; font-weight: 900; text-transform: uppercase; letter-spacing: 1px; cursor: pointer; transition: 0.2s; }
        button:active { transform: scale(0.98); }
        .error { color: var(--accent); font-size: 0.8rem; font-weight: 900; margin-top: 15px; text-transform: uppercase; }
    </style>
</head>
<body>
    <div class="login-box">
        <h1>PALE<span>APP</span></h1>
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
