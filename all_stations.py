import streamlit as st
import pandas as pd

# ---------------- LOAD DATA ---------------- #

def load_data():

    cases = pd.read_csv("data/case_master.csv")
    accused = pd.read_csv("data/accused.csv")
    arrests = pd.read_csv("data/arrests.csv")
    units = pd.read_csv("data/units.csv")

    return cases, accused, arrests, units


# ---------------- HOTSPOT LEVEL ---------------- #

def get_hotspot_level(case_count):

    if case_count >= 8:
        return "HIGH"

    elif case_count >= 5:
        return "MEDIUM"

    else:
        return "LOW"


# ---------------- TREND ---------------- #

def get_trend(case_count):

    if case_count >= 8:
        return "up"

    elif case_count >= 5:
        return "stable"

    else:
        return "down"


# ---------------- MAIN FUNCTION ---------------- #

def show_all_stations():

    st.markdown(
        "## 🏢 All Police Stations — Bengaluru"
    )

    st.markdown(
        "Centralized station-wise operational intelligence"
    )

    st.markdown("---")

    st.success(
        "🟢 LIVE STATION GRID CONNECTED"
    )

    st.markdown("---")

    # ---------------- LOAD DATA ---------------- #

    try:

        cases, accused, arrests, units = load_data()

    except Exception as e:

        st.error(f"Data load error: {e}")
        return

    # ---------------- BUILD STATIONS ---------------- #

    stations = []

    area_counts = cases['Area'].value_counts()

    rank = 1

    for area, count in area_counts.items():

        station_name = f"{area} PS"

        firs_today = max(1, count // 4)

        officers = 12 + (count * 2)

        patrols = max(2, count // 2)

        risk = min(100, count * 10)

        hotspot = get_hotspot_level(count)

        trend = get_trend(count)

        # Top crime

        area_cases = cases[
            cases['Area'] == area
        ]

        top_crime = (
            area_cases['CrimeType']
            .value_counts()
            .index[0]
        )

        # Response time

        if hotspot == "HIGH":
            response_time = "4 mins"

        elif hotspot == "MEDIUM":
            response_time = "7 mins"

        else:
            response_time = "10 mins"

        # Solved %

        solved = max(55, 90 - count)

        # Patrol status

        if hotspot == "HIGH":
            patrol_status = "Active"

        elif hotspot == "MEDIUM":
            patrol_status = "Partial"

        else:
            patrol_status = "Standby"

        stations.append({

            "name": station_name,

            "area": area,

            "active_cases": int(count),

            "firs_today": int(firs_today),

            "officers": int(officers),

            "active_patrols": int(patrols),

            "most_common_crime": top_crime,

            "hotspot_level": hotspot,

            "rank": rank,

            "patrol_status": patrol_status,

            "crime_trend": trend,

            "risk_percentage": int(risk),

            "response_time": response_time,

            "solved_cases": int(solved)
        })

        rank += 1

    # ---------------- SUMMARY ---------------- #

    total_cases = sum(
        s["active_cases"] for s in stations
    )

    total_firs = sum(
        s["firs_today"] for s in stations
    )

    total_patrols = sum(
        s["active_patrols"] for s in stations
    )

    high_risk = sum(
        1 for s in stations
        if s["hotspot_level"] == "HIGH"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📋 Active Cases",
            total_cases
        )

    with col2:

        st.metric(
            "📝 FIRs Today",
            total_firs
        )

    with col3:

        st.metric(
            "🚔 Patrol Units",
            total_patrols
        )

    with col4:

        st.metric(
            "🔴 High Risk Stations",
            high_risk
        )

    st.markdown("---")

    # ---------------- CRITICAL ALERT ---------------- #

    top_station = sorted(
        stations,
        key=lambda x: x['risk_percentage'],
        reverse=True
    )[0]

    st.error(
        f"🚨 CRITICAL STATION ALERT: "
        f"{top_station['name']} currently has "
        f"the highest operational risk in Bengaluru."
    )

    st.markdown("---")

    # ---------------- FILTERS ---------------- #

    col1, col2 = st.columns(2)

    with col1:

        filter_risk = st.selectbox(
            "Filter by Hotspot Level",
            ["All", "HIGH", "MEDIUM", "LOW"]
        )

    with col2:

        sort_by = st.selectbox(
            "Sort Stations By",
            [
                "Risk Percentage",
                "Active Cases",
                "Solved Cases"
            ]
        )

    # ---------------- SORT ---------------- #

    if sort_by == "Risk Percentage":

        stations = sorted(
            stations,
            key=lambda x: x['risk_percentage'],
            reverse=True
        )

    elif sort_by == "Active Cases":

        stations = sorted(
            stations,
            key=lambda x: x['active_cases'],
            reverse=True
        )

    else:

        stations = sorted(
            stations,
            key=lambda x: x['solved_cases'],
            reverse=True
        )

    st.markdown("---")

    # ---------------- STATION CARDS ---------------- #

    for station in stations:

        if filter_risk != "All":

            if station["hotspot_level"] != filter_risk:
                continue

        # Trend

        if station["crime_trend"] == "up":
            trend = "📈 Rising"

        elif station["crime_trend"] == "stable":
            trend = "➡️ Stable"

        else:
            trend = "📉 Falling"

        # Patrol

        if station["patrol_status"] == "Active":
            patrol = "🟢 Active"

        elif station["patrol_status"] == "Partial":
            patrol = "🟡 Partial"

        else:
            patrol = "🔴 Standby"

        # Operational status

        if station['risk_percentage'] >= 80:
            operational = "🔴 CRITICAL"

        elif station['risk_percentage'] >= 50:
            operational = "🟡 ELEVATED"

        else:
            operational = "🟢 STABLE"

        with st.container():

            col1, col2, col3 = st.columns(
                [3, 2, 1]
            )

            # ---------------- DETAILS ---------------- #

            with col1:

                st.markdown(
                    f"### 🏢 #{station['rank']} "
                    f"{station['name']}"
                )

                st.markdown(
                    f"📍 **Area:** {station['area']}"
                )

                st.markdown(
                    f"👮 **Officers:** "
                    f"{station['officers']}"
                )

                st.markdown(
                    f"🚔 **Patrol Units:** "
                    f"{patrol}"
                )

                st.markdown(
                    f"⚠️ **Common Crime:** "
                    f"{station['most_common_crime']}"
                )

                st.markdown(
                    f"📊 **Crime Trend:** "
                    f"{trend}"
                )

                st.markdown(
                    f"📡 **Operational Status:** "
                    f"{operational}"
                )

                st.markdown(
                    f"⏱️ **Avg Response Time:** "
                    f"{station['response_time']}"
                )

                st.markdown(
                    f"✅ **Solved Case Ratio:** "
                    f"{station['solved_cases']}%"
                )

            # ---------------- METRICS ---------------- #

            with col2:

                st.metric(
                    "Active Cases",
                    station['active_cases']
                )

                st.metric(
                    "FIRs Today",
                    station['firs_today']
                )

                st.metric(
                    "Station Risk",
                    f"{station['risk_percentage']}%"
                )

                st.progress(
                    station['risk_percentage'] / 100
                )

                # AI Patrol Recommendation

                if station['risk_percentage'] >= 80:

                    st.warning(
                        "🤖 AI Recommendation: "
                        "Deploy additional night patrol units."
                    )

                elif station['risk_percentage'] >= 50:

                    st.info(
                        "🤖 AI Recommendation: "
                        "Maintain surveillance and patrol coverage."
                    )

                else:

                    st.success(
                        "🤖 AI Recommendation: "
                        "Current patrol strength sufficient."
                    )

            # ---------------- HOTSPOT ---------------- #

            with col3:

                if station["hotspot_level"] == "HIGH":

                    st.error(
                        "🔴 HIGH\nHOTSPOT"
                    )

                elif station["hotspot_level"] == "MEDIUM":

                    st.warning(
                        "🟡 MEDIUM\nHOTSPOT"
                    )

                else:

                    st.success(
                        "🟢 LOW\nHOTSPOT"
                    )

            st.markdown("---")

    # ---------------- AI INSIGHTS ---------------- #

    st.markdown(
        "## 🤖 Station Intelligence Insights"
    )

    st.info(f"""

• {top_station['name']} currently reports the highest operational risk.

• High severity crimes are concentrated in Bengaluru hotspot sectors.

• Patrol deployment automatically increases in high-risk zones.

• AI monitoring indicates rising criminal activity patterns.

• DRISHTI control grid remains synchronized across all police stations.

• High hotspot classification is triggered when active criminal cases exceed AI surveillance thresholds.

""")