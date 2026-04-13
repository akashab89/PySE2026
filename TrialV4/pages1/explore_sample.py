import streamlit as st
from pages1.Utils1 import viewpoints_menu
from pages1.Utils1 import ppr_view
from pages1.Utils1 import additonal_views

def show():
    dummy_nodes={}
    dummy_links=[]
    st.header("📦 Explore Sample")
    st.markdown("A predefined example to understand the structure.")
    selected_view = viewpoints_menu.handle("Explore Sample")
    if selected_view=="PPR View":
        ppr_view.show(nodes={}, links=[], locked=True)        
    if selected_view=="Engineering View":
        additonal_views.show(nodes=dummy_nodes, links=dummy_links, selected_view=selected_view, locked=True)
    if selected_view=="Sustainability View":
        additonal_views.show(nodes=dummy_nodes, links=dummy_links, selected_view=selected_view, locked=True)


