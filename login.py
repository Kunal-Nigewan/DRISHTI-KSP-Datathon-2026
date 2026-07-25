import streamlit as st

def show_login():

    # ---------------------------------------------------
    # SAFE CSS
    # ---------------------------------------------------

    st.markdown("""
    <style>

    .login-card {

        background: rgba(17, 24, 39, 0.88);

        padding: 30px;

        border-radius: 18px;

        border: 1px solid rgba(255,255,255,0.08);

        box-shadow:
        0 0 25px rgba(249,115,22,0.15);

    }

    .logo-title {

        text-align: center;

        color: #f97316;

        font-size: 42px;

        font-weight: 800;

        letter-spacing: 5px;

        margin-bottom: 0px;
    }

    .logo-sub {

        text-align: center;

        color: #d1d5db;

        font-size: 13px;

        letter-spacing: 2px;

        margin-top: 5px;

        margin-bottom: 25px;
    }

    .scanner {

        width: 100%;

        height: 2px;

        background:
        linear-gradient(
        90deg,
        transparent,
        #f97316,
        transparent
        );

        animation: scan 3s linear infinite;

        margin-bottom: 25px;
    }

    @keyframes scan {

        0% {
            transform: translateX(-100%);
        }

        100% {
            transform: translateX(100%);
        }
    }

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

        height: 48px;

        transition: 0.3s;
    }

    .stButton > button:hover {

        transform: translateY(-2px);

        box-shadow:
        0 0 20px rgba(249,115,22,0.45);
    }

    </style>
    """, unsafe_allow_html=True)

    # ---------------------------------------------------
    # HEADER
    # ---------------------------------------------------

    st.markdown("""
    <div class="scanner"></div>

    <h1 class="logo-title">
    🛰️ DRISHTI
    </h1>

    <p class="logo-sub">
    DEEP RECOGNITION & INTELLIGENCE SYSTEM
    </p>
    """, unsafe_allow_html=True)

    # ---------------------------------------------------
    # LOGIN CARD
    # ---------------------------------------------------

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        st.markdown('<div class="login-card">', unsafe_allow_html=True)

        st.markdown("""
        <h2 style='
        text-align:center;
        color:white;
        margin-bottom:0px;'>

        🔐 Secure Intelligence Access

        </h2>

        <p style='
        text-align:center;
        color:#9ca3af;
        margin-bottom:25px;'>

        Authorized Karnataka Police Personnel Only

        </p>
        """, unsafe_allow_html=True)

        officer_id = st.text_input(
            "Officer ID",
            placeholder="Enter Officer ID"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter Password"
        )

        role = st.selectbox(
            "Access Level",
            [
                "Select Role",
                "Constable",
                "Inspector",
                "DCP",
                "Admin"
            ]
        )

        st.write("")

        if st.button(
            "🚀 ACCESS INTELLIGENCE CORE",
            use_container_width=True
        ):

            if (
                officer_id
                and password
                and role != "Select Role"
            ):

                st.session_state.logged_in = True
                st.session_state.officer_id = officer_id
                st.session_state.role = role

                st.rerun()

            else:

                st.error(
                    "Please fill all fields"
                )

        st.warning(
            "⚠️ Unauthorized access attempts are monitored,tracked and logged by the Intelligence Core."
        )

        st.markdown("</div>", unsafe_allow_html=True)