import streamlit as st
import xml.etree.ElementTree as et
from yfiles_graphs_for_streamlit import StreamlitGraphWidget, Layout
from yfiles_graphs_for_streamlit import NodeStyle, NodeShape
import xml.etree.ElementTree as ET
import networkx as nx
from streamlit_option_menu import option_menu
from pages1 import import_model, build_ppr, explore_sample, help_docs
from pages1.Utils1.sample_data import sample_eng_nodes, sample_eng_edges, sample_sus_nodes, sample_sus_edges
from custom_css import inject_custom_css
## Importing custom CSS style
inject_custom_css()

## App heading
st.set_page_config(page_title="Product-Process-Resource (PPR) Visualizer", page_icon="⚙️", layout="wide",
                   initial_sidebar_state="collapsed")
# st.title("⚙️ Product-Process-Resource (PPR) Visualizer")
st.markdown("""
<div class="hero">
    <div class="hero-content">
        <h1>Product-Process-Resource (PPR) Visualizer</h1>
        <p>
            Build, visualize, and validate Product–Process–Resource systems 
            with an intuitive engineering interface.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

sidebar_menu = ["Import Model", "Build PPR Model", "Explore Sample", "Help and Docs"]

if "main_menu" not in st.session_state:
    st.session_state.main_menu = "Import Model"
if "engineering_nodes" not in st.session_state:
    st.session_state.engineering_nodes = {}  # Store a copy of the elements dictionary in session state
if "engineering_edges" not in st.session_state:
    st.session_state.engineering_edges = []  # Store a copy of the engineering link list in session state
if "sustainability_nodes" not in st.session_state:
    st.session_state.sustainability_nodes = {}
if "sustainability_edges" not in st.session_state:
    st.session_state.sustainability_edges = []
if "built_nodes" not in st.session_state:
    st.session_state.built_nodes = {}  # Store a copy of the built nodes dictionary in session state
if "built_edges" not in st.session_state:
    st.session_state.built_edges = []  # Store a copy of the built edges list in session state

engineering_nodes = st.session_state.engineering_nodes
engineering_edges = st.session_state.engineering_edges
sustainability_nodes = st.session_state.sustainability_nodes
sustainability_edges = st.session_state.sustainability_edges

current = st.session_state.get("main_menu")
current_index = sidebar_menu.index(current)

## Sidebar Menu initialisation
with st.sidebar:
    selected_sidebar = option_menu("Workspace",
                                   sidebar_menu,
                                   icons=["upload", "diagram-3", "box-seam", "question-circle"],
                                   menu_icon="grid",
                                   default_index=current_index,
                                   orientation="vertical",
                                   key="main_menu")

    st.divider()
# Reset App Configuration
    if st.button("Reset Workspace", key="reset_button"):
        @st.dialog("Reset Workspace")
        def reset_workspace():
            st.write("Are you sure you want to reset everything?")

            if st.button("OK"):

                a = st.session_state.main_menu
                if "view_of" in st.session_state:
                    b = st.session_state.view_of
                st.session_state.clear()
                st.session_state.main_menu = a
                if "view_of" not in st.session_state:
                    st.session_state.view_of = b
                st.rerun()


        reset_workspace()

if "view_of" not in st.session_state:
    st.session_state.view_of = {}
# IMPORT MODEL WORKFLOW
if selected_sidebar == "Import Model":
    import_model.show(engineering_nodes=engineering_nodes, engineering_edges=engineering_edges,
                      sustainability_nodes=sustainability_nodes, sustainability_edges=sustainability_edges)

# BUILD PPR MODEL WORKFLOW
elif selected_sidebar == "Build PPR Model":
    build_ppr.show(engineering_nodes=engineering_nodes, engineering_edges=engineering_edges,
                   sustainability_nodes=sustainability_nodes, sustainability_edges=sustainability_edges)

# EXPLORE SAMPLE WORKFLOW
elif selected_sidebar == "Explore Sample":
    explore_sample.show(engineering_nodes=sample_eng_nodes, engineering_edges=sample_eng_edges,
                        sustainability_nodes=sample_sus_nodes, sustainability_edges=sample_sus_edges)

# HELP AND DOCUMENTATION WORKFLOW
elif selected_sidebar == "Help and Docs":
    help_docs.show()