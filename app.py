from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

# Rota principal que serve a página HTML
@app.route('/')
def index():
    return render_template('index.html')

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
