import streamlit as st
import networkx as nx
from yfiles_graphs_for_streamlit import StreamlitGraphWidget, Layout
import xml.etree.ElementTree as ET
from aml_visual_utils_v2 import nx_to_yfiles_graph, class_to_shape
from node_create_utils import create_new_node_form, append_new_node
from node_update_utils import view_update_node
from node_delete_utils import delete_node

# HEADER / PAGE CONFIGURATION
st.set_page_config(
    page_title="AML Visualisation",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🤖 AML Visualisation in Python")
st.subheader("AML Visualisation in Python using yFiles")
st.write("Version 1: Reading data, visualising")

# FILE UPLOAD IN SIDEBAR
with st.sidebar:
    st.header("Input Settings")
    uploaded_file = st.file_uploader(
        "Upload Process File",
        type=["aml"],
        accept_multiple_files=False
    )

# MAIN AML PROCESSING BLOCK
if uploaded_file:
    st.success("Successfully uploaded the file.")
    st.write(uploaded_file)

    with st.expander("Uploaded Process File"):
        st.write(uploaded_file.getvalue())

    st.subheader("AML Integration")

    # PARSE THE AML FILE
    try:
        tree = ET.parse(uploaded_file)
        root = tree.getroot()

        st.success("File parsed successfully.")
        st.write("Root tag:", root.tag)

    except Exception as e:
        st.error(f"Error while parsing AML: {e}")
        with st.expander("Full error"):
            st.write(f"Error while parsing AML: {e}")
        st.stop()

    # EXTRACT NAMESPACE AND FIND INSTANCE HIERARCHY
    if "{" in root.tag:
        ns = root.tag.split("}")[0].strip("{")
        actual_tag = root.tag.split("}")[1]
        st.write("Root tag:", actual_tag)

        ns_dict = {"aml": ns}
        ih = root.find(".//aml:InstanceHierarchy", ns_dict)
        st.write("Instance hierarchy:", ih)

        if ih is None:
            st.error("No InstanceHierarchy found in the AML file.")
            st.stop()

        # RECURSIVE FUNCTION TO EXTRACT INTERNAL ELEMENT
        element_list = []

        def extract_internal_elements(elem, parent_id=None):
            ie_name = elem.get("Name")
            ie_id = elem.get("ID")
            ie_class = elem.get("RefBaseSystemUnitPath")

            # Read all direct AML attributes of this element
            attribute_list = []
            for attr in elem.findall("aml:Attribute", ns_dict):
                attr_name = attr.get("Name")
                value_elem = attr.find("aml:Value", ns_dict)
                attr_value = value_elem.text.strip() if value_elem is not None and value_elem.text else None

                attribute_list.append({
                    "attr_name": attr_name,
                    "value": attr_value
                })

            # Store current element
            element_list.append({
                "Name": ie_name,
                "ID": ie_id,
                "Class": ie_class,
                "ParentID": parent_id,
                "Attributes": attribute_list
            })

            # Recurse into child InternalElements
            for child in elem.findall("aml:InternalElement", ns_dict):
                extract_internal_elements(child, ie_id)

        # Start extraction from top-level InternalElements
        for ie in ih.findall("aml:InternalElement", ns_dict):
            extract_internal_elements(ie, parent_id=None)

        with st.expander("Internal Elements List"):
            st.write(element_list)

        # GET INTERNAL LINKS
        link_list = []
        for ie in ih.findall(".//aml:InternalElement", ns_dict):
            for il in ie.findall("aml:InternalLink", ns_dict):
                il_name = il.get("Name")
                il_source = il.get("RefPartnerSideA")
                il_target = il.get("RefPartnerSideB")
                link_list.append({
                    "Name": il_name,
                    "Source": il_source,
                    "Target": il_target
                })

        with st.expander("InternalLinks"):
            st.write(link_list)

        # MAP EXTERNAL INTERFACE ID -> OWNER INTERNAL ELEMENT ID
        ei_mapping_dict = {}
        for ie in ih.findall(".//aml:InternalElement", ns_dict):
            ie_id = ie.get("ID")
            for external_interface in ie.findall("aml:ExternalInterface", ns_dict):
                ei_id = external_interface.get("ID")
                ei_mapping_dict[ei_id] = ie_id

        with st.expander("ExternalInterface Owner mapping"):
            st.write(ei_mapping_dict)

        # TAB CREATION
        tab1, tab2, tab3 = st.tabs(["PPR View", "Basic Engineering View", "Sustainability View"])

        # PPR GRAPH
        with tab1:
            col1, col2 = st.columns([1,3])
            with col1:
                st.subheader("PPR Editor")

                #NODE EDIT
                if "element_list" not in st.session_state or st.session_state.element_list is None:
                    st.session_state.element_list = element_list.copy()

                s_op = st.selectbox("Select Operation", ("Create new node", "Update existing node", "Delete existing node"))
                st.divider()
                #CREATE NEW NODE
                if s_op == "Create new node":
                    new_node = create_new_node_form(st.session_state.element_list)
                    if new_node:
                        st.session_state.element_list = append_new_node(
                            st.session_state.element_list,
                            new_node
                        )
                        st.success("New node created successfully.")
                        st.write(new_node)
                #UPDATE EXISTING NODE
                if s_op == "Update existing node":
                    updated_list = view_update_node(st.session_state.element_list)
                    if updated_list is not None:
                        st.session_state.element_list = updated_list

                #DELETE EXISTING NODE
                if s_op == "Delete existing node":
                    updated_list = delete_node(st.session_state.element_list)
                    if updated_list is not None:
                        st.session_state.element_list = updated_list

            with col2:
                st.subheader("PPR Visualisation:")

                # CREATE GRAPH
                G = nx.DiGraph()

                # CREATE NX NODES
                for ie in st.session_state.element_list:
                    G.add_node(
                        ie["ID"],
                        name=ie["Name"],
                        suc=ie["Class"],
                        parent_id=ie["ParentID"],
                        attributes=ie["Attributes"]
                    )

                # CREATE NX EDGES ONLY FOR NODES STILL PRESENT
                remaining_node_ids = {item["ID"] for item in st.session_state.element_list}

                for il in link_list:
                    actual_source = ei_mapping_dict.get(il["Source"])
                    actual_target = ei_mapping_dict.get(il["Target"])

                    if actual_source in remaining_node_ids and actual_target in remaining_node_ids:
                        G.add_edge(actual_source, actual_target, label=il["Name"])

                # CONVERT NETWORKX GRAPH TO YFILES FORMAT
                nodes, edges = nx_to_yfiles_graph(G)

                # CREATE YFILES GRAPH WIDGET
                graph = StreamlitGraphWidget(
                    nodes=nodes,
                    edges=edges,
                    directed_mapping="True",
                    node_styles_mapping=class_to_shape
                )

                # CHANGE NODE SIZE BASED ON PARENT-CHILD RELATION
                # parent node = larger box
                # child node = smaller box
                graph.node_size_mapping = lambda node: (
                    (130, 60) if node.get("properties", {}).get("is_parent") else
                    (95, 42) if node.get("properties", {}).get("is_child") else
                    (110, 50)
                )

                graph.show(graph_layout=Layout.HIERARCHIC)

        # BASIC ENGINEERING GRAPH
        with tab2:
            st.subheader("Basic Engineering Visualisation:")


        # SUSTAINABILITY GRAPH
        with tab3:
            st.subheader("Sustainability Visualisation:")
