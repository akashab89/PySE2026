import streamlit as st
from streamlit_option_menu import option_menu 
from pages1.Utils1.config import VIEW_ATTRS_MAPPING


def selection():
    selected_view = option_menu(
    "Viewpoints",
    options=list(VIEW_ATTRS_MAPPING.keys()),
    icons=["diagram-3", "gear", "globe"],
    orientation="horizontal",
    default_index=0,
    key="view_menu"
    )
    return selected_view

