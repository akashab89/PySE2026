import streamlit as st
from pages1.Utils1 import viewpoints_menu
from pages1.Utils1 import ppr_view
from pages1.Utils1 import additonal_views
from pages1.Utils1 import viewpoints_menu

def show():
    st.header("🛠️ Build PPR Model")
    st.markdown("Create a Process Product Resource model from scratch.")
    selected_view = viewpoints_menu.handle("Build PPR Model")
    if selected_view=="PPR View":
        ppr_view.show()        
    if selected_view=="Engineering View":
        additonal_views.show(selected_view)
    if selected_view=="Sustainability View":
        additonal_views.show(selected_view)