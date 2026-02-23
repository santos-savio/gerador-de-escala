from flask import Flask, render_template, send_from_directory, redirect, url_for
from flask_login import login_required, current_user
import os
from database import init_db
from auth import auth as auth_blueprint
from routes import api as api_blueprint

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

# Inicializa banco de dados
init_db(app)

# Registra blueprints
app.register_blueprint(auth_blueprint)
app.register_blueprint(api_blueprint)

# Rota principal que serve a página HTML
@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    return render_template('index.html', user=current_user)

# Rota para servir as imagens da pasta IMG
@app.route('/IMG/<filename>')
def serve_image(filename):
    return send_from_directory('IMG', filename)

# Rota para favicon (evita erro 404)
@app.route('/favicon.ico')
def favicon():
    return '', 204

if __name__ == '__main__':
    # Verifica se a pasta IMG existe
    if not os.path.exists('IMG'):
        print("AVISO: Pasta IMG não encontrada. As imagens não serão carregadas.")
    
    print("Servidor Flask iniciado!")
    print("Acesse: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
