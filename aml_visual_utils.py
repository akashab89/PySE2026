import networkx as nx
import yfiles_graphs_for_streamlit
import streamlit as st
from openpyxl.styles.colors import BLUE
from pygments.styles.paraiso_dark import RED, GREEN
from yfiles_graphs_for_streamlit import NodeStyle, NodeShape


def nx_to_yfiles_graph(nx_graph):
    nodes = []
    edges = []

    for node_id, attrs in nx_graph.nodes(data=True):
        node_label = attrs.get("name", str(node_id))
        node_class = attrs.get("suc", "")

        nodes.append({
            "id": str(node_id),
            "properties": {
                "label": node_label,
                "Class": node_class
            }
        })

    for source, target, attrs in nx_graph.edges(data=True):

        edges.append({
            "id": f"{source}-{target}",
            "start": str(source),
            "end": str(target)
        })

    return nodes, edges

def class_to_shape(node):
    props = node.get("properties", {})
    node_class = props.get("Class", "")

    if node_class == "SystemUnitClassLib/Process":
        return NodeStyle(shape=NodeShape.RECTANGLE)

    elif node_class == "SystemUnitClassLib/Product":
        return NodeStyle(shape=NodeShape.ELLIPSE, color=RED)

    elif node_class == "SystemUnitClassLib/Resource":
        return NodeStyle(shape=NodeShape.ROUND_RECTANGLE, color=GREEN)

    else:
        return NodeStyle(shape=NodeShape.HEXAGON)