import streamlit as st
from yfiles_graphs_for_streamlit import StreamlitGraphWidget, Node, Edge, Layout, NodeStyle, NodeShape, LabelPosition
import networkx as nx

#NX GRAPH RELATED UTILS

def nx_Digraph(nodes_dict: dict, link_list: list)-> nx.DiGraph:
    G=nx.DiGraph()
    for node in nodes_dict.values():
        G.add_node(
            node["name"], 
            name=node["name"],
            node_class=node["class"],  # Renamed 'class' to 'node_class' to avoid Python errors
            xml=node.get("xml", None),  # Optional: Store the original XML element if needed
            port_id=node.get("port_id", None),
            parent=node.get("parent", None),
            attributes=node.get("attributes", [])
        )

    for il in link_list:
        actual_source= il["source"]
        actual_target=il["target"]

        G.add_edge(actual_source, actual_target,label=il["type"],cardinal=il.get("cardinality", None))
    return G





# UTILS FOR RENDERING GRAPHS AND INTERACTING WITH THEM IN STREAMLIT using yfiles_graphs_for_streamlit

# def node_cardinality_mapping(G: nx.DiGraph) -> dict:
#     mapping = {}
#     for u, v, data in G.edges(data=True):
#         card = data.get("cardinal", "")
#         if not card:
#             continue
#
#         try:
#             mapping[u] = int(card)
#         except (ValueError, TypeError):
#             pass
#     return mapping

def class_to_shape(node):
    props = node.get("properties", {})
    node_class = props.get("class", "")

    if node_class == "Process":
        return NodeStyle(shape=NodeShape.RECTANGLE)

    elif node_class == "Product":
        return NodeStyle(shape=NodeShape.ELLIPSE,color="red")

    elif node_class == "Resource":
        return NodeStyle(shape=NodeShape.ROUND_RECTANGLE,color="green")

    else:
        return NodeStyle(shape=NodeShape.HEXAGON)

def show_yfiles_graph(nodes1, edges1):
    graph = StreamlitGraphWidget()
    graph = StreamlitGraphWidget(nodes=nodes1, edges=edges1, directed_mapping= "True", 
                                 edge_label_mapping=lambda edge: (edge["properties"]["label"] if edge["properties"]["label"] !="PPR_port" else ""
                                 ),
                                 node_styles_mapping=class_to_shape)
    graph.node_size_mapping = lambda node: (
        (90, 40) if node.get("properties", {}).get("parent") is not None else (120, 60)
    )
    graph.show(graph_layout=Layout.HIERARCHIC)


# def nx_to_yfiles_graph(nx_graph,node_cardinality_mapping=None):
#     nodes = []
#     edges = []
#
#     # ---- Nodes ----
#     for node_id, attrs in nx_graph.nodes(data=True):
#         parent = attrs.get("parent", None)
#         attributes = attrs.get("attributes", [])
#         base_label= attrs.get("name",str(node_id))
#
#         #Append cardinality to label if exists
#         card= node_cardinality_mapping.get(node_id) if node_cardinality_mapping else None
#         label=f"{base_label}\n({card}x)" if card else base_label
#         # Start with parent
#         properties = {
#             "parent": parent,
#             "class": attrs.get("node_class",""),
#             "label": label
#         }
#
#         # Flatten attributes list into properties
#         for attr in attributes:
#             attr_name = attr.get("attr_name")
#             value = attr.get("value")
#
#             if attr_name:
#                 properties[attr_name] = value
#
#         nodes.append({
#             "id": str(node_id),
#             "properties": properties
#         })
#     # ---- Edges ----
#     for source, target, attrs in nx_graph.edges(data=True):
#         cardinality = attrs.get("cardinal", None)
#
#         edges.append({
#             "id": f"{source}-{target}",
#             "start": str(source),
#             "end": str(target),
#             "cardinality": cardinality,
#             "properties": {"label": attrs.get("label", "")}
#         })
#
#     return nodes, edges

def nx_to_yfiles_graph(nx_graph):
    nodes = []
    edges = []

    # ---- Nodes ----
    for node_id, attrs in nx_graph.nodes(data=True):
        parent = attrs.get("parent", None)
        attributes = attrs.get("attributes", [])
        base_label = attrs.get("name", str(node_id))

        # NO cardinality in nodes anymore
        properties = {
            "parent": parent,
            "class": attrs.get("node_class", ""),
            "label": base_label
        }

        # Flatten attributes list into properties
        for attr in attributes:
            attr_name = attr.get("attr_name")
            value = attr.get("value")

            if attr_name:
                properties[attr_name] = value

        nodes.append({
            "id": str(node_id),
            "properties": properties
        })

    # ---- Edges ----
    for source, target, attrs in nx_graph.edges(data=True):
        cardinality = attrs.get("cardinal", None)
        label = attrs.get("label", "")

        if label == "PPR_port":
            label = ""

        if cardinality is not None:
            label = f"{cardinality}" if not label else f"{label} ({cardinality})"

        edges.append({
            "id": f"{source}-{target}",
            "start": str(source),
            "end": str(target),
            "properties": {"label": label}
        })

    return nodes, edges

def render_ppr_graph(edge_label: str):
    """
    Renders a simple two-node graph with a custom edge label.
    """
    # 1. Create two basic nodes
    nodes = [
        Node("n1", {"label": "Start"}),
        Node("n2", {"label": "End"})
    ]

    # 2. Create the edge using the provided label
    edges = [
        Edge("n1", "n2", properties={"text": edge_label})
    ]

    # 3. Build and display the widget
    # We use a lambda to map the 'text' property to the edge label
    return StreamlitGraphWidget(
        nodes=nodes,
        edges=edges,
        node_label_mapping="label",
        edge_label_mapping=lambda edge: edge["properties"]["text"]
    ).show(graph_layout=Layout.HIERARCHIC)

def ppr_req_check(nodes2, edges2):
    StreamlitGraphWidget(
        # pass node and edge dicts
        nodes=nodes2,
        edges=edges2,
        node_size_mapping=lambda node: (
            (90, 40) if node.get("properties", {}).get("parent") is not None else (120, 60)),
        node_styles_mapping=req_group_style,
        # provide a mapping along which the nodes should be grouped
        node_parent_group_mapping="class",
        edge_label_mapping=lambda edge: (
            edge["properties"]["label"] if edge["properties"]["label"] != "PPR_port"
            else ""
        ),
    ).show(graph_layout=Layout.HIERARCHIC)

def req_group_style(node):
    props = node.get("properties", {})
    node_class = props.get("class", "")
    label = props.get("label", "")

    # GROUP NODES CREATED FROM node_parent_group_mapping="class"
    if label == "Product":
        return NodeStyle(shape=NodeShape.ROUND_RECTANGLE, color="#d62728")   # red
    elif label == "Process":
        return NodeStyle(shape=NodeShape.ROUND_RECTANGLE, color="#17becf")   # cyan
    elif label == "Resource":
        return NodeStyle(shape=NodeShape.ROUND_RECTANGLE, color="#2ca02c")

    # NORMAL NODES
    if node_class == "Process":
        return NodeStyle(shape=NodeShape.RECTANGLE, color="#17becf")
    elif node_class == "Product":
        return NodeStyle(shape=NodeShape.ELLIPSE, color="#ff0000")
    elif node_class == "Resource":
        return NodeStyle(shape=NodeShape.ROUND_RECTANGLE, color="#008000")
    else:
        return NodeStyle(shape=NodeShape.HEXAGON)