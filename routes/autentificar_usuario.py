from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from config import get_db_connection

autentificar_usuario_bp = Blueprint('autentificar_usuario', __name__)

# Rota para a pagina de login
@autentificar_usuario_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['senha']
        connection = get_db_connection()
        usuario = None

        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
            usuario = cursor.fetchone()
            cursor.close()
            connection.close()

        if usuario and check_password_hash(usuario['senha_hash'], senha):
            session['user_id'] = usuario['id']
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('autentificar_usuario.index'))  # Redireciona após o login
        else:
            flash('Usuário ou senha incorretos.', 'danger')

    return render_template('login.html')  # Página do login

# rota para a página de cadastro
@autentificar_usuario_bp.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['senha']
        senha_hash = generate_password_hash(senha)
        connection = get_db_connection()

        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO usuarios (username, senha_hash) VALUES (%s, %s)", 
                    (username, senha_hash)
                )
                connection.commit()
                flash('Cadastro realizado com sucesso! Faça login.', 'success')
                return redirect(url_for('autentificar_usuario.login'))  # Redireciona após cadastro
            except Exception as e:
                flash('Erro ao cadastrar usuário: ' + str(e), 'danger')
            finally:
                cursor.close()
                connection.close()

    return render_template('cadastro_usuario.html')  # Página de cadastro

# rota para a pagina protegida (Index.html)
@autentificar_usuario_bp.route('/index')
def index():
    if 'user_id' not in session:
        flash('Por favor, faça login para acessar esta página.', 'warning')
        return redirect(url_for('autentificar_usuario.login'))  # Redireciona para login se não estiver logado
    return render_template('index.html')  # Página index após login

# rota para Logout do usuário
@autentificar_usuario_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('autentificar_usuario.login'))  # Redireciona após logout

# rota para editar perfil do usuário
@autentificar_usuario_bp.route('/editar_perfil', methods=['GET', 'POST'])
def editar_perfil():
    if 'user_id' not in session:
        flash("Por favor, faça login para acessar esta página.", "warning")
        return redirect(url_for('autentificar_usuario.login'))

    user_id = session['user_id']
    connection = get_db_connection()
    usuario = None

    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
        usuario = cursor.fetchone()
        cursor.close()

    if not usuario:
        flash("Usuário não encontrado.", "danger")
        return redirect(url_for('autentificar_usuario.login'))

    if request.method == 'POST':
        username = request.form['username']
        senha = request.form.get('senha')
        senha_hash = generate_password_hash(senha) if senha else usuario['senha_hash']

        try:
            if connection:
                cursor = connection.cursor()
                cursor.execute("""
                    UPDATE usuarios
                    SET username = %s, senha_hash = %s
                    WHERE id = %s
                """, (username, senha_hash, user_id))
                connection.commit()
                flash("Perfil atualizado com sucesso!", "success")
        except Exception as e:
            flash(f"Erro ao atualizar o perfil: {str(e)}", "danger")
        finally:
            cursor.close()

        return redirect(url_for('autentificar_usuario.index'))

    return render_template('editar_perfil.html', usuario=usuario)

# rota para excluir perfil do usuário
@autentificar_usuario_bp.route('/deletar_perfil', methods=['POST'])
def deletar_perfil():
    if 'user_id' not in session:
        flash("Por favor, faça login para acessar esta página.", "warning")
        return redirect(url_for('autentificar_usuario.login'))  # Redireciona para login se não estiver logado

    user_id = session['user_id']
    connection = get_db_connection()

    try:
        if connection:
            cursor = connection.cursor()

            # Excluir o usuário da tabela
            cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
            connection.commit()
            cursor.close()
            connection.close()

            # Remove o usuário da sessão após a exclusão
            session.pop('user_id', None)
            flash("Seu perfil foi excluído com sucesso.", "success")
    except Exception as e:
        flash(f"Erro ao excluir o perfil: {str(e)}", "danger")
        return redirect(url_for('autentificar_usuario.editar_perfil'))  # Volta para a página de edição do perfil se houver erro

    # Redireciona para a página de login após a exclusão
    return redirect(url_for('autentificar_usuario.login'))
