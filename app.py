from flask import Flask, render_template, request, session, redirect
import os
import sqlite3

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from werkzeug.security import generate_password_hash, check_password_hash

import config

# =================== База данных ===================

"""
# Удалить данные1
c.execute('DELETE FROM users WHERE id > ?', ('3',))

# Oбновить данные
c.execute('UPDATE users SET age = ? WHERE name = ?', (28, 'Alice'))
"""


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
            username TEXT NOT NULL,
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

def get_user_by_email(email):
    with ConectDB() as c:
        c.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = c.fetchone()

        return user


def login_user(user, password):
    if isinstance(user, str):
        user = get_user_by_email(user)

    if user is None or user == "None":
        return "userNotFound"  # пользователь не найден
    
    if check_password_hash(user["password"], password):
        session["username"] = user["username"]
        return "success"  # успешный вход
    else:
        return "wrongPass"  # неверный пароль


def register_user(username, email, password):
    if get_user_by_email(email):
        return "emailExist"

    hashed_password = generate_password_hash(password)
    with ConectDB() as c:
        c.execute('''
            INSERT INTO users (username, email, password) VALUES (?, ?, ?)
        ''', (username, email, hashed_password)
        )
        session["username"] = username

        print(f"\033[94mЗарегестрирован {username}, пароль: {password}\033[0m")
        return "success"


def send_email(theme, message, recipient):
    sender = "viverna2alt@gmail.com"
    password = config.email_password

    # Создаём сообщение
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = theme
    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())
        server.quit()
        return "✅ Сообщение отправилось"

    except Exception as e:
        return f"{e}\n Проверьте логин или пароль"





# ==================== Сайт ====================

app = Flask(__name__)
app.secret_key = 'jhjkwf3489980upigojn54klntkjdsbfh'


@app.route('/')
def home():
    return render_template('index.html')


# ----- Аккаунт -----

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']


        status = login_user(email, password)

        if status == "success":
            return redirect('/')
        return render_template('login.html', error=status,
                               email=email, password=password)

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        status = register_user(username, email, password)

        if status == "success":
            return redirect('/')
        elif status == "emailExist":
            return render_template('register.html', error="emailExist",
                                username=username, email=email, password=password)
        return redirect('/')

    return render_template('register.html')


@app.route('/resetPassword', methods=['GET', 'POST'])
def resetPassword():
    if request.method == 'POST':
        email = request.form['email']

        user =  get_user_by_email(email)

        if user:
            message = f"Имя: {user["username"]}\nПароль: {user["password"]}"
            result = send_email("Ваш логин и пароль", message, email)
            print(result, email)
            return render_template('/resetPassword.html', status="emailCorrect",
                                   email=email)
        else:
            return render_template('/resetPassword.html', status="userNotFound",
                                   email=email)

    return render_template('/resetPassword.html')


# ----- Настройки -----

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    return render_template("/settings.html")


@app.route('/changeUsername', methods=['POST'])
def change_username():
    new_username = request.form.get('value')
    
    return render_template("/settings.html", status="success")

@app.route('/changeEmail', methods=['POST'])
def change_email():
    new_email = request.form.get('value')
    
    return render_template("/settings.html", status="success")

@app.route('/changePhoto', methods=['POST'])
def change_photo():
    photo = request.files.get('value')

    return render_template("/settings.html", status="success")

@app.route('/changeNumber', methods=['POST'])
def change_number():
    new_number = request.form.get('value')
    
    return render_template("/settings.html", status="success")

# Функции на сайте:

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


    
if __name__ == '__main__':
    init_db()
    app.run(debug=True)

