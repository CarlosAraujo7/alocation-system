from flask import Blueprint
from routes.professores import professores_bp
from routes.disciplinas import disciplinas_bp

# Blueprint principal que agrupa todas as rotas
api_bp = Blueprint('api', __name__)

# Registro dos Blueprints individuais
api_bp.register_blueprint(professores_bp, url_prefix='/professores')
api_bp.register_blueprint(disciplinas_bp, url_prefix='/disciplinas')
