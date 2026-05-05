from flask import Flask, request, session, redirect, url_for, send_from_directory, render_template_string
from werkzeug.security import check_password_hash
from dotenv import load_dotenv
import os

# Carica le variabili dal file .env se presente
load_dotenv()

app = Flask(__name__)
# Per sicurezza, usa una chiave segreta dalle variabili d'ambiente
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'pale-secret-key-123')
PASSWORD_HASH = os.environ.get('APP_PASSWORD_HASH')

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
        # Se non hai ancora impostato l'hash, puoi usare una password temporanea in chiaro per il primo accesso
        # Ma è consigliato impostare APP_PASSWORD_HASH nell'ambiente.
        if PASSWORD_HASH:
            if check_password_hash(PASSWORD_HASH, password):
                session['logged_in'] = True
                return redirect(url_for('index'))
        elif password == "admin": # Password di emergenza se non c'è hash
            session['logged_in'] = True
            return redirect(url_for('index'))
        
        error = "Accesso negato"
    return render_template_string(LOGIN_HTML, error=error)

# Serve the main index.html file
@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return send_from_directory('.', 'index.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# Serve any other static files if needed
@app.route('/<path:path>')
def static_proxy(path):
    if not session.get('logged_in') and path != 'login':
        return redirect(url_for('login'))
    return send_from_directory('.', path)

if __name__ == '__main__':
    # Use PORT environment variable if defined, otherwise default to 5000
    port = int(os.environ.get('PORT', 5000))
    print(f"Pale App is running on http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
