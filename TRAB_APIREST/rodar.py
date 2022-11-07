import sqlite3

db = sqlite3.connect('agenda.db')
cursor = db.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS contatos (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        empresa TEXT NOT NULL,
        telefone TEXT NOT NULL,
        email TEXT NOT NULL
    )
''')