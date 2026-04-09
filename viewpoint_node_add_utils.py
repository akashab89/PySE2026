import streamlit as st


# ==========================================================
# GET DEFAULT FIXED ATTRIBUTE NAME FOR A NODE CLASS
# Example:
# Product -> Cost / CO2 emission per unit
# ==========================================================
def get_view_default_attribute_name(node_class, config):
    return config["class_default_attributes"].get(node_class)


# ==========================================================
# ENSURE CUSTOM ATTRIBUTE REGISTRY EXISTS IN SESSION STATE
# One registry per viewpoint:
# be_class_custom_attrs / sus_class_custom_attrs
# ==========================================================
def ensure_view_custom_attr_registry(config):
    view_key = config["view_key"]
    custom_attr_key = f"{view_key}_class_custom_attrs"

    if custom_attr_key not in st.session_state or st.session_state[custom_attr_key] is None:
        st.session_state[custom_attr_key] = {
            "SystemUnitClassLib/Product": [],
            "SystemUnitClassLib/Process": [],
            "SystemUnitClassLib/Resource": []
        }


# ==========================================================
# GET ALL ATTRIBUTE NAMES AVAILABLE FOR A CLASS
# Includes:
# 1. fixed default attribute
# 2. user-created custom attributes
# ==========================================================
def get_view_attribute_names_for_class(node_class, config):
    ensure_view_custom_attr_registry(config)

    view_key = config["view_key"]
    custom_attr_key = f"{view_key}_class_custom_attrs"

    default_attr = get_view_default_attribute_name(node_class, config)
    custom_attrs = st.session_state[custom_attr_key].get(node_class, [])

    attr_names = []
    if default_attr:
        attr_names.append(default_attr)

    for attr in custom_attrs:
        if attr not in attr_names:
            attr_names.append(attr)

    return attr_names


# ==========================================================
# ADD A CUSTOM ATTRIBUTE NAME TO A CLASS
# Once added, it becomes available for all nodes of same class
# ==========================================================
def add_custom_attr_to_view_class(node_class, custom_attr_name, config):
    ensure_view_custom_attr_registry(config)

    view_key = config["view_key"]
    custom_attr_key = f"{view_key}_class_custom_attrs"

    custom_attr_name = custom_attr_name.strip()
    if not custom_attr_name:
        return False

    existing_attrs = st.session_state[custom_attr_key].get(node_class, [])
    existing_lower = [x.strip().lower() for x in existing_attrs]

    default_attr = get_view_default_attribute_name(node_class, config)
    if default_attr and custom_attr_name.lower() == default_attr.lower():
        return False

    if custom_attr_name.lower() not in existing_lower:
        st.session_state[custom_attr_key][node_class].append(custom_attr_name)
        return True

    return False


# ==========================================================
# VALIDATE FIXED ATTRIBUTE VALUE
# Fixed attribute accepts only float or empty
# ==========================================================
def validate_fixed_attr_value(value_raw, attr_name):
    if value_raw.strip() == "":
        return True, None

    try:
        return True, float(value_raw.strip())
    except ValueError:
        return False, f"{attr_name} must be a float or empty."


# ==========================================================
# ADD NODE INTO A VIEWPOINT
# - Select node from PPR list
# - Add fixed + custom attributes
# - Save node into viewpoint node list
# ==========================================================
def add_view_node_attribute(ppr_element_list, view_node_list, config):
    if not ppr_element_list:
        st.warning("No PPR nodes available.")
        return view_node_list

    ensure_view_custom_attr_registry(config)

    view_key = config["view_key"]
    view_name = config["view_name"]

    existing_view_ids = {item["ID"] for item in view_node_list}
    available_nodes = [
        item for item in ppr_element_list
        if item["ID"] not in existing_view_ids
    ]

    if not available_nodes:
        st.info(f"All PPR nodes are already added to {view_name}.")
        return view_node_list

    st.subheader("Add Node Attributes")

    selected_node = st.selectbox(
        "Select Node",
        available_nodes,
        format_func=lambda x: f"{x['Name']} ({x['Class'].split('/')[-1]})",
        key=f"{view_key}_add_node_select"
    )

    node_class = selected_node["Class"]
    fixed_attr_name = get_view_default_attribute_name(node_class, config)

    # ------------------------------------------------------
    # Allow user to add a new custom attribute name here
    # ------------------------------------------------------
    st.markdown("### Add Custom Attribute Name")
    custom_attr_name = st.text_input(
        "Custom attribute name",
        key=f"{view_key}_add_custom_attr_name"
    )

    if st.button("Add Custom Attribute for this Class", key=f"{view_key}_add_custom_attr_button"):
        if not custom_attr_name.strip():
            st.error("Please enter a custom attribute name.")
            return view_node_list

        was_added = add_custom_attr_to_view_class(node_class, custom_attr_name, config)
        if was_added:
            st.success(
                f"Custom attribute '{custom_attr_name.strip()}' added for class {node_class.split('/')[-1]}."
            )
        else:
            st.info("This custom attribute already exists or matches the fixed attribute name.")
        st.rerun()

    # ------------------------------------------------------
    # Show all attribute inputs for the selected class
    # ------------------------------------------------------
    attr_names = get_view_attribute_names_for_class(node_class, config)

    st.markdown("### Enter Attribute Values")
    temp_attr_values = {}

    for attr_name in attr_names:
        if attr_name == fixed_attr_name:
            temp_attr_values[attr_name] = st.text_input(
                f"{attr_name} (float or empty)",
                key=f"{view_key}_add_attr_{selected_node['ID']}_{attr_name}"
            )
        else:
            temp_attr_values[attr_name] = st.text_input(
                f"{attr_name} (text / float / empty)",
                key=f"{view_key}_add_attr_{selected_node['ID']}_{attr_name}"
            )

    # ------------------------------------------------------
    # Save the selected node into the viewpoint
    # ------------------------------------------------------
    if st.button(f"Add Node to {view_name}", key=f"{view_key}_add_node_button"):
        attributes = []

        for attr_name, attr_value in temp_attr_values.items():
            if attr_name == fixed_attr_name:
                is_valid, parsed_value = validate_fixed_attr_value(attr_value, attr_name)
                if not is_valid:
                    st.error(parsed_value)
                    return view_node_list
                value_to_store = None if parsed_value is None else str(parsed_value)
            else:
                value_to_store = attr_value if attr_value != "" else None

            attributes.append({
                "attr_name": attr_name,
                "value": value_to_store
            })

        new_view_node = {
            "Name": selected_node["Name"],
            "ID": selected_node["ID"],
            "Class": selected_node["Class"],
            "ParentID": selected_node["ParentID"],
            "Attributes": attributes
        }

        updated_view_node_list = view_node_list + [new_view_node]
        st.success(f"Added '{selected_node['Name']}' to {view_name}.")
        return updated_view_node_list

    return view_node_list