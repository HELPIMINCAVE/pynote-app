import json
import os
import typer

cli = typer.Typer() # Renamed from 'app' to avoid confusion with app.py

# Get the directory where this script (main.py) is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up two levels to the root Pynote-app folder
DB_PATH = os.path.join(BASE_DIR, "..", "..", "notes_db.json")

def load_notes():
    if not os.path.exists(DB_PATH):
        return []
    with open(DB_PATH, "r") as f:
        try:
            return json.load(f)
        except:
            return []

def save_notes(notes):
    with open("notes_db.json", "w") as f:
        json.dump(notes, f, indent=4)

# This is the function Streamlit will call
def add(title: str, content: str):
    notes = load_notes()
    new_id = len(notes) + 1
    new_note = {"id": new_id, "title": title, "content": content}
    notes.append(new_note)
    save_notes(notes)
    return new_note

def delete_note(note_id: int):
    notes = load_notes()
    # Create a new list excluding the note with the matching ID
    updated_notes = [n for n in notes if n['id'] != note_id]
    save_notes(updated_notes)

# This links the function to your Command Line interface
@cli.command()
def add_note_cli(title: str, content: str):
    add(title, content)
    print(f"Added {title}")

if __name__ == "__main__":
    cli()