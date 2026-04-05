import streamlit as st
import streamlit as st
from yfiles_graphs_for_streamlit import StreamlitGraphWidget, Layout
from yfiles_graphs_for_streamlit import NodeStyle, NodeShape
import xml.etree.ElementTree as ET
import networkx as nx
from streamlit_option_menu import option_menu
from pages1 import import_model, build_ppr, explore_sample, reset_workspace, help_docs

st.set_page_config(page_title="Product-Process-Resource (PPR) Visualizer", page_icon="⚙️",layout="wide",initial_sidebar_state="collapsed")
st.title("⚙️ Product-Process-Resource (PPR) Visualizer")


with st.sidebar:
    selected_sidebar=option_menu("Workspace",
                     ["Import Model","Build PPR Model", "Explore Sample","Reset Workspace", "Help and Docs"],
                         icons=["upload","diagram-3","box-seam","arrow-counterclockwise","question-circle"], 
    menu_icon="grid",default_index=0, orientation= "vertical", key="main_menu" )

if selected_sidebar == "Import Model":
    import_model.show()

elif selected_sidebar == "Build PPR Model":
    build_ppr.show()

elif selected_sidebar == "Explore Sample":
    explore_sample.show()

elif selected_sidebar == "Help and Docs":
    help_docs.show()

elif selected_sidebar == "Reset Workspace":
    reset_workspace.show()

