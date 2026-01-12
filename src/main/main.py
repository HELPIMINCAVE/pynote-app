import json
import os
import typer

cli = typer.Typer() # Renamed from 'app' to avoid confusion with app.py

def load_notes():
    if not os.path.exists("notes_db.json"):
        return []
    with open("notes_db.json", "r") as f:
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

# This links the function to your Command Line interface
@cli.command()
def add_note_cli(title: str, content: str):
    add(title, content)
    print(f"Added {title}")

if __name__ == "__main__":
    cli()