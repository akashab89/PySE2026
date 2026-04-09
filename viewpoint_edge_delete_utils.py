import streamlit as st


# ==========================================================
# DELETE AN EDGE INSIDE A VIEWPOINT
# ==========================================================
def delete_view_edge(view_node_list, view_edge_list, config):
    if not view_node_list:
        st.warning(f"No {config['view_name']} nodes available.")
        return view_edge_list

    if not view_edge_list:
        st.warning(f"No {config['view_name']} edges available to delete.")
        return view_edge_list

    view_key = config["view_key"]

    st.subheader("Delete Existing Edge")

    node_lookup = {item["ID"]: item for item in view_node_list}

    source_ids_with_edges = []
    seen = set()

    for edge in view_edge_list:
        source_id = edge.get("source_id")
        if source_id in node_lookup and source_id not in seen:
            source_ids_with_edges.append(source_id)
            seen.add(source_id)

    if not source_ids_with_edges:
        st.warning("No source nodes with edges found.")
        return view_edge_list

    source_nodes = [node_lookup[source_id] for source_id in source_ids_with_edges]

    source_node = st.selectbox(
        "Select Source Node",
        source_nodes,
        format_func=lambda x: f"{x['Name']} ({x['Class'].split('/')[-1]})",
        key=f"{view_key}_delete_edge_source"
    )

    if source_node is None:
        return view_edge_list

    source_id = source_node["ID"]

    outgoing_edges = [
        edge for edge in view_edge_list
        if edge.get("source_id") == source_id
    ]

    if not outgoing_edges:
        st.warning("No outgoing edges found for the selected source node.")
        return view_edge_list

    target_ids = []
    seen_targets = set()

    for edge in outgoing_edges:
        target_id = edge.get("target_id")
        if target_id in node_lookup and target_id not in seen_targets:
            target_ids.append(target_id)
            seen_targets.add(target_id)

    target_nodes = [node_lookup[target_id] for target_id in target_ids]

    target_node = st.selectbox(
        "Select Target Node",
        target_nodes,
        format_func=lambda x: f"{x['Name']} ({x['Class'].split('/')[-1]})",
        key=f"{view_key}_delete_edge_target"
    )

    if target_node is None:
        return view_edge_list

    target_id = target_node["ID"]

    matching_edges = [
        edge for edge in view_edge_list
        if edge.get("source_id") == source_id and edge.get("target_id") == target_id
    ]

    if not matching_edges:
        st.warning("No edge found for the selected source-target pair.")
        return view_edge_list

    if len(matching_edges) == 1:
        selected_edge = matching_edges[0]
        st.write("Selected Edge:", selected_edge.get("name", "Unnamed Edge"))
    else:
        selected_edge = st.selectbox(
            "Select Edge",
            matching_edges,
            format_func=lambda x: x.get("name", "Unnamed Edge"),
            key=f"{view_key}_delete_edge_name"
        )

    if st.button("Delete Edge", key=f"{view_key}_delete_edge_button"):
        selected_edge_id = selected_edge.get("id")

        updated_view_edge_list = [
            edge for edge in view_edge_list
            if edge.get("id") != selected_edge_id
        ]

        st.success(
            f"Deleted edge: {source_node['Name']} -> {target_node['Name']}"
        )
        return updated_view_edge_list

    return view_edge_list