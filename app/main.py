from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from crud import init_db, get_items, add_items, delete_item, register_user, login_user
import os

app = Flask(__name__)
CORS(app)
db = init_db()

@app.route('/')
@app.route('/index.html')
def home():
    base_dir = os.path.abspath(os.path.dirname(__file__))

    possible_paths = [
        base_dir,
        os.path.join(base_dir, 'app'),
        os.path.join(base_dir, 'frontend')
    ]

    for path in possible_paths:
        if os.path.exists(os.path.join(path, 'index.html')):
            return send_from_directory(path, 'index.html')

    return jsonify({
        "error": "index.html not found in container",
        "working_dir": base_dir,
        "files_in_dir": os.listdir(base_dir)
    }), 404

@app.route('/items', methods=['GET'])
def read_items():
    return jsonify(get_items(db))

@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    return jsonify(add_items(db, data))

@app.route('/items/<item_id>', methods=['DELETE'])
def delete_item_route(item_id):
    return jsonify(delete_item(db, item_id))

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    return jsonify(register_user(db, data['username'], data['password']))

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    response = login_user(db, data['username'], data['password'])
    
    if response.get("status") == "error":
        return jsonify(response), 401
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)