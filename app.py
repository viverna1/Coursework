from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # тут можно что-то делать с введёнными данными
        return f"Ты ввёл: {username}, {password}"
    return render_template('auth.html')

if __name__ == '__main__':
    app.run(debug=True)
