import sqlite3

conexao = sqlite3.connect("database.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS transportadoras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    nome TEXT NOT NULL UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS roteiros(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    data TEXT NOT NULL UNIQUE,
               
    status TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS notas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
        
    numero_nf TEXT NOT NULL UNIQUE,
               
    transportadora_id INTEGER NOT NULL,
            
    roteiro_id INTEGER NOT NULL,
               
    status TEXT NOT NULL,
               
    hora_pronta TEXT,
               
    FOREIGN KEY (transportadora_id)
        REFERENCES transportadoras(id),
    
    FOREIGN KEY (roteiro_id)
        REFERENCES roteiros(id)
)
""")

conexao.commit()
conexao.close()