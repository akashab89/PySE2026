import streamlit as st
from xml.etree import ElementTree as et

from pages1.Utils1 import viewpoints_menu, ppr_view, additonal_views
from pages1.Utils1.aml_utils import (
    build_elements_dict,
    extract_links,
    extract_ppr_links,
    iface_mapping
)

from pages1.Utils1.config import global_nodes_list
from pages1.Utils1.excel_utils import parse_excel
## IMPORT MODEL WORKFLOW
# Model from defined XLSX or AML format will be imported for visualisation and CRUD operations
def show(engineering_nodes: dict,
         engineering_edges: list,
         sustainability_nodes: dict,
         sustainability_edges: list):

    st.header("📥 Import Model")

    if "upload" not in st.session_state:
        st.session_state.upload = None

    if st.session_state.upload is None:

        st.subheader("Upload an AML/XLSX file to visualize and analyze the PPR graph.")

        lock1 = bool(st.session_state.get("built_nodes"))

        if lock1:
            st.warning("You are already working on another PPR. Reset Workspace to upload file")

        uploaded_file = st.file_uploader(
            "Upload AML/XLSX file",
            type=["aml", "xlsx"],
            key="file_uploader",
            disabled=lock1
        )
        ## File parsing depending on format
        if uploaded_file:

            file_name = uploaded_file.name.lower()

            # ---------------- AML ----------------
            if file_name.endswith(".aml"):
                try:
                    tree = et.parse(uploaded_file)
                    root = tree.getroot()
                    ns = {"caex": "http://www.dke.de/CAEX"}

                    elements_dict = build_elements_dict(root, ns)
                    link_list = extract_links(root, ns)
                    iface_mappi = iface_mapping(root, ns)

                    ppr_link_list = extract_ppr_links(link_list, iface_mappi)

                except Exception as e:
                    st.warning("Your AML file might be corrupted.")
                    with st.expander("Full error"):
                        st.write(e)
                    return

            # ---------------- XLSX ----------------
            elif file_name.endswith(".xlsx"):
                try:
                    elements_dict, ppr_link_list = parse_excel(uploaded_file)

                except ValueError as e:
                    st.error(str(e))
                    return

            else:
                st.error("Unsupported file type.")
                return

            # ---------------- STORE SESSION ----------------
            st.session_state.upload = uploaded_file.name

            if "imported_nodes" not in st.session_state:
                st.session_state.imported_nodes = elements_dict.copy()

            if "imported_edges" not in st.session_state:
                st.session_state.imported_edges = ppr_link_list.copy()

    # ---------------- DISPLAY ----------------
    if st.session_state.upload is not None:

        imported_nodes = st.session_state.imported_nodes
        imported_edges = st.session_state.imported_edges

        st.info(f"Uploaded File is:  ***{st.session_state.upload}***")

        ## Error Handling
        null_class_keys = [
            key for key, value in imported_nodes.items()
            if value.get("class") is None
        ]

        invalid_class_keys = {
            key for key, value in imported_nodes.items()
            if value.get("class") not in global_nodes_list
        }

        if null_class_keys:
            st.error("No class keys found in imported nodes.")
            st.error(
                f"Nodes missing class: {null_class_keys}. Fix and re-upload."
            )

        elif invalid_class_keys:
            st.error("**Invalid class keys** found in imported nodes.")
            st.error(
                f"Invalid classes: ***{invalid_class_keys}***. Please add the classes from following PPR conform semantics: **'Product'**, **'Process'** or **'Resource'**."
            )

        elif not imported_nodes:
            st.error("No Nodes found in imported model.")

        else:
            selected_view = viewpoints_menu.handle("Import Model")

            if selected_view == "PPR View":
                ppr_view.show(
                    nodes=imported_nodes,
                    links=imported_edges,
                    engineering_nodes=engineering_nodes,
                    engineering_edges=engineering_edges,
                    sustainability_nodes=sustainability_nodes,
                    sustainability_edges=sustainability_edges
                )

            elif selected_view == "Engineering View":
                additonal_views.show(
                    ppr_nodes=imported_nodes,
                    nodes=engineering_nodes,
                    links=engineering_edges,
                    selected_view=selected_view
                )

            elif selected_view == "Sustainability View":
                additonal_views.show(
                    ppr_nodes=imported_nodes,
                    nodes=sustainability_nodes,
                    links=sustainability_edges,
                    selected_view=selected_view
                )