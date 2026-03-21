import streamlit as st
import networkx as nx
from streamlit_option_menu import option_menu
import streamlit_antd_components as sac
import pandas as pd

st.set_page_config(page_title="Product-Process-Resource (PPR) Visualizer", page_icon="⚙️",layout="wide")
st.title("⚙️ Product-Process-Resource (PPR) Visualizer")
uploaded_files = st.file_uploader(
    "Upload PPR File", accept_multiple_files=False, type="xlsx")
st.button("Create New PPR diagram")

if uploaded_files:
    st.success("File successfully loaded")

if "G" not in st.session_state:
        st.session_state.G = nx.DiGraph()

if "show_right" not in st.session_state:
    st.session_state.show_right = True

# Sidebar details

with st.sidebar:
    st.header("📂 Model Explorer")
    st.subheader("Model Structure")

    selected_element = sac.tree(
        items=[
            # Product Category
            sac.TreeItem('Product', icon='box', children=[
                sac.TreeItem('Product 1'),
                sac.TreeItem('Product 2'),
                sac.TreeItem('Product 3'),
            ]),
            
            # Process Category
            sac.TreeItem('Process', icon='gear', children=[
                sac.TreeItem('Process 1'),
                sac.TreeItem('Process 2'),
                sac.TreeItem('Process 3'),
            ]),
            
            # Resource Category
            sac.TreeItem('Resource', icon='wrench', children=[
                sac.TreeItem('Resource 1'),
                sac.TreeItem('Resource 2'),
                sac.TreeItem('Resource 3'),
            ]),
        ],
        index=0,        # Default selection (Product)
        open_all=True,  # Keeps all folders open automatically
        show_line=True  # Shows the vertical connection lines
    )

    st.divider()
    st.subheader("Analysis")
    selected_item = sac.tree(
        items=[
            # Root Node 1: Viewpoints (Subtree starts here)
            sac.TreeItem(
                'Viewpoints',
                children=[
                    sac.TreeItem('Engineering Viewpoint'),
                    sac.TreeItem('Sustainability Viewpoint'),
                ],
            ),
            sac.TreeItem('Requirements', children=["Something"]),
        ],
        index=1,        # Starts on 'Engineering Viewpoint'
        open_all=True,  # Keeps the Viewpoints subtree visible
        show_line=True  # Note: applies to entire tree (cannot limit per node)
    )

    st.subheader("Object Attributes")

    st.markdown("Attributes for Object 1")
    df=pd.DataFrame({"Attributes":["A1","A2", "A3"],
                     "Values":[100,200,300],
                     "Units":["ms","kg","NaN"]})
   
    st.sidebar.table(df)
    
    reset_submit=st.sidebar.button("Reset Data")
    if reset_submit:
        st.session_state.G.clear()


selected=option_menu("Navigation",
                     ["PPR Composition","Model Editor", "Graph"],
                     icons=["info-circle", "tools", "bar-chart-steps"], 
    menu_icon="cast", 
    default_index=0,
                     orientation= "horizontal"
                     )
