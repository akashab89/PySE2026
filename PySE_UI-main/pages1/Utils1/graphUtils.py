import streamlit as st
from yfiles_graphs_for_streamlit import StreamlitGraphWidget, Node, Edge, Layout


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