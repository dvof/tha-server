from flask import Flask, request, jsonify
import sqlite3
import os
import argparse

# Flask web server
app = Flask(__name__)

# Directory to store SQLite databases
#DB_DIR = "databases"
DB_DIR = "/mnt/databases"
os.makedirs(DB_DIR, exist_ok=True)

def get_db_connection(db_name):
    """ Connect to the SQLite database, creating it if necessary. """
    db_path = os.path.join(DB_DIR, f"{db_name}.db")
    conn = sqlite3.connect(db_path)
    return conn

def create_table_if_not_exists(conn):
    """ Ensure the table exists within the SQLite database. """
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entity_id TEXT,
            temperature REAL,
            humidity REAL,
            timestamp TEXT
        )
    ''')
    conn.commit()

@app.route('/store_data', methods=['POST'])
def store_data():
    try:
        data = request.get_json()

        entity_id = str(data.get("id"))
        if not entity_id:
            return jsonify({"error": "No ID found in JSON"}), 400

        # Connect to the database
        conn = get_db_connection(entity_id)
        create_table_if_not_exists(conn)

        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO sensor_data (entity_id, temperature, humidity, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (
            entity_id,
            data.get("temperature"),
            data.get("humidity"),
            data.get("timestamp")
        ))

        conn.commit()
        conn.close()

        return jsonify({"message": "Data stored successfully!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', help="Enable debug mode")
    args = parser.parse_args()
    
    app.run(debug=args.debug)
