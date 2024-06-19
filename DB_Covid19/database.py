import mysql.connector # -> Importação da Lib MySQL
from mysql.connector import Error # -> Importação do pacote de erros do SQL

# Criação da Conexão
con = mysql.connector.connect(host="localhost", database="covid_db",user="root", password="admin")

cursor = con.cursor()
