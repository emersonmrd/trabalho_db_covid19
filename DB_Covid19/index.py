import tkinter as tk
from tkinter import ttk, messagebox
import database

def close_program():
    database.cursor.close()
    database.con.close()
    janela.destroy()

def login():
    user = userEntry.get()
    password = passEntry.get()
    database.cursor.execute("SELECT * FROM pesquisadores WHERE user = %s AND senha = %s", (user, password))
    if database.cursor.fetchall():
        messagebox.showinfo(title="Login Info", message="Login efetuado com sucesso!")
        open_dashboard(user)
    else:
        messagebox.showerror(title="Login Error", message="Usuário ou senha inválidos!")

def open_dashboard(user):
    dashboard = tk.Toplevel(janela)
    dashboard.title("Janela Principal")	
    dashboard.geometry("800x600")
    dashboard.configure(background="white")
    dashboard.resizable(width=False, height=False)
    dashboard.iconbitmap("./imgs/umsfavicon.ico")

    # Carregando Imagem para a nova janela
    logo = tk.PhotoImage(file="./imgs/umslogo200.png")
    logoLabel = tk.Label(dashboard, image=logo, bg="white")
    logoLabel.image = logo  # Manter a referência para a imagem
    logoLabel.pack(pady=20)

    # Obter o nome do pesquisador do banco de dados
    database.cursor.execute("SELECT nome FROM pesquisadores WHERE user = %s", (user,))
    result = database.cursor.fetchone()
    if result:
        nome_pesquisador = result[0]
    else:
        nome_pesquisador = "Usuário"

    welcome_label = tk.Label(dashboard, text=f"Bem-vindo(a), {nome_pesquisador}!", font="Arial 20 bold", bg="white")
    welcome_label.pack(pady=20)

    # Frame para centralizar os botões
    btn_frame = tk.Frame(dashboard, bg="white")
    btn_frame.pack(expand=True)

    # Botões para exibir dados das tabelas
    btn_pacientes = ttk.Button(btn_frame, text="Exibir Pacientes", command=lambda: show_table_data("Pacientes", dashboard))
    btn_pacientes.grid(row=0, column=0, padx=10, pady=5)

    btn_amostras = ttk.Button(btn_frame, text="Exibir Amostras Biológicas", command=lambda: show_table_data("Amostras_Biologicas", dashboard))
    btn_amostras.grid(row=1, column=0, padx=10, pady=5)

    btn_dados = ttk.Button(btn_frame, text="Exibir Dados Moleculares", command=lambda: show_table_data("Dados_Moleculares", dashboard))
    btn_dados.grid(row=2, column=0, padx=10, pady=5)

    logout_button = ttk.Button(dashboard, text="Logout", command=dashboard.destroy)
    logout_button.pack(pady=10)

def show_table_data(table_name, parent_window):
    data_window = tk.Toplevel(parent_window)
    if table_name == "Pacientes":
        ntable_name = "Pacientes"
    elif table_name == "Amostras_Biologicas":
        ntable_name = "Amostaras Biologicas"
    elif table_name == "Dados_Moleculares":
        ntable_name = "Dados Moleculares"
    data_window.title(f"{ntable_name}")
    data_window.configure(background="white")
    data_window.resizable(width=True, height=True)
    data_window.iconbitmap("./imgs/umsfavicon.ico")


    # Função para atualizar a tabela de pacientes
    def update_table():
        tree.delete(*tree.get_children())  # Limpar todos os itens da tabela atual
        database.cursor.execute(sql_query)
        rows = database.cursor.fetchall()
        for row in rows:
            tree.insert("", tk.END, values=row) 
    
    # Função para cadastrar nova amostra biológica
    def open_new_sample_window():
        new_sample_window = tk.Toplevel(data_window)
        new_sample_window.title("Cadastrar Nova Amostra Biológica")
        new_sample_window.geometry("800x600")
        new_sample_window.configure(background="white")
        new_sample_window.resizable(width=False, height=False)
        new_sample_window.iconbitmap("./imgs/umsfavicon.ico")

        # Função para obter os pacientes do banco de dados
        def get_pacientes():
            database.cursor.execute("SELECT paciente_id, nome FROM Pacientes")
            return database.cursor.fetchall()

        # Widgets para o formulário de cadastro de amostras
        lbl_paciente = ttk.Label(new_sample_window, text="Selecione o Paciente:")
        lbl_paciente.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        # Combobox para exibir os nomes dos pacientes
        combo_paciente = ttk.Combobox(new_sample_window, width=50, state="readonly")
        combo_paciente.grid(row=0, column=1, padx=10, pady=5)

        # Preencher a combobox com os nomes dos pacientes
        pacientes = get_pacientes()
        combo_paciente["values"] = [f"{id}: {nome}" for id, nome in pacientes]

        lbl_tipo_amostra = ttk.Label(new_sample_window, text="Tipo de Amostra:")
        lbl_tipo_amostra.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

        entry_tipo_amostra = ttk.Entry(new_sample_window, width=50)
        entry_tipo_amostra.grid(row=1, column=1, padx=10, pady=5)

        lbl_data_coleta = ttk.Label(new_sample_window, text="Data de Coleta:")
        lbl_data_coleta.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

        entry_data_coleta = ttk.Entry(new_sample_window, width=20)
        entry_data_coleta.grid(row=2, column=1, padx=10, pady=5)

        lbl_condicoes_armazenamento = ttk.Label(new_sample_window, text="Condições de Armazenamento:")
        lbl_condicoes_armazenamento.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

        entry_condicoes_armazenamento = ttk.Entry(new_sample_window, width=50)
        entry_condicoes_armazenamento.grid(row=3, column=1, padx=10, pady=5)

        # Função para salvar a nova amostra no banco de dados
        def save_sample():
            tipo_amostra = entry_tipo_amostra.get()
            data_coleta = entry_data_coleta.get()
            condicoes_armazenamento = entry_condicoes_armazenamento.get()

            # Obter o ID do paciente selecionado
            selected_paciente_option = combo_paciente.get()
            selected_paciente_id = selected_paciente_option.split(":")[0].strip() if selected_paciente_option else None

            if not tipo_amostra or not data_coleta or not condicoes_armazenamento or not selected_paciente_id:
                messagebox.showerror("Campos Vazios", "Por favor, preencha todos os campos e selecione um paciente.")
                return

            try:
                database.cursor.execute("""
                                        INSERT INTO Amostras_Biologicas (paciente_id, tipo_amostra, data_coleta, condicoes_armazenamento)
                                        VALUES (%s, %s, %s, %s)
                                        """, (selected_paciente_id, tipo_amostra, data_coleta, condicoes_armazenamento))
                database.con.commit()
                messagebox.showinfo("Cadastro de Amostra", "Amostra cadastrada com sucesso!")
                new_sample_window.destroy()
            except Exception as e:
                messagebox.showerror("Erro ao Cadastrar", f"Ocorreu um erro ao cadastrar a amostra: {e}")

        btn_salvar = ttk.Button(new_sample_window, text="Salvar", command=save_sample)
        btn_salvar.grid(row=4, column=1, padx=10, pady=10)

    # Botão para cadastrar novo paciente
    def open_new_patient_window():
        new_patient_window = tk.Toplevel(data_window)
        new_patient_window.title("Cadastrar Novo Paciente")
        new_patient_window.geometry("600x400")
        new_patient_window.configure(background="white")
        new_patient_window.resizable(width=False, height=False)
        new_patient_window.iconbitmap("./imgs/umsfavicon.ico")

        # Widgets para o formulário de cadastro de paciente
        lbl_nome = ttk.Label(new_patient_window, text="Nome:")
        lbl_nome.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        entry_nome = ttk.Entry(new_patient_window, width=50)
        entry_nome.grid(row=0, column=1, padx=10, pady=5)

        lbl_data_nascimento = ttk.Label(new_patient_window, text="Data de Nascimento:")
        lbl_data_nascimento.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

        entry_data_nascimento = ttk.Entry(new_patient_window, width=20)
        entry_data_nascimento.grid(row=1, column=1, padx=10, pady=5)

        lbl_sexo = ttk.Label(new_patient_window, text="Sexo:")
        lbl_sexo.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

        combo_sexo = ttk.Combobox(new_patient_window, values=["Masculino", "Feminino"])
        combo_sexo.grid(row=2, column=1, padx=10, pady=5)
        combo_sexo.current(0)

        lbl_endereco = ttk.Label(new_patient_window, text="Endereço:")
        lbl_endereco.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

        entry_endereco = ttk.Entry(new_patient_window, width=50)
        entry_endereco.grid(row=3, column=1, padx=10, pady=5)

        lbl_telefone = ttk.Label(new_patient_window, text="Telefone:")
        lbl_telefone.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)

        entry_telefone = ttk.Entry(new_patient_window, width=20)
        entry_telefone.grid(row=4, column=1, padx=10, pady=5)

        lbl_email = ttk.Label(new_patient_window, text="Email:")
        lbl_email.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)

        entry_email = ttk.Entry(new_patient_window, width=50)
        entry_email.grid(row=5, column=1, padx=10, pady=5)

        # Função para salvar o novo paciente no banco de dados
        def save_patient():
            nome = entry_nome.get()
            data_nascimento = entry_data_nascimento.get()
            sexo = combo_sexo.get()
            if sexo == "Masculino":
                sexo = "M"
            elif sexo == "Feminino":
                sexo = "F"
            endereco = entry_endereco.get()
            telefone = entry_telefone.get()
            email = entry_email.get()

            if not nome or not data_nascimento or not sexo or not endereco or not telefone or not email:
                messagebox.showerror("Campos Vazios", "Por favor, preencha todos os campos.")
                return

            try:
                database.cursor.execute("""
                                        INSERT INTO Pacientes (nome, data_nascimento, sexo, endereco, telefone, email)
                                        VALUES (%s, %s, %s, %s, %s, %s)
                                        """, (nome, data_nascimento, sexo, endereco, telefone, email))
                database.con.commit()
                messagebox.showinfo("Cadastro de Paciente", "Paciente cadastrado com sucesso!")
                new_patient_window.destroy()
            except Exception as e:
                messagebox.showerror("Erro ao Cadastrar", f"Ocorreu um erro ao cadastrar o paciente: {e}")

        btn_salvar = ttk.Button(new_patient_window, text="Salvar", command=save_patient)
        btn_salvar.grid(row=6, column=1, padx=10, pady=10)

    # Definir colunas e cabeçalhos com base na tabela
    columns = []
    if table_name == "Pacientes":
        columns = ["ID do Paciente", "Nome", "Data Nascimento", "Sexo", "Endereco", "Telefone", "Email"]
        sql_query = "SELECT * FROM Pacientes"
    elif table_name == "Amostras_Biologicas":
        ntable_name = "Amostras Biologicas"
        columns = ["ID da Amostra","ID do Paciente", "Tipo de Amostra", "Data da Coleta", "Condições de Armazenamento"]
        sql_query = "SELECT amostra_id, paciente_id, tipo_amostra, data_coleta, condicoes_armazenamento FROM Amostras_Biologicas"
    elif table_name == "Dados_Moleculares":
        columns = ["ID do Dado", "ID da Amostra", "Tipo de Dado", "Sequência"]
        sql_query = "SELECT * FROM Dados_Moleculares"

    tree = ttk.Treeview(data_window, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col, anchor=tk.CENTER)
        tree.column(col, anchor=tk.CENTER, minwidth=100)

    tree.pack(fill=tk.BOTH, expand=True)

    # Atualizar a tabela inicialmente
    #update_table()  

    
    # Botão para cadastrar novo paciente
    btn_cadastrar = ttk.Button(data_window, text="Cadastrar Novo Paciente", command=open_new_patient_window)
    btn_cadastrar.pack(padx=10, pady=10)

    # Botão para cadastrar nova amostra biológica
    btn_cadastrar_amostra = ttk.Button(data_window, text="Cadastrar Nova Amostra", command=open_new_sample_window)
    btn_cadastrar_amostra.pack(padx=10, pady=10)

    # Botão de atualização da tabela
    update_button = ttk.Button(data_window, text="Atualizar", command=update_table)
    update_button.pack(padx=10, pady=10)

    # Obter dados do banco de dados e inserir na tabela
    database.cursor.execute(sql_query)
    rows = database.cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)

# Criação da janela principal
janela = tk.Tk()
janela.title("UMS Covid-19")
janela.geometry("1200x600")
janela.configure(background="white")
janela.resizable(width=False, height=False)
janela.attributes("-alpha", 0.9)
janela.iconbitmap("./imgs/umsfavicon.ico")

# Capturar evento de fechamento da janela principal
janela.protocol("WM_DELETE_WINDOW", close_program)

# Carregando Imagens
logo = tk.PhotoImage(file="./imgs/umslogo200.png")

# Widgets
leftFrame = tk.Frame(janela, width=400, height=600, bg="#7FA653", relief="raise")
leftFrame.pack(side=tk.LEFT)

rightFrame = tk.Frame(janela, width=795, height=600, bg="#7FA653", relief="raise")
rightFrame.pack(side=tk.RIGHT)

logoLabel = tk.Label(leftFrame, image=logo, bg="#7FA653")
logoLabel.place(x=100, y=220)

# Campo de usuario
userLabel = tk.Label(rightFrame, text="Usuário:", font="Arial 20 bold", bg="#7FA653", fg="white")
userLabel.place(x=275, y=220)

userEntry = ttk.Entry(rightFrame, width=30)
userEntry.place(x=395, y=230)

# Campo de senha
passLabel = tk.Label(rightFrame, text="Senha:", font="Arial 20 bold", bg="#7FA653", fg="white")
passLabel.place(x=275, y=250)

passEntry = ttk.Entry(rightFrame, width=30, show="•")
passEntry.place(x=375, y=260)

# Botões
loginButton = ttk.Button(rightFrame, text="Entrar", width=30, command=login)
loginButton.place(x=330, y=300)

def registrar():
    # Removendo widgets de login
    loginButton.place(x=5000)
    registerButton.place(x=5000)
    # Inserindo widgets de cadastro
    # Campo de nome do pesquisador
    nome_pesquisadorLabel = tk.Label(rightFrame, text="Nome:", font="Arial 20 bold", bg="#7FA653", fg="white")
    nome_pesquisadorLabel.place(x=275, y=100)

    nome_pesquisadorEntry = ttk.Entry(rightFrame, width=30)
    nome_pesquisadorEntry.place(x=375, y=110)

    # Campo de instituição
    instituicaoLabel = tk.Label(rightFrame, text="Instituição:", font="Arial 20 bold", bg="#7FA653", fg="white")
    instituicaoLabel.place(x=275, y=130)

    instituicaoEntry = ttk.Entry(rightFrame, width=30)
    instituicaoEntry.place(x=430, y=140)

    # Campo de Email
    emailLabel = tk.Label(rightFrame, text="Email:", font="Arial 20 bold", bg="#7FA653", fg="white")
    emailLabel.place(x=275, y=160)

    emailEntry = ttk.Entry(rightFrame, width=30)
    emailEntry.place(x=370, y=170)

    # Campo de telefone 
    telefoneLabel = tk.Label(rightFrame, text="Telefone:", font="Arial 20 bold", bg="#7FA653", fg="white")
    telefoneLabel.place(x=275, y=190)

    telefoneEntry = ttk.Entry(rightFrame, width=30)
    telefoneEntry.place(x=420, y=200)

    # Campo de usuário
    userLabel = tk.Label(rightFrame, text="Usuário:", font="Arial 20 bold", bg="#7FA653", fg="white")
    userLabel.place(x=275, y=220)

    userEntry = ttk.Entry(rightFrame, width=30)
    userEntry.place(x=395, y=230)

    # Campo de senha
    passLabel = tk.Label(rightFrame, text="Senha:", font="Arial 20 bold", bg="#7FA653", fg="white")
    passLabel.place(x=275, y=250)

    passEntry = ttk.Entry(rightFrame, width=30, show="•")
    passEntry.place(x=375, y=260)

    # Botão de registrar no banco de dados
    def registerToDataBase():
        nome_pesquisador = nome_pesquisadorEntry.get()
        instituicao = instituicaoEntry.get()
        email = emailEntry.get()
        tel = telefoneEntry.get()
        user = userEntry.get()
        senha = passEntry.get()

        if nome_pesquisador == "" or instituicao == "" or email == "" or tel == "" or user == "" or senha == "":
            messagebox.showerror(title="Register Error", message="Preencha todos os campos!")
        else:
            # Inserindo os dados no banco
            database.cursor.execute(f"""INSERT INTO pesquisadores (nome, instituicao, email, telefone, user, senha)
                                        VALUES('{nome_pesquisador}', '{instituicao}', '{email}', '{tel}', '{user}', '{senha}');""")
            database.con.commit()
            messagebox.showinfo(title="Register Info", message="Usuário registrado com sucesso!")
            BackToLogin()

    register = ttk.Button(rightFrame, text="Registrar", width=30, command=registerToDataBase)
    register.place(x=330, y=300)

    def BackToLogin():
        # Removendo widgets de cadastro
        nome_pesquisadorLabel.place(x=5000)
        nome_pesquisadorEntry.place(x=5000)
        instituicaoLabel.place(x=5000)
        instituicaoEntry.place(x=5000)
        emailLabel.place(x=5000)
        emailEntry.place(x=5000)
        telefoneLabel.place(x=5000)
        telefoneEntry.place(x=5000)
        userLabel.place(x=5000)
        userEntry.place(x=5000)
        passLabel.place(x=5000)
        passEntry.place(x=5000)
        register.place(x=5000)
        back.place(x=5000)
        # Trazendo widgets de login
        loginButton.place(x=330, y=300)
        registerButton.place(x=300, y=550)

    # Botão de voltar
    back = ttk.Button(rightFrame, text="Voltar", width=30, command=BackToLogin)
    back.place(x=330, y=330)

registerButton = ttk.Button(rightFrame, text="Registrar", width=30, command=registrar)
registerButton.place(x=300, y=550)

janela.mainloop()
