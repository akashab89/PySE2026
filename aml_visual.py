import streamlit as st
import networkx as nx
import pandas as pd
from yfiles_graphs_for_streamlit import StreamlitGraphWidget, Layout
import xml.etree.ElementTree as ET
from aml_visual_utils import nx_to_yfiles_graph, class_to_shape

#HEADER
st.set_page_config(page_title="AML Visualisation", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")
st.title("🤖 AML Visualisation in Python")
st.subheader("AML Visualisation in Python using yFiles")
st.write("Version 1: Reading data, visualising")

#UPLOADING THE FILE
with st.sidebar:
    st.header("Input Settings")
    uploaded_file = st.file_uploader("Upload Process File", type=["aml", "xml"], accept_multiple_files=False)

if uploaded_file:
    st.success("Successfully uploaded the file.")
    st.write(uploaded_file)
    with st.expander("Uploaded Process File"):
        st.write(uploaded_file.getvalue())
    st.subheader("AML Integration")

    # PARSING THE FILE
    try:
        tree = ET.parse(uploaded_file)
        root = tree.getroot()

        st.success("File parsed successfully.")
        st.write("Root tag:", root.tag)

    except Exception as e:
        st.error(f"Error while parsing AML: {e}")
        with st.expander("Full error"):
            st.write(f"Error while parsing AML: {e}")

    # CLEARING THE NAMESPACE
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

        # GETTING ELEMENTS
        element_list = []
        for ie in ih.findall(".//aml:InternalElement", ns_dict):
            # st.write(ie)
            ie_name = ie.get("Name")
            ie_id = ie.get("ID")
            ie_class = ie.get("RefBaseSystemUnitPath")
            element_list.append({"Name": ie_name, "ID": ie_id, "Class": ie_class})

        with st.expander("Internal Elements List"):
            st.write(element_list)

        # GETTING LINKS
        link_list = []
        for ie in ih.findall(".//aml:InternalElement", ns_dict):
            for il in ie.findall("aml:InternalLink", ns_dict):
                il_name = il.get("Name")
                il_source = il.get("RefPartnerSideA")
                il_target = il.get("RefPartnerSideB")
                link_list.append({"Name": il_name, "Source": il_source, "Target": il_target})

        with st.expander("InternalLinks"):
            st.write(link_list)

        # SEGREGATING INTERNAL LINKS - PPR, ENGG, SUST
        ppr_link_list = []
        for item in link_list:
            if "PPR View" in item["Name"]:
                ppr_link_list.append(item)
        with st.expander("PPR Links"):
            st.write("PPR Links:", ppr_link_list)

        engg_link_list = []
        for item in link_list:
            if "Engineering View" in item["Name"]:
                engg_link_list.append(item)
        with st.expander("Engineering Links"):
            st.write("Engineering Links:", engg_link_list)

        sust_link_list = []
        for item in link_list:
            if "Sustainability View" in item["Name"]:
                sust_link_list.append(item)
        with st.expander("Sustainability Links"):
            st.write("Sustainability Links:", sust_link_list)

        # MAPPING EXTERNAL INTERFACE ID TO ELEMENT
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

        #PPR GRAPH
        with tab1:
            st.subheader("PPR Visualisation:")

            # CREATE GRAPH
            G = nx.DiGraph()

            # CREATE NX NODES
            for ie in element_list:
                G.add_node(ie["ID"], name=ie["Name"], suc=ie["Class"])

            # CREATE NX EDGES
            for il in ppr_link_list:
                actual_source = ei_mapping_dict[il["Source"]]
                actual_target = ei_mapping_dict[il["Target"]]
                G.add_edge(actual_source, actual_target, label=il["Name"])

            nodes, edges = nx_to_yfiles_graph(G)

            graph = StreamlitGraphWidget(nodes=nodes, edges=edges, directed_mapping= "True", node_styles_mapping=class_to_shape)
            graph.show(graph_layout=Layout.HIERARCHIC)

        with tab2:
            st.subheader("Basic Engineering Visualisation:")

            # CREATE GRAPH
            G = nx.DiGraph()

            # CREATE NX NODES
            for ie in element_list:
                G.add_node(ie["ID"], name=ie["Name"], suc=ie["Class"])

            # CREATE NX EDGES
            for il in engg_link_list:
                actual_source = ei_mapping_dict[il["Source"]]
                actual_target = ei_mapping_dict[il["Target"]]
                G.add_edge(actual_source, actual_target, label=il["Name"])

            nodes, edges = nx_to_yfiles_graph(G)

            graph = StreamlitGraphWidget(nodes=nodes, edges=edges, directed_mapping= "True", node_styles_mapping=class_to_shape)
            graph.show(graph_layout=Layout.HIERARCHIC)

        with tab3:
            st.subheader("Basic Engineering Visualisation:")

            # CREATE GRAPH
            G = nx.DiGraph()

            # CREATE NX NODES
            for ie in element_list:
                G.add_node(ie["ID"], name=ie["Name"], suc=ie["Class"])

            # CREATE NX EDGES
            for il in sust_link_list:
                actual_source = ei_mapping_dict[il["Source"]]
                actual_target = ei_mapping_dict[il["Target"]]
                G.add_edge(actual_source, actual_target, label=il["Name"])

            nodes, edges = nx_to_yfiles_graph(G)

            graph = StreamlitGraphWidget(nodes=nodes, edges=edges, directed_mapping= "True", node_styles_mapping=class_to_shape)
            graph.show(graph_layout=Layout.HIERARCHIC)