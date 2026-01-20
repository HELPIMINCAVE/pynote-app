import streamlit as st
import pandas as pd
from src.main.main import (
    add, load_notes, save_db, delete_note, load_db,
    update_note, register_user, login_user, delete_account
)

st.set_page_config(page_title="Pynote Secure", page_icon="🔐")

# --- INITIALIZE SESSION STATE ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# --- LOGIN / SIGNUP PAGE ---
if not st.session_state.logged_in:
    st.title("🔐 Secure Pynote")
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        u = st.text_input("Username", key="login_u")
        p = st.text_input("Password", type="password", key="login_p")
        if st.button("Login", use_container_width=True):
            if login_user(u, p):
                st.session_state.logged_in = True
                st.session_state.username = u
                st.rerun()
            else:
                st.error("Invalid username or password.")
    
    with tab2:
        nu = st.text_input("New Username", key="reg_u").strip()  # .strip() removes accidental spaces
        np = st.text_input("New Password", type="password", key="reg_p").strip()
        
        if st.button("Register Account", use_container_width=True):
            # We now catch the boolean AND the message from our new function
            success, message = register_user(nu, np)
            if success:
                st.success(message)
            else:
                st.error(message)
    st.stop()

# --- LOGGED IN APP ---
db = load_db()
user_data = next((u for u in db['users'] if u['username'] == st.session_state.username), None)
notes = load_notes(st.session_state.username)

# --- SIDEBAR ---
with st.sidebar:
    st.subheader(f"👤 {st.session_state.username}")
    if user_data and 'last_login' in user_data:
        st.caption(f"Last login: {user_data['last_login']}")
    
    # Settings: Account Deletion
    with st.expander("Settings"):
        st.warning("Delete Account")
        del_pass = st.text_input("Verify Password", type="password", key="del_verify")
        if st.button("Confirm Deletion", type="primary", use_container_width=True):
            if delete_account(st.session_state.username, del_pass):
                st.session_state.logged_in = False
                st.success("Account deleted.")
                st.rerun()
            else:
                st.error("Incorrect password.")
    
    if st.button("Logout", use_container_width=True):
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
    
    # Export & Clear All (Only show if notes exist)
    if notes:
        st.divider()
        st.header("Backup")
        
        # CSV Export
        df = pd.DataFrame(notes)
        st.download_button("📥 Export .CSV", data=df.to_csv(index=False), file_name="notes.csv",
                           use_container_width=True)
        
        # TXT Export
        txt_body = ""
        for n in notes:
            txt_body += f"TITLE: {n['title']}\nDATE: {n.get('timestamp', 'N/A')}\nCONTENT: {n['content']}\n{'-' * 20}\n"
        st.download_button("📄 Export .TXT", data=txt_body.encode('utf-8'), file_name="notes.txt",
                           use_container_width=True)
        
        st.divider()
        st.subheader("Danger Zone")
        if st.button("Clear All My Notes", type="primary", use_container_width=True):
            # Only remove notes belonging to this user
            db['notes'] = [n for n in db['notes'] if n.get('owner') != st.session_state.username]
            save_db(db)
            st.rerun()

# --- MAIN AREA ---
st.header("Your Notes")
search = st.text_input("🔍 Search your notes...", "").lower()
filtered = [n for n in notes if search in n['title'].lower() or search in n['content'].lower()]

if not filtered:
    st.info("No matching notes found.")
else:
    for note in reversed(filtered):
        with st.expander(f"📌 {note['title']} ({note.get('timestamp', 'N/A')})"):
            edit_key = f"is_editing_{note['id']}"
            if edit_key not in st.session_state:
                st.session_state[edit_key] = False
            
            if not st.session_state[edit_key]:
                # VIEW MODE
                st.write(note['content'])
                st.divider()
                col_l, col_m, col_r = st.columns([4, 1, 1])
                with col_m:
                    if st.button("🗑️", key=f"del_{note['id']}", help="Delete"):
                        delete_note(note['id'])
                        st.rerun()
                with col_r:
                    if st.button("✏️", key=f"edit_btn_{note['id']}", help="Edit"):
                        st.session_state[edit_key] = True
                        st.rerun()
            else:
                # EDIT MODE
                e_title = st.text_input("Edit Title", value=note['title'], key=f"et_{note['id']}")
                e_content = st.text_area("Edit Content", value=note['content'], key=f"ec_{note['id']}")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("💾 Save", key=f"save_{note['id']}", use_container_width=True):
                        update_note(note['id'], e_title, e_content)
                        st.session_state[edit_key] = False
                        st.rerun()
                with c2:
                    if st.button("❌ Cancel", key=f"can_{note['id']}", use_container_width=True):
                        st.session_state[edit_key] = False
                        st.rerun()