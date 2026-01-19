import json
import os
import hashlib
from datetime import datetime

DB_PATH = "notes_db.json"

def hash_password(password):
    # Turns "password123" into a long, unreadable string
    return hashlib.sha256(password.encode()).hexdigest()

def load_db():
    if not os.path.exists(DB_PATH):
        return {"users": [], "notes": []}
    with open(DB_PATH, "r") as f:
        try:
            data = json.load(f)
            if not isinstance(data, dict) or "users" not in data:
                return {"users": [], "notes": []}
            return data
        except:
            return {"users": [], "notes": []}

def save_db(db):
    with open(DB_PATH, "w") as f:
        json.dump(db, f, indent=4)

def register_user(username, password):
    db = load_db()
    if any(u['username'] == username for u in db['users']):
        return False
    db['users'].append({"username": username, "password": hash_password(password)})
    save_db(db)
    return True

def login_user(username, password):
    db = load_db()
    hashed = hash_password(password)
    return any(u['username'] == username and u['password'] == hashed for u in db['users'])

def delete_account(username):
    db = load_db()
    # 1. Remove the user
    db['users'] = [u for u in db['users'] if u['username'] != username]
    # 2. Remove all notes belonging to that user
    db['notes'] = [n for n in db['notes'] if n.get('owner') != username]
    save_db(db)

def load_notes(username):
    db = load_db()
    # Only return notes belonging to this specific user
    return [n for n in db['notes'] if n.get('owner') == username]

def add(title, content, username):
    db = load_db()
    new_id = 1 if not db['notes'] else max(n['id'] for n in db['notes']) + 1
    new_note = {
        "id": new_id,
        "owner": username, # Keep track of who owns the note
        "title": title,
        "content": content,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    db['notes'].append(new_note)
    save_db(db)

def delete_note(note_id):
    db = load_db()
    db['notes'] = [n for n in db['notes'] if n['id'] != note_id]
    save_db(db)

def update_note(note_id, title, content):
    db = load_db()
    for n in db['notes']:
        if n['id'] == note_id:
            n['title'] = title
            n['content'] = content
            n['timestamp'] = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (Edited)"
    save_db(db)