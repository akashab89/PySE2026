import streamlit as st
import pandas as pd
import networkx as nx

def sim_struc_elem(nodes, links):
    st.subheader("Similarly Structured Elements")
    # with st.expander("Nodes"):
    #     st.write(nodes)
    # with st.expander("Edges"):
    #     st.write(links)

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

    st.markdown("### Summary")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Nodes", int(total_nodes))
    c2.metric("Products", int(product_count))
    c3.metric("Processes", int(process_count))
    c4.metric("Resources", int(resource_count))

    c5, c6 = st.columns(2)
    c5.metric("Root Nodes", int(root_count))
    c6.metric("Child Nodes", int(child_count))

    # SHOW 3 SEPARATE INTERACTIVE TABLES BASED ON CLASS
    with st.expander("Product Nodes"):
        product_df = df[df["class"] == "Product"]
        st.caption(f"Total Product nodes: {len(product_df)}")
        st.dataframe(product_df, use_container_width=True)

    with st.expander("Process Nodes"):
        process_df = df[df["class"] == "Process"]
        st.caption(f"Total Process nodes: {len(process_df)}")
        st.dataframe(process_df, use_container_width=True)

    with st.expander("Resource Nodes"):
        resource_df = df[df["class"] == "Resource"]
        st.caption(f"Total Resource nodes: {len(resource_df)}")
        st.dataframe(resource_df, use_container_width=True)

def isolated_check(nx_ppr_graph):

    if st.button("Check for isolated nodes"):

        # ----------------------------
        # 1. Isolated nodes check
        # ----------------------------
        isolated_nodes = [
            n for n in nx_ppr_graph.nodes()
            if nx_ppr_graph.in_degree(n) == 0 and nx_ppr_graph.out_degree(n) == 0
        ]

        if isolated_nodes:
            st.warning("⚠️ Isolated nodes detected:")
            for n in isolated_nodes:
                st.write(f"- {n}")
        else:
            st.success("✅ No isolated nodes found.")

        # ----------------------------
        # 2. Subgraphs ≥ 5 nodes
        # ----------------------------
        # components = list(nx.weakly_connected_components(nx_ppr_graph))
        #
        # large_subgraphs = [c for c in components if len(c) >= 5]
        #
        # st.markdown("### 📊 Subgraphs with ≥ 5 nodes")
        #
        # if large_subgraphs:
        #     st.warning(f"⚠️ Found {len(large_subgraphs)} large subgraph(s):")
        #
        #     for i, sg in enumerate(large_subgraphs, start=1):
        #         st.write(f"**Subgraph {i} ({len(sg)} nodes):**")
        #         st.write(list(sg))
        # else:
        #     st.success("✅ No subgraphs with 5 or more nodes found.")