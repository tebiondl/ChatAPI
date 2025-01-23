import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Crear una tabla si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT NOT NULL,
            result TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    
def insert_question(prompt, result):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO questions (prompt, result) VALUES (?, ?)
    ''', (prompt, result))

    conn.commit()
    conn.close()
    
def get_questions():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT prompt, result FROM questions
    ''')

    questions = cursor.fetchall()
    conn.close()
    
    return questions