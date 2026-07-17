import sqlite3
from datetime import date
# ==========================
# CONEXÃO
# ==========================
def conectar():
    return sqlite3.connect("database.db")

# ==========================
# CRIAÇÃO DO BANCO
# ==========================
def criar_banco():

    conexao = conectar()
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

# ==========================
# TRANSPORTADORAS
# ==========================

def cadastrar_transportadora(nome):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO transportadoras (nome)
        VALUES(?)
    """, (nome,))

    conexao.commit()
    conexao.close()

def listar_transportadoras():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT * FROM transportadoras
        ORDER BY LOWER(nome);
    """)

    transportadoras = cursor.fetchall()

    conexao.close()

    return transportadoras

def buscar_transportadora(id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT * FROM transportadoras
        WHERE id = ?
    """, (id,))

    transportadora = cursor.fetchone()

    conexao.close()

    return transportadora

def atualizar_transportadora(id, nome):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE transportadoras
        SET nome = ?
        WHERE id = ?
    """, (
        nome,
        id
    ))

    conexao.commit()
    conexao.close()

def excluir_transportadora(id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        DELETE FROM transportadoras
        WHERE id = ?
    """, (id,))

    conexao.commit()
    conexao.close()

# ==========================
# ROTEIROS
# ==========================


def criar_roteiro():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT *
        FROM roteiros
        WHERE status = 'Aberto'
    """)

    roteiro_aberto = cursor.fetchone()

    if roteiro_aberto:
        conexao.close()
        return False
    
    data_atual = date.today()

    cursor.execute("""
        INSERT INTO roteiros(data, status)
        VALUES (?,?)
    """, (data_atual, "Aberto"))

    conexao.commit()
    conexao.close()

    return True

def listar_roteiros():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT *
        FROM roteiros
        ORDER BY data DESC
    """)

    roteiros = cursor.fetchall()

    conexao.close()

    return roteiros

def buscar_roteiro(id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT *
        FROM roteiros
        WHERE id = ?
    """, (id,))

    roteiro = cursor.fetchone()

    conexao.close()

    return roteiro

def fechar_roteiro(id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE roteiros
        SET status = 'Fechado'
        WHERE id = ?
    """, (id,))

    conexao.commit()
    conexao.close()


# ==========================
# NOTAS
# ==========================

def buscar_roteiro_aberto():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT *
        FROM roteiros
        WHERE status = 'Aberto'
    """)

    roteiro = cursor.fetchone()

    conexao.close()

    return roteiro

def cadastrar_nota(numero_nf, transportadora_id):

    conexao = conectar()
    cursor = conexao.cursor()

    roteiro = buscar_roteiro_aberto()

    if not roteiro:
        conexao.close()
        return False

    roteiro_id = roteiro[0]

    cursor.execute("""
        INSERT INTO notas (
            numero_nf,
            transportadora_id,
            roteiro_id,
            status,
            hora_pronta
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        numero_nf,
        transportadora_id,
        roteiro_id,
        "Pendente",
        None
    ))

    conexao.commit()
    conexao.close()

    return True

def listar_notas():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            notas.id,
            notas.numero_nf,
            transportadoras.nome,
            notas.status,
            notas.hora_pronta
        FROM notas
        JOIN transportadoras
            ON notas.transportadora_id = transportadoras.id
        ORDER BY status ASC, numero_nf DESC   
    """)

    notas = cursor.fetchall()

    conexao.close()

    return notas

def listar_notas_roteiro(roteiro_id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            notas.id,
            notas.numero_nf,
            transportadoras.nome,
            notas.status,
            notas.hora_pronta
        FROM notas

        JOIN transportadoras
            ON notas.transportadora_id = transportadoras.id

        WHERE notas.roteiro_id = ?

        ORDER BY notas.numero_nf     

    """, (roteiro_id,))

    notas = cursor.fetchall()

    conexao.close()

    return notas

if __name__ == "__main__":
    criar_banco()