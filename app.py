from flask import Flask, render_template, request, session, redirect
import os
import sqlite3




# =================== База данных ===================

"""
# Удалить данные
c.execute('DELETE FROM users WHERE id > ?', ('3',))

# Oбновить данные
c.execute('UPDATE users SET age = ? WHERE name = ?', (28, 'Alice'))

c.execute('SELECT * FROM users')
print_table(c.fetchall())

db.commit()
db.close()"""


def init_db():
    """Инициализация базы данных"""
    # Создаем папку для базы данных, если она не существует
    os.makedirs(os.path.join(os.path.dirname(__file__), 'db'), exist_ok=True)
    
    db_path = os.path.join(os.path.dirname(__file__), 'db', 'database.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Создать новую таблицу
    c.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE,
            password TEXT NOT NULL,
            tel TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def get_db_connection():
    """Создает новое соединение с базой данных для каждого запроса"""
    db_path = os.path.join(os.path.dirname(__file__), 'db', 'database.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Чтобы получать результаты как словари
    return conn


class ConectDB:
    def __init__(self):
        self.conn = get_db_connection()
        self.c = self.conn.cursor()

    def __enter__(self):
        return self.c

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        exc_type - тип исключения (или None, если исключения не было)
        exc_val - объект исключения (или None)
        exc_tb - traceback объекта (или None)
        """
        
        self.conn.commit()
        self.conn.close()
        return False


# =================== Функции ==================

def get_username_by_email(email):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT username FROM users WHERE email = ?", (email,))
    row = c.fetchone()
    conn.close()
    if row:
        return row["username"]   # у тебя row_factory = sqlite3.Row, можно по имени
    return None


# ==================== Сайт ====================

app = Flask(__name__)
app.secret_key = 'jhjkwf3489980upigojn54klntkjdsbfh'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Соединение с бд
        with ConectDB() as c:
            # Проверка на существование логина

            user = None

            # сначала ищем по username
            c.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = c.fetchone()

            # если не нашли, ищем по email
            if not user:
                c.execute("SELECT * FROM users WHERE email = ?", (username,))
                user = c.fetchone()
                username = get_username_by_email(username)

            if user:
                pass
            else:
                c.execute('''
                    INSERT INTO users (username, email, password) VALUES (?, ?, ?)
                ''', (username, "test@gmail.com", password)
                )

                print(f"Зарегестрирован {username}, пароль: {password}")
            session["username"] = username

    return render_template('auth.html')



# Функции на сайте
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


if __name__ == '__main__':
    init_db()
    app.run(debug=True)

