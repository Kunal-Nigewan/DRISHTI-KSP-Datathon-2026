import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime

def show_crime_clock():
    st.markdown("## 🕐 Crime Analytics")
    st.markdown("---")

    try:
        cases = pd.read_csv("data/case_master.csv")
    except Exception as e:
        st.error(f"Data load error: {e}")
        return

    # Prepare time data
    cases['Hour'] = pd.to_datetime(
        cases['CrimeTime'],
        format='%H:%M',
        errors='coerce'
    ).dt.hour

    cases['Date'] = pd.to_datetime(
        cases['CrimeRegisteredDate'],
        errors='coerce'
    )
    cases['Weekday'] = cases['Date'].dt.day_name()

    # Current time
    now = datetime.now()
    current_hour = now.hour
    current_time = now.strftime("%I:%M:%S %p")

    top_area = cases['Area'].value_counts().index[0]
    top_crime = cases['CrimeType'].value_counts().index[0]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### Crime Analytics")
    with col2:
        st.metric("🕐 Current Time", current_time)
    with col3:
        if current_hour >= 20 or current_hour <= 4:
            st.error("🔴 HIGH RISK HOUR")
        elif current_hour >= 17:
            st.warning("🟡 MEDIUM RISK")
        else:
            st.success("🟢 LOW RISK")

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs([
        "🕐 Crime Clock",
        "📊 Distribution",
        "📍 Area Analysis",
        "📅 Weekday Analysis"
    ])

    # ---- TAB 1: CRIME CLOCK ----
    with tab1:
        hour_counts = cases.groupby(
            'Hour'
        ).size().reset_index(name='Count')
        hours_all = pd.DataFrame({'Hour': range(24)})
        hour_counts = hours_all.merge(
            hour_counts, on='Hour', how='left'
        ).fillna(0)

        hour_labels = [f"{h}:00" for h in range(24)]

        critical_cases = cases[cases['CrimeSeverity'] == 'CRITICAL']
        high_cases = cases[cases['CrimeSeverity'] == 'HIGH']
        medium_cases = cases[cases['CrimeSeverity'] == 'MEDIUM']

        def get_hour_counts(df):
            counts = df.groupby('Hour').size()
            return [counts.get(h, 0) for h in range(24)]

        fig = go.Figure()

        fig.add_trace(go.Barpolar(
            r=get_hour_counts(critical_cases),
            theta=hour_labels,
            name='Critical',
            marker_color='#ff3b30',
            opacity=0.9
        ))

        fig.add_trace(go.Barpolar(
            r=get_hour_counts(high_cases),
            theta=hour_labels,
            name='High',
            marker_color='#ff9500',
            opacity=0.8
        ))

        fig.add_trace(go.Barpolar(
            r=get_hour_counts(medium_cases),
            theta=hour_labels,
            name='Medium',
            marker_color='#ffd60a',
            opacity=0.7
        ))

        fig.update_layout(
            polar=dict(
                bgcolor="#1a1a2e",
                radialaxis=dict(
                    visible=True,
                    color="white",
                    gridcolor="#333355"
                ),
                angularaxis=dict(
                    color="white",
                    gridcolor="#333355",
                    direction="clockwise"
                )
            ),
            paper_bgcolor="#0e1117",
            font_color="white",
            showlegend=True,
            height=600,
            title=dict(
                text=f"Crime Clock — Current Hour: {current_hour}:00",
                font=dict(color="white", size=14)
            )
        )

        st.plotly_chart(fig, use_container_width=True)

        # Peak hour
        if not hour_counts.empty:
            peak_hour = int(
                hour_counts.loc[
                    hour_counts['Count'].idxmax(), 'Hour'
                ]
            )
            st.markdown(
                f"🕖 **Peak Crime Hour: {peak_hour}:00**"
            )

        # Most dangerous time window
        danger_hours = hour_counts.sort_values(
            by='Count', ascending=False
        ).head(3)

        st.error(
            f"🚨 Most Dangerous Time Window: "
            f"{int(danger_hours.iloc[0]['Hour'])}:00 — "
            f"{int(danger_hours.iloc[0]['Hour'])+1}:00"
        )

        st.markdown(f"📍 **{top_area} marked as current hotspot**")
        st.warning("🚨 Crime activity increases after 8 PM")

    # ---- TAB 2: DISTRIBUTION ----
    with tab2:
        st.markdown("### 📊 Crime Type Distribution")

        crime_counts = cases['CrimeType'].value_counts().reset_index()
        crime_counts.columns = ['Crime Type', 'Count']

        fig2 = px.bar(
            crime_counts,
            x='Crime Type',
            y='Count',
            color='Count',
            color_continuous_scale='Reds',
            title="Crime Types in Bengaluru"
        )
        fig2.update_layout(
            paper_bgcolor="#0e1117",
            plot_bgcolor="#0e1117",
            font_color="white",
            height=400
        )
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("### 🔴 Severity Breakdown")
        severity_counts = cases['CrimeSeverity'].value_counts()

        col1, col2 = st.columns(2)
        with col1:
            for sev, count in severity_counts.items():
                pct = count / len(cases)
                st.progress(pct)
                if sev == "CRITICAL":
                    st.error(f"🔴 {sev}: {count} cases")
                elif sev == "HIGH":
                    st.warning(f"🟠 {sev}: {count} cases")
                elif sev == "MEDIUM":
                    st.info(f"🟡 {sev}: {count} cases")
                else:
                    st.success(f"🟢 {sev}: {count} cases")

        with col2:
            fig3 = px.pie(
                values=severity_counts.values,
                names=severity_counts.index,
                color_discrete_map={
                    'CRITICAL': '#ff3b30',
                    'HIGH': '#ff9500',
                    'MEDIUM': '#ffd60a',
                    'LOW': '#32d74b'
                },
                title="Severity Distribution"
            )
            fig3.update_layout(
                paper_bgcolor="#0e1117",
                font_color="white",
                height=350
            )
            st.plotly_chart(fig3, use_container_width=True)

    # ---- TAB 3: AREA ANALYSIS ----
    with tab3:
        st.markdown("### 📍 Area Wise Crime Analysis")

        area_counts = cases['Area'].value_counts().reset_index()
        area_counts.columns = ['Area', 'Cases']

        fig4 = px.bar(
            area_counts,
            x='Area',
            y='Cases',
            color='Cases',
            color_continuous_scale='Reds',
            title="Crime Count by Area"
        )
        fig4.update_layout(
            paper_bgcolor="#0e1117",
            plot_bgcolor="#0e1117",
            font_color="white",
            height=400
        )
        st.plotly_chart(fig4, use_container_width=True)

        st.markdown("### 🔴 Hotspot Status")
        for _, row in area_counts.iterrows():
            if row['Cases'] >= 8:
                st.error(
                    f"🔴 {row['Area']}: {row['Cases']} cases"
                )
            elif row['Cases'] >= 5:
                st.warning(
                    f"🟡 {row['Area']}: {row['Cases']} cases"
                )
            else:
                st.success(
                    f"🟢 {row['Area']}: {row['Cases']} cases"
                )

    # ---- TAB 4: WEEKDAY ANALYSIS ----
    with tab4:
        st.markdown("### 📅 Crime Trend by Weekday")

        weekday_counts = (
            cases['Weekday']
            .value_counts()
            .reindex([
                'Monday', 'Tuesday', 'Wednesday',
                'Thursday', 'Friday', 'Saturday', 'Sunday'
            ])
            .fillna(0)
        )

        fig5 = px.line(
            x=weekday_counts.index,
            y=weekday_counts.values,
            markers=True,
            title="Crime Trend by Weekday",
            labels={'x': 'Day', 'y': 'Cases'}
        )
        fig5.update_traces(
            line_color='#ff4b4b',
            marker=dict(size=10, color='#ff9500')
        )
        fig5.update_layout(
            paper_bgcolor="#0e1117",
            plot_bgcolor="#0e1117",
            font_color="white",
            height=400
        )
        st.plotly_chart(fig5, use_container_width=True)

        # Peak weekday
        peak_day = weekday_counts.idxmax()
        peak_day_count = int(weekday_counts.max())

        st.error(
            f"🚨 Most Dangerous Day: "
            f"**{peak_day}** with {peak_day_count} cases"
        )

        st.markdown("---")

        # AI Intelligence Insights
        st.markdown("### 🤖 AI Intelligence Insights")
        st.info(
            f"""
• {top_area} is currently the highest crime hotspot.

• Crime activity sharply increases after evening hours.

• {top_crime} is the most repeated offense pattern.

• Critical severity crimes contribute significantly to nighttime activity.

• Peak criminal activity recorded on {peak_day}.

• Surveillance recommended between 8 PM and 1 AM.
            """
        )