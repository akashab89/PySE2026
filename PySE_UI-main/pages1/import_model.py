import xml.etree.ElementTree as et
import streamlit as st
from pages1.Utils1 import viewpoints_menu
from pages1.Utils1 import ppr_view
from pages1.Utils1 import additonal_views

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

        selected_view_import = viewpoints_menu.selection()

        if selected_view_import=="PPR View":
            ppr_view.show()
        
        if selected_view_import=="Engineering View":
            additonal_views.show(selected_view_import)

        if selected_view_import=="Sustainability View":
            additonal_views.show(selected_view_import)

        
        # def view_content():
    #     ph={}
    #     ph={"engineering":"Engineering"}
        
