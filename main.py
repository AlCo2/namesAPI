from flask import Flask, render_template, Response, jsonify
import mysql.connector
import json
from db import DATABASE_CONFIG
app = Flask(__name__)


def get_mysql_connection():
    connection = mysql.connector.connect(**DATABASE_CONFIG)
    return connection

def formatToJson(data):
    list = []
    for row in data:
        name = {
            "id": row[0],
            "name": row[1],
            "gender": row[2],
        }
        list.append(name)
    return list

@app.route('/')
def welcome():
    return render_template('index.html')



@app.route("/api/names", methods=['GET'])
def get_names():
    connection = get_mysql_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM names")
    data = cursor.fetchall()
    result = formatToJson(data)
    response = Response(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
    )
    cursor.close()
    if(result):
        return response
    return jsonify({"message": "error in fetching data"}), 404

@app.route("/api/names/<int:id>")
def get_name(id):
    connection = get_mysql_connection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM names where id={id}")
    data = cursor.fetchall()
    result = formatToJson(data)
    response = Response(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
    )
    cursor.close()
    if(result):
        return response
    return jsonify({"message": "error in fetching data"}), 404

app.run()