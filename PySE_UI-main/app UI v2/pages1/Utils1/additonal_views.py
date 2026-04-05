import streamlit as st
from pages1.Utils1.graphUtils import render_ppr_graph
from pages1.Utils1.config import PPR_ATTRS, ENG_ATTRS, SUST_ATTRS, edgeType_by_view, global_nodes_list, VIEW_ATTRS_MAPPING
from pages1.Utils1 import info1
def show(selected_view: str, locked: bool = False):  
        trial_nodes_list=["a", "b", "c","d","e"] # This is just a placeholder. Replace with actual list of nodes from the graph.      
        view_name= selected_view.split()[0] # Extracting 'PPR', 'Engineering', or 'Sustainability' from the selected view
        VIEW_ATTRS = VIEW_ATTRS_MAPPING.get(selected_view)
        VIEW_EDGE_TYPES=edgeType_by_view[selected_view]
        col1,col2= st.columns([3,10])
        with col1:
# Fixed: Removed the dot and switched to single quotes inside the braces
            tab_create, tab_delete = st.tabs([
                f"🏗️ Adjust {view_name} view", 
                f"🗑️ Delete {view_name} view Edge"
            ])
            with tab_create:
                view_radio=st.radio("What do you want to do?",[f"Adjust {view_name} attributes", f"Create {view_name} view Edge"], key=f"adjust_{view_name}_node_or_edge")
                with st.container(border=True,key="view_adjust_container"):
                    if view_radio == f"Adjust {view_name} attributes":
                        st.markdown(f"#### Adjust {view_name} attributes")
                        node_type= st.selectbox("Node Type",global_nodes_list,key="node_type_select")
                    
                        with st.form(key=f"adjust_{view_name}_attr_form"):
                            selected_node = st.selectbox("Choose Node", options=trial_nodes_list)                   
                            # selected_ppr_attrs= {}
                            if VIEW_ATTRS[node_type]:  # Check if there are attributes defined for this element type                         
                                available_attrs= list(VIEW_ATTRS[node_type].keys())
                                num_attrs= len(available_attrs)
                                button_label= "Adjust Attribute" if num_attrs==1 else "Adjust Attributes"
                                for attr in available_attrs:
                                    attrs_info= VIEW_ATTRS[node_type][attr]
                                    unit= attrs_info["unit"]
                                    st.text("Adjust Attribute:")
                                    col1_1, col1_2 = st.columns([2, 1])   
                                    with col1_1:
                                        value = st.number_input(f"{attr.replace('_', ' ').title()}",
                                                                disabled=locked,
                                                                min_value=0.0,step=0.1,format="%f",key=f"{attr}_value")

                                    with col1_2:
                                        st.text_input("Unit",value=unit,disabled=True,key=f"{attr}_unit")
                            

                            # elem_data={}
                            submitted= st.form_submit_button(button_label,disabled=locked)

                            if submitted:
                                    st.success(f"Attributes for node **{selected_node}** adjusted!")
                    
                    if view_radio == f"Create {view_name} view Edge":
                        st.markdown(f"#### Create {view_name} view Edge")
                        with st.form(key=f"create_{view_name}_edge_form"):
                            view_edge_type= st.selectbox("Edge Type", VIEW_EDGE_TYPES, key="view_edge_type_select")
                            source_node= st.selectbox("Source Node Name",options=trial_nodes_list, index=None)
                            target_node= st.selectbox("Target Node Name",options=trial_nodes_list, index=None)
                            submitted_edge= st.form_submit_button("Create Edge", disabled=locked)
                            if submitted_edge:
                                if source_node is None or target_node is None:
                                    st.error("🚨 **Validation Error:** You must select both a Source and a Target node to create a link.")
                                elif source_node == target_node:
                                    st.error("🚨 **Validation Error:** Source and Target nodes cannot be the same.")
                                else:
                                    st.success(f"Edge of type **{view_edge_type}** created between {source_node} and {target_node}!")
            with tab_delete:
                st.markdown(f"#### Delete {view_name} view Edge")
                del_edge_type= st.selectbox("Edge Type", VIEW_EDGE_TYPES, key="del_view_edge_type_select")
                with st.form(key=f"delete_{view_name}_edge_form"):
                    view_edge_to_del= st.selectbox("Select Edge to Delete", options=trial_nodes_list, key="view_edge_to_del_select") # Replace with actual list of edges from the graph
                    submitted_del_view_edge= st.form_submit_button("Delete Edge", disabled=locked)
                    if submitted_del_view_edge:
                        st.warning(f"Are you sure you want to delete {view_edge_to_del}?") # Replace with actual delete logic


        with col2:
            info_tab, graph_tab= st.tabs(["ℹ️ Info", "📊 Graph"])
            with info_tab:
                st.write("This is where you can find information about the uploaded model and its components.")
                info1.create_table()
                    
            with graph_tab:
                with st.container(border=True):
                    st.write("PPR Graph Visualization will appear here after uploading a file.")
                    render_ppr_graph("PPR view")