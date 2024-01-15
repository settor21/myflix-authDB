from flask import Flask, jsonify, request
import psycopg2
from bcrypt import hashpw, gensalt

app = Flask(__name__)

# PostgreSQL Configuration
DB_HOST = '35.239.170.49'  # Replace with the IP address of your GCP VM
DB_PORT = 5432
DB_USER = 'amedikusettor'
DB_PASSWORD = 'Skaq0084'
DB_NAME = 'users'

# Establish connection to PostgreSQL


def create_tables():
    with psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    ) as connection:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscriptions (
                subscriptionId SERIAL PRIMARY KEY,
                userId INTEGER,
                paidSubscriber TEXT NOT NULL,
                amount REAL NOT NULL,
                FOREIGN KEY (userId) REFERENCES users (id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id SERIAL PRIMARY KEY,
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

    with psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    ) as connection:
        cursor = connection.cursor()
        cursor.execute(
            'SELECT * FROM users WHERE email=%s', (email,))
        user = cursor.fetchone()

        if user and hashpw(password.encode('utf-8'), user[4].encode('utf-8')) == user[4].encode('utf-8'):
            # Passwords match
            return jsonify({'user': user})
        else:
            # Invalid credentials
            return jsonify({'user': None})


@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')

    # Hash the password before storing it
    hashed_password = hashpw(password.encode(
        'utf-8'), gensalt()).decode('utf-8')

    with psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    ) as connection:
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)',
            (first_name, last_name, email, hashed_password)
        )
        connection.commit()

    return jsonify({'message': 'User added successfully'})


@app.route('/get_user_id', methods=['POST'])
def get_user_id():
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')

    with psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    ) as connection:
        cursor = connection.cursor()
        cursor.execute('''
            SELECT id FROM users
            WHERE first_name = %s AND last_name = %s AND email = %s
        ''', (first_name, last_name, email))

        user_id = cursor.fetchone()

    return jsonify({'user_id': user_id[0] if user_id else None})


@app.route('/add_subscription', methods=['POST'])
def add_subscription():
    data = request.json
    user_id = data.get('user_id')  # Assuming 'userId' should be 'user_id'
    paidSubscriber = data.get('paidSubscriber')
    amount = data.get('amount')

    with psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    ) as connection:
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO subscriptions (user_id, paidSubscriber, amount) VALUES (%s, %s, %s)',
            (user_id, paidSubscriber, amount)
        )
        connection.commit()

    return jsonify({'message': 'Subscription added successfully'}), 200


@app.route('/add_session', methods=['POST'])
def add_session():
    data = request.json
    user_id = data.get('user_id')
    session_id = data.get('session_id')

    with psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    ) as connection:
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO sessions (user_id, session_id) VALUES (%s, %s)',
            (user_id, session_id)
        )
        connection.commit()

    return jsonify({'message': 'Session added successfully'})


if __name__ == '__main__':
    create_tables()  # creates table first
    app.run(host="0.0.0.0", debug=True, port=6000)
