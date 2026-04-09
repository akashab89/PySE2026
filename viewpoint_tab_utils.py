import streamlit as st
import networkx as nx
from yfiles_graphs_for_streamlit import StreamlitGraphWidget, Layout

from viewpoint.viewpoint_node_add_utils import add_view_node_attribute
from viewpoint.viewpoint_node_update_utils import update_view_node_attribute
from viewpoint.viewpoint_node_delete_utils import delete_view_node_from_view
from viewpoint.viewpoint_edge_create_utils import create_view_edge_form
from viewpoint.viewpoint_edge_delete_utils import delete_view_edge


# ==========================================================
# INITIALIZE SESSION STATE FOR A VIEWPOINT
# Creates:
# - <view_key>_node_list
# - <view_key>_edge_list
# - <view_key>_class_custom_attrs
# ==========================================================
def initialize_viewpoint_state(config):
    view_key = config["view_key"]

    node_key = f"{view_key}_node_list"
    edge_key = f"{view_key}_edge_list"
    custom_attr_key = f"{view_key}_class_custom_attrs"

    if node_key not in st.session_state or st.session_state[node_key] is None:
        st.session_state[node_key] = []

    if edge_key not in st.session_state or st.session_state[edge_key] is None:
        st.session_state[edge_key] = []

    if custom_attr_key not in st.session_state or st.session_state[custom_attr_key] is None:
        st.session_state[custom_attr_key] = {
            "SystemUnitClassLib/Product": [],
            "SystemUnitClassLib/Process": [],
            "SystemUnitClassLib/Resource": []
        }


# ==========================================================
# RENDER EDITOR PANEL FOR A VIEWPOINT
# Handles:
# 1. Add node attributes
# 2. Update existing node attributes
# 3. Delete existing node from viewpoint
# 4. Create new edge
# 5. Delete existing edge
# ==========================================================
def render_viewpoint_editor(ppr_element_list, config):
    view_key = config["view_key"]
    view_name = config["view_name"]

    node_key = f"{view_key}_node_list"
    edge_key = f"{view_key}_edge_list"

    st.subheader(f"{view_name} Editor")

    initialize_viewpoint_state(config)

    selected_operation = st.selectbox(
        "Select Operation",
        (
            "Add node attributes",
            "Update existing node attributes",
            "Delete existing node from viewpoint",
            "Create new edge",
            "Delete existing edge"
        ),
        key=f"{view_key}_select_operation"
    )

    st.divider()

    # ------------------------------------------------------
    # 1. ADD NODE ATTRIBUTES
    # ------------------------------------------------------
    if selected_operation == "Add node attributes":
        updated_nodes = add_view_node_attribute(
            ppr_element_list,
            st.session_state[node_key],
            config
        )
        if updated_nodes is not None:
            st.session_state[node_key] = updated_nodes

    # ------------------------------------------------------
    # 2. UPDATE EXISTING NODE ATTRIBUTES
    # ------------------------------------------------------
    if selected_operation == "Update existing node attributes":
        updated_nodes = update_view_node_attribute(
            st.session_state[node_key],
            config
        )
        if updated_nodes is not None:
            st.session_state[node_key] = updated_nodes

    # ------------------------------------------------------
    # 3. DELETE EXISTING NODE FROM VIEWPOINT
    # ------------------------------------------------------
    if selected_operation == "Delete existing node from viewpoint":
        updated_nodes, updated_edges = delete_view_node_from_view(
            st.session_state[node_key],
            st.session_state[edge_key],
            config
        )
        if updated_nodes is not None:
            st.session_state[node_key] = updated_nodes
        if updated_edges is not None:
            st.session_state[edge_key] = updated_edges

    # ------------------------------------------------------
    # 4. CREATE NEW EDGE
    # ------------------------------------------------------
    if selected_operation == "Create new edge":
        updated_edges = create_view_edge_form(
            st.session_state[node_key],
            st.session_state[edge_key],
            config
        )
        if updated_edges is not None:
            st.session_state[edge_key] = updated_edges

    # ------------------------------------------------------
    # 5. DELETE EXISTING EDGE
    # ------------------------------------------------------
    if selected_operation == "Delete existing edge":
        updated_edges = delete_view_edge(
            st.session_state[node_key],
            st.session_state[edge_key],
            config
        )
        if updated_edges is not None:
            st.session_state[edge_key] = updated_edges


# ==========================================================
# BUILD NETWORKX GRAPH FOR A VIEWPOINT
# Uses:
# - viewpoint node list
# - viewpoint edge list
# ==========================================================
def build_viewpoint_graph(config):
    view_key = config["view_key"]

    node_key = f"{view_key}_node_list"
    edge_key = f"{view_key}_edge_list"

    G = nx.DiGraph()

    # ------------------------------------------------------
    # ADD NODES TO GRAPH
    # ------------------------------------------------------
    for node in st.session_state[node_key]:
        G.add_node(
            node["ID"],
            name=node["Name"],
            suc=node["Class"],
            parent_id=node["ParentID"],
            attributes=node["Attributes"]
        )

    # ------------------------------------------------------
    # ADD EDGES TO GRAPH
    # ------------------------------------------------------
    remaining_node_ids = {item["ID"] for item in st.session_state[node_key]}

    for edge in st.session_state[edge_key]:
        source_id = edge.get("source_id")
        target_id = edge.get("target_id")
        edge_name = edge.get("name", "")

        if source_id in remaining_node_ids and target_id in remaining_node_ids:
            G.add_edge(source_id, target_id, label=edge_name)

    return G


# ==========================================================
# RENDER GRAPH PANEL FOR A VIEWPOINT
# - converts NX graph to yFiles graph
# - shows edge labels
# ==========================================================
def render_viewpoint_graph(config, nx_to_yfiles_graph, class_to_shape):
    view_name = config["view_name"]

    st.subheader(f"{view_name} Visualisation:")

    G = build_viewpoint_graph(config)

    nodes, edges = nx_to_yfiles_graph(G, show_edge_labels=True)

    graph = StreamlitGraphWidget(
        nodes=nodes,
        edges=edges,
        directed_mapping="True",
        node_styles_mapping=class_to_shape
    )

    # ------------------------------------------------------
    # SHOW EDGE LABELS ONLY FOR NON-PPR VIEWS
    # ------------------------------------------------------
    graph.edge_label_mapping = lambda edge: edge.get("properties", {}).get("label", "")

    # ------------------------------------------------------
    # NODE SIZE BASED ON PARENT / CHILD RELATION
    # ------------------------------------------------------
    graph.node_size_mapping = lambda node: (
        (130, 60) if node.get("properties", {}).get("is_parent") else
        (95, 42) if node.get("properties", {}).get("is_child") else
        (110, 50)
    )

    graph.show(
        graph_layout=Layout.HIERARCHIC,
        key=f"{config['view_key']}_graph_component"
    )


# ==========================================================
# FULL VIEWPOINT TAB RENDERER
# Combines:
# - left editor panel
# - right graph panel
# ==========================================================
def render_viewpoint_tab(ppr_element_list, config, nx_to_yfiles_graph, class_to_shape):
    col1, col2 = st.columns([1, 3])

    with col1:
        render_viewpoint_editor(ppr_element_list, config)

    with col2:
        render_viewpoint_graph(config, nx_to_yfiles_graph, class_to_shape)