import streamlit as st
import pandas as pd
from src.main.main import add, load_notes, save_notes, delete_note, update_note

st.set_page_config(page_title="Pynote Pro", page_icon="📝")
st.title("📝 Pynote Streamlit")

# --- SIDEBAR: Add & Export ---
with st.sidebar:
    st.header("New Note")
    title_in = st.text_input("Title", key="new_title")
    content_in = st.text_area("Content", key="new_content")
    if st.button("Add Note", use_container_width=True):
        if title_in and content_in:
            add(title_in, content_in)
            st.rerun()
    
    # Load notes once here to use for logic below
    notes = load_notes()
    
    # If notes exist, show Export and then Danger Zone
    if notes:
        st.divider()
        st.header("Backup & Export")
        
        # 1. Export as CSV
        df = pd.DataFrame(notes)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export as .CSV", data=csv, file_name='notes.csv', mime='text/csv',
                           use_container_width=True)
        
        # 2. Export as TXT (The missing part of your bug)
        txt_content = ""
        for n in notes:
            txt_content += f"TITLE: {n['title']}\nDATE: {n.get('timestamp', 'N/A')}\nCONTENT: {n['content']}\n{'-' * 20}\n"
        
        st.download_button("📄 Export as .TXT", data=txt_content.encode('utf-8'), file_name='notes.txt',
                           mime='text/plain', use_container_width=True)
    
    # DANGER ZONE: Always separated by one divider from the section above
    st.divider()
    st.subheader("Danger Zone")
    if "confirm_delete" not in st.session_state:
        st.session_state.confirm_delete = False
    
    if not st.session_state.confirm_delete:
        if st.button("Clear All Notes", type="primary", use_container_width=True):
            st.session_state.confirm_delete = True
            st.rerun()
    else:
        st.warning("Are you sure?")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Yes", type="primary", use_container_width=True):
                save_notes([])
                st.session_state.confirm_delete = False
                st.rerun()
        with c2:
            if st.button("❌ No", use_container_width=True):
                st.session_state.confirm_delete = False
                st.rerun()

# --- MAIN AREA ---
search_query = st.text_input("🔍 Search notes...", "").lower()

if not notes:
    st.info("No notes found. Create one in the sidebar!")
else:
    filtered = [n for n in notes if search_query in n['title'].lower() or search_query in n['content'].lower()]
    
    for note in reversed(filtered):
        with st.expander(f"📌 {note['title']} ({note.get('timestamp', 'No Date')})"):
            edit_mode_key = f"edit_mode_{note['id']}"
            if edit_mode_key not in st.session_state:
                st.session_state[edit_mode_key] = False
            
            if not st.session_state[edit_mode_key]:
                st.write(note['content'])
                st.divider()
                col_l, col_m, col_r = st.columns([4, 1, 1])
                with col_m:
                    if st.button("🗑️", key=f"del_{note['id']}"):
                        delete_note(note['id'])
                        st.rerun()
                with col_r:
                    if st.button("✏️", key=f"edit_{note['id']}"):
                        st.session_state[edit_mode_key] = True
                        st.rerun()
            else:
                edit_title = st.text_input("Edit Title", value=note['title'], key=f"t_{note['id']}")
                edit_content = st.text_area("Edit Content", value=note['content'], key=f"c_{note['id']}")
                cs, cc = st.columns(2)
                with cs:
                    if st.button("💾 Save", key=f"s_{note['id']}", use_container_width=True):
                        update_note(note['id'], edit_title, edit_content)
                        st.session_state[edit_mode_key] = False
                        st.rerun()
                with cc:
                    if st.button("❌ Cancel", key=f"can_{note['id']}", use_container_width=True):
                        st.session_state[edit_mode_key] = False
                        st.rerun()