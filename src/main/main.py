import typer
import json
import os
from datetime import datetime

# Rename 'app' to 'cli' to prevent circular import with app.py
cli = typer.Typer()

def load_notes():
    file_path = "notes_db.json"
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        try:
            return json.load(f)
        except:
            return []

def save_notes(notes):
    with open("notes_db.json", "w") as f:
        json.dump(notes, f, indent=4)

def delete_note(note_id: int):
    notes = load_notes()
    updated_notes = [n for n in notes if n['id'] != note_id]
    save_notes(updated_notes)

def update_note(note_id: int, new_title: str, new_content: str):
    notes = load_notes()
    for note in notes:
        if note['id'] == note_id:
            note['title'] = new_title
            note['content'] = new_content
            note['timestamp'] = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (Edited)"
            break
    save_notes(notes)

def add(title: str, content: str):
    notes = load_notes()
    new_id = len(notes) + 1 if not notes else max(n['id'] for n in notes) + 1
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_note = {"id": new_id, "title": title, "content": content, "timestamp": timestamp}
    notes.append(new_note)
    save_notes(notes)

@cli.command()
def add_note_cli(title: str, content: str):
    add(title, content)

if __name__ == "__main__":
    cli()