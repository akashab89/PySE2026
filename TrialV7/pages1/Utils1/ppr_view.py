import streamlit as st
import pandas as pd
from pages1.Utils1.graphUtils import render_ppr_graph
from pages1.Utils1.config import PPR_ATTRS, ENG_ATTRS, SUST_ATTRS, edgeType_by_view, global_nodes_list
from pages1.Utils1.graphUtils import nx_Digraph, show_yfiles_graph, nx_to_yfiles_graph, ppr_req_check
import networkx as nx
from pages1.Utils1.data_transform import nodes_by_class, remove_links_of_node
from pages1.Utils1.req_check import sim_struc_elem, isolated_check

def show(nodes: dict, links: list, engineering_nodes: dict, engineering_edges: list,
           sustainability_nodes: dict, sustainability_edges: list,locked: bool = False,):
        selected_view= "PPR View"
        grouped_nodes= nodes_by_class(nodes)
        all_nodes= [node for node in nodes.keys()]
        link_names= [link["name"] for link in links]
        c1, c2 = st.columns([1,3])
        with c1:
            active_panel = st.segmented_control(
                "PPR Action Panel",
                options=["🏗️ Edit Network", "🗑️ Delete Components", "✅ Requirement Check"],
                default="🏗️ Edit Network",
                key="ppr_active_panel",
                width="stretch"
            )
            # with tab_edit:
            if active_panel == "🏗️ Edit Network":
                ppr_radio=st.radio("Select the operation",["Create PPR Node", "Edit PPR Node", "Create PPR Edge"], key="create_node_or_edge_or_check")
                with st.container(border=True,key="ppr_node_container"):
                    if ppr_radio == "Create PPR Node":
                        st.markdown("#### Create PPR Node")
                        node_type= st.selectbox("Node Type", global_nodes_list,key="node_type_select")
                    
                        with st.form(key="create_ppr_node_form"):
                            node_name= st.text_input("Node Name",disabled=locked)
                            parent_node = st.selectbox("Choose Parent", options= grouped_nodes.get(node_type, []),
                                                       disabled=locked, key="parent_node_select",index=None,
                                                        help="Choose the parent of this node if there is one. If none, select none.")                   
                            selected_ppr_attrs= []
                            if PPR_ATTRS[node_type]:  # Check if there are attributes defined for this element type
                                available_attrs= list(PPR_ATTRS[node_type].keys())
                                for attr in available_attrs:
                                    attr_options = PPR_ATTRS[node_type][attr]["options"]
                                    chosen_value= st.selectbox(f"Choose {attr} attribute", options=attr_options, index=None, key=f"{node_type}_{attr}")
                                    selected_ppr_attrs.append({"attr_name": attr, "value": chosen_value})

                            elem_data={}
                            submitted= st.form_submit_button("Create Node", disabled=locked, key="create_node_button")

                            if submitted:
                            #Also check if there are duplicate node names here before creating the element. Check if empty node name is allowed or not.
                                if not node_name.strip():
                                    st.error("🚨 **Validation Error:** Node Name cannot be empty.")
                                elif node_name in all_nodes:
                                    st.error("🚨 **Validation Error:** A node with this name already exists. Please choose a different name.")
                                else:
                                        elem_data = {
                                            "name": node_name,
                                            "class": node_type,
                                            "parent": parent_node,
                                            "attributes": selected_ppr_attrs
                                        }
                                        nodes[node_name] = elem_data  # Add the new node to the nodes dictionary
                                        if parent_node:
                                            links.append({"name":parent_node + "_to_" + node_name,
                                                          "source": parent_node,
                                                    "target": node_name,"type":"PPR_port"})
                                        st.success(f"Node {node_name} of type **{node_type}** created!")
                                        st.rerun()

                    if ppr_radio == "Create PPR Edge":                    
                        st.markdown("#### Create PPR Edge")
                        with st.form(key="create_ppr_edge_form"):
                            edge_type= st.selectbox("Edge Type", edgeType_by_view[selected_view], key="edge_type_select")
                            source_node= st.selectbox("Source Node Name",options=all_nodes, index=None)
                            target_node= st.selectbox("Target Node Name",options=all_nodes, index=None)
                            cardinality = st.number_input("Cardinality (optional)",
                                                          min_value=1, step=1, value=None)
                            submitted_edge= st.form_submit_button("Create Edge", disabled=locked)
                            if submitted_edge:
                                if source_node is None or target_node is None:
                                    st.error("🚨 **Validation Error:** You must select both a Source and a Target node to create a link.")
                                elif source_node == target_node:
                                    st.error("🚨 **Validation Error:** Source and Target nodes cannot be the same.")
                                else:
                                    duplicate_exists = any(link for link in links if
                                                           link["source"] == source_node and link[
                                                               "target"] == target_node)
                                    if duplicate_exists:
                                        st.error(
                                            "🚨 **Validation Error:** An edge between the selected Source and Target nodes already exists. Please choose a different combination.")
                                    else:
                                        cardinality_conflict = False
                                        for link in links:
                                            if (link.get("source") == source_node and link.get(
                                                    "cardinality") is not None):
                                                cardinality_conflict = True
                                                break
                                        if cardinality is not None and cardinality_conflict:
                                            st.error(
                                                "⚠️ This source node already has a cardinality assigned. Only one cardinality per source node is allowed.")
                                        else:
                                            links.append(
                                                {"name": source_node + "_to_" + target_node, "source": source_node,
                                                 "target": target_node, "cardinality": cardinality, "type": edge_type})
                                            st.success(
                                                f"Edge of type **{edge_type}** created between {source_node} and {target_node}!")
                                            st.rerun()
                    #Edit PPR Node
                    if ppr_radio == "Edit PPR Node":
                        st.markdown("#### Edit PPR Node")
                        node_type = st.selectbox("Node Type", global_nodes_list, key="ppr_node_type_select")
                        node_name = st.selectbox("Choose Node to edit", options=grouped_nodes.get(node_type, []), disabled=locked, key="ppr_node_name_select")
                        new_class = st.selectbox("Change Class of the node", global_nodes_list, key="ppr_new_class_select")

                        with st.form(key="edit_ppr_node_form"):
                            new_node_name = st.text_input("Rename node", disabled=locked,value=str(node_name))
                            parent_candidates = [item for item in grouped_nodes.get(new_class,[]) if item != node_name]
                            new_parent_node = st.selectbox("Change Parent of the node", options=parent_candidates, disabled=locked, index=None)
                            selected_ppr_attrs = []
                            if PPR_ATTRS[new_class]:  # Check if there are attributes defined for this element type
                                available_attrs = list(PPR_ATTRS[new_class].keys())
                                for attr in available_attrs:
                                    attr_options = PPR_ATTRS[new_class][attr]["options"]
                                    chosen_value = st.selectbox(f"Change {attr} attribute", options=attr_options,
                                                                index=None, key=f"{new_class}_{attr}")
                                    selected_ppr_attrs.append({"attr_name": attr, "value": chosen_value})
                            elem_data = {}
                            submitted = st.form_submit_button("Edit Node", disabled=locked, key="edit_node_button")

                            if submitted:
                            #Also check if there are duplicate node names here before editing the element. Check if empty node name is allowed or not.
                                if not new_node_name.strip():
                                    st.error("🚨 **Validation Error:** Renamed Node Name cannot be empty.")
                                else:
                                    elem_data = {
                                        "name": new_node_name,
                                        "class": new_class,
                                        "parent": new_parent_node,
                                        "attributes": selected_ppr_attrs
                                    }
                                    new_name = elem_data["name"]
                                    nodes[new_name] = elem_data
                                    if new_name != node_name:
                                        del nodes[node_name]
                                    st.write(nodes)
                                    for link in links:
                                        if link["source"] == node_name:
                                            link["source"] = new_name
                                        if link["target"] == node_name:
                                            link["target"] = new_name
                                        link["name"] = f"{link['source']}_to_{link['target']}"


                                    if new_parent_node:
                                        links.append({"name":new_parent_node + "_to_" + new_name,
                                                      "source": new_parent_node,
                                                "target": new_name,"type":"PPR_port"})
                                    st.success(f"Node {new_name} of type **{new_class}** created!")
                                    st.rerun()

            elif active_panel == "🗑️ Delete Components":
                ppr_del_radio=st.radio("Select the operation",["Delete Node", "Delete Edge"], key="del_node_or_edge")
                with st.container(border=True,key="ppr_del_container"):
                    if ppr_del_radio == "Delete Node":
                        st.markdown("#### Delete PPR Node")
                        del_node_type= st.selectbox("Node Type",global_nodes_list,key="del_node_type_select")
                        with st.form(key="delete_ppr_node_form"):
                            node_to_delete= st.selectbox("Select Node to Delete", options=grouped_nodes.get(del_node_type,[]), index=None, key="node_to_del_select") # Replace with actual list of nodes from the graph
                            submitted_del_node= st.form_submit_button("Delete Node", disabled=locked)
                            if submitted_del_node:
                                if node_to_delete is None:
                                    st.error("🚨 **Validation Error:** You must select a node to delete.")
                                else:
                                    remove_links_of_node(links, node_to_delete)  # Remove all links associated with the node
                                    remove_links_of_node(engineering_edges, node_to_delete)  # Also remove from engineering edges
                                    remove_links_of_node(sustainability_edges, node_to_delete)  # Also remove from
                                    nodes.pop(node_to_delete, None)  # Remove the node from the nodes dictionary
                                    engineering_nodes.pop(node_to_delete, None)  # Also remove from engineering nodes
                                    sustainability_nodes.pop(node_to_delete, None)  # Also remove from sustainability nodes
                                    st.success(f"Node **{node_to_delete}** deleted!")
                                    st.rerun()
                    
                    if ppr_del_radio == "Delete Edge":
                        st.markdown("#### Delete PPR Edge")
                        del_edge_type= st.selectbox("Edge Type", edgeType_by_view[selected_view], key="del_edge_type_select")
                        with st.form(key="delete_ppr_edge_form"):
                            edge_to_delete= st.selectbox("Select Edge to Delete", options=link_names,index=None, key="edge_to_del_select") # Replace with actual list of edges from the graph
                            submitted_del_edge= st.form_submit_button("Delete Edge", disabled=locked)
                            if submitted_del_edge:
                                if edge_to_delete is None:
                                    st.error("🚨 **Validation Error:** You must select an edge to delete.")
                                else:
                                    for i in range(len(links)-1, -1, -1):  # Iterate backwards to avoid index issues when deleting
                                        if links[i]["name"] == edge_to_delete and links[i]["type"] == del_edge_type:
                                            del links[i]  # Remove the link from the links list
                                            st.success(f"Edge **{edge_to_delete}** deleted!")
                                            st.rerun()
                                            break
            # with tab_req_check:
            elif active_panel == "✅ Requirement Check":
                sim_struc_elem(nodes, links)
                st.subheader("Isolated Production Elements")
                nx_ppr_graph = nx_Digraph(nodes_dict=nodes, link_list=links)
                isolated_check(nx_ppr_graph)


        with c2:
            with st.container(border=True, height=700):
                if active_panel in ["🏗️ Edit Network", "🗑️ Delete Components"]:
                    st.info("PPR Graph Visualization")
                    nx_ppr_graph = nx_Digraph(nodes_dict=nodes, link_list=links)
                    # node_cardinality = node_cardinality_mapping(nx_ppr_graph)
                    nodes, edges = nx_to_yfiles_graph(nx_ppr_graph)
                    show_yfiles_graph(nodes, edges)
                elif active_panel == "✅ Requirement Check":
                    st.info("Similar Production Elements Visualization")
                    # node_cardinality = node_cardinality_mapping(nx_ppr_graph)
                    nodes, edges = nx_to_yfiles_graph(nx_ppr_graph)
                    ppr_req_check(nodes, edges)
