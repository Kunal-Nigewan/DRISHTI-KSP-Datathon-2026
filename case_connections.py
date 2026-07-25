import streamlit as st

def show_case_connections(cases_df, accused_df):

    st.markdown("# 🔗 Case Connections")
    st.markdown("AI-powered investigation relationship mapping")
    st.markdown("---")

    # CASE LIST
    case_list = cases_df["CaseNo"].astype(str).unique()

    selected_case = st.selectbox(
        "Select Case",
        case_list
    )

    # SELECTED CASE
    selected_data = cases_df[
        cases_df["CaseNo"].astype(str) == selected_case
    ]

    if selected_data.empty:
        st.error("Case not found")
        return

    case = selected_data.iloc[0]

    # CASE DETAILS
    st.markdown(f"## 📂 Case {case['CaseNo']}")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Crime Type:** {case['CrimeType']}")
        st.write(f"**Area:** {case['Area']}")

    with col2:
        st.write(f"**Severity:** {case['CrimeSeverity']}")
        st.write(f"**Police Station ID:** {case['PoliceStationID']}")

    st.write(f"**Brief Facts:** {case['BriefFacts']}")

    st.markdown("---")

    # CONNECTION LOGIC
    st.markdown("## 🔍 Related Cases")

    same_area_cases = cases_df[
        (cases_df["Area"] == case["Area"]) &
        (cases_df["CaseNo"] != case["CaseNo"])
    ]

    same_crime_cases = cases_df[
        (cases_df["CrimeType"] == case["CrimeType"]) &
        (cases_df["CaseNo"] != case["CaseNo"])
    ]

    # REMOVE DUPLICATES
    connected_cases = same_area_cases.merge(
        same_crime_cases,
        how="outer"
    )

    if connected_cases.empty:
        st.info("No connected cases found.")
    else:

        for _, row in connected_cases.iterrows():

            st.warning(f"""
Case No: {row['CaseNo']}

Crime Type: {row['CrimeType']}

Area: {row['Area']}

Severity: {row['CrimeSeverity']}
            """)