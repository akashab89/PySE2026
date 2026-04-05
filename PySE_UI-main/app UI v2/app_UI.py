import streamlit as st
import xml.etree.ElementTree as et
from yfiles_graphs_for_streamlit import StreamlitGraphWidget, Layout
from yfiles_graphs_for_streamlit import NodeStyle, NodeShape
import xml.etree.ElementTree as ET
import networkx as nx
from streamlit_option_menu import option_menu
from pages1 import import_model, build_ppr, explore_sample, help_docs


st.set_page_config(page_title="Product-Process-Resource (PPR) Visualizer", page_icon="⚙️",layout="wide",initial_sidebar_state="collapsed")
st.title("⚙️ Product-Process-Resource (PPR) Visualizer")

st.write(st.session_state)

sidebar_menu = ["Import Model", "Build PPR Model", "Explore Sample","Help and Docs"]

if "main_menu" not in st.session_state:
    st.session_state.main_menu = "Import Model"

current = st.session_state.get("main_menu")
current_index = sidebar_menu.index(current)

with st.sidebar:
    selected_sidebar=option_menu("Workspace",
                     sidebar_menu,
                         icons=["upload","diagram-3","box-seam","question-circle"], 
    menu_icon="grid",default_index=current_index, orientation= "vertical", key="main_menu" )



    if st.button("Reset Workspace", key="reset_button"):
        @st.dialog("Reset Workspace")
        def reset_workspace():
            st.write("Are you sure you want to reset everything?")

            if st.button("OK"):

                a= st.session_state.main_menu
                if "view_of" in st.session_state:
                    b= st.session_state.view_of
                st.session_state.clear()
                st.session_state.main_menu = a
                if "view_of" not in st.session_state:
                    st.session_state.view_of = b
                st.rerun()
        reset_workspace()
    

#st.write(st.session_state)

if "view_of" not in st.session_state:
    st.session_state.view_of = {}

if selected_sidebar == "Import Model":
    import_model.show()

elif selected_sidebar == "Build PPR Model":

    build_ppr.show()

elif selected_sidebar == "Explore Sample":
    explore_sample.show()

elif selected_sidebar == "Help and Docs":
    help_docs.show()
