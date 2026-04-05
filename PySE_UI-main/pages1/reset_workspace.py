import streamlit as st

def has_data():
    # Check for keys, ignoring the menu state itself
    return len([k for k in st.session_state.keys() if k != "main_menu"]) > 0

@st.dialog("Workspace Management")
def reset_dialog():
    if not has_data():
        st.info("ℹ️ Nothing to clear. Your workspace is already empty.")
        if st.button("OK"):
            # Reset the sidebar selection to the first page before rerunning
            st.session_state.main_menu = "Import Model"
            selected = st.session_state.main_menu
            st.rerun()
    else:
        st.warning("⚠️ This will delete all stored session data. This cannot be undone.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Yes, clear everything", use_container_width=True):
                # Clear everything EXCEPT the menu selection
                for key in list(st.session_state.keys()):
                    if key != "main_menu":
                        del st.session_state[key]
                # Redirect to home page
                st.session_state.main_menu = "Import Model"
                st.rerun()
        with col2:
            if st.button("❌ Cancel", use_container_width=True):
                # Redirect to home page
                st.session_state.main_menu = "Import Model"
                st.rerun()

def show():
    # This calls the dialog immediately when the page is rendered
    reset_dialog()