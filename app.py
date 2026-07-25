import streamlit as st
import pandas as pd

from login import show_login
from streamlit_option_menu import option_menu

from dashboard import show_dashboard
from criminal_search import show_criminal_search
from network_graph import show_network_graph
from case_connections import show_case_connections
from crime_clock import show_crime_clock
from precog import show_precog
from live_feed import show_live_feed
from all_stations import show_all_stations
from chatbot import show_chatbot
from heatmap import show_heatmap

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="DRISHTI Intelligence System",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# PREMIUM SAFE CSS
# ---------------------------------------------------

st.markdown("""
<style>

/* ---------------------------------------------------
MAIN BACKGROUND
--------------------------------------------------- */

.main {

    background:
    radial-gradient(circle at top left,
    rgba(249,115,22,0.10),
    transparent 25%),

    radial-gradient(circle at bottom right,
    rgba(59,130,246,0.08),
    transparent 25%),

    #020617;

    color: white;
}

/* ---------------------------------------------------
SIDEBAR
--------------------------------------------------- */

section[data-testid="stSidebar"] {

    background:
    linear-gradient(
    180deg,
    #111827,
    #0f172a
    );

    border-right:
    1px solid rgba(255,255,255,0.06);
}

/* ---------------------------------------------------
METRIC CARDS
--------------------------------------------------- */

div[data-testid="stMetric"] {

    background:
    rgba(30,41,59,0.78);

    backdrop-filter: blur(10px);

    border-radius: 16px;

    padding: 16px;

    border:
    1px solid rgba(255,255,255,0.05);

    transition: all 0.3s ease;
}

div[data-testid="stMetric"]:hover {

    transform: translateY(-6px);

    box-shadow:
    0 8px 25px rgba(249,115,22,0.35);

    border:
    1px solid rgba(249,115,22,0.30);
}

/* ---------------------------------------------------
BUTTONS
--------------------------------------------------- */

.stButton > button {

    background:
    linear-gradient(
    135deg,
    #f97316,
    #ea580c
    );

    color: white;

    border: none;

    border-radius: 10px;

    font-weight: 700;

    transition: 0.3s;
}

.stButton > button:hover {

    transform: scale(1.03);

    box-shadow:
    0 0 20px rgba(249,115,22,0.45);
}

/* ---------------------------------------------------
OPTION MENU
--------------------------------------------------- */

.nav-link {

    border-radius: 10px;

    transition: 0.3s;
}

.nav-link:hover {

    background-color:
    #1e293b !important;

    transform: translateX(3px);
}

/* ---------------------------------------------------
SELECTED MENU
--------------------------------------------------- */

.nav-link-selected {

    background:
    linear-gradient(
    135deg,
    #f97316,
    #ea580c
    ) !important;

    font-weight: 700 !important;

    box-shadow:
    0 0 18px rgba(249,115,22,0.35);
}

/* ---------------------------------------------------
CHAT MESSAGES
--------------------------------------------------- */

div[data-testid="stChatMessage"] {

    background:
    rgba(30,41,59,0.75);

    border-radius: 14px;

    border:
    1px solid rgba(255,255,255,0.06);

    padding: 10px;
}

/* ---------------------------------------------------
SCROLLBAR
--------------------------------------------------- */

::-webkit-scrollbar {

    width: 6px;
}

::-webkit-scrollbar-thumb {

    background: #f97316;

    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data
def load_data():

    accused = pd.read_csv(
        "data/accused.csv"
    )

    cases = pd.read_csv(
        "data/case_master.csv"
    )

    arrests = pd.read_csv(
        "data/arrests.csv"
    )

    return accused, cases, arrests

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False

# ---------------------------------------------------
# LOGIN
# ---------------------------------------------------

if not st.session_state.logged_in:

    show_login()

# ---------------------------------------------------
# MAIN APP
# ---------------------------------------------------

else:

    accused, cases, arrests = load_data()

    role = st.session_state.role

    # ---------------------------------------------------
    # SIDEBAR
    # ---------------------------------------------------

    with st.sidebar:

        st.markdown("""

# 🛰️ DRISHTI
### Intelligence Core

""")

        st.markdown("""

<div style="
height:2px;
background:linear-gradient(
90deg,
transparent,
#f97316,
transparent
);
margin-bottom:20px;
"></div>

""", unsafe_allow_html=True)

        st.success(
            f"👮 Officer: {st.session_state.officer_id}"
        )

        st.info(
            f"🛡️ Role: {role}"
        )

        st.markdown("---")

        # ---------------------------------------------------
        # ROLE MENUS
        # ---------------------------------------------------

        if role == "Constable":

            options = [
                "Dashboard",
                "Chatbot",
                "Criminal Search"
            ]

            icons = [
                "house",
                "robot",
                "search"
            ]

        elif role == "Inspector":

            options = [
                "Dashboard",
                "Chatbot",
                "Criminal Search",
                "Network Graph",
                "Case Connections"
            ]

            icons = [
                "house",
                "robot",
                "search",
                "diagram-3",
                "link"
            ]

        elif role == "DCP":

            options = [
                "Dashboard",
                "Chatbot",
                "Criminal Search",
                "Network Graph",
                "Heatmap",
                "PRECOG"
            ]

            icons = [
                "house",
                "robot",
                "search",
                "diagram-3",
                "map",
                "activity"
            ]

        else:

            options = [
                "Dashboard",
                "Chatbot",
                "Criminal Search",
                "Network Graph",
                "Case Connections",
                "Crime Clock",
                "Heatmap",
                "PRECOG",
                "Live Feed",
                "All Stations"
            ]

            icons = [
                "house",
                "robot",
                "search",
                "diagram-3",
                "link",
                "clock",
                "map",
                "activity",
                "broadcast",
                "building"
            ]

        # ---------------------------------------------------
        # OPTION MENU
        # ---------------------------------------------------

        selected = option_menu(

            menu_title="Navigation",

            options=options,

            icons=icons,

            default_index=0,

            styles={

                "container": {

                    "background-color": "#111827",

                    "padding": "5px"
                },

                "icon": {

                    "color": "#fb923c",

                    "font-size": "18px"
                },

                "nav-link": {

                    "font-size": "15px",

                    "text-align": "left",

                    "margin": "4px",

                    "border-radius": "10px"
                },

                "nav-link-selected": {

                    "background":
                    "linear-gradient(135deg,#f97316,#ea580c)",

                    "font-weight": "700"
                }
            }
        )

        st.markdown("---")

        st.markdown("### 🛰️ System Status")

        st.success("🟢 Intelligence Core Online")

        st.success("🟢 Criminal Database Active")

        st.success("🟢 PRECOG Engine Running")

        st.warning(
            f"🚨 Active FIRs: {len(cases)}"
        )

        st.warning(
            f"👤 Criminal Records: {len(accused)}"
        )

        critical_cases = len(
            cases[
                cases["CrimeSeverity"] == "CRITICAL"
            ]
        )

        st.error(
            f"🚨 Critical Cases: {critical_cases}"
        )

        st.markdown("---")

        # ---------------------------------------------------
        # LOGOUT
        # ---------------------------------------------------

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            st.session_state.logged_in = False

            st.rerun()

    # ---------------------------------------------------
    # PAGE ROUTING
    # ---------------------------------------------------

    if selected == "Dashboard":

        show_dashboard(role)

    elif selected == "Chatbot":

        show_chatbot()

    elif selected == "Criminal Search":

        show_criminal_search(
            accused,
            cases
        )

    elif selected == "Network Graph":

        show_network_graph()

    elif selected == "Case Connections":

        show_case_connections(cases,accused)

    elif selected == "Crime Clock":

        show_crime_clock()

    elif selected == "Heatmap":

        show_heatmap()

    elif selected == "PRECOG":

        show_precog()

    elif selected == "Live Feed":

        show_live_feed()

    elif selected == "All Stations":

        show_all_stations()

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.caption(
    "DRISHTI Intelligence Core v3.0"
)