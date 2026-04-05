import streamlit as st
import xml.etree.ElementTree as et
from streamlit_option_menu import option_menu
from pages1.graphUtils import render_ppr_graph, edgeType_by_view
from pages1.graphUtils import PPR_ATTRS, ENG_ATTRS, SUST_ATTRS





def show():
    st.header("📥 Import Model")
    st.markdown("Upload an AML/XLXS file to visualize and analyze the PPR graph.")

    uploaded_file= st.file_uploader("Upload AML/XLXS file", type=["aml", "xlsx"])
    if uploaded_file:
        #Check separately for AML and XLSX files
        try:
            tree= et.parse(uploaded_file)
            root= tree.getroot()

        except Exception as e:
            st.write("Your AML file might be corrupted.")
            with st.expander ("Full error"):
                st.write(e)


    st.subheader("PPR Visualizer")
    selected_view = option_menu(
    "Viewpoints",
    ["PPR View", "Engineering View", "Sustainability View"],
    icons=["diagram-3", "gear", "globe"],
    orientation="horizontal",
    default_index=0,
    key="view_menu"
    )

    if selected_view=="PPR View":
        c1,c2= st.columns([3,10])
        with c1:
            tab_create, tab_delete = st.tabs(["🏗️ Create Network", "🗑️ Delete Components"])
            with tab_create:

                c1_1, c1_2= st.columns([3,2])
                with c1_1:
                    elem_name= st.text_input("Element Name")
                with c1_2:
                    elem_type= st.selectbox("Element Type", ["Product", "Process", "Resource"])
                
                selected_ppr_attrs= {}
                if PPR_ATTRS[elem_type]:  # Check if there are attributes defined for this element type
                    add_attr = st.checkbox(f"Do you want to add attribute to the {elem_type}?")
                    if add_attr:
                        available_attrs= list(PPR_ATTRS[elem_type].keys())
                        attr_count=0
                        while True:
                            if not available_attrs:
                                break
                            attr_key = f"attr_{attr_count}"
                            chosen_attr = st.selectbox(f"Choose Attribute {attr_count + 1}",options=available_attrs,key=attr_key)
                            attr_options = PPR_ATTRS[elem_type][chosen_attr]["options"]
                            chosen_value= st.selectbox(f"Choose {chosen_attr}", options=attr_options, key=f"value_{attr_count}")
                            selected_ppr_attrs[chosen_attr]= chosen_value
                            available_attrs.remove(chosen_attr)
                            #Check if more attributes can be added
                            if available_attrs:
                                add_more = st.checkbox("Do you want to add another attribute?",key=f"add_more_{attr_count}")
                                if add_more:
                                    attr_count += 1
                                    continue
                            break
                elem_data={}
                submitted= st.button("Create Element")

                if submitted:
                    elem_data = {
                        "name": elem_name,
                        "type": elem_type,
                        "attributes": selected_ppr_attrs
                    }

                    st.success("Element Created!")

            # with tab_delete:
        
        with c2:
            info_tab, graph_tab= st.tabs(["ℹ️ Info", "📊 Graph"])
            with info_tab:
                st.write("This is where you can find information about the uploaded model and its components.")
                st.write("You can also manage the components of your PPR graph here.")
            
            with graph_tab:
                with st.container(border=True):
                    st.write("PPR Graph Visualization will appear here after uploading a file.")
                    render_ppr_graph("PPR view")
