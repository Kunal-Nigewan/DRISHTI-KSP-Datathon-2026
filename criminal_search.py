import streamlit as st
import pandas as pd
from rapidfuzz import fuzz
import plotly.express as px

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="DRISHTI Intelligence System",
    page_icon="🕵️",
    layout="wide"
)

# ---------------- LOAD DATA ----------------

@st.cache_data
def load_data():

    accused = pd.read_csv("data/accused.csv")

    cases = pd.read_csv("data/case_master.csv")

    arrests = pd.read_csv("data/arrests.csv")

    return accused, cases, arrests

# ---------------- RISK BADGE ----------------

def get_risk_badge(severity):

    if severity == "CRITICAL":
        return "🔴 CRITICAL", "error"

    elif severity == "HIGH":
        return "🔴 HIGH", "error"

    elif severity == "MEDIUM":
        return "🟡 MEDIUM", "warning"

    else:
        return "🟢 LOW", "success"

# ---------------- THREAT ENGINE ----------------

def calculate_threat(person):

    total_cases = len(person)

    severity = person['CrimeSeverity'].iloc[0]

    status = person['Status'].iloc[0]

    threat_score = total_cases * 10

    if status == "Absconding":
        threat_score += 30

    if severity == "CRITICAL":
        threat_score += 40

    elif severity == "HIGH":
        threat_score += 25

    if threat_score >= 80:
        threat_level = "🚨 NATIONAL THREAT"

    elif threat_score >= 50:
        threat_level = "⚠️ HIGH RISK"

    else:
        threat_level = "👁️ MONITORED"

    return threat_score, threat_level

# ---------------- FUZZY SEARCH ----------------

def search_criminals(query, accused):

    if not query:
        return []

    results = []

    seen = []

    for _, row in accused.iterrows():

        name = str(row['AccusedName'])

        person_id = str(row['PersonID'])

        unique_key = f"{name}_{person_id}"

        if unique_key in seen:
            continue

        score = fuzz.partial_ratio(
            query.lower(),
            name.lower()
        )

        if score > 60:

            seen.append(unique_key)

            results.append({
                "name": name,
                "person_id": person_id
            })

    return results

# ---------------- QUICK STATS ----------------

def show_stats(accused, cases, arrests):

    st.markdown("## 📊 Intelligence Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    top_criminal = (
        accused['AccusedName']
        .value_counts()
        .index[0]
    )

    top_cases = (
        accused['AccusedName']
        .value_counts()
        .iloc[0]
    )

    absconding = len(
        accused[
            accused['Status'] == 'Absconding'
        ]
    )

    with col1:
        st.metric(
            "👥 Total Accused",
            len(accused)
        )

    with col2:
        st.metric(
            "📂 Total FIRs",
            len(cases)
        )

    with col3:
        st.metric(
            "🚨 Absconding",
            absconding
        )

    with col4:
        st.metric(
            "🔴 Most Dangerous",
            f"{top_criminal} ({top_cases})"
        )

    st.markdown("---")

# ---------------- AREA ANALYSIS ----------------

def show_area_analysis(cases):

    st.markdown("## 🗺️ Area Risk Intelligence")

    area_counts = (
        cases['Area']
        .value_counts()
        .reset_index()
    )

    area_counts.columns = ['Area', 'Cases']

    fig = px.bar(
        area_counts,
        x='Area',
        y='Cases',
        title="Crime Distribution by Area"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ---------------- CRIMINAL SEARCH ----------------

def show_criminal_search(accused, cases):

    st.markdown("## 🔍 Criminal Intelligence Search")

    st.markdown("---")

    query = st.text_input(
        "Search Criminal Name",
        placeholder="Enter criminal name..."
    )

    if query:

        matched_names = search_criminals(
            query,
            accused
        )

        if matched_names:

            st.success(
                f"Found {len(matched_names)} Criminal Record(s)"
            )

            # ---------------------------------------------------
            # LOOP
            # ---------------------------------------------------

            for criminal in matched_names:

                name = criminal["name"]

                person_id = criminal["person_id"]

                # IMPORTANT FIX
                person = accused[
                    (accused['AccusedName'] == name)
                    &
                    (accused['PersonID'] == person_id)
                ]

                crimes = person['CrimeType'].tolist()

                ipc_list = person[
                    'IPCSectionID'
                ].tolist()

                severity = person[
                    'CrimeSeverity'
                ].iloc[0]

                status = person[
                    'Status'
                ].iloc[0]

                case_ids = person[
                    'CaseMasterID'
                ].tolist()

                badge, color = get_risk_badge(
                    severity
                )

                threat_score, threat_level = (
                    calculate_threat(person)
                )

                latest_case = person.sort_values(
                    by="CaseMasterID",
                    ascending=False
                ).iloc[0]

                latest_crime = latest_case[
                    'CrimeType'
                ]

                latest_ipc = latest_case[
                    'IPCSectionID'
                ]

                latest_area = latest_case.get(
                    'Area',
                    'Unknown'
                )

                st.markdown("---")

                col1, col2 = st.columns([4,1])

                # ---------------- LEFT ----------------

                with col1:

                    st.markdown(
                        f"## 👤 {name}"
                    )

                    st.markdown(
                        f"**Person ID:** {person_id}"
                    )

                    st.markdown(
                        f"**Status:** {status}"
                    )

                    st.markdown(
                        f"**Threat Level:** {threat_level}"
                    )

                    st.markdown(
                        f"**Threat Score:** {threat_score}"
                    )

                    st.markdown(
                        f"**Latest Crime:** {latest_crime}"
                    )

                    st.markdown(
                        f"**Latest IPC:** IPC {latest_ipc}"
                    )

                    st.markdown(
                        f"**Latest Area:** {latest_area}"
                    )

                    st.markdown(
                        f"**Total Cases:** {len(person)}"
                    )

                    st.markdown(
                        f"**Crime Types:** "
                        f"{', '.join(set(crimes))}"
                    )

                    st.markdown(
                        f"**IPC Sections:** "
                        f"{', '.join(set(map(str, ipc_list)))}"
                    )

                    st.markdown(
                        f"**Case IDs:** "
                        f"{', '.join(map(str, case_ids))}"
                    )

                    # ---------------- ALERTS ----------------

                    if status == "Absconding":

                        st.error(
                            "🚨 ACTIVE FUGITIVE ALERT"
                        )

                    if len(person) >= 5:

                        st.error(
                            "🚨 HABITUAL OFFENDER"
                        )

                    if "Drug Trafficking" in crimes:

                        st.error(
                            "🚨 NARCOTICS MONITORING REQUIRED"
                        )

                # ---------------- RIGHT ----------------

                with col2:

                    if color == "error":

                        st.error(badge)

                    elif color == "warning":

                        st.warning(badge)

                    else:

                        st.success(badge)

                # ---------------- CASE DETAILS ----------------

                with st.expander(
                    "📂 View Detailed Criminal Records"
                ):

                    matched_cases = cases[
                        cases['CaseMasterID'].isin(
                            case_ids
                        )
                    ]

                    for _, row in matched_cases.iterrows():

                        st.markdown(
                            f"""
### 📁 Case {row['CaseNo']}

- Crime Type: {row['CrimeType']}
- IPC Section: {row['IPCSectionID']}
- Area: {row['Area']}
- Severity: {row['CrimeSeverity']}
- Date: {row['CrimeRegisteredDate']}
- Time: {row['CrimeTime']}

**Brief Facts:**  
{row['BriefFacts']}
"""
                        )

        else:

            st.warning(
                "No criminal records found."
            )

# ---------------- MAIN APP ----------------

def main():

    st.title(
        "🕵️ DRISHTI Criminal Intelligence System"
    )

    st.markdown(
        "AI Powered Criminal Intelligence Platform "
        "for Karnataka State Police"
    )

    st.markdown("---")

    try:

        accused, cases, arrests = load_data()

    except Exception as e:

        st.error(
            f"Database Load Error: {e}"
        )

        return

    # ---------------- DASHBOARD ----------------

    show_stats(
        accused,
        cases,
        arrests
    )

    # ---------------- AREA ANALYSIS ----------------

    show_area_analysis(cases)

    st.markdown("---")

    # ---------------- SEARCH ----------------

    show_criminal_search(
        accused,
        cases
    )

# ---------------- RUN ----------------

if __name__ == "__main__":

    main()