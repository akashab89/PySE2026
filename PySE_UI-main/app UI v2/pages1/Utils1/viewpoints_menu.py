import streamlit as st
from streamlit_option_menu import option_menu 
from pages1.Utils1.config import VIEW_ATTRS_MAPPING
from pages1.Utils1 import ppr_view
from pages1.Utils1 import additonal_views

def handle(selected_sidebar):
    if selected_sidebar not in st.session_state.view_of:
        st.session_state.view_of[selected_sidebar] = "PPR View"
    
    options = list(VIEW_ATTRS_MAPPING.keys())
    current_index = options.index(st.session_state.view_of[selected_sidebar])


    selected_view = option_menu(
        "Viewpoints",
        options=options,
        icons=["diagram-3", "gear", "globe"],
        orientation="horizontal",
        default_index=current_index,
        key=f"view_menu_{selected_sidebar}"  # still unique
    )
    st.session_state.view_of[selected_sidebar] = selected_view
    return selected_view




