import streamlit as st
import pandas as pd

# UPDATE THE NODES
def view_update_node(element_list):
    if not element_list:
        st.warning("No nodes available to edit.")
        return element_list

    name_list = [item["Name"] for item in element_list]
    s_node = st.selectbox("Select Node", name_list, key="update_select_node")

    selected_element = next(item for item in element_list if item["Name"] == s_node)

    attributes = selected_element.get("Attributes", [])

    if attributes:
        attr_df = pd.DataFrame(attributes)
        st.dataframe(attr_df, use_container_width=True)
    else:
        st.warning("No attributes available.")

    st.divider()

    # EDIT BASIC NODE FIELDS
    current_id = selected_element.get("ID")
    current_name = selected_element.get("Name", "")
    current_class = selected_element.get("Class", "")
    current_parent_id = selected_element.get("ParentID", None)
    current_attributes = selected_element.get("Attributes", [])

    new_name = st.text_input("Edit Name", value=current_name, key="update_name")

    class_options = [
        "SystemUnitClassLib/Product",
        "SystemUnitClassLib/Process",
        "SystemUnitClassLib/Resource"
    ]

    class_index = class_options.index(current_class) if current_class in class_options else 0

    new_class = st.selectbox(
        "Edit Class",
        class_options,
        index=class_index,
        key="update_class"
    )

    # FILTER PARENT OPTIONS BASED ON NEW CLASS
    parent_candidates = [
        item for item in element_list
        if item.get("Class") == new_class and item.get("ID") != current_id
    ]

    parent_options = [None] + parent_candidates

    default_parent_index = 0
    for i, item in enumerate(parent_options):
        if item is not None and item.get("ID") == current_parent_id:
            default_parent_index = i
            break

    selected_parent = st.selectbox(
        "Edit Parent",
        parent_options,
        index=default_parent_index,
        format_func=lambda x: "No Parent" if x is None else x["Name"],
        key="update_parent"
    )

    new_parent_id = None if selected_parent is None else selected_parent["ID"]

    # SHOW ATTRIBUTES ONLY IF CLASS IS PRODUCT
    updated_attributes = []

    if new_class == "SystemUnitClassLib/Product":
        st.markdown("### Edit Attributes")

        product_attr_names = sorted({
            attr.get("attr_name")
            for element in element_list
            if element.get("Class") == "SystemUnitClassLib/Product"
            for attr in element.get("Attributes", [])
            if attr.get("attr_name")
        })

        current_attr_lookup = {
            attr.get("attr_name"): attr.get("value")
            for attr in current_attributes
            if attr.get("attr_name")
        }

        for attr_name in product_attr_names:
            attr_name_clean = attr_name.strip().lower()
            current_value = current_attr_lookup.get(attr_name)

            if attr_name_clean == "quantity":
                try:
                    default_quantity = int(float(current_value)) if current_value not in [None, ""] else 1
                except (ValueError, TypeError):
                    default_quantity = 1

                attr_value = st.number_input(
                    f"{attr_name}",
                    min_value=1,
                    step=1,
                    value=default_quantity,
                    key=f"update_attr_{attr_name}"
                )
                value_to_store = str(attr_value)

            elif attr_name_clean == "color":
                color_options = ["Black", "White", "Red", "Green", "Blue", "Yellow", "Orange", "Gray"]
                default_color = current_value if current_value in color_options else "White"

                attr_value = st.selectbox(
                    f"{attr_name}",
                    options=color_options,
                    index=color_options.index(default_color),
                    key=f"update_attr_{attr_name}"
                )
                value_to_store = attr_value

            elif attr_name_clean == "size":
                size_options = ["S", "M", "L"]
                default_size = current_value if current_value in size_options else "M"

                attr_value = st.selectbox(
                    f"{attr_name}",
                    options=size_options,
                    index=size_options.index(default_size),
                    key=f"update_attr_{attr_name}"
                )
                value_to_store = attr_value

            else:
                attr_value = st.text_input(
                    f"{attr_name}",
                    value="" if current_value is None else str(current_value),
                    key=f"update_attr_{attr_name}"
                )
                value_to_store = attr_value if attr_value != "" else None

            updated_attributes.append({
                "attr_name": attr_name,
                "value": value_to_store
            })

    # UPDATE BUTTON
    if st.button("Update Node", key="update_node_button"):
        if not new_name.strip():
            st.error("Please enter a node name.")
            return element_list

        duplicate_exists = any(
            item.get("ID") != current_id and
            item.get("Name", "").strip().lower() == new_name.strip().lower()
            for item in element_list
        )

        if duplicate_exists:
            st.error(f"A node with the name '{new_name}' already exists.")
            return element_list

        updated_node = {
            "Name": new_name.strip(),
            "ID": current_id,
            "Class": new_class,
            "ParentID": new_parent_id,
            "Attributes": updated_attributes if new_class == "SystemUnitClassLib/Product" else []
        }

        updated_element_list = []
        for item in element_list:
            if item.get("ID") == current_id:
                updated_element_list.append(updated_node)
            else:
                updated_element_list.append(item)

        st.success(f"Node '{current_name}' updated successfully.")
        return updated_element_list

    # IMPORTANT: always return the original list when nothing is updated
    return element_list