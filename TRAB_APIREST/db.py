# Código

import sqlite3
from flask import Flask, request

app = Flask(__name__)

@app.route('/contatos', methods=['GET', 'POST', 'PUT', 'DELETE'])
def contatos():
    if request.method == 'GET':
        return get_contatos()
    elif request.method == 'POST':
        return create_contato()
    elif request.method == 'PUT':
        return update_contato()
    else:
        return delete_contato()

def get_contatos():
    nome = request.args.get('nome', '')
    empresa = request.args.get('empresa', '')
    email = request.args.get('email', '')

    query = 'SELECT * FROM contatos'
    params = []
    if nome:
        query += ' WHERE nome LIKE ?'
        params.append('%' + nome + '%')
    if empresa:
        query += ' WHERE empresa LIKE ?'
        params.append('%' + empresa + '%')
    if email:
        query += ' WHERE email LIKE ?'
        params.append('%' + email + '%')

    db = sqlite3.connect('agenda.db')
    cursor = db.cursor()
    cursor.execute(query, params)
    contatos = cursor.fetchall()
    db.close()

    return {'contatos': contatos}

def create_contato():
    nome = request.args.get('nome')
    empresa = request.args.get('empresa')
    telefone = request.args.get('telefone')
    email = request.args.get('email')

    query = 'INSERT INTO contatos (nome, empresa, telefone, email) VALUES (?,?,?,?)'
    params = (nome, empresa, telefone, email)

    db = sqlite3.connect('agenda.db')
    cursor = db.cursor()
    cursor.execute(query, params)
    db.commit()
    db.close()

    return {'message': 'Contato criado com sucesso!'}

def update_contato():
    nome = request.args.get('nome')
    empresa = request.args.get('empresa')
    telefone = request.args.get('telefone')
    email = request.args.get('email')
    id = request.args.get('id')

    query = 'UPDATE contatos SET nome=?, empresa=?, telefone=?, email=? WHERE id=?'
    params = (nome, empresa, telefone, email, id)

    db = sqlite3.connect('agenda.db')
    cursor = db.cursor()
    cursor.execute(query, params)
    db.commit()
    db.close()

    return {'message': 'Contato atualizado com sucesso!'}

def delete_contato():
    id = request.args.get('id')

    query = 'DELETE FROM contatos WHERE id=?'
    params = (id,)

    db = sqlite3.connect('agenda.db')
    cursor = db.cursor()
    cursor.execute(query, params)
    db.commit()
    db.close()

    return {'message': 'Contato deletado com sucesso!'}

if __name__ == '__main__':
    app.run(debug=True)
