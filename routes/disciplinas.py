from flask import Blueprint, request, render_template, redirect, url_for, flash
from config import get_db_connection

# Criação do Blueprint
disciplinas_bp = Blueprint('disciplinas', __name__)

# Rota para cadastro de disciplina
@disciplinas_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastrar_disciplina():
    connection = get_db_connection()
    if request.method == 'POST':
        nome = request.form['nome']
        curso = request.form['curso']
        semestre = request.form['semestre']
        carga_teorica = request.form['carga_teorica']
        carga_pratica = request.form['carga_pratica']
        professor_id = request.form.get('professor_id')  # Pode ser None (não selecionado)

        if connection:
            cursor = connection.cursor()
            query = """
            INSERT INTO disciplinas (nome, curso, semestre, carga_teorica, carga_pratica, professor_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (nome, curso, semestre, carga_teorica, carga_pratica, professor_id or None))  # Aloca NULL se não houver professor
            connection.commit()
            cursor.close()
            connection.close()

        flash("Disciplina cadastrada com sucesso!", "success")
        return redirect(url_for('disciplinas.listar_disciplinas'))
    
    # Carregar professores para o formulário
    professores = []
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM professores")
        professores = cursor.fetchall()
        cursor.close()
        connection.close()

    return render_template('cadastro_disciplina.html', professores=professores)

# Rota para listagem de disciplinas
@disciplinas_bp.route('/listar', methods=['GET'])
def listar_disciplinas():
    connection = get_db_connection()
    disciplinas = []
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT d.id, d.nome, d.curso, d.semestre, d.carga_teorica, d.carga_pratica, p.nome AS professor_nome
        FROM disciplinas d
        LEFT JOIN professores p ON d.professor_id = p.id
        """
        cursor.execute(query)
        disciplinas = cursor.fetchall()
        cursor.close()
        connection.close()
    
    return render_template('listar_disciplinas.html', disciplinas=disciplinas)

# Rota para editar uma disciplina
@disciplinas_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_disciplina(id):
    connection = get_db_connection()
    disciplina = None
    professores = []
    if connection:
        cursor = connection.cursor(dictionary=True)

        # Recupera a disciplina para edição
        cursor.execute("SELECT * FROM disciplinas WHERE id = %s", (id,))
        disciplina = cursor.fetchone()

        # Carregar todos os professores para o formulário
        cursor.execute("SELECT * FROM professores")
        professores = cursor.fetchall()

        if request.method == 'POST':
            nome = request.form['nome']
            curso = request.form['curso']
            semestre = request.form['semestre']
            carga_teorica = request.form['carga_teorica']
            carga_pratica = request.form['carga_pratica']
            professor_id = request.form.get('professor_id')  # Pode ser None para desassociar

            query = """
            UPDATE disciplinas
            SET nome = %s, curso = %s, semestre = %s, carga_teorica = %s, carga_pratica = %s, professor_id = %s
            WHERE id = %s
            """
            cursor.execute(query, (nome, curso, semestre, carga_teorica, carga_pratica, professor_id or None, id))
            connection.commit()
            cursor.close()
            connection.close()

            flash("Disciplina editada com sucesso!", "success")
            return redirect(url_for('disciplinas.listar_disciplinas'))

        cursor.close()
        connection.close()

    return render_template('editar_disciplina.html', disciplina=disciplina, professores=professores)

# Rota para excluir disciplina
@disciplinas_bp.route('/excluir/<int:id>', methods=['POST'])
def excluir_disciplina(id):
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()

        try:
            cursor.execute("DELETE FROM disciplinas WHERE id = %s", (id,))
            connection.commit()
            flash("Disciplina excluída com sucesso.", "success")
        except Exception as e:
            flash(f"Ocorreu um erro ao excluir a disciplina: {str(e)}", "danger")
        finally:
            cursor.close()
            connection.close()

    return redirect(url_for('disciplinas.listar_disciplinas'))
