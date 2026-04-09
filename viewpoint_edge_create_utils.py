import uuid
import streamlit as st


# ==========================================================
# GET DEFAULT EDGE LABEL BASED ON SOURCE/TARGET CLASS PAIR
# ==========================================================
def get_view_default_edge_label(source_class, target_class, config):
    return config["edge_label_map"].get((source_class, target_class), "relation")


# ==========================================================
# CREATE A NEW EDGE INSIDE A VIEWPOINT
# ==========================================================
def create_view_edge_form(view_node_list, view_edge_list, config):
    if not view_node_list:
        st.warning(f"No {config['view_name']} nodes available to connect.")
        return view_edge_list

    view_key = config["view_key"]

    st.subheader("Create New Edge")

    source_node = st.selectbox(
        "Select Source Node",
        view_node_list,
        format_func=lambda x: f"{x['Name']} ({x['Class'].split('/')[-1]})",
        key=f"{view_key}_create_edge_source"
    )

    if source_node is None:
        return view_edge_list

    source_id = source_node["ID"]
    source_name = source_node["Name"]
    source_class = source_node["Class"]

    target_candidates = [
        item for item in view_node_list
        if item["ID"] != source_id and item.get("Class") in [
            "SystemUnitClassLib/Product",
            "SystemUnitClassLib/Process",
            "SystemUnitClassLib/Resource"
        ]
    ]

    if not target_candidates:
        st.warning("No valid target nodes available for the selected source node.")
        return view_edge_list

    target_node = st.selectbox(
        "Select Target Node",
        target_candidates,
        format_func=lambda x: f"{x['Name']} ({x['Class'].split('/')[-1]})",
        key=f"{view_key}_create_edge_target"
    )

    target_id = target_node["ID"]
    target_name = target_node["Name"]
    target_class = target_node["Class"]

    default_edge_name = get_view_default_edge_label(source_class, target_class, config)
    edge_pair_key = f"{source_id}->{target_id}"

    if st.session_state.get(f"{view_key}_last_edge_pair") != edge_pair_key:
        st.session_state[f"{view_key}_create_edge_name"] = default_edge_name
        st.session_state[f"{view_key}_last_edge_pair"] = edge_pair_key

    edge_name = st.text_input(
        "Edge Label",
        key=f"{view_key}_create_edge_name"
    )

    st.caption(f"Default relation: {default_edge_name}")

    duplicate_exists = any(
        edge.get("source_id") == source_id and edge.get("target_id") == target_id
        for edge in view_edge_list
    )

    if duplicate_exists:
        st.info("This edge already exists.")

    if st.button("Create Edge", key=f"{view_key}_create_edge_button"):
        if duplicate_exists:
            st.error("This edge already exists.")
            return view_edge_list

        final_edge_name = edge_name.strip() if edge_name.strip() else default_edge_name

        new_edge = {
            "id": str(uuid.uuid4()),
            "name": final_edge_name,
            "source_id": source_id,
            "target_id": target_id
        }

        updated_view_edge_list = view_edge_list + [new_edge]

        st.success(f"Edge created: {source_name} -> {target_name} [{final_edge_name}]")
        st.session_state[f"{view_key}_last_edge_pair"] = None

        return updated_view_edge_list

    return view_edge_list