from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

DATABASE = 'myflix.db'


def create_tables():
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscriptions (
                subscriptionId INTEGER PRIMARY KEY AUTOINCREMENT,
                userId INTEGER,
                paidSubscriber TEXT NOT NULL,
                amount REAL NOT NULL,
                FOREIGN KEY (userId) REFERENCES users (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                session_id TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')


        connection.commit()


@app.route('/authenticate', methods=['POST'])
def authenticate_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute(
            'SELECT * FROM users WHERE email=? AND password=?', (email, password))
        user = cursor.fetchone()

    return jsonify({'user': user})


@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')

    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO users (first_name, last_name, email, password) VALUES (?, ?, ?, ?)',
            (first_name, last_name, email, password)
        )
        connection.commit()

    return jsonify({'message': 'User added successfully'})


@app.route('/get_user_id', methods=['POST'])
def get_user_id():
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')

    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('''
            SELECT id FROM users
            WHERE first_name = ? AND last_name = ? AND email = ?
        ''', (first_name, last_name, email))

        user_id = cursor.fetchone()

    return jsonify({'user_id': user_id[0] if user_id else None})


@app.route('/add_subscription', methods=['POST'])
def add_subscription():
    data = request.json
    userId = data.get('userId')
    paidSubscriber = data.get('paidSubscriber')
    amount = data.get('amount')

    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO subscriptions (userId, paidSubscriber, amount) VALUES (?, ?, ?)',
            (userId, paidSubscriber, amount)
        )
        connection.commit()

    return jsonify({'message': 'Subscription added successfully'}), 200


@app.route('/add_session', methods=['POST'])
def add_session():
    data = request.json
    user_id = data.get('user_id')
    session_id = data.get('session_id')

    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO sessions (user_id, session_id) VALUES (?, ?)',
            (user_id, session_id)
        )
        connection.commit()

    return jsonify({'message': 'Session added successfully'})
 
if __name__ == '__main__':
    create_tables() #creates table first
    app.run(host = "0.0.0.0",debug=True, port=6000)
