# db_users.py
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = os.path.join(BASE_DIR, "users.db")

def init_db():
    """Crea la tabla de usuarios e inserta las cuentas de prueba si está vacía."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    
    cursor.execute('SELECT COUNT(*) FROM usuarios')
    if cursor.fetchone()[0] == 0:
        usuarios_defecto = [
            ('Marvin', '12345'),
            ('johndoe', 'Roblox123')
        ]
        cursor.executemany('INSERT INTO usuarios (username, password) VALUES (?, ?)', usuarios_defecto)
        conn.commit()
        
    conn.close()

def verify_credentials(username, password):
    """Verifica en el archivo .db si el usuario y la contraseña coinciden."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT password FROM usuarios WHERE username = ?', (username,))
    resultado = cursor.fetchone()
    conn.close()
    if resultado and resultado[0] == password:
        return True
    return False

def add_user(username, password):
    """
    Registra un nuevo usuario en la base de datos.
    Devuelve True si se creó con éxito, o False si el usuario ya existe.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute('INSERT INTO usuarios (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        exito = True
    except sqlite3.IntegrityError:
        # Esto pasa si el username ya existe (porque es PRIMARY KEY)
        exito = False
    finally:
        conn.close()
        
    return exito

def update_user_password(username, new_password):
    """Actualiza la contraseña de un usuario específico en la base de datos."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('UPDATE usuarios SET password = ? WHERE username = ?', (new_password, username))
    conn.commit()
    conn.close()
    
def get_user_by_id(username):
    """Busca al usuario en el archivo .db por su ID para Flask-Login."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT username FROM usuarios WHERE username = ?', (username,))
    resultado = cursor.fetchone()
    conn.close()
    
    if resultado:
        return {'username': resultado[0]}
    return None
init_db()