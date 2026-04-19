import streamlit as st
from pages1.Utils1 import viewpoints_menu
from pages1.Utils1 import ppr_view
from pages1.Utils1 import additonal_views
from pages1.Utils1 import viewpoints_menu


def show(engineering_nodes: dict, engineering_edges: list, sustainability_nodes: dict, sustainability_edges: list):
    built_nodes = st.session_state.built_nodes
    built_edges = st.session_state.built_edges

    if "upload" not in st.session_state:
        st.session_state.upload = None

    st.header("🛠️ Build PPR Model")
    st.markdown("Create a Process Product Resource model from scratch.")
    selected_view = viewpoints_menu.handle("Build PPR Model")
    if st.session_state.upload is not None:
        st.warning("You have already uploaded. So, Please Reset to create New PPR")
        lock = True
    else:
        lock = False

    if selected_view == "PPR View":
        ppr_view.show(nodes=built_nodes, links=built_edges,
                      engineering_nodes=engineering_nodes, engineering_edges=engineering_edges,
                      sustainability_nodes=sustainability_nodes, sustainability_edges=sustainability_edges, locked=lock)
    if selected_view == "Engineering View":
        additonal_views.show(ppr_nodes=built_nodes, nodes=engineering_nodes, links=engineering_edges,
                             selected_view=selected_view, locked=lock)
    if selected_view == "Sustainability View":
        additonal_views.show(ppr_nodes=built_nodes, nodes=sustainability_nodes, links=sustainability_edges,
                             selected_view=selected_view, locked=lock)