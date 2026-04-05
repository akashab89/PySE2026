import uuid
import streamlit as st

# GET UNIQUE EXISTING ATTRIBUTE NAMES FROM element_list
def get_existing_attribute_names(element_list):
    attr_names = set()

    for element in element_list:
        for attr in element.get("Attributes", []):
            attr_name = attr.get("attr_name")
            if attr_name:
                attr_names.add(attr_name)

    return sorted(attr_names)


# CREATE NEW NODE FORM
def create_new_node_form(element_list, prefix="create_node"):
    existing_attr_names = get_existing_attribute_names(element_list)

    st.subheader("Create New Node")

    # NODE NAME
    node_name = st.text_input("Node Name", key=f"{prefix}_name")

    # NODE CLASS
    node_class = st.selectbox(
        "Node Class",
        options=[
            "SystemUnitClassLib/Product",
            "SystemUnitClassLib/Process",
            "SystemUnitClassLib/Resource"
        ],
        key=f"{prefix}_class"
    )

    # FILTER PARENTS BASED ON SELECTED CLASS
    parent_candidates = [
        item for item in element_list
        if item.get("Class") == node_class
    ]

    parent_options = [None] + parent_candidates

    selected_parent = st.selectbox(
        "Parent Node",
        options=parent_options,
        format_func=lambda x: "No Parent" if x is None else x["Name"],
        key=f"{prefix}_parent"
    )

    parent_id = None if selected_parent is None else selected_parent["ID"]

    # SHOW ATTRIBUTES ONLY FOR PRODUCT CLASS
    temp_existing_values = {}
    if node_class == "SystemUnitClassLib/Product":
        st.markdown("### Existing Attributes")
        st.caption("Fill values for all attribute names already present in the model.")

        for attr_name in existing_attr_names:
            attr_name_clean = attr_name.strip().lower()

            if attr_name_clean == "quantity":
                temp_existing_values[attr_name] = st.number_input(
                    f"{attr_name}",
                    min_value=1,
                    step=1,
                    value=1,
                    key=f"{prefix}_existing_{attr_name}"
                )

            elif attr_name_clean == "color":
                temp_existing_values[attr_name] = st.selectbox(
                    f"{attr_name}",
                    options=[
                        "Black", "White", "Red", "Green",
                        "Blue", "Yellow", "Orange", "Gray"
                    ],
                    key=f"{prefix}_existing_{attr_name}"
                )

            elif attr_name_clean == "size":
                temp_existing_values[attr_name] = st.selectbox(
                    f"{attr_name}",
                    options=["S", "M", "L"],
                    key=f"{prefix}_existing_{attr_name}"
                )

            else:
                temp_existing_values[attr_name] = st.text_input(
                    f"{attr_name}",
                    key=f"{prefix}_existing_{attr_name}"
                )

    submitted = st.button("Create Node", key=f"{prefix}_submit")

    if not submitted:
        return None

    # VALIDATION
    if not node_name:
        st.error("Please enter a node name.")
        return None

    # AVOID DUPLICATE NODE NAMES
    existing_names = [item.get("Name", "").strip().lower() for item in element_list]
    if node_name.strip().lower() in existing_names:
        st.error(f"A node with the name '{node_name}' already exists. Please choose a different name.")
        return None

    # BUILD ATTRIBUTES ONLY FOR PRODUCT CLASS
    attributes = []
    if node_class == "SystemUnitClassLib/Product":
        for attr_name, attr_value in temp_existing_values.items():
            if attr_name.strip().lower() == "quantity":
                value_to_store = str(attr_value) if attr_value is not None else None
            else:
                value_to_store = attr_value if attr_value != "" else None

            attributes.append({
                "attr_name": attr_name,
                "value": value_to_store
            })

    # BUILD NEW NODE
    new_node = {
        "Name": node_name,
        "ID": str(uuid.uuid4()),
        "Class": node_class,
        "ParentID": parent_id,
        "Attributes": attributes
    }

    return new_node


# APPEND NEW NODE TO element_list
def append_new_node(element_list, new_node):
    if new_node:
        element_list.append(new_node)
    return element_list