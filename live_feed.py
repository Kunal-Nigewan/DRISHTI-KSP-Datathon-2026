import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# ---------------- LOAD DATA ---------------- #

def load_data():
    cases = pd.read_csv("data/case_master.csv")
    accused = pd.read_csv("data/accused.csv")
    arrests = pd.read_csv("data/arrests.csv")
    return cases, accused, arrests


# ---------------- RANDOM TIMESTAMP ---------------- #

def generate_recent_timestamp(days_back=5):

    now = datetime.now()

    random_days = random.randint(0, days_back)
    random_hours = random.randint(0, 23)
    random_minutes = random.randint(0, 59)

    generated_time = now - timedelta(
        days=random_days,
        hours=random_hours,
        minutes=random_minutes
    )

    return generated_time.strftime("%d %b %Y %H:%M")


# ---------------- LIVE FEED ---------------- #

def show_live_feed():

    st.markdown("## 📡 Live Intelligence Feed")
    st.markdown(
        "Real-time operational crime intelligence monitor"
    )

    st.markdown("---")

    try:
        cases, accused, arrests = load_data()

    except Exception as e:
        st.error(f"Data load error: {e}")
        return

    # ---------------- SUMMARY STATS ---------------- #

    total_cases = len(cases)

    absconding = len(
        accused[accused['Status'] == 'Absconding']
    )

    critical = len(
        cases[cases['CrimeSeverity'] == 'CRITICAL']
    )

    top_area = cases['Area'].value_counts().index[0]

    # ---------------- LIVE STATUS ---------------- #

    st.success("⚪ LIVE MONITORING ACTIVE")

    st.markdown("---")

    # ---------------- TOP METRICS ---------------- #

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📋 Total FIRs", total_cases)

    with col2:
        st.error(f"🚨 Absconding: {absconding}")

    with col3:
        st.error(f"🔴 Critical: {critical}")

    with col4:
        st.warning(f"📍 Hotspot: {top_area}")

    st.markdown("---")

    # ---------------- STATE ALERT ---------------- #

    dangerous = accused[
        accused['Status'] == 'Absconding'
    ]

    if not dangerous.empty:

        criminal_name = dangerous.iloc[0]['AccusedName']

        st.error(
            f"🚨 STATEWIDE ALERT: "
            f"{criminal_name} identified as "
            f"high-priority repeat offender. "
            f"All Bengaluru units notified."
        )

    st.markdown("---")

    # ---------------- FILTERS ---------------- #

    col1, col2 = st.columns(2)

    with col1:

        priority_filter = st.selectbox(
            "Filter by Priority",
            ["All", "HIGH", "MEDIUM", "LOW"]
        )

    with col2:

        event_filter = st.selectbox(
            "Filter by Event Type",
            [
                "All",
                "FUGITIVE ALERT",
                "Critical FIR",
                "Arrest Made",
                "Hotspot Alert",
                "System"
            ]
        )

    st.markdown("---")

    # ---------------- EVENTS LIST ---------------- #

    events = []

    # ---------------- FUGITIVE ALERTS ---------------- #

    absconding_people = accused[
        accused['Status'] == 'Absconding'
    ]

    for _, row in absconding_people.head(5).iterrows():

        events.append({

            "time": generate_recent_timestamp(),

            "type": "🚨 FUGITIVE ALERT",

            "category": "FUGITIVE ALERT",

            "detail":
                f"{row['AccusedName']} linked to "
                f"{row['CrimeType']} activity in "
                f"{random.choice(cases['Area'].tolist())}. "
                f"Currently absconding.",

            "priority": "HIGH"
        })

    # ---------------- CRITICAL FIRS ---------------- #

    critical_cases = cases[
        cases['CrimeSeverity'] == 'CRITICAL'
    ]

    for _, case in critical_cases.head(8).iterrows():

        events.append({

            "time": generate_recent_timestamp(),

            "type": "🔴 Critical FIR",

            "category": "Critical FIR",

            "detail":
                f"Case {case['CaseNo']} — "
                f"{case['CrimeType']} — "
                f"{case['Area']} zone.",

            "priority": "HIGH"
        })

    # ---------------- ARREST EVENTS ---------------- #

    for _, arrest in arrests.head(6).iterrows():

        events.append({

            "time": generate_recent_timestamp(),

            "type": "✅ Arrest Made",

            "category": "Arrest Made",

            "detail":
                f"{arrest['AccusedName']} "
                f"taken into custody — "
                f"Case {arrest['CaseMasterID']}",

            "priority": "MEDIUM"
        })

    # ---------------- HOTSPOT ALERTS ---------------- #

    hotspot_areas = (
        cases['Area']
        .value_counts()
        .head(4)
    )

    for area, count in hotspot_areas.items():

        events.append({

            "time": generate_recent_timestamp(),

            "type": "📍 Hotspot Alert",

            "category": "Hotspot Alert",

            "detail":
                f"{area} reporting "
                f"{count} active criminal cases. "
                f"Increased patrol recommended.",

            "priority":
                "MEDIUM" if count >= 8 else "LOW"
        })

    # ---------------- SYSTEM EVENTS ---------------- #

    system_events = [

        "DRISHTI Intelligence Core — Online",

        "Criminal database synchronized — "
        "75 records active",

        "AI crime analytics engine operational",

        "Surveillance grid connected "
        "to Bengaluru control room",

        "PRECOG monitoring engine active",

        "All station nodes synchronized"
    ]

    for system in system_events:

        events.append({

            "time": generate_recent_timestamp(),

            "type": "🟢 System",

            "category": "System",

            "detail": system,

            "priority": "LOW"
        })

    # ---------------- SORT EVENTS ---------------- #

    events = sorted(

        events,

        key=lambda x: datetime.strptime(
            x['time'],
            "%d %b %Y %H:%M"
        ),

        reverse=True
    )

    # ---------------- ALERT COUNT ---------------- #

    st.metric(
        "🚨 Live Alerts",
        len(events)
    )

    st.markdown("---")

    # ---------------- DISPLAY EVENTS ---------------- #

    for event in events:

        # Priority filter

        if priority_filter != "All":

            if event['priority'] != priority_filter:
                continue

        # Event filter

        if event_filter != "All":

            if event['category'] != event_filter:
                continue

        col1, col2, col3 = st.columns([2, 8, 1])

        with col1:

            st.markdown(
                f"**{event['time']}**"
            )

        with col2:

            if event['priority'] == "HIGH":

                st.error(
                    f"{event['type']} — "
                    f"{event['detail']}"
                )

            elif event['priority'] == "MEDIUM":

                st.warning(
                    f"{event['type']} — "
                    f"{event['detail']}"
                )

            else:

                st.success(
                    f"{event['type']} — "
                    f"{event['detail']}"
                )

        with col3:

            st.markdown(
                f"**{event['priority']}**"
            )

    # ---------------- AI INSIGHTS ---------------- #

    st.markdown("---")

    st.markdown("## 👁️ AI Operational Insights")

    st.info(f"""

• {top_area} remains the most active crime hotspot.

• Fugitive activity currently requires intensified surveillance.

• Critical severity FIRs are increasing across Bengaluru sectors.

• PRECOG engine recommends increased patrol deployment in hotspot zones.

• AI monitoring systems remain active across all connected police units.

""")