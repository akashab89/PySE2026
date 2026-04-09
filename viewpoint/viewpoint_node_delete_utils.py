import streamlit as st


# ==========================================================
# DELETE A NODE FROM A VIEWPOINT
# Also removes all connected edges in that viewpoint
# ==========================================================
def delete_view_node_from_view(view_node_list, view_edge_list, config):
    if not view_node_list:
        st.warning(f"No {config['view_name']} nodes available to delete.")
        return view_node_list, view_edge_list

    view_key = config["view_key"]

    st.subheader("Delete Existing Node from Viewpoint")

    selected_node = st.selectbox(
        "Select Node",
        view_node_list,
        format_func=lambda x: f"{x['Name']} ({x['Class'].split('/')[-1]})",
        key=f"{view_key}_delete_node_select"
    )

    st.write("Selected node:", selected_node["Name"])

    if st.button(f"Delete Node from {config['view_name']}", key=f"{view_key}_delete_node_button"):
        delete_id = selected_node["ID"]

        updated_view_node_list = [
            item for item in view_node_list
            if item["ID"] != delete_id
        ]

        updated_view_edge_list = [
            edge for edge in view_edge_list
            if edge.get("source_id") != delete_id and edge.get("target_id") != delete_id
        ]

        st.success(f"Deleted '{selected_node['Name']}' from {config['view_name']}.")
        return updated_view_node_list, updated_view_edge_list

    return view_node_list, view_edge_list