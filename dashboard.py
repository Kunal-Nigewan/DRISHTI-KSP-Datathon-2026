import streamlit as st
import pandas as pd
from datetime import datetime

def show_dashboard(role):

    try:
        cases = pd.read_csv("data/case_master.csv")
        accused = pd.read_csv("data/accused.csv")
        arrests = pd.read_csv("data/arrests.csv")
        units = pd.read_csv("data/units.csv")
    except Exception as e:
        st.error(f"Data load error: {e}")
        return

    # Real calculations
    total_firs = len(cases)
    total_accused = len(accused['AccusedName'].unique())
    absconding = len(accused[accused['Status'] == 'Absconding'])
    released = len(accused[accused['Status'] == 'Released'])
    critical = len(cases[cases['CrimeSeverity'] == 'CRITICAL'])
    high = len(cases[cases['CrimeSeverity'] == 'HIGH'])
    medium = len(cases[cases['CrimeSeverity'] == 'MEDIUM'])
    top_area = cases['Area'].value_counts().index[0]
    top_crime = cases['CrimeType'].value_counts().index[0]

    # Header
    if role == "Admin":
        st.markdown("## 🖥️ DRISHTI Control Room")
    else:
        st.markdown("## 📊 DRISHTI Dashboard")

    st.markdown(
        f"*{datetime.now().strftime('%A, %d %B %Y — %I:%M %p')}*"
    )
    st.markdown("---")

    # AI Briefing
    st.error(
        f"📋 AI BRIEFING: {top_crime} cases rising in "
        f"{top_area}. {absconding} criminals currently "
        f"absconding. Immediate surveillance recommended."
    )

    st.markdown("---")

    # Row 1 — Core stats
    st.markdown("### 📊 Live Intelligence Summary")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📋 Total FIRs", total_firs)
    with col2:
        st.metric("👤 Total Accused", total_accused)
    with col3:
        st.metric("🚨 Absconding", absconding)
    with col4:
        st.metric("🔓 Released", released)

    st.markdown("---")

    # Threat distribution with progress bars
    st.markdown("### 🚨 Threat Distribution")

    col1, col2 = st.columns(2)

    with col1:
        st.progress(critical / total_firs)
        st.error(f"🔴 Critical Threat Cases: {critical}")

        st.progress(high / total_firs)
        st.warning(f"🟠 High Threat Cases: {high}")

        st.progress(medium / total_firs)
        st.info(f"🟡 Medium Threat Cases: {medium}")

    with col2:
        st.markdown("#### 📍 Area Wise Crime")
        area_counts = cases['Area'].value_counts()
        for area, count in area_counts.items():
            if count >= 8:
                st.error(f"🔴 {area}: {count} cases")
            elif count >= 5:
                st.warning(f"🟡 {area}: {count} cases")
            else:
                st.success(f"🟢 {area}: {count} cases")

    st.markdown("---")

    # Intelligence Alert Feed
    st.markdown("### 📡 Live Intelligence Alerts")

    alerts = [
        f"🚨 Repeat {top_crime} pattern detected in {top_area}",
        f"⚠️ {absconding} criminals currently absconding — surveillance required",
        f"🔍 {critical} critical severity cases active",
        f"👁️ Surveillance triggered on {released} recently released criminals",
        f"📍 {top_area} marked as primary crime hotspot"
    ]

    for alert in alerts:
        st.warning(alert)

    st.markdown("---")

    # Top 5 criminals
    st.markdown("### 🚨 Top 5 Most Wanted")
    top5 = accused['AccusedName'].value_counts().head(5)
    col1, col2 = st.columns(2)

    for idx, (name, count) in enumerate(top5.items()):
        person = accused[accused['AccusedName'] == name]
        status = person['Status'].iloc[0]
        severity = person['CrimeSeverity'].iloc[0]
        crimes = person['CrimeType'].unique().tolist()

        if idx % 2 == 0:
            with col1:
                if status == "Absconding":
                    st.error(
                        f"🔴 #{idx+1} {name}\n\n"
                        f"Cases: {count} | {status}\n\n"
                        f"Crimes: {', '.join(set(crimes))}"
                    )
                elif severity in ["CRITICAL", "HIGH"]:
                    st.warning(
                        f"🟠 #{idx+1} {name}\n\n"
                        f"Cases: {count} | {status}\n\n"
                        f"Crimes: {', '.join(set(crimes))}"
                    )
                else:
                    st.info(
                        f"🔵 #{idx+1} {name}\n\n"
                        f"Cases: {count} | {status}\n\n"
                        f"Crimes: {', '.join(set(crimes))}"
                    )
        else:
            with col2:
                if status == "Absconding":
                    st.error(
                        f"🔴 #{idx+1} {name}\n\n"
                        f"Cases: {count} | {status}\n\n"
                        f"Crimes: {', '.join(set(crimes))}"
                    )
                elif severity in ["CRITICAL", "HIGH"]:
                    st.warning(
                        f"🟠 #{idx+1} {name}\n\n"
                        f"Cases: {count} | {status}\n\n"
                        f"Crimes: {', '.join(set(crimes))}"
                    )
                else:
                    st.info(
                        f"🔵 #{idx+1} {name}\n\n"
                        f"Cases: {count} | {status}\n\n"
                        f"Crimes: {', '.join(set(crimes))}"
                    )

    st.markdown("---")

    # Admin only section
    if role == "Admin":
        st.markdown("### 👑 Admin Intelligence Panel")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🏢 Total Stations", len(units))
        with col2:
            st.metric("📁 Total Arrests", len(arrests))
        with col3:
            ipc_top = cases['IPCSectionID'].value_counts().index[0]
            st.metric("⚖️ Top IPC Section", f"IPC {ipc_top}")

        # Active stations
        st.markdown("### 🏢 Active Police Stations")
        for _, unit in units.iterrows():
            st.info(f"🚔 {unit['UnitName']}")