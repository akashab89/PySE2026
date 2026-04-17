import streamlit as st


def inject_custom_css():
    import streamlit as st

    st.markdown("""
    <style>

    /* =========================
       SIDEBAR PANEL
    ========================= */
    section[data-testid="stSidebar"] {
        background-color: #F4F6F8;
        border-right: 1px solid #E0E3E7;
        padding-top: 1rem;
    }

    /* Sidebar title spacing */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        margin-bottom: 0.5rem;
    }

    /* =========================
       RADIO / SEGMENTED CONTROL
    ========================= */

    /* Container */
    div[role="radiogroup"] {
        background-color: #FFFFFF;
        padding: 6px;
        border-radius: 12px;
        border: 1px solid #E0E3E7;
        display: flex;
        gap: 6px;
    }

    /* Each option */
    div[role="radiogroup"] label {
        flex: 1;
        text-align: center;
        padding: 6px 8px;
        border-radius: 8px;
        font-weight: 500;
        cursor: pointer;
    }

    /* Selected option */
    div[role="radiogroup"] input:checked + div {
        color: blue;
        border-radius: 8px;
    }

    /* Hover effect */
    div[role="radiogroup"] label:hover {
        background-color: #EEF2F7;
    }

    /* =========================
       BUTTONS (clean engineering style)
    ========================= */
    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        border: none;
        padding: 0.45rem 0.8rem;
        font-weight: 600;
        background-color: #0B5ED7;
        color: white;
    }

    div.stButton > button:hover {
        background-color: #0A58CA;
    }

    /* =========================
       INPUT FIELDS
    ========================= */
    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {
        border-radius: 10px;
        border: 1px solid #D0D5DD;
    }

    /* =========================
       SECTION GROUPING (IMPORTANT)
    ========================= */
    .sidebar-section {
        background-color: white;
        padding: 12px;
        border-radius: 12px;
        border: 1px solid #E0E3E7;
        margin-bottom: 12px;
    }

    /* =========================
       LABEL TEXT (clean)
    ========================= */
    label {
        font-size: 0.85rem;
        font-weight: 500;
        color: #344054;
    }

    </style>
    """, unsafe_allow_html=True)

    