import streamlit as st
import pandas as pd

# ---------------- LOAD DATA ---------------- #

def load_data():
    accused = pd.read_csv("data/accused.csv")
    arrests = pd.read_csv("data/arrests.csv")
    cases = pd.read_csv("data/case_master.csv")
    return accused, arrests, cases


# ---------------- RISK ENGINE ---------------- #

def calculate_risk_score(person, arrests):

    score = 0
    name = person['AccusedName'].iloc[0]

    # Total cases
    case_count = len(person)
    score += case_count * 12

    # Severity weight
    severity = person['CrimeSeverity'].iloc[0]

    if severity == "CRITICAL":
        score += 35
    elif severity == "HIGH":
        score += 25
    elif severity == "MEDIUM":
        score += 15
    else:
        score += 5

    # Status weight
    status = person['Status'].iloc[0]

    if status == "Absconding":
        score += 30
    elif status == "Released":
        score += 20
    elif status == "Under Surveillance":
        score += 12
    elif status == "Arrested":
        score += 5

    # Arrest history
    person_arrests = arrests[
        arrests['AccusedName'] == name
    ]

    score += len(person_arrests) * 5

    return min(score, 100)


# ---------------- RISK LEVEL ---------------- #

def get_risk_level(score):

    if score >= 80:
        return "🔴 CRITICAL THREAT", "critical"

    elif score >= 60:
        return "🟠 HIGH RISK", "high"

    elif score >= 40:
        return "🟡 MEDIUM RISK", "medium"

    else:
        return "🟢 LOW RISK", "low"


# ---------------- AI REASONING ---------------- #

def get_reasons(person):

    reasons = []

    case_count = len(person)
    severity = person['CrimeSeverity'].iloc[0]
    status = person['Status'].iloc[0]
    crimes = person['CrimeType'].tolist()

    # Repeat offender logic
    if case_count >= 5:
        reasons.append(
            f"Involved in {case_count} criminal cases — habitual offender"
        )

    elif case_count >= 3:
        reasons.append(
            f"{case_count} recorded cases — repeat offender pattern"
        )

    # Status logic
    if status == "Absconding":
        reasons.append(
            "Currently absconding — active fugitive"
        )

    elif status == "Released":
        reasons.append(
            "Recently released — high reoffend probability"
        )

    elif status == "Under Surveillance":
        reasons.append(
            "Under active police surveillance"
        )

    # Severity logic
    if severity == "CRITICAL":
        reasons.append(
            "Involved in critical severity crimes"
        )

    elif severity == "HIGH":
        reasons.append(
            "History of high severity offenses"
        )

    # Crime-specific reasoning
    if "Murder" in crimes:
        reasons.append(
            "History of violent crimes including murder"
        )

    if "Kidnapping" in crimes:
        reasons.append(
            "Kidnapping offense on record"
        )

    if "Drug Trafficking" in crimes:
        reasons.append(
            "Narcotics network involvement detected"
        )

    if "Cyber Fraud" in crimes:
        reasons.append(
            "Digital fraud activity identified"
        )

    if "Online Scam" in crimes:
        reasons.append(
            "Online scam pattern repeatedly detected"
        )

    if len(reasons) == 0:
        reasons.append(
            "Limited recent criminal activity"
        )

    return reasons


# ---------------- RECOMMENDED ACTION ---------------- #

def get_action(score):

    if score >= 80:
        return (
            "🚨 Immediate arrest recommended — "
            "national threat level"
        )

    elif score >= 60:
        return (
            "⚠️ Increase surveillance and "
            "patrol monitoring"
        )

    elif score >= 40:
        return (
            "👁️ Periodic monitoring recommended"
        )

    else:
        return (
            "📋 Maintain standard observation"
        )


# ---------------- HOTSPOTS ---------------- #

hotspots = [
    "Whitefield",
    "MG Road",
    "Indiranagar",
    "Hebbal",
    "Koramangala",
    "Jayanagar"
]


# ---------------- MAIN FUNCTION ---------------- #

def show_precog():

    st.markdown(
        "## ⚠️ PRECOG — Reoffend Prediction Engine"
    )

    st.markdown(
        "AI powered criminal threat intelligence and reoffend prediction system"
    )

    st.markdown("---")

    # Load data
    try:
        accused, arrests, cases = load_data()

    except Exception as e:
        st.error(f"Data load error: {e}")
        return

    # Unique criminals
    unique_names = accused[
        'AccusedName'
    ].unique()

    # Calculate scores
    all_scores = []

    for name in unique_names:

        person = accused[
            accused['AccusedName'] == name
        ]

        score = calculate_risk_score(
            person,
            arrests
        )

        all_scores.append({
            "name": name,
            "score": score,
            "status": person['Status'].iloc[0],
            "severity": person['CrimeSeverity'].iloc[0],
            "cases": len(person)
        })

    scores_df = pd.DataFrame(
        all_scores
    ).sort_values(
        by='score',
        ascending=False
    )

    # ---------------- SUMMARY ---------------- #

    critical = len(
        scores_df[scores_df['score'] >= 80]
    )

    high = len(
        scores_df[
            (scores_df['score'] >= 60) &
            (scores_df['score'] < 80)
        ]
    )

    medium = len(
        scores_df[
            (scores_df['score'] >= 40) &
            (scores_df['score'] < 60)
        ]
    )

    low = len(
        scores_df[scores_df['score'] < 40]
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.error(
            f"🔴 Critical Threat: {critical}"
        )

    with col2:
        st.error(
            f"🟠 High Risk: {high}"
        )

    with col3:
        st.warning(
            f"🟡 Medium Risk: {medium}"
        )

    with col4:
        st.success(
            f"🟢 Low Risk: {low}"
        )

    st.markdown("---")

    # ---------------- FILTERS ---------------- #

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:

        risk_filter = st.selectbox(
            "Filter by Risk",
            [
                "All",
                "Critical Threat",
                "High Risk",
                "Medium Risk",
                "Low Risk"
            ]
        )

    with filter_col2:

        status_filter = st.selectbox(
            "Filter by Status",
            [
                "All",
                "Absconding",
                "Released",
                "Arrested",
                "Under Surveillance"
            ]
        )

    st.markdown("---")

    # ---------------- RESULTS ---------------- #

    st.markdown(
        "### 🚨 AI Risk Assessment Results"
    )

    shown = 0

    for _, row in scores_df.iterrows():

        name = row['name']
        score = row['score']

        # Apply filters
        if risk_filter != "All":

            if (
                risk_filter == "Critical Threat"
                and score < 80
            ):
                continue

            elif (
                risk_filter == "High Risk"
                and not (60 <= score < 80)
            ):
                continue

            elif (
                risk_filter == "Medium Risk"
                and not (40 <= score < 60)
            ):
                continue

            elif (
                risk_filter == "Low Risk"
                and score >= 40
            ):
                continue

        if status_filter != "All":

            if row['status'] != status_filter:
                continue

        person = accused[
            accused['AccusedName'] == name
        ]

        crimes = person[
            'CrimeType'
        ].unique().tolist()

        ipc_list = person[
            'IPCSectionID'
        ].unique().tolist()

        reasons = get_reasons(person)

        action = get_action(score)

        risk_label, risk_type = get_risk_level(
            score
        )

        status = person['Status'].iloc[0]

        # ---------------- CARD ---------------- #

        with st.container():

            col1, col2, col3 = st.columns(
                [3, 1, 1]
            )

            # LEFT INFO
            with col1:

                st.markdown(
                    f"### 👤 {name}"
                )

                st.markdown(
                    f"**Status:** {status}"
                )

                st.markdown(
                    f"**Total Cases:** {row['cases']}"
                )

                st.markdown(
                    f"**Crimes:** "
                    f"{', '.join(set(crimes))}"
                )

                st.markdown(
                    f"**IPC Sections:** "
                    f"{', '.join(set(map(str, ipc_list)))}"
                )

            # CENTER METRICS
            with col2:

                st.metric(
                    "Risk Score",
                    f"{score}/100"
                )

                st.metric(
                    "Reoffend %",
                    f"{score}%"
                )

            # RIGHT RISK LABEL
            with col3:

                if risk_type == "critical":
                    st.error(risk_label)

                elif risk_type == "high":
                    st.error(risk_label)

                elif risk_type == "medium":
                    st.warning(risk_label)

                else:
                    st.success(risk_label)

            # Progress
            st.progress(score / 100)

            # Threat meter
            if score >= 80:
                st.error(
                    f"Threat Level: {score}%"
                )

            elif score >= 60:
                st.warning(
                    f"Threat Level: {score}%"
                )

            else:
                st.success(
                    f"Threat Level: {score}%"
                )

            # ---------------- AI REASONING ---------------- #

            st.markdown(
                "### 🧠 AI Reasoning"
            )

            for reason in reasons:
                st.markdown(f"• {reason}")

            # ---------------- ACTION ---------------- #

            st.info(action)

            # ---------------- HOTSPOT WARNING ---------------- #

            area_cases = person.merge(
                cases[
                    ['CaseMasterID', 'Area']
                ],
                on='CaseMasterID',
                how='left'
            )

            areas = area_cases[
                'Area'
            ].dropna().tolist()

            for area in areas:

                if area in hotspots:

                    st.warning(
                        f"⚠️ Active in {area} — "
                        f"current hotspot zone"
                    )

                    break

            st.markdown("---")

            shown += 1

            if shown >= 15:

                st.info(
                    "Showing top 15 criminals — "
                    "use filters for more"
                )

                break