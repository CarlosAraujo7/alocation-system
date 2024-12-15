from flask import Blueprint, request, render_template, redirect, url_for, flash
from config import get_db_connection

# Criação do Blueprint
professores_bp = Blueprint('professores', __name__)

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

# Rota para cadastrar professor
@professores_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastrar_professor():
    if request.method == 'POST':
        nome = request.form['nome']
        cor = request.form['cor']
        siape = request.form['siape']  # Capturando o valor do campo 'siape'

        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            query = "INSERT INTO professores (nome, cor, siape) VALUES (%s, %s, %s)"
            cursor.execute(query, (nome, cor, siape))  # Passando o valor de 'siape'
            connection.commit()
            cursor.close()
            connection.close()

        return redirect(url_for('professores.listar_professores'))

    return render_template('cadastro_professor.html')

# Rota para editar professor
@professores_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_professor(id):
    connection = get_db_connection()

    if request.method == 'POST':
        nome = request.form['nome']
        cor = request.form['cor']
        siape = request.form['siape']

        if connection:
            cursor = connection.cursor()
            query = "UPDATE professores SET nome = %s, cor = %s, siape = %s WHERE id = %s"
            cursor.execute(query, (nome, cor, siape, id))
            connection.commit()
            cursor.close()
            connection.close()

        return redirect(url_for('professores.listar_professores'))

    professor = None
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM professores WHERE id = %s", (id,))
        professor = cursor.fetchone()
        cursor.close()
        connection.close()

    return render_template('editar_professor.html', professor=professor)

# Rota para excluir professor
@professores_bp.route('/excluir/<int:id>', methods=['POST'])
def excluir_professor(id):
    connection = get_db_connection()
    try:
        if connection:
            cursor = connection.cursor()
            
            # Excluindo registros da tabela 'disciplinas' que referenciam o professor
            cursor.execute("DELETE FROM disciplinas WHERE professor_id = %s", (id,))
            
            # Excluindo o registro do professor
            cursor.execute("DELETE FROM professores WHERE id = %s", (id,))
            
            # Confirmando as alterações
            connection.commit()
            
            # Mensagem de sucesso (usando flash para mensagens)
            flash("Professor excluído com sucesso.", "success")
        
    except Exception as e:
        # Tratamento de erro genérico
        flash(f"Ocorreu um erro ao excluir o professor: {str(e)}", "danger")
    finally:
        cursor.close()
        connection.close()

    # Redirecionando para a lista de professores
    return redirect(url_for('professores.listar_professores'))
