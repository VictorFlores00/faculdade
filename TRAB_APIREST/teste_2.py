import sqlite3
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return 'API_TRAB para Agenda de Contatos'

@app.route('/contatos', methods=['GET'])
def listar():
    nome = request.args.get('nome')
   
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
   
    if nome:
        cursor.execute("""
            SELECT * FROM contatos
            WHERE nome LIKE ?
        """, (nome,))
   
    else:
        cursor.execute("""
            SELECT * FROM contatos
        """)
   
    contatos = []
   
    for linha in cursor.fetchall():
        contatos.append({
            'id': linha[0],
            'nome': linha[1],
            'empresa': linha[2],
            'telefone': linha[3],
            'email': linha[4]
        })
   
    conn.close()
   
    return {'contatos': contatos}

@app.route('/contatos/<int:id>', methods=['GET'])
def localizar(id):
   
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
   
    cursor.execute("""
        SELECT * FROM contatos
        WHERE id = ?
    """, (id,))
   
    linha = cursor.fetchone()
   
    contato = {
        'id': linha[0],
        'nome': linha[1],
        'empresa': linha[2],
        'telefone': linha[3],
        'email': linha[4]
    }
   
    conn.close()
   
    return {'contato': contato}

@app.route('/contatos', methods=['POST'])
def inserir():
   
    contato = request.get_json()
   
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
   
    cursor.execute("""
        INSERT INTO contatos (nome, empresa, telefone, email)
        VALUES (?, ?, ?, ?)
    """, (contato['nome'], contato['empresa'], contato['telefone'], contato['email']))
   
    conn.commit()
   
    contato['id'] = cursor.lastrowid
   
    conn.close()
   
    return {'contato': contato}

@app.route('/contatos/<int:id>', methods=['PUT'])
def atualizar(id):
    contato = request.get_json()
   
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
   
    cursor.execute("""
        UPDATE contatos
        SET nome = ?,
            empresa = ?,
            telefone = ?,
            email = ?
        WHERE id = ?
    """, (contato['nome'], contato['empresa'], contato['telefone'], contato['email'], id))
   
    conn.commit()
   
    conn.close()
   
    return {'contato': contato}

@app.route('/contatos/<int:id>', methods=['DELETE'])
def remover(id):
   
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
   
    cursor.execute("""
        DELETE FROM contatos
        WHERE id = ?
    """, (id,))
   
    conn.commit()
   
    conn.close()
   
    return {'message': 'Contato excluído com sucesso!'}

if __name__ == '__main__':
    app.run(debug=True)