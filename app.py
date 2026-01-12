import streamlit as st
import sys
import os

# Ensure the root project is in the path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Import the module as an object
try:
    import src.main.main as logic
except ImportError as e:
    st.error(f"Could not find the file: {e}")
    st.stop()


# Add the current directory to sys.path so 'src' is findable
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Try importing the module first, then the functions
try:
    from src.main.main import add, load_notes
except ImportError as e:
    st.error(f"Import Error: {e}")
    st.stop()

st.title("📝 Pynote Streamlit")

# Sidebar for adding notes
with st.sidebar:
    st.header("New Note")
    title = st.text_input("Title")
    content = st.text_area("Content")
    if st.button("Add Note"):
        if title and content:
            add(title, content)
            st.success("Note added!")
            st.rerun()

# Displaying notes
st.header("Your Notes")
notes = load_notes()

if not notes:
    st.info("No notes yet.")
else:
    for note in reversed(notes):
        with st.expander(f"{note['title']}"):
            st.write(note['content'])