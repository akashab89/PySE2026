
import streamlit as st
from pages1.Utils1 import viewpoints_menu
from pages1.Utils1 import ppr_view
from pages1.Utils1 import additonal_views
from xml.etree import ElementTree as et

from pages1.Utils1 import viewpoints_menu

def build_elements_dict(root, ns):
    elements = {}   # ✅ local dictionary

    def extract_elements(elem, parent_name=None):
        elem_name = elem.get("Name")
        elem_id = elem.get("ID")
        elem_class= elem.get("RefBaseSystemUnitPath")

        ppr_iface = elem.find("caex:ExternalInterface[@Name='PPR_port']", ns)
        port_id = ppr_iface.get("ID") if ppr_iface is not None else None
        ppr_attrs = []
        for attr in elem.findall("caex:Attribute", ns):
            value_elem= attr.find("caex:Value",ns)
            value = value_elem.text.strip() if value_elem is not None and value_elem.text else None
            ppr_attrs.append({
                "attr_name": attr.get("Name"),
                "data_type": attr.get("AttributeDataType"),
                "value": value
                })

        elements[elem_name] = {
            "name": elem_name,
            "id": elem_id,
            "class": elem_class,
            "xml": elem,
            "port_id": port_id,
            "parent": parent_name,
            "attributes": ppr_attrs
        }

        for child in elem.findall("caex:InternalElement", ns):
            extract_elements(child, elem_name)

    # Start recursion
    for top_elem in root.findall(".//caex:InstanceHierarchy/caex:InternalElement", ns):
        extract_elements(top_elem)

    return elements

def extract_links(root, ns):
    link_list=[]
    for elem in root.findall(".//caex:InternalElement",ns):
        for il in elem.findall("caex:InternalLink",ns):
            il_name = il.get("Name")
            il_source = il.get("RefPartnerSideA")
            il_target = il.get("RefPartnerSideB")
            cardinality = None
            for attr in il.findall("caex:Attribute", ns):
                if attr.get("Name")== "cardinality":
                    cardinality = attr.get("Value")
            link_list.append({"name": il_name, "source": il_source, "target": il_target, "cardinality": cardinality})
    return link_list

def show():
    elements = {}  # Initialize elements as an empty dictionary
    st.header("📥 Import Model")
    
    if "upload" not in st.session_state:
        st.session_state.upload = None
    
    if st.session_state.upload is None:       
        st.markdown("Upload an AML/XLXS file to visualize and analyze the PPR graph.")
        uploaded_file= st.file_uploader("Upload AML/XLXS file", type=["aml", "xlsx"], key="file_uploader")
 
        if uploaded_file:
            #Check separately for AML and XLSX files
                try:
                    tree= et.parse(uploaded_file)
                    root= tree.getroot()
                    ns = {"caex": "http://www.dke.de/CAEX"}

                except Exception as e:
                    st.write("Your AML file might be corrupted.")
                    with st.expander ("Full error"):
                        st.write(e)

                elements_dict=build_elements_dict(root, ns)
                link_list= extract_links(root, ns)
                st.session_state.upload = uploaded_file.name  # Mark file as processed
                if "imported_nodes" not in st.session_state:
                    st.session_state.imported_nodes = elements_dict
                if "imported_edges" not in st.session_state:
                    st.session_state.imported_edges = link_list 
                st.write(st.session_state.imported_nodes)
    
    if st.session_state.upload is not None:
        st.markdown(f"Uploaded File is {st.session_state.upload}.")

        selected_view = viewpoints_menu.handle("Import Model")
        if selected_view=="PPR View":
            ppr_view.show()        
        if selected_view=="Engineering View":
            additonal_views.show(selected_view)
        if selected_view=="Sustainability View":
            additonal_views.show(selected_view)





