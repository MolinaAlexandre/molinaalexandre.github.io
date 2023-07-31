from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = '9086123019bdfjazuzdoai'  # Replace this with a real secret key
login_manager = LoginManager(app)
login_manager.login_view = 'login'
 
# User class to represent users
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id
        self.password = None

    def set_password(self, password):
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    # Fetch user information from the database based on the user_id
    user_data = get_user_from_db(user_id)
    if user_data:
        user = User(user_id)
        user.set_password(user_data['password'])
        return user
    return None

def get_license_from_db(username):
    conn = sqlite3.connect('license.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM GENERATED WHERE username=?", (username,))
    user_data = cursor.fetchall()
    cursor.close()
    conn.close()
    user_data_as_dict = []
    for data in user_data:
        user_dict = {
            'id': data[0],
            'license_type': data[1],
            'key_1': data[2],
            'key_2': data[3],
            'duration': data[4],
            'site_name': data[5],
            'adress': data[6],
            'code_1': data[7],
            'code2': data[8],
            'username': data[9],
            'date': data[10],
        }
        user_data_as_dict.append(user_dict)
    return user_data_as_dict

def push_log_to_db(username, status):
    conn = sqlite3.connect('license.db')
    cursor = conn.cursor()
    time = datetime.now()
    d1 = time.strftime("%d/%m/%Y %H:%M")
    print(d1, username, status)
    cursor.execute("INSERT INTO LOG (datetime, username, status_connection) VALUES (?, ?, ?)", (d1, username, status))
    conn.commit()
    cursor.close()
    conn.close()

def push_licence_to_db(form_data):
    conn = sqlite3.connect('license.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO generated (license_type, key_1, key_2, duration, site_name, adress, code_1, code2, username, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (form_data['license_type'],
                    form_data['key_1'],
                    form_data['key_2'],
                    form_data['duration'],
                    form_data['site_name'],
                    form_data['adress'],
                    form_data['code_1'],
                    form_data['code2'],
                    form_data['username'],
                    form_data['date']))
    conn.commit()
    cursor.close()
    conn.close()

def get_user_from_db(user_id):
    conn = sqlite3.connect('license.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM USERS WHERE username=?", (user_id,))
    user_data = cursor.fetchone()

    cursor.close()
    conn.close()

    if user_data:
        user_dict = {
            'username': user_data[1],
            'password': user_data[2]
        }
        return user_dict
    return None


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_data = get_user_from_db(username)
        print(username, password)

        if user_data and user_data['password'] == password:
            user = User(username)
            push_log_to_db(username, True)
            user.set_password(user_data['password'])
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            push_log_to_db(username, False)
    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    user_data = get_license_from_db(current_user.id)
    return render_template('dashboard.html', user_data=user_data)


@app.route('/request_license', methods=['GET', 'POST'])
def request_license():
    time = datetime.now()
    d1 = time.strftime("%d/%m/%Y %H:%M")
    if request.method == 'POST':
        form_data = {
            'site_name': request.form['site_name'],
            'adress': request.form['adress'],
            'license_type': request.form['license_type'],
            'duration': request.form['duration'],
            'code_1': request.form['code_1'],
            'code2': request.form['code2'],
            #CODE VB GENERATION LICENCES
            'date': d1,
            'key_1': 7981237891,
            'key_2': 7981237892,
            'username': current_user.id
        }
        print(form_data)
        push_licence_to_db(form_data)
        return redirect('/dashboard')
    return render_template('request_license.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
