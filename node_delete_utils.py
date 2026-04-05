import streamlit as st

def delete_node(element_list):
    if not element_list:
        st.warning("No nodes available to delete.")
        return element_list

    # ----------------------------------------------------------
    # SELECT NODE TO DELETE
    # ----------------------------------------------------------
    name_list = [item["Name"] for item in element_list]
    s_node = st.selectbox("Select Node", name_list, key="delete_select_node")

    selected_element = next(item for item in element_list if item["Name"] == s_node)

    current_id = selected_element.get("ID")
    current_name = selected_element.get("Name", "")
    current_class = selected_element.get("Class", "")
    current_parent_id = selected_element.get("ParentID", None)
    current_attributes = selected_element.get("Attributes", [])

    # ----------------------------------------------------------
    # SHOW SELECTED NODE DETAILS
    # ----------------------------------------------------------
    st.write("### Selected Node Details")
    st.write({
        "Name": current_name,
        "Class": current_class,
        "ParentID": current_parent_id,
        "Attributes": current_attributes
    })

    # ----------------------------------------------------------
    # DELETE OPTIONS
    # ----------------------------------------------------------
    delete_children = st.checkbox(
        "Also delete child nodes of the selected node",
        value=False,
        key="delete_with_children"
    )

    confirm_delete = st.checkbox(
        f"Confirm deletion of '{current_name}'",
        value=False,
        key="delete_confirm_checkbox"
    )

    # ----------------------------------------------------------
    # DELETE BUTTON
    # ----------------------------------------------------------
    if st.button("Delete Node", key="delete_node_button"):
        if not confirm_delete:
            st.error("Please confirm deletion before proceeding.")
            return element_list

        if delete_children:
            # collect all descendants recursively
            ids_to_delete = {current_id}
            changed = True

            while changed:
                changed = False
                for item in element_list:
                    if item.get("ParentID") in ids_to_delete and item.get("ID") not in ids_to_delete:
                        ids_to_delete.add(item.get("ID"))
                        changed = True

            updated_element_list = [
                item for item in element_list
                if item.get("ID") not in ids_to_delete
            ]

            st.success(f"Node '{current_name}' and its child nodes were deleted successfully.")
            return updated_element_list

        else:
            # delete only selected node
            updated_element_list = [
                item for item in element_list
                if item.get("ID") != current_id
            ]

            # detach children of deleted node
            for item in updated_element_list:
                if item.get("ParentID") == current_id:
                    item["ParentID"] = None

            st.success(f"Node '{current_name}' was deleted successfully.")
            return updated_element_list

    return element_list