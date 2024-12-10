import mysql.connector
from mysql.connector import errorcode

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='0701',
            database='sistema_database'
        )
        return connection
    except mysql.connector.Error as error:
        if error.errno == errorcode.ER_BAD_DB_ERROR:
            print("O banco de dados não existe!")
        elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Usuário ou senha inválidos!")
        else:
            print("Erro ao conectar ao banco de dados:", error)
        return None
