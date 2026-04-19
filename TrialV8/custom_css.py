import streamlit as st


def inject_custom_css():
    import streamlit as st

    st.markdown("""
    <style>
        /* =========================
        HEADING SECTION
        ========================= */
    .hero {
        width: 100%;
        padding: 80px 40px;
        border-radius: 20px;
        background: linear-gradient(135deg, #7C3AED, #06B6D4);
        color: white;
        margin-bottom: 30px;
    }
    
    .hero-content {
        max-width: 1600px;
    }
    
    .hero h1 {
        font-size: 56px;
        font-weight: 700;
        margin-bottom: 20px;
        line-height: 1.1;
    }
    
    .hero p {
        font-size: 18px;
        opacity: 0.9;
        margin-bottom: 30px;
    }
    
    .block-container {
    padding-top: 2rem;
    }
    

    .nav-link:hover {
        background-color: #47484a;
    }

    .nav-link.active {
        background: #7C3AED !important;
        color: white !important;
        font-weight: 600;
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
        color: purple;
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
        background-color: #7C3AED;
        color: white;
    }

    div.stButton > button:hover {
        background-color: #7C3AED;
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
       LABEL TEXT (clean)
    ========================= */
    label {
        font-size: 0.85rem;
        font-weight: 500;
        color: #344054;
    }

    /* =========================
        SEGMENTED CONTROL → VERTICAL
    ========================= */

    div[data-baseweb="button-group"] {
        flex-direction: column !important;   /* 🔥 KEY CHANGE */
        align-items: stretch;
        gap: 6px;
    }

    /* Each button full width */
    div[data-baseweb="button-group"] button {
        width: 100%;
        justify-content: flex-start;   /* left align text */
        text-align: left;
        padding: 10px 14px;
        border: 2px solid #7C3AED !important;
    }
        /* Container */
    div[data-baseweb="button-group"] {
        background: #F4F6F8;
        padding: 6px;
        border-radius: 12px;   /* not 999px for vertical */
        border: 1px solid #E0E3E7;
    }

    /* Buttons */
    div[data-baseweb="button-group"] button {
        border-radius: 50px !important;
        background: transparent;
        color: #344054;
        font-weight: 500;
        transition: all 0.2s ease;
    }

    /* Hover */
    div[data-baseweb="button-group"] button:hover {
        background: #EEF2F7;
    }

    /* Selected */
    div[data-baseweb="button-group"] button[aria-pressed="true"] {
        background: #7C3AED !important;
        color: blue !important;
    }
    
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 16px;
        border: 1px solid #E5E7EB;
        background: blue;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E5E7EB;
    }
        /* =========================
       ACTION PANEL BUTTONS
    ========================= */
    
    /* Default state */
    div[data-baseweb="button-group"] button {
        background: #FFFFFF;
        border: 2px solid #7C3AED;
        border-radius: 999px !important;
        color: #344054;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    /* Hover state */
    div[data-baseweb="button-group"] button:hover {
        background: rgba(124, 58, 237, 0.08);
        border-color: #7C3AED;
        color: #7C3AED;
    }
    
    /* Selected (ACTIVE) */
    div[data-baseweb="button-group"] button[aria-pressed="true"] {
        background: linear-gradient(135deg, #7C3AED, #6D28D9) !important;
        color: white !important;
        border: 2px solid #7C3AED !important;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.25);
    }
    </style>
    """, unsafe_allow_html=True)

