import streamlit as st
from pages1.Utils1 import viewpoints_menu
from pages1.Utils1 import ppr_view
from pages1.Utils1 import additonal_views
from xml.etree import ElementTree as et
from pages1.Utils1 import viewpoints_menu
from pages1.Utils1.aml_utils import build_elements_dict, extract_links, extract_ppr_links, iface_mapping
from pages1.Utils1.config import global_nodes_list
from pages1.Utils1.excel_utils import elements_from_excel, links_from_excel


def show(engineering_nodes: dict, engineering_edges: list, sustainability_nodes: dict, sustainability_edges: list):
    st.header("📥 Import Model")
    
    if "upload" not in st.session_state:
        st.session_state.upload = None
    
    
    if st.session_state.upload is None:       
        st.subheader("Upload an AML/XLXS file to visualize and analyze the PPR graph.")
        if st.session_state.built_nodes:
            lock1= True
            st.warning("You are already working on another PPR. Reset Workspace to upload file")
        else:
            lock1=False
        uploaded_file= st.file_uploader("Upload AML/XLXS file", type=["aml", "xlsx"], key="file_uploader", disabled=lock1)
 
        if uploaded_file:
            file_name = uploaded_file.name.lower()
            #Check separately for AML and XLSX files
            if file_name.endswith(".aml"):
                try:
                    tree= et.parse(uploaded_file)
                    root= tree.getroot()
                    ns = {"caex": "http://www.dke.de/CAEX"}

                except Exception as e:
                    st.warning("Your AML file might be corrupted.")
                    with st.expander ("Full error"):
                        st.write(e)

                elements_dict=build_elements_dict(root, ns)

                link_list= extract_links(root, ns)
                iface_mappi= iface_mapping(root, ns)

                #for debugging and code experiment
                ppr_link_list = extract_ppr_links(link_list, iface_mappi)
                st.session_state.upload = uploaded_file.name  # Mark file as processed
                if "imported_nodes" not in st.session_state:
                    st.session_state.imported_nodes = elements_dict.copy()  # Store a copy of the elements dictionary in session state

                if "imported_edges" not in st.session_state:
                    st.session_state.imported_edges = ppr_link_list.copy()  # Store a copy of the link list in session state

            elif file_name.endswith(".xlsx"):
                elements_dict = elements_from_excel(uploaded_file)
                ppr_link_list = links_from_excel(uploaded_file)

                st.session_state.upload = uploaded_file.name  # Mark file as processed
                if "imported_nodes" not in st.session_state:
                    st.session_state.imported_nodes = elements_dict.copy()  # Store a copy of the elements dictionary in session state

                if "imported_edges" not in st.session_state:
                    st.session_state.imported_edges = ppr_link_list.copy()  # Store a copy of the link list in session state
            
    
    if st.session_state.upload is not None:
        imported_nodes= st.session_state.imported_nodes
        imported_edges= st.session_state.imported_edges
    
        st.info(f"Uploaded File is:  ***{st.session_state.upload}***")
        # st.write(imported_nodes)
        null_class_keys = [
            key for key, value in imported_nodes.items()
            if value.get("class") is None
        ]
        # st.write(global_nodes_list)
        invalid_class_keys = {
            key for key, value in imported_nodes.items()
            if value.get("class") not in global_nodes_list
        }
        # st.write(invalid_class_keys)
        # st.write(null_class_keys)
        if null_class_keys:
            st.warning("No class keys found in imported nodes.")
            st.warning(f"Following nodes have no class value: {null_class_keys}. Please add the class values to respective nodes and try again.")
        elif invalid_class_keys:
            st.warning("Nodes with invalid class keys found in imported nodes.")
            st.warning(f"Following nodes have invalid class value: {invalid_class_keys}. Please change the class to PPR conform and try again.")
        elif not imported_nodes:
            st.warning("No Nodes found in imported model. Please check and try again.")
        else:
            selected_view = viewpoints_menu.handle("Import Model")
            if selected_view=="PPR View":
                ppr_view.show(nodes=imported_nodes, links=imported_edges,
                               engineering_nodes=engineering_nodes, engineering_edges=engineering_edges,
                               sustainability_nodes=sustainability_nodes, sustainability_edges=sustainability_edges)
            if selected_view=="Engineering View":
                additonal_views.show(ppr_nodes=imported_nodes, nodes=engineering_nodes, links=engineering_edges, selected_view=selected_view)
            if selected_view=="Sustainability View":
                additonal_views.show(ppr_nodes=imported_nodes, nodes=sustainability_nodes, links=sustainability_edges, selected_view=selected_view)





