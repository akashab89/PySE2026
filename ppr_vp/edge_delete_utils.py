import streamlit as st

def delete_edge(element_list, edge_list):
    if not element_list:
        st.warning("No nodes available.")
        return edge_list

    if not edge_list:
        st.warning("No edges available to delete.")
        return edge_list

    st.subheader("Delete Existing Edge")

    # ----------------------------------------------------------
    # BUILD LOOKUP: node_id -> node dict
    # ----------------------------------------------------------
    node_lookup = {item["ID"]: item for item in element_list}

    # ----------------------------------------------------------
    # SOURCE NODES = only nodes that currently have outgoing edges
    # ----------------------------------------------------------
    source_ids_with_edges = []
    seen = set()

    for edge in edge_list:
        source_id = edge.get("source_id")
        if source_id in node_lookup and source_id not in seen:
            source_ids_with_edges.append(source_id)
            seen.add(source_id)

    if not source_ids_with_edges:
        st.warning("No source nodes with edges found.")
        return edge_list

    source_nodes = [node_lookup[source_id] for source_id in source_ids_with_edges]

    # ----------------------------------------------------------
    # SELECT SOURCE NODE
    # ----------------------------------------------------------
    source_node = st.selectbox(
        "Select Source Node",
        source_nodes,
        format_func=lambda x: x["Name"],
        key="delete_edge_source"
    )

    if source_node is None:
        return edge_list

    source_id = source_node["ID"]

    # ----------------------------------------------------------
    # TARGET NODES = only targets connected from selected source
    # ----------------------------------------------------------
    outgoing_edges = [
        edge for edge in edge_list
        if edge.get("source_id") == source_id
    ]

    if not outgoing_edges:
        st.warning("No outgoing edges found for the selected source node.")
        return edge_list

    target_ids = []
    seen_targets = set()

    for edge in outgoing_edges:
        target_id = edge.get("target_id")
        if target_id in node_lookup and target_id not in seen_targets:
            target_ids.append(target_id)
            seen_targets.add(target_id)

    target_nodes = [node_lookup[target_id] for target_id in target_ids]

    # ----------------------------------------------------------
    # SELECT TARGET NODE
    # ----------------------------------------------------------
    target_node = st.selectbox(
        "Select Target Node",
        target_nodes,
        format_func=lambda x: x["Name"],
        key="delete_edge_target"
    )

    if target_node is None:
        return edge_list

    target_id = target_node["ID"]

    # ----------------------------------------------------------
    # FIND MATCHING EDGES FOR SOURCE -> TARGET
    # ----------------------------------------------------------
    matching_edges = [
        edge for edge in edge_list
        if edge.get("source_id") == source_id and edge.get("target_id") == target_id
    ]

    if not matching_edges:
        st.warning("No edge found for the selected source-target pair.")
        return edge_list

    # If there are multiple edges between same source and target,
    # let user choose the exact one by name.
    if len(matching_edges) == 1:
        selected_edge = matching_edges[0]
        st.write("Selected Edge:", selected_edge.get("name", "Unnamed Edge"))
    else:
        selected_edge = st.selectbox(
            "Select Edge",
            matching_edges,
            format_func=lambda x: x.get("name", "Unnamed Edge"),
            key="delete_edge_name"
        )

    # ----------------------------------------------------------
    # DELETE BUTTON
    # ----------------------------------------------------------
    if st.button("Delete Edge", key="delete_edge_button"):
        selected_edge_id = selected_edge.get("id")

        updated_edge_list = [
            edge for edge in edge_list
            if edge.get("id") != selected_edge_id
        ]

        st.success(
            f"Deleted edge: {source_node['Name']} -> {target_node['Name']}"
        )
        return updated_edge_list

    return edge_list