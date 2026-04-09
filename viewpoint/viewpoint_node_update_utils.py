import streamlit as st


# ==========================================================
# GET DEFAULT FIXED ATTRIBUTE NAME FOR A NODE CLASS
# ==========================================================
def get_view_default_attribute_name(node_class, config):
    return config["class_default_attributes"].get(node_class)


# ==========================================================
# ENSURE CUSTOM ATTRIBUTE REGISTRY EXISTS
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
# GET ALL ATTRIBUTE NAMES FOR A CLASS
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
# VALIDATE FIXED ATTRIBUTE VALUE
# ==========================================================
def validate_fixed_attr_value(value_raw, attr_name):
    if value_raw.strip() == "":
        return True, None

    try:
        return True, float(value_raw.strip())
    except ValueError:
        return False, f"{attr_name} must be a float or empty."


# ==========================================================
# UPDATE NODE ATTRIBUTE VALUES INSIDE A VIEWPOINT
# ==========================================================
def update_view_node_attribute(view_node_list, config):
    if not view_node_list:
        st.warning(f"No {config['view_name']} nodes available to update.")
        return view_node_list

    ensure_view_custom_attr_registry(config)

    view_key = config["view_key"]

    st.subheader("Update Existing Node Attributes")

    selected_node = st.selectbox(
        "Select Node",
        view_node_list,
        format_func=lambda x: f"{x['Name']} ({x['Class'].split('/')[-1]})",
        key=f"{view_key}_update_node_select"
    )

    node_class = selected_node["Class"]
    fixed_attr_name = get_view_default_attribute_name(node_class, config)
    current_attributes = selected_node.get("Attributes", [])

    current_attr_lookup = {
        attr.get("attr_name"): attr.get("value")
        for attr in current_attributes
        if attr.get("attr_name")
    }

    attr_names = get_view_attribute_names_for_class(node_class, config)

    st.markdown("### Edit Attributes")
    updated_attr_values = {}

    for attr_name in attr_names:
        existing_value = current_attr_lookup.get(attr_name)

        if attr_name == fixed_attr_name:
            updated_attr_values[attr_name] = st.text_input(
                f"{attr_name} (float or empty)",
                value="" if existing_value is None else str(existing_value),
                key=f"{view_key}_update_attr_{selected_node['ID']}_{attr_name}"
            )
        else:
            updated_attr_values[attr_name] = st.text_input(
                f"{attr_name} (text / float / empty)",
                value="" if existing_value is None else str(existing_value),
                key=f"{view_key}_update_attr_{selected_node['ID']}_{attr_name}"
            )

    if st.button("Update Node Attribute", key=f"{view_key}_update_node_button"):
        updated_attributes = []

        for attr_name, attr_value in updated_attr_values.items():
            if attr_name == fixed_attr_name:
                is_valid, parsed_value = validate_fixed_attr_value(attr_value, attr_name)
                if not is_valid:
                    st.error(parsed_value)
                    return view_node_list
                value_to_store = None if parsed_value is None else str(parsed_value)
            else:
                value_to_store = attr_value if attr_value != "" else None

            updated_attributes.append({
                "attr_name": attr_name,
                "value": value_to_store
            })

        updated_view_node_list = []
        for item in view_node_list:
            if item["ID"] == selected_node["ID"]:
                updated_view_node = {
                    "Name": item["Name"],
                    "ID": item["ID"],
                    "Class": item["Class"],
                    "ParentID": item["ParentID"],
                    "Attributes": updated_attributes
                }
                updated_view_node_list.append(updated_view_node)
            else:
                updated_view_node_list.append(item)

        st.success(f"Updated '{selected_node['Name']}'.")
        return updated_view_node_list

    return view_node_list