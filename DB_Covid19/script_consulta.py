import mysql.connector # -> Importação da Lib MySQL
from mysql.connector import Error # -> Importação do pacote de erros do SQL

try:
    # Criação da Conexão
    con = mysql.connector.connect(host="localhost", database="covid_db",user="root", password="admin")

    # Consulta SQL
    consulta_sql = "SELECT * FROM Pacientes;"
    cursor = con.cursor()
    cursor.execute(consulta_sql)
    linhas = cursor.fetchall()
    print("Número total de regisrtos retornados: ", cursor.rowcount)
   
   # Impressão da consulta realizada
    print("\nMostrando os Pacientes cadastrados:")
    for linha in linhas:
        print("ID: ", linha[0])
        print("Nome: ", linha[1])
        print("Data de Nascimento: ", linha[2])
        print("Sexo: ", linha[3])
        print("Endereço: ", linha[4])
        print("Telefone: ", linha[5])
        print("Email: ", linha[6], "\n")

except Error as e: #-> Captura erros do SQL
    print("Erro ao acessar a tabela MySQL", e)

finally:
    # Encerra a Conexão
    if con.is_connected():
        cursor.close()
        con.close()
        print("Conexão ao MySQL foi encerrada.")