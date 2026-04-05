import streamlit as st
from pages1.Utils1 import viewpoints_menu
from pages1.Utils1 import ppr_view
from pages1.Utils1 import additonal_views

def show():
    st.header("🛠️ Build PPR Model")
    st.markdown("Create a Process Product Resource model from scratch.") 
    selected_view_build = viewpoints_menu.selection()

    if selected_view_build=="PPR View":
        ppr_view.show()
    
    if selected_view_build=="Engineering View":
        additonal_views.show(selected_view_build)

    if selected_view_build=="Sustainability View":
        additonal_views.show(selected_view_build)