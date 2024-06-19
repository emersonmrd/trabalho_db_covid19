Criação do Banco de Dados:

    CREATE DATABASE covid_db;


Estrutura do Banco de Dados:
    Tabelas Principais:
        Pacientes:
            CREATE TABLE Pacientes (
                paciente_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                data_nascimento DATE NOT NULL,
                sexo CHAR(1) NOT NULL,
                endereco TEXT,
                telefone VARCHAR(20),
                email VARCHAR(100)
            );

        Amostras Biológicas:
            CREATE TABLE Amostras_Biologicas (
                amostra_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                paciente_id INT UNSIGNED,
                tipo_amostra VARCHAR(50) NOT NULL,
                data_coleta DATE NOT NULL,
                condicoes_armazenamento TEXT NOT NULL,
                FOREIGN KEY (paciente_id) REFERENCES Pacientes(paciente_id)
            );

        Dados Moleculares:
            CREATE TABLE Dados_Moleculares (
                dados_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                amostra_id INT UNSIGNED,
                tipo_dados VARCHAR(50) NOT NULL,
                sequencia TEXT NOT NULL,
                FOREIGN KEY (amostra_id) REFERENCES Amostras_Biologicas(amostra_id)
            );

        Pesquisadores:
                CREATE TABLE Pesquisadores (
                    pesquisador_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL,
                    instituicao VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    telefone VARCHAR(20) NOT NULL,
                    user VARCHAR(50) NOT NULL,
                    senha VARCHAR(100) NOT NULL
                );

        Associação Pesquisadores-Amostras:
            CREATE TABLE Pesquisadores_Amostras (
                pesquisador_id INT UNSIGNED,
                amostra_id INT UNSIGNED,
                PRIMARY KEY (pesquisador_id, amostra_id),
                FOREIGN KEY (pesquisador_id) REFERENCES Pesquisadores(pesquisador_id),
                FOREIGN KEY (amostra_id) REFERENCES Amostras_Biologicas(amostra_id)
            );

Funcionalidades:

    Inserção de Dados:
        Ex: 
            INSERT INTO Pacientes (nome, data_nascimento, sexo, endereco, telefone, email)
            VALUES
                ('João Silva', '1990-05-15', 'M', 'Rua Principal, 123', '9999-8888', 'joao.silva@email.com'),
                ('Maria Santos', '1985-10-25', 'F', 'Avenida Central, 456', '9888-7777', 'maria.santos@email.com'),
                ('Pedro Oliveira', '1988-07-02', 'M', 'Praça da Paz, 789', NULL, 'pedro.oliveira@email.com');

            INSERT INTO Amostras_Biologicas (paciente_id, tipo_amostra, data_coleta, condicoes_armazenamento)
            VALUES
                (1, 'Sangue', '2023-01-10', 'Armazenamento refrigerado'),
                (2, 'Saliva', '2023-01-12', 'Armazenamento em temperatura ambiente'),
                (3, 'Tecido', '2023-01-15', 'Armazenamento em nitrogênio líquido');

            INSERT INTO Dados_Moleculares (amostra_id, tipo_dados, sequencia)
            VALUES
                (1, 'Sequenciamento de DNA', 'ATCGGTAACCTTGGCCAGTTCGAGT'),
                (2, 'Análise de Expressão Gênica', 'GTCAAGTTCGCGGTCAATCGGTAAC'),
                (3, 'Sequenciamento de RNA', 'GCTTAGCCGATCGGTAACCGGTAAT');

            INSERT INTO Pesquisadores (nome, instituicao, email, telefone, user, senha)
            VALUES
                ('Ana Souza', 'Universidade XYZ', 'ana.souza@universidade.com', '9777-6666', 'ana.souza', '1234'),
                ('Carlos Pereira', 'Instituto ABC', 'carlos.pereira@instituto.com', '9555-4444', 'carlos.pereira', '1234'),;
                ('Daniel Alves', 'Instituto 123', 'daniel.alves@instituto.com', '9888-5555', 'daniel.alves', '1234');

            INSERT INTO Pesquisadores_Amostras (pesquisador_id, amostra_id)
            VALUES
                (1, 1),
                (1, 2),
                (2, 3);

    Consultas:
        Ex:
            SELECT * FROM Amostras_Biologicas WHERE paciente_id = 1;
            SELECT * FROM Dados_Moleculares WHERE amostra_id = 1;

    Atualização e Exclusão:
        Ex:
            UPDATE Pacientes SET telefone = '11888888888' WHERE paciente_id = 1;