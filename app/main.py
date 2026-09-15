from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from crud import init_db, get_items, add_items, delete_item, register_user, login_user

app = Flask(__name__)
CORS(app)
db = init_db()

@app.route('/')
def home():
    return send_from_directory('app', 'index.html')

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