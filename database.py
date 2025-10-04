import sqlite3

def create_database():
    con = sqlite3.connect(database = r"Cafe.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS usuario(uid INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, email TEXT, genero TEXT, contato TEXT, datanascimento TEXT, datacontrataçao TEXT, senha TEXT, utype TEXT, endereço TEXT)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS estoque(id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, quantidade INTEGER, preco_unitario REAL, categoria TEXT)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS cardapio(id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, nome TEXT, preco REAL NOT NULL)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS pedidos(id INTEGER PRIMARY KEY AUTOINCREMENT, itens TEXT, total REAL, data TEXT)") 
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS fluxo_caixa(id INTEGER PRIMARY KEY AUTOINCREMENT, tipo TEXT, descricao TEXT, valor REAL, data TEXT)")
    con.commit()
    
create_database()
