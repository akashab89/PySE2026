import streamlit as st
from yfiles_graphs_for_streamlit import StreamlitGraphWidget, Node, Edge, Layout, NodeStyle, NodeShape
import networkx as nx


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


def nx_to_yfiles_graph(nx_graph,node_cardinality_mapping=None):
    nodes = []
    edges = []

    # ---- Nodes ----
    for node_id, attrs in nx_graph.nodes(data=True):
        parent = attrs.get("parent", None)
        attributes = attrs.get("attributes", [])
        base_label= attrs.get("name",str(node_id))

        #Append cardinality to label if exists
        card= node_cardinality_mapping.get(node_id)
        label=f"{base_label}\n({card}x)" if card else base_label
        # Start with parent
        properties = {
            "parent": parent,
            "class": attrs.get("node_class",""),
            "label": label
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

        edges.append({
            "id": f"{source}-{target}",
            "start": str(source),
            "end": str(target),
            "cardinality": cardinality
        })

    return nodes, edges

def class_to_shape(node):
    props = node.get("properties", {})
    node_class = props.get("class", "")

    if node_class == "SystemUnitClassLib/Process":
        return NodeStyle(shape=NodeShape.RECTANGLE)

    elif node_class == "SystemUnitClassLib/Product":
        return NodeStyle(shape=NodeShape.ELLIPSE,color="red")

    elif node_class == "SystemUnitClassLib/Resource":
        return NodeStyle(shape=NodeShape.ROUND_RECTANGLE,color="green")

    else:
        return NodeStyle(shape=NodeShape.HEXAGON)



