from flask import Blueprint, request, render_template, redirect, url_for
from config import get_db_connection

# Criação do Blueprint
professores_bp = Blueprint('professores', __name__)

# Rota para cadastro de professor
@professores_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastrar_professor():
    if request.method == 'POST':
        nome = request.form['nome']
        cor = request.form['cor']

        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            query = "INSERT INTO professores (nome, cor) VALUES (%s, %s)"
            cursor.execute(query, (nome, cor))
            connection.commit()
            cursor.close()
            connection.close()

        return redirect(url_for('professores.listar_professores'))  # Corrigir para 'professores.listar_professores'
    
    return render_template('cadastro_professor.html')

# Rota para listar professores
@professores_bp.route('/listar', methods=['GET'])
def listar_professores():
    connection = get_db_connection()
    professores = []
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM professores")
        professores = cursor.fetchall()
        cursor.close()
        connection.close()
    
    return render_template('listar_professores.html', professores=professores)
