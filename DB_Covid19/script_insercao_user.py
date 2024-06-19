import mysql.connector # -> Importação da Lib MySQL
from mysql.connector import Error # -> Importação do pacote de erros do SQL

print("Rotina para cadastro de Pacientes acometidos pelo COVID.")
print("Por favor, preencha os dados solicitados abaixo:")
nome_paciente = input("Nome:")
data_nasc = input("Data de Nascimento: ")
sexo = input("Sexo: ")
endereco = input("Endereço: ")
telefone = input("Telefone: ")
email = input("Email: ")

inserir_dados = f"""INSERT INTO Pacientes (nome, data_nascimento, sexo, endereco, telefone, email)
                        VALUES('{nome_paciente}', '{data_nasc}', '{sexo}', '{endereco}', '{telefone}', '{email}');"""

try:
    # Criação da Conexão
    con = mysql.connector.connect(host="localhost", database="covid_db",user="root", password="admin")

    # Inserção de dados no SQL
    inserir_dados = f"""INSERT INTO Pacientes (nome, data_nascimento, sexo, endereco, telefone, email)
                        VALUES('{nome_paciente}', '{data_nasc}', '{sexo}', '{endereco}', '{telefone}', '{email}');"""
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
