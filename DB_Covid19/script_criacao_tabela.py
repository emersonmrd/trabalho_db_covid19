import mysql.connector # -> Importação da Lib MySQL

try:
    # Criação da Conexão
    con = mysql.connector.connect(host="localhost", database="covid_db",user="root", password="admin")

    '''
    # Verificação da conexão:
    if con.is_connected():
        db_info = con.get_server_info()
        print("Conectado ao servidor MySQL versão ", db_info)
        cursor = con.cursor()
        cursor.execute("select database();")
        linha = cursor.fetchone()
        print("Conectado ao banco de dados ", linha)
    '''
    
    # Declaração SQL a ser executada
    criar_tabela_sql = """CREATE TABLE Pacientes (
                paciente_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                data_nascimento DATE NOT NULL,
                sexo CHAR(1) NOT NULL,
                endereco TEXT,
                telefone VARCHAR(20),
                email VARCHAR(100)
            );"""

    # Criar cursor e executar SQL no banco de dados
    cursor = con.cursor()
    cursor.execute(criar_tabela_sql)
    print("Tabela de Pacientes criada com sucesso!")
except mysql.connector.Error as erro:
    print(f"Erro ao criar tabela Pacientes: {erro}")
    


finally:
    # Encerra a Conexão
    if con.is_connected():
        cursor.close()
        con.close()
        print("Conexão ao MySQL foi encerrada.")