import streamlit as st
from pages1.Utils1 import viewpoints_menu
from pages1.Utils1 import ppr_view
from pages1.Utils1 import additonal_views

def show():
    st.header("📦 Explore Sample")
    st.markdown("A predefined example to understand the structure.")
    selected_view_explore = viewpoints_menu.selection()

    if selected_view_explore=="PPR View":
        ppr_view.show(locked=True)
    
    if selected_view_explore=="Engineering View":
        additonal_views.show(selected_view_explore, locked=True)

    if selected_view_explore=="Sustainability View":
        additonal_views.show(selected_view_explore, locked=True)


