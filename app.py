import streamlit as st
import pandas as pd
from src.main.main import (
    add, load_notes, save_db, delete_note,
    update_note, register_user, login_user, delete_account
)

st.set_page_config(page_title="Pynote Secure", page_icon="🔐")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# --- LOGIN / SIGNUP ---
if not st.session_state.logged_in:
    st.title("🔐 Secure Pynote")
    t1, t2 = st.tabs(["Login", "Sign Up"])
    with t1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            if login_user(u, p):
                st.session_state.logged_in = True
                st.session_state.username = u
                st.rerun()
            else:
                st.error("Invalid credentials")
    with t2:
        nu = st.text_input("New Username")
        np = st.text_input("New Password", type="password")
        if st.button("Register", use_container_width=True):
            if register_user(nu, np):
                st.success("User created!")
            else:
                st.error("User exists")
    st.stop()

# --- LOGGED IN APP ---
notes = load_notes(st.session_state.username)

with st.sidebar:
    st.subheader(f"👤 {st.session_state.username}")
    
    # SETTINGS: Delete Account
    with st.expander("Settings"):
        if st.button("🗑️ Delete Account", type="primary"):
            delete_account(st.session_state.username)
            st.session_state.logged_in = False
            st.rerun()
    
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
    
    st.divider()
    st.header("New Note")
    tin = st.text_input("Title")
    cin = st.text_area("Content")
    if st.button("Add Note", use_container_width=True):
        if tin and cin:
            add(tin, cin, st.session_state.username)
            st.rerun()
    
    # FIX: Grouping Exports and Clear All
    if notes:
        st.divider()
        st.header("Backup")
        # CSV Export
        df = pd.DataFrame(notes)
        st.download_button("📥 Export .CSV", data=df.to_csv(index=False), file_name="notes.csv",
                           use_container_width=True)
        # TXT Export
        txt = "\n".join([f"{n['title']}\n{n['content']}\n---" for n in notes])
        st.download_button("📄 Export .TXT", data=txt, file_name="notes.txt", use_container_width=True)
        
        st.divider()
        st.subheader("Danger Zone")
        if st.button("Clear All Notes", type="primary", use_container_width=True):
            from src.main.main import load_db, save_db
            
            db = load_db()
            db['notes'] = [n for n in db['notes'] if n.get('owner') != st.session_state.username]
            save_db(db)
            st.rerun()

# --- MAIN AREA: View & Edit ---
st.header(f"Your Notes")
search = st.text_input("🔍 Search...", "").lower()
filtered = [n for n in notes if search in n['title'].lower() or search in n['content'].lower()]

for n in reversed(filtered):
    with st.expander(f"📌 {n['title']} ({n.get('timestamp', 'N/A')})"):
        # Unique Edit State for each note
        edit_key = f"edit_{n['id']}"
        if edit_key not in st.session_state: st.session_state[edit_key] = False
        
        if not st.session_state[edit_key]:
            st.write(n['content'])
            c1, c2 = st.columns([5, 1])
            if c2.button("✏️", key=f"btn_{n['id']}"):
                st.session_state[edit_key] = True
                st.rerun()
        else:
            new_t = st.text_input("Title", value=n['title'], key=f"nt_{n['id']}")
            new_c = st.text_area("Content", value=n['content'], key=f"nc_{n['id']}")
            if st.button("💾 Save", key=f"sv_{n['id']}"):
                update_note(n['id'], new_t, new_c)
                st.session_state[edit_key] = False
                st.rerun()