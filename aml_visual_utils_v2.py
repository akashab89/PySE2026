import networkx as nx
from yfiles_graphs_for_streamlit import NodeStyle, NodeShape

# CONVERT NETWORKX GRAPH TO YFILES NODE / EDGE FORMAT
# - adds Quantity in label like "Wheel (2X)"
# - adds flags for parent / child relation
def nx_to_yfiles_graph(nx_graph, show_edge_labels=False):
    nodes = []
    edges = []

    for node_id, attrs in nx_graph.nodes(data=True):
        # BASIC NODE DATA
        node_label = attrs.get("name", str(node_id))
        node_class = attrs.get("suc", "")
        node_parent_id = attrs.get("parent_id", None)
        node_attributes = attrs.get("attributes", [])

        # READ QUANTITY FROM AML ATTRIBUTES
        quantity = None
        for attr in node_attributes:
            attr_name = attr.get("attr_name")
            attr_value = attr.get("value")

            if attr_name and attr_name.strip().lower() == "quantity":
                quantity = attr_value
                break

        # APPEND QUANTITY TO NODE LABEL
        if quantity not in [None, ""]:
            try:
                quantity_num = float(quantity)
                if quantity_num > 1:
                    if quantity_num.is_integer():
                        node_label = f"{node_label} ({int(quantity_num)}X)"
                    else:
                        node_label = f"{node_label} ({quantity_num}X)"
            except (ValueError, TypeError):
                # if quantity is non-numeric, do not append anything
                pass

        # CHECK WHETHER NODE IS A PARENT OR A CHILD
        is_child = node_parent_id is not None
        is_parent = nx_graph.out_degree(node_id) > 0 or any(
            nx_graph.nodes[n].get("parent_id") == node_id for n in nx_graph.nodes()
        )

        # CREATE ONE SINGLE PROPERTIES DICTIONARY
        properties = {
            "label": node_label,
            "Class": node_class,
            "is_parent": is_parent,
            "is_child": is_child
        }

        # ADD ALL AML ATTRIBUTES SEPARATELY TO THE SIDEBAR
        for attr in node_attributes:
            attr_name = attr.get("attr_name")
            attr_value = attr.get("value")

            if attr_name:
                properties[attr_name] = attr_value

        # APPEND NODE ONLY ONCE
        nodes.append({
            "id": str(node_id),
            "properties": properties
        })

    # CONVERT NETWORKX EDGES TO YFILES EDGES
    for source, target, attrs in nx_graph.edges(data=True):
        edge_data = {
            "id": f"{source}-{target}",
            "start": str(source),
            "end": str(target)
        }

        if show_edge_labels:
            edge_label = attrs.get("label", "")
            edge_data["properties"] = {"label": edge_label}

        edges.append(edge_data)

    return nodes, edges

# MAP AML CLASS TO NODE SHAPE / COLOR
def class_to_shape(node):
    props = node.get("properties", {})
    node_class = props.get("Class", "")

    if node_class == "SystemUnitClassLib/Process":
        return NodeStyle(shape=NodeShape.RECTANGLE)

    elif node_class == "SystemUnitClassLib/Product":
        return NodeStyle(shape=NodeShape.ELLIPSE, color="red")

    elif node_class == "SystemUnitClassLib/Resource":
        return NodeStyle(shape=NodeShape.ROUND_RECTANGLE, color="green")

    else:
        return NodeStyle(shape=NodeShape.HEXAGON)