from flask import Flask
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    conn = mysql.connector.connect(
        host="appdb.cb8auq6qgygi.ap-south-1.rds.amazonaws.com",
        user="admin",
        password="mrunali3925",
        database="appdb"
    )

    cursor = conn.cursor()
    cursor.execute("SELECT text FROM message LIMIT 1")
    result = cursor.fetchone()

    conn.close()

    return result[0]

app.run(host="0.0.0.0", port=5000)