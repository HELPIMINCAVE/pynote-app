import streamlit as st
import pandas as pd
from src.main.main import add, load_notes, save_db, delete_note, update_note, register_user, login_user

st.set_page_config(page_title="Pynote Secure", page_icon="🔒")

# --- LOGIN LOGIC ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

if not st.session_state.logged_in:
    st.title("🔐 Welcome to Pynote")
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        u = st.text_input("Username", key="l_user")
        p = st.text_input("Password", type="password", key="l_pass")
        if st.button("Login"):
            if login_user(u, p):
                st.session_state.logged_in = True
                st.session_state.username = u
                st.rerun()
            else:
                st.error("Invalid username or password")
    
    with tab2:
        new_u = st.text_input("New Username", key="s_user")
        new_p = st.text_input("New Password", type="password", key="s_pass")
        if st.button("Create Account"):
            if register_user(new_u, new_p):
                st.success("Account created! You can now login.")
            else:
                st.error("Username already exists.")
    st.stop()  # Prevents the rest of the app from loading until logged in

# --- LOGGED IN APP ---
st.title(f"📝 {st.session_state.username}'s Notes")

with st.sidebar:
    st.write(f"Logged in as: **{st.session_state.username}**")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
    st.divider()
    
    st.header("New Note")
    t_in = st.text_input("Title")
    c_in = st.text_area("Content")
    if st.button("Add Note", use_container_width=True):
        if t_in and c_in:
            add(t_in, c_in, st.session_state.username)
            st.rerun()
    
    notes = load_notes(st.session_state.username)
    if notes:
        st.divider()
        csv = pd.DataFrame(notes).to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export CSV", data=csv, file_name='notes.csv', use_container_width=True)

# --- MAIN AREA ---
search = st.text_input("🔍 Search...", "").lower()
filtered = [n for n in notes if search in n['title'].lower() or search in n['content'].lower()]

for note in reversed(filtered):
    with st.expander(f"📌 {note['title']} ({note.get('timestamp', 'N/A')})"):
        st.write(note['content'])
        col1, col2 = st.columns([5, 1])
        with col2:
            if st.button("🗑️", key=f"del_{note['id']}"):
                delete_note(note['id'])
                st.rerun()