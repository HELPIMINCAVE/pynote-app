import streamlit as st
import sys
import os

# Ensure the root directory is in your python path so 'src' can be found
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Importing your logic from main.py
try:
    from src.main.main import add, load_notes, save_notes, delete_note
except ImportError as e:
    st.error(f"Error: Could not import functions from main.py. {e}")
    st.stop()

# --- Page Configuration ---
st.set_page_config(page_title="Pynote App", page_icon="📝", layout="centered")

st.title("📝 Pynote Streamlit")

# --- SIDEBAR: Add Notes & Maintenance ---
with st.sidebar:
    st.header("New Note")
    # Form to handle note input
    with st.form("note_form", clear_on_submit=True):
        title_input = st.text_input("Title", placeholder="Enter note title...")
        content_input = st.text_area("Content", placeholder="Enter note content...")
        submit = st.form_submit_button("Add Note", use_container_width=True)
        
        if submit:
            if title_input and content_input:
                add(title_input, content_input)
                st.success(f"Note '{title_input}' saved!")
                st.rerun()
            else:
                st.warning("Please fill in both fields.")
    
    st.divider()
    
    # Clear All Feature
    st.subheader("Danger Zone")
    if st.button("Clear All Notes", type="primary", use_container_width=True):
        save_notes([])
        st.success("All notes cleared!")
        st.rerun()

# --- MAIN AREA: Search & Display ---
st.header("Your Notes")

# 1. Search Bar
search_query = st.text_input("🔍 Search notes by title or content...", "").lower()

# 2. Load Data
notes = load_notes()

if not notes:
    st.info("Your notebook is currently empty.")
else:
    # 3. Filter notes based on the search query
    filtered_notes = [
        n for n in notes
        if search_query in n.get('title', '').lower()
           or search_query in n.get('content', '').lower()
    ]
    
    if not filtered_notes:
        st.warning(f"No notes found matching '{search_query}'")
    else:
        # 4. Display the filtered list (Newest first)
        for note in reversed(filtered_notes):
            with st.expander(f"📌 {note['title']}"):
                st.write(note['content'])
                st.caption(f"Note ID: {note['id']}")
                
                # Delete button for individual notes
                # Note: 'key' must be unique for every button in Streamlit
                if st.button(f"🗑️ Delete Note", key=f"del_{note['id']}"):
                    delete_note(note['id'])
                    st.rerun()