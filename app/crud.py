from pymongo import MongoClient
import os
from bson import ObjectId
import bcrypt

def register_user(db, username, password):
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    result = db.users.insert_one({
        "username": username,
        "password": hashed_pw.decode('utf-8')
    })
    return {"inserted_id": str(result.inserted_id)}

def login_user(db, username, password):
    user = db.users.find_one({"username": username})
    
    if user:
        stored_hash = user['password'].encode('utf-8')
        user_input_pw = password.encode('utf-8')
        
        if bcrypt.checkpw(user_input_pw, stored_hash):
            return {"status": "success", "username": username}
            
    return {"status": "error", "message": "Invalid credentials"}


def init_db():
    uri = os.environ.get('MONGO_URI')
    client = MongoClient(uri)
    return client["FlaskApp-Docker"]

def get_items(db):
    return [ {"_id": str(doc['_id']), "name": doc['name']} for doc in db.items.find()]

def add_items(db, data):
    result = db.items.insert_one({"name": data['name']})
    return {"inserted_id": str(result.inserted_id)}

def delete_item(db, item_id):
    db.items.delete_one({'_id': ObjectId(item_id)})
    return {"status": "deleted"}
