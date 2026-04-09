import uuid
import streamlit as st


def create_new_edge_form(element_list, edge_list):
    if not element_list:
        st.warning("No nodes available to connect.")
        return edge_list

    st.subheader("Create New Edge")

    # ----------------------------------------------------------
    # SELECT SOURCE NODE
    # ----------------------------------------------------------
    source_node = st.selectbox(
        "Select Source Node",
        element_list,
        format_func=lambda x: x["Name"],
        key="create_edge_source"
    )

    if source_node is None:
        return edge_list

    source_id = source_node["ID"]
    source_name = source_node["Name"]
    source_class = source_node["Class"]

    # ----------------------------------------------------------
    # FILTER TARGET NODES BASED ON SOURCE CLASS
    # 1. Product  -> Process
    # 2. Process  -> Product, Resource
    # 3. Resource -> Child Resource if present
    # ----------------------------------------------------------
    if source_class == "SystemUnitClassLib/Product":
        target_candidates = [
            item for item in element_list
            if item["ID"] != source_id and item.get("Class") == "SystemUnitClassLib/Process"
        ]

    elif source_class == "SystemUnitClassLib/Process":
        target_candidates = [
            item for item in element_list
            if item["ID"] != source_id and item.get("Class") in [
                "SystemUnitClassLib/Product",
                "SystemUnitClassLib/Resource"
            ]
        ]

    elif source_class == "SystemUnitClassLib/Resource":
        target_candidates = [
            item for item in element_list
            if item["ID"] != source_id
            and item.get("Class") == "SystemUnitClassLib/Resource"
            and item.get("ParentID") == source_id
        ]

    else:
        target_candidates = []

    if not target_candidates:
        st.warning("No valid target nodes available for the selected source node.")
        return edge_list

    # ----------------------------------------------------------
    # SELECT TARGET NODE
    # ----------------------------------------------------------
    target_node = st.selectbox(
        "Select Target Node",
        target_candidates,
        format_func=lambda x: x["Name"],
        key="create_edge_target"
    )

    target_id = target_node["ID"]
    target_name = target_node["Name"]

    # ----------------------------------------------------------
    # EDGE NAME
    # ----------------------------------------------------------
    default_edge_name = f"PPR View_{source_name}_to_{target_name}"
    edge_pair_key = f"{source_id}->{target_id}"

    if st.session_state.get("last_edge_pair") != edge_pair_key:
        st.session_state["create_edge_name"] = default_edge_name
        st.session_state["last_edge_pair"] = edge_pair_key

    edge_name = st.text_input(
        "Edge Name",
        key="create_edge_name"
    )

    # ----------------------------------------------------------
    # VALIDATION HELP
    # ----------------------------------------------------------
    duplicate_exists = any(
        edge.get("source_id") == source_id and edge.get("target_id") == target_id
        for edge in edge_list
    )

    if duplicate_exists:
        st.info("This edge already exists.")

    # ----------------------------------------------------------
    # CREATE BUTTON
    # ----------------------------------------------------------
    if st.button("Create Edge", key="create_edge_button"):
        if duplicate_exists:
            st.error("This edge already exists.")
            return edge_list

        new_edge = {
            "id": str(uuid.uuid4()),
            "name": edge_name.strip() if edge_name.strip() else default_edge_name,
            "source_id": source_id,
            "target_id": target_id
        }

        updated_edge_list = edge_list + [new_edge]

        st.success(f"Edge created: {source_name} -> {target_name}")
        return updated_edge_list

    return edge_list