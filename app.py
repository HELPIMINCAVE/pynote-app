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
    
    st.divider()
    st.header("Backup & Export")
    notes = load_notes()
    
    if notes:
        df = pd.DataFrame(notes)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export as .CSV", data=csv, file_name='notes.csv', mime='text/csv',
                           use_container_width=True)
    
    st.divider()
    st.subheader("Danger Zone")
    
    # --- DELETE ALL CONFIRMATION ---
    if "confirm_delete" not in st.session_state:
        st.session_state.confirm_delete = False
    
    if not st.session_state.confirm_delete:
        if st.button("Clear All Notes", type="primary", use_container_width=True):
            st.session_state.confirm_delete = True
            st.rerun()
    else:
        st.warning("Are you sure? This cannot be undone.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Yes, Delete", type="primary", use_container_width=True):
                save_notes([])
                st.session_state.confirm_delete = False
                st.rerun()
        with col2:
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state.confirm_delete = False
                st.rerun()

# --- MAIN AREA: Search & Edit ---
search_query = st.text_input("🔍 Search notes...", "").lower()

if not notes:
    st.info("No notes found.")
else:
    filtered = [n for n in notes if search_query in n['title'].lower() or search_query in n['content'].lower()]
    
    for note in reversed(filtered):
        with st.expander(f"📌 {note['title']} ({note.get('timestamp', 'No Date')})"):
            # EDIT FIELDS
            edit_title = st.text_input("Edit Title", value=note['title'], key=f"t_{note['id']}")
            edit_content = st.text_area("Edit Content", value=note['content'], key=f"c_{note['id']}")
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("💾 Save Changes", key=f"save_{note['id']}", use_container_width=True):
                    update_note(note['id'], edit_title, edit_content)
                    st.success("Updated!")
                    st.rerun()
            with c2:
                if st.button("🗑️ Delete", key=f"del_{note['id']}", use_container_width=True):
                    delete_note(note['id'])
                    st.rerun()