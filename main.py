from flask import Flask, render_template, Response, jsonify, request
import mysql.connector
import json
import random

DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Iamalegend',
    'database': 'nameapi'
}

def create_app():
    app = Flask(__name__)
    @app.route('/', methods=['GET', 'POST'])
    def welcome():
        name = 'name'
        if request.method == 'POST':
            gender = request.form['gender']
            region = request.form.getlist('region')
            if(len(region)>0):
                name = get_randome_name(gender, region[0])
            else:
                region = random.randrange(1,4)
                name = get_randome_name(gender, region)
        return render_template('index.html', name=name)


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

    @app.route('/api/randomname')
    def get_random_data():
        connection = get_mysql_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM names")
        random_data = cursor.fetchall()
        result = formatToJson(random_data)
        result = random.choices(result)
        response = Response(
            response=json.dumps(result),
            status=200,
            mimetype='application/json'
        )
        cursor.close()
        if(result):
            return response
        return jsonify({"message": "error in fetching data"}), 404

    @app.route('/api/randomname/<int:id>')
    def get_random_multiple_data(id):
        if(id>50):
            id = 50
        if(id<=0):
            id = 1
        connection = get_mysql_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM names")
        random_data = cursor.fetchall()
        result = formatToJson(random_data)
        result = random.choices(result, k=id)
        response = Response(
            response=json.dumps(result),
            status=200,
            mimetype='application/json'
        )
        cursor.close()
        if(result):
            return response
        return jsonify({"message": "error in fetching data"}), 404
    return app


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
            "region": row[3],
        }
        list.append(name)
    return list


def get_randome_name(gender, region):
    connection = get_mysql_connection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM names where gender='{gender}' and region={region}")
    random_data = cursor.fetchall()
    result = random.choices(random_data)
    return result[0][1]

if __name__ == '__main__':
    app = create_app()
    app.run()