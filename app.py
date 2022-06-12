import time
import serial
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

DB_URI = "mysql+pymysql://root:root@localhost/kursova"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI

db = SQLAlchemy(app)
ma = Marshmallow(app)

arduino_serial = serial.Serial("COM3", 9600, timeout=1)
cors = CORS(app)

list_of_commands = []


class Example(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    example = db.Column(db.String(255), nullable=False)

    def __init__(self, example):
        self.example = example

    def __repr__(self):
        return f"id: {self.id}, example: {self.example}"


class ExampleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'example')


example_schema = ExampleSchema()
examples_schema = ExampleSchema(many=True)


@app.route("/calculator", methods=["GET"])
def get_me():
    examples = Example.query.all()
    result = examples_schema.dump(examples)
    return jsonify(result)


@app.route("/calculator", methods=["POST"])
def post_me():
    data = request.get_json()
    list_of_commands.append(data)
    send_list_of_commands(list_of_commands)

    if data == "button_equals":
        send_data(arduino_serial.readline().decode('Ascii'))
        print(arduino_serial.readline().decode('Ascii'))

    return 'Success', 200


def send_data(example):
    data_set = {"example": example}
    json_dump = json.dumps(data_set)
    print(json_dump)
    data = ExampleSchema().loads(json_dump)

    new_example = Example(**data)
    print(new_example)
    db.session.add(new_example)
    db.session.commit()


def send_list_of_commands(commands):
    for command in commands:
        send_command(command)
        time.sleep(1.3)
    list_of_commands.clear()


def send_command(command):
    arduino_serial.write(command.encode())


if __name__ == '__main__':
    app.run(use_reloader=False)


