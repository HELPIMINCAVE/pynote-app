import json
import os
import hashlib
from datetime import datetime

DB_PATH = "notes_db.json"


def hash_password(password):
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


# Add this function to your src/main/main.py

def validate_credentials(username, password):
    # Rule 1: Cannot be empty
    if not username or not password:
        return False, "Username and Password cannot be empty."
    
    # Rule 2: Minimum 3 characters
    if len(username) < 3 or len(password) < 3:
        return False, "Username and Password must be at least 3 characters long."
    
    # Rule 3: Username and Password cannot be the same
    if username.lower() == password.lower():
        return False, "Username and Password cannot be the same."
    
    return True, "Valid"


def register_user(username, password):
    db = load_db()
    
    # First, check our new validation rules
    is_valid, message = validate_credentials(username, password)
    if not is_valid:
        return False, message
    
    # Second, check if username already exists
    if any(u['username'] == username for u in db['users']):
        return False, "Username already exists."
    
    db['users'].append({
        "username": username,
        "password": hash_password(password),
        "last_login": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_db(db)
    return True, "Account created successfully!"


# IMPORTANT: Make sure this function is also present
def login_user(username, password):
    db = load_db()
    hashed = hash_password(password)
    for user in db['users']:
        if user['username'] == username and user['password'] == hashed:
            user['last_login'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_db(db)
            return True
    return False


def delete_account(username, password):
    db = load_db()
    hashed = hash_password(password)
    # Check if user exists and password matches
    user_to_delete = next((u for u in db['users'] if u['username'] == username and u['password'] == hashed), None)
    
    if user_to_delete:
        db['users'] = [u for u in db['users'] if u['username'] != username]
        db['notes'] = [n for n in db['notes'] if n.get('owner') != username]
        save_db(db)
        return True
    return False


# Ensure update_note is robust
def update_note(note_id, title, content):
    db = load_db()
    for n in db['notes']:
        if n['id'] == note_id:
            n['title'] = title
            n['content'] = content
            n['timestamp'] = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (Edited)"
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