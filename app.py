from flask import Flask, render_template, request, redirect, url_for
from routes.disciplinas import disciplinas_bp
from routes.professores import professores_bp
from routes.autentificar_usuario import autentificar_usuario_bp
from config import get_db_connection

app = Flask(__name__)
app.secret_key = 'admin'
# Registra os Blueprints
app.register_blueprint(disciplinas_bp, url_prefix='/disciplinas')
app.register_blueprint(professores_bp, url_prefix='/professores')
app.register_blueprint(autentificar_usuario_bp, url_prefix='/autentificar_usuario')

# Rota para a página inicial
@app.route('/')
def home():
    return redirect(url_for('autentificar_usuario.login'))

if __name__ == '__main__':
    app.run(debug=True)
