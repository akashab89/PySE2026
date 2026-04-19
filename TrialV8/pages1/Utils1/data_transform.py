from collections import defaultdict

def nodes_by_class(nodes_dict:dict):
    grouped_nodes = defaultdict(list)
    for node in nodes_dict.values():
        node_class = node.get("class", "Undefined")
        node_name = node.get("name")
        if node_class and node_name:
            grouped_nodes[node_class].append(node_name)
    return dict(grouped_nodes)

def edges_by_type(edges_list: list):
    grouped_edges = defaultdict(list)

    for edge in edges_list:
        edge_type = edge.get("type", "Undefined")
        edge_name = edge.get("name")

        if edge_type and edge_name:
            grouped_edges[edge_type].append(edge_name)

    return dict(grouped_edges)

# --- Helper: extract numeric value from "12.5 kg" ---
def extract_numeric(value_str):
    try:
        return float(value_str.split()[0])
    except:
        return 0.0

def are_attributes_same(existing_attrs: dict, selected_attrs: list, tol: float = 1e-6) -> bool:
    """
    Compare existing node attributes with newly selected attributes.

    Args:
        existing_attrs (dict): {"attr_name": numeric_value}
        selected_attrs (list): [{"attr_name": ..., "value": "10 kg"}]
        tol (float): tolerance for float comparison

    Returns:
        bool: True if attributes are the same, False otherwise
    """
    # Convert selected attrs → numeric dict
    new_attrs = {}
    for attr in selected_attrs:
        attr_name = attr.get("attr_name")
        value_str = attr.get("value", "0")
        new_attrs[attr_name] = extract_numeric(value_str)

    # Compare keys first
    if existing_attrs.keys() != new_attrs.keys():
        return False

    # Compare values with tolerance
    for key in existing_attrs:
        if abs(existing_attrs[key] - new_attrs[key]) > tol:
            return False

    return True

def remove_links_of_node(links: list, node_to_remove: str):
    for i in range(len(links)-1, -1, -1):
        if links[i]["source"] == node_to_remove or links[i]["target"] == node_to_remove:
            del links[i]  # Remove the link from the links list