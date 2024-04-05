from flask import Flask, request
import sqlite3
import json
from datetime import datetime

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('prova.db')
    c = conn.cursor()

    # Create the table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS prova (
    idSensor TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    tipoPoluente FLOAT NOT NULL,
    nivel FLOAT NOT NULL,
);''')

    conn.commit()
    conn.close()

# API endpoint for receiving JSON data
@app.route('/dados', methods=['POST'])
def receive_data():
    data = request.get_json()

    print(data['idSensor'])
    print(data['timestamp'])
    print(data['tipoPoluente'])
    print(data['nivel'])
    print(data)

    # Store the data in the database
    conn = sqlite3.connect('prova.db')
    c = conn.cursor()

    c.execute("INSERT INTO prova VALUES (?, ?, ?, ?)", (data['idSensor'], data['timestamp'], data['tipoPoluente'], data['nivel']))

    conn.commit()
    conn.close()

    return 'Data stored successfully'

# API endpoint for querying the database
@app.route('/dados', methods=['GET'])
def query_data():
    conn = sqlite3.connect('ponderada.db')
    c = conn.cursor()

    # Get the data from the database
    c.execute("SELECT * FROM megamente")
    data = c.fetchall()

    conn.close()

    # Convert the data to JSON
    data_json = []
    for row in data:
        data_json.append({
            'sensor': row[0],
            'longitude': row[1],
            'latitude': row[2],
            'dado': row[3]
        })

    return json.dumps(data_json)

if __name__ == '__main__':
    init_db()
    app.run()