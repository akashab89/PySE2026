import streamlit as st
from pages1.Utils1.graphUtils import render_ppr_graph
from pages1.Utils1.config import PPR_ATTRS, ENG_ATTRS, SUST_ATTRS, edgeType_by_view, global_nodes_list
from pages1.Utils1 import info1

def show(locked: bool = False):
        selected_view= "PPR View"
        trial_nodes_list=["a", "b", "c","d","e"] # This is just a placeholder. Replace with actual list of nodes from the graph.
        c1,c2= st.columns([3,10])
        with c1:
            tab_create, tab_delete = st.tabs(["🏗️ Create Network", "🗑️ Delete Components"])
            with tab_create:
                ppr_radio=st.radio("What do you want to do?",["Create PPR Node", "Create PPR Edge","Check PPR Requirements"], key="create_node_or_edge_or_check")
                with st.container(border=True,key="ppr_node_container"):
                    if ppr_radio == "Create PPR Node":

                        st.markdown("#### Create PPR Node")
                        node_type= st.selectbox("Node Type", global_nodes_list,key="node_type_select")
                    
                        with st.form(key="create_ppr_node_form"):
                            node_name= st.text_input("Node Name",disabled=locked)
                            parent_node = st.selectbox("Choose Parent", options=["None", "Parent A", "Parent B"],
                                                       disabled=locked, key="parent_node_select",
                                                        help="Choose the parent of this node if there is one. If none, select none.")                   
                            selected_ppr_attrs= {}
                            if PPR_ATTRS[node_type]:  # Check if there are attributes defined for this element type
                                    available_attrs= list(PPR_ATTRS[node_type].keys())
                                    for attr in available_attrs:
                                        attr_options = PPR_ATTRS[node_type][attr]["options"]
                                        chosen_value= st.selectbox(f"Choose {attr} attribute", options=attr_options, index=None, key=f"{node_name}_{attr}")
                                        selected_ppr_attrs[attr]= chosen_value

                            elem_data={}
                            submitted= st.form_submit_button("Create Node", disabled=locked)

                            if submitted:
                            #Also check if there are duplicate node names here before creating the element. Check if empty node name is allowed or not.
                                if not node_name.strip():
                                    st.error("🚨 **Validation Error:** Node Name cannot be empty.")
                                else:
                                    elem_data = {
                                        "name": node_name,
                                        "type": node_type,
                                        "parent": parent_node,
                                        "attributes": selected_ppr_attrs
                                    }
                                    st.success(f"Node {node_name} of type **{node_type}** created!")
                    if ppr_radio == "Create PPR Edge":
                         
                                        
                        st.markdown("#### Create PPR Edge")
                        with st.form(key="create_ppr_edge_form"):
                            edge_type= st.selectbox("Edge Type", edgeType_by_view[selected_view], key="edge_type_select")
                            source_node= st.selectbox("Source Node Name",options=trial_nodes_list, index=None)
                            target_node= st.selectbox("Target Node Name",options=trial_nodes_list, index=None)
                            submitted_edge= st.form_submit_button("Create Edge", disabled=locked)
                            if submitted_edge:
                                if source_node is None or target_node is None:
                                    st.error("🚨 **Validation Error:** You must select both a Source and a Target node to create a link.")
                                elif source_node == target_node:
                                    st.error("🚨 **Validation Error:** Source and Target nodes cannot be the same.")
                                else:
                                    st.success(f"Edge of type **{edge_type}** created between {source_node} and {target_node}!")
                    if ppr_radio == "Check PPR Requirements":
                        st.markdown("#### Check PPR Requirements")
                        st.info("This feature will analyze your graph and identify any missing elements or relationships based on standard PPR requirements.")
                        if st.button("Run PPR Check"):
                            # Placeholder for actual PPR check logic
                            st.success("PPR Check completed! No issues found.")  # Replace with actual results of the check
            
            with tab_delete:
                ppr_del_radio=st.radio("What do you want to do?",["Delete Node", "Delete Edge"], key="del_node_or_edge")
                with st.container(border=True,key="ppr_del_container"):
                    if ppr_del_radio == "Delete Node":
                        st.markdown("#### Delete PPR Node")
                        del_node_type= st.selectbox("Node Type",global_nodes_list,key="del_node_type_select")
                        with st.form(key="delete_ppr_node_form"):
                            node_to_delete= st.selectbox("Select Node to Delete", options=trial_nodes_list, key="node_to_del_select") # Replace with actual list of nodes from the graph
                            submitted_del_node= st.form_submit_button("Delete Node", disabled=locked)
                            if submitted_del_node:
                                st.warning(f"Node {node_to_delete} will delete all its connected edges as well. Are you sure you want to proceed?")
                                 # Replace with actual delete logic
                    
                    if ppr_del_radio == "Delete Edge":
                        st.markdown("#### Delete PPR Edge")
                        del_edge_type= st.selectbox("Edge Type", edgeType_by_view[selected_view], key="del_edge_type_select")
                        with st.form(key="delete_ppr_edge_form"):
                            edge_to_delete= st.selectbox("Select Edge to Delete", options=trial_nodes_list, key="edge_to_del_select") # Replace with actual list of edges from the graph
                            submitted_del_edge= st.form_submit_button("Delete Edge", disabled=locked)
                            if submitted_del_edge:
                                st.warning(f"Are you sure you want to delete {edge_to_delete}?") # Replace with actual delete logic
                    
        
        with c2:
            with st.container(border=True, height=700):
                info_tab, graph_tab= st.tabs(["ℹ️ Info", "📊 Graph"])            
                with info_tab:
                    st.write("This is where you can find information about the model and its components.")
                    info1.create_table()
            
                with graph_tab:
                    st.write("PPR Graph Visualization will appear here after uploading a file.")
                    render_ppr_graph("PPR view")