from flask import Flask, request, jsonify, render_template
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db, Queue

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['ENV'] = 'development'
app.config['DEBUG'] = True 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db.init_app(app)
Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)
CORS(app)

queue = Queue()

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/new", methods=['POST'])
def add_item():
    item = request.get_json()
    name = request.json.get("name")
    phone = request.json.get("phone")

    if not name:
        return jsonify({"msg": "name is required"}), 400
    if not phone:
        return jsonify({"msg": "phone is required"}), 400

    return jsonify(queue.enqueue(item)), 200 

@app.route("/next")
def next_item():
    response = queue.dequeue()
    if not response:
        return jsonify({"msg": "No one in the queue"}), 404
    else:
        return jsonify(response), 200

@app.route("/all")
def all_item():
    listado = queue.get_queue()
    if not listado:
        return jsonify({"msg": "No one in the queue"}), 404
    else:
        return jsonify(listado), 200


if __name__ == '__main__':
    manager.run()