from flask import Blueprint, request, render_template, redirect, url_for
from config import get_db_connection

# Criação do Blueprint
disciplinas_bp = Blueprint('disciplinas', __name__)

# Rota para cadastro de disciplina
@disciplinas_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastrar_disciplina():
    if request.method == 'POST':
        nome = request.form['nome']
        curso = request.form['curso']
        semestre = request.form['semestre']
        carga_teorica = request.form['carga_teorica']
        carga_pratica = request.form['carga_pratica']

        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            query = """
            INSERT INTO disciplinas (nome, curso, semestre, carga_teorica, carga_pratica)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (nome, curso, semestre, carga_teorica, carga_pratica))
            connection.commit()
            cursor.close()
            connection.close()

        return redirect(url_for('disciplinas.listar_disciplinas'))
    
    return render_template('cadastro_disciplina.html')

# Rota para listar disciplinas
@disciplinas_bp.route('/listar', methods=['GET'])
def listar_disciplinas():
    connection = get_db_connection()
    disciplinas = []
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM disciplinas")
        disciplinas = cursor.fetchall()
        cursor.close()
        connection.close()
    
    return render_template('listar_disciplinas.html', disciplinas=disciplinas)
