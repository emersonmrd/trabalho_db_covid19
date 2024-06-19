import mysql.connector # -> Importação da Lib MySQL
from mysql.connector import Error # -> Importação do pacote de erros do SQL

try:
    # Criação da Conexão
    con = mysql.connector.connect(host="localhost", database="covid_db",user="root", password="admin")

    # Inserção de dados no SQL
    inserir_dados = """INSERT INTO Pacientes (nome, data_nascimento, sexo, endereco, telefone, email)
                        VALUES('Carlos Oliveira', '1975-04-12', 'M', 'Av. dos Estados, 789', '9777-8888', 'carlos.oliveira@email.com');"""
    cursor = con.cursor()
    cursor.execute(inserir_dados)
    con.commit()
    print(cursor.rowcount, "Registros inseridos com sucesso!")
    cursor.close()

except Error as e: #-> Captura erros do SQL
    print(f"Falha ao inserir dados no MySQL: {e}",)

finally:
    # Encerra a Conexão
    if con.is_connected():
        cursor.close()
        con.close()
        print("Conexão ao MySQL foi encerrada.")