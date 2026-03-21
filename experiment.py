import streamlit as st

st.set_page_config(layout="wide")

# -------------------------------
# Session state for toggle
# -------------------------------
if "show_right" not in st.session_state:
    st.session_state.show_right = True

def toggle_panel():
    st.session_state.show_right = not st.session_state.show_right

# -------------------------------
# Layout logic
# -------------------------------
if st.session_state.show_right:
    col_main, col_right = st.columns([7, 1])
else:
    col_main, col_right = st.columns([1000, 27])  # narrow strip

# -------------------------------
# MAIN AREA
# -------------------------------
with col_main:
    st.title("Main Content Area")
    st.write("This is where your graph / main app goes.")
    st.write("Resize the right panel using the toggle button.")

# -------------------------------
# RIGHT PANEL
# -------------------------------
with col_right:
    if st.session_state.show_right:
        # Expanded panel
        st.markdown("### ⚙️ Right Panel")

        st.button("⬅ Collapse", on_click=toggle_panel)

        st.divider()
        st.write("Controls:")
        st.slider("Value", 0, 100)
        st.checkbox("Enable option")
        st.text_input("Enter name")

    else:
        # Collapsed thin strip
        st.markdown("### ")
        st.button("▶", on_click=toggle_panel)