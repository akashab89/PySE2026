import streamlit as st
import pandas as pd
import networkx as nx
from pages1.Utils1.data_transform import extract_numeric
def sim_struc_elem(nodes, links):
    st.write("Summary of Similarly Structured Elements")
    rows = []

    for node_name, node_data in nodes.items():
        row = {
            "name": node_data.get("name"),
            "id": node_data.get("id"),
            "class": node_data.get("class"),
            "parent": node_data.get("parent"),
            "port_id": node_data.get("port_id"),
        }

        for attr in node_data.get("attributes", []):
            attr_name = attr.get("attr_name")
            attr_value = attr.get("value")
            if attr_name:
                row[attr_name] = attr_value

        rows.append(row)

    df = pd.DataFrame(rows)

    if df.empty:
        st.warning("No nodes available.")
        return

    # BASIC SUMMARY ONLY
    total_nodes = len(df)
    product_count = (df["class"] == "Product").sum()
    process_count = (df["class"] == "Process").sum()
    resource_count = (df["class"] == "Resource").sum()

    root_count = df["parent"].isna().sum() + (df["parent"] == "").sum()
    child_count = total_nodes - root_count

    # st.markdown("### Summary")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Nodes", int(total_nodes))
    c2.metric("Products", int(product_count))
    c3.metric("Processes", int(process_count))
    c4.metric("Resources", int(resource_count))

def isolated_check(nx_ppr_graph):

    if st.button("Check for isolated nodes"):

        # Isolated nodes check
        isolated_nodes = [
            n for n in nx_ppr_graph.nodes()
            if nx_ppr_graph.in_degree(n) == 0 and nx_ppr_graph.out_degree(n) == 0
        ]

        if isolated_nodes:
            st.warning("⚠️ Isolated nodes detected:")
            isolated_info = []
            for n in isolated_nodes:
                node_class = nx_ppr_graph.nodes[n].get("node_class", "Unknown")
                isolated_info.append({
                    "Node Name": n,
                    "Class": node_class
                })

            st.dataframe(isolated_info, use_container_width=True)
        else:
            st.success("✅ No isolated nodes found.")

def get_matching_elements_by_attribute(nodes: dict, node_type: str, selected_attr: str, fun: str, val: float):
    matching_rows = []

    for node_name, node_data in nodes.items():
        # Check only nodes of selected class
        if node_data.get("class") != node_type:
            continue

        # Find the selected attribute in node attributes
        attr_value_raw = None
        for attr_item in node_data.get("attributes", []):
            if attr_item.get("attr_name") == selected_attr:
                attr_value_raw = attr_item.get("value")
                break

        # Skip if attribute not present
        if attr_value_raw is None:
            continue

        # Convert value like "10 Euro" -> 10.0
        attr_value_num = extract_numeric(str(attr_value_raw))

        # Apply selected comparison
        condition_met = False

        if fun == "equal to (=)":
            condition_met = (attr_value_num == val)
        elif fun == "less than (<)":
            condition_met = (attr_value_num < val)
        elif fun == "greater than (>)":
            condition_met = (attr_value_num > val)
        elif fun == "less than or equal to (<=)":
            condition_met = (attr_value_num <= val)
        elif fun == "greater than or equal to (>=)":
            condition_met = (attr_value_num >= val)

        if condition_met:
            matching_rows.append({
                "Name": node_name,
                "Class": node_data.get("class"),
                "Attribute": selected_attr,
                "Value": attr_value_raw,
            })

    return pd.DataFrame(matching_rows)

def check_axle_wheel_rule(G):

    if st.button("Run Axle-Wheel Check"):

        axle_node = None
        wheel_node = None

        # ---- Find nodes by NAME ----
        for node, attrs in G.nodes(data=True):
            node_name = attrs.get("name")

            if node_name == "Axle":
                axle_node = node
            elif node_name == "Wheel":
                wheel_node = node

        # ---- Validate existence ----
        if axle_node is None:
            st.error("❌ No Axle node found")
            return

        if wheel_node is None:
            st.error("❌ No Wheel node found")
            return

        # ---- Sum outgoing cardinalities ----
        axle_sum = sum(
            int(attrs["cardinal"])
            for _, _, attrs in G.out_edges(axle_node, data=True)
            if attrs.get("cardinal") is not None
        )

        wheel_sum = sum(
            int(attrs["cardinal"])
            for _, _, attrs in G.out_edges(wheel_node, data=True)
            if attrs.get("cardinal") is not None
        )

        if wheel_sum != 2 * axle_sum:
            st.error(
                f"❌ Cardinality mismatch: wheel={wheel_sum}, axle={axle_sum} "
                f"(expected wheel = 2 × axle)"
            )
            return

        st.success(
            f"✅ Requirement satisfied: An axle must be connected to two wheels "
            f"(axle={axle_sum}, wheel={wheel_sum})"
        )