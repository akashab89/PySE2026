import streamlit as st
from pages1.Utils1 import viewpoints_menu
from pages1.Utils1 import ppr_view
from pages1.Utils1 import additonal_views
from pages1.Utils1.sample_data import sample_ppr_nodes, sample_ppr_edges

def show(engineering_nodes: dict, engineering_edges: list, sustainability_nodes: dict, sustainability_edges: list):

    st.header("📦 Explore Sample")
    st.markdown("A predefined example to understand the structure.")
    selected_view = viewpoints_menu.handle("Explore Sample")
    if selected_view=="PPR View":
        ppr_view.show(nodes=sample_ppr_nodes, links=sample_ppr_edges,
                       engineering_nodes=engineering_nodes, engineering_edges=engineering_edges,
                       sustainability_nodes=sustainability_nodes, sustainability_edges=sustainability_edges, locked=True)
    if selected_view=="Engineering View":
        additonal_views.show( ppr_nodes=sample_ppr_nodes,nodes= engineering_nodes,links=engineering_edges,selected_view=selected_view,locked=True)
    if selected_view=="Sustainability View":
         additonal_views.show( ppr_nodes=sample_ppr_nodes,nodes= sustainability_nodes,links=sustainability_edges,selected_view=selected_view,locked=True)

