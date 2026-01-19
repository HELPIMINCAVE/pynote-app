import json
import os
from datetime import datetime

DB_PATH = "notes_db.json"

def load_db():
    if not os.path.exists(DB_PATH):
        # Initialize the file with empty lists if it doesn't exist
        return {"users": [], "notes": []}
    with open(DB_PATH, "r") as f:
        try:
            return json.load(f)
        except:
            return {"users": [], "notes": []}

def save_db(db):
    with open(DB_PATH, "w") as f:
        json.dump(db, f, indent=4)

def register_user(username, password):
    db = load_db()
    # Check if username already exists
    if any(u['username'] == username for u in db['users']):
        return False
    db['users'].append({"username": username, "password": password})
    save_db(db)
    return True

def login_user(username, password):
    db = load_db()
    for user in db['users']:
        if user['username'] == username and user['password'] == password:
            return True
    return False

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