import mysql.connector # -> Importação da Lib MySQL
from mysql.connector import Error # -> Importação do pacote de erros do SQL


# Atualização de registros em uma banco de dados MySQL

# Criação da Conexão
def conectar():
    try:
        global con
        con = mysql.connector.connect(host="localhost", database="covid_db",user="root", password="admin")
    except Error as erro:
        print(f"Erro de conexão {erro}.")

def consulta(id_paciente):
    try:
        conectar()
        consulta_sql = f'select * from Pacientes where paciente_id = {id_paciente};'
        cursor = con.cursor()
        cursor.execute(consulta_sql)
        linhas = cursor.fetchall()

    
        for linha in linhas:
            print("ID: ", linha[0])
            print("Nome: ", linha[1])
            print("Data de Nascimento: ", linha[2])
            print("Sexo: ", linha[3])
            print("Endereço: ", linha[4])
            print("Telefone: ", linha[5])
            print("Email: ", linha[6], "\n")

    except Error as erro: #-> Captura erros do SQL
        print(f"Falha ao consultar a tabela: {erro}")
    
    finally:
        # Encerra a Conexão
        if con.is_connected():
            cursor.close()
            con.close()
            

def atualiza(declaracao):
    try:
        conectar()
        altera_telefone = declaracao
        cursor = con.cursor()
        cursor.execute(altera_telefone)
        con.commit()
        print("Telefone alterado com sucesso!")
    except Error as erro:
        print(f"Falha ao alterar o telefone: {erro}")
    finally:
        # Encerra a Conexão
        if con.is_connected():
            cursor.close()
            con.close()

    
if __name__ == '__main__':
    print("Atualizar dados de Pacientes no Banco de Dados")
    print("Entre com os dados conforme solicitado: ")

    print("\nDigite o código do paciente a alterar:")
    id_paciente = int(input("ID do Paciente: "))

    consulta(id_paciente)

    print("\nDigite o novo telefone: ")
    novo_telefone = input("Novo Telefone: ")

    declaracao = f'UPDATE Pacientes SET telefone = "{novo_telefone}" WHERE paciente_id = {id_paciente};'

    atualiza(declaracao) # -> executa o UPDATE no banco de dados

    verifica = input("Deseja verificar os dados alterados? (S/N): ")
    if verifica.upper() == 'S':
        consulta(id_paciente)
    else:
        print("Programa encerrado.")