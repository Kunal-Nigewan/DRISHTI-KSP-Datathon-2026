import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
from collections import Counter
import tempfile

def show_network_graph():

    st.markdown("""
    # 🕸 Criminal Intelligence Network

    Visual intelligence mapping of criminals, cases, and shared criminal activity.
    """)

    st.markdown("---")

    # LOAD DATA
    accused = pd.read_csv("data/accused.csv")
    cases = pd.read_csv("data/case_master.csv")

    # STATS
    total_criminals = accused['AccusedName'].nunique()
    total_cases = cases['CaseNo'].nunique()
    critical = len(accused[accused['CrimeSeverity'] == "CRITICAL"])
    absconding = len(accused[accused['Status'] == "Absconding"])

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("👤 Criminals", total_criminals)

    with col2:
        st.metric("📁 Cases", total_cases)

    with col3:
        st.metric("🔴 Critical", critical)

    with col4:
        st.metric("🚨 Absconding", absconding)

    st.markdown("---")

    # SEARCH
    focus = st.text_input(
        "🎯 Intelligence Focus Search",
        placeholder="Track suspect, gang, or repeat offender..."
    )

    # GRAPH
    G = nx.Graph()

    # CRIMINAL NODES
    for name in accused['AccusedName'].unique():

        person = accused[accused['AccusedName'] == name]

        case_count = len(person)

        severity = person['CrimeSeverity'].iloc[0]

        status = person['Status'].iloc[0]

        if severity == "CRITICAL":
            color = "#ff3b30"

        elif severity == "HIGH":
            color = "#ff9500"

        elif severity == "MEDIUM":
            color = "#ffd60a"

        else:
            color = "#32d74b"

        node_size = 20 + (case_count * 4)

        title = f"""
        <b>{name}</b><br>
        Cases: {case_count}<br>
        Severity: {severity}<br>
        Status: {status}
        """

        G.add_node(
            name,
            color=color,
            size=node_size,
            title=title
        )

    # CASE NODES
    for _, case in cases.iterrows():

        case_node = f"Case {case['CaseNo']}"

        title = f"""
        <b>{case['CaseNo']}</b><br>
        Crime: {case['CrimeType']}<br>
        Area: {case['Area']}<br>
        Severity: {case['CrimeSeverity']}
        """

        G.add_node(
            case_node,
            color="#64d2ff",
            size=10,
            title=title
        )

    # CRIMINAL -> CASE CONNECTIONS
    for _, acc in accused.iterrows():

        matched_case = cases[
            cases['CaseMasterID'] == acc['CaseMasterID']
        ]

        if not matched_case.empty:

            case_no = matched_case.iloc[0]['CaseNo']

            case_node = f"Case {case_no}"

            G.add_edge(
                acc['AccusedName'],
                case_node,
                color="#7d8597",
                width=1
            )

    # CRIMINAL -> CRIMINAL CONNECTIONS
    grouped = accused.groupby('CaseMasterID')

    for _, group in grouped:

        criminals = group['AccusedName'].unique()

        if len(criminals) > 1:

            for i in range(len(criminals)):

                for j in range(i + 1, len(criminals)):

                    G.add_edge(
                        criminals[i],
                        criminals[j],
                        color="#ff453a",
                        width=2
                    )

    # FOCUS FILTER
    if focus:

        focus = focus.lower()

        filtered_nodes = []

        for node in G.nodes():

            if focus in str(node).lower():

                filtered_nodes.append(node)

                filtered_nodes.extend(list(G.neighbors(node)))

        subgraph = G.subgraph(filtered_nodes)

    else:
        subgraph = G

    # PYVIS NETWORK
    net = Network(
        height="850px",
        width="100%",
        bgcolor="#0e1117",
        font_color="white"
    )

    net.from_nx(subgraph)

    # SMOOTH INTERACTION
    net.repulsion(
        node_distance=160,
        central_gravity=0.25,
        spring_length=140,
        spring_strength=0.06,
        damping=0.09
    )

    # INTERACTION + PHYSICS
    net.set_options("""
    var options = {

      "interaction": {
        "hover": true,
        "dragNodes": true,
        "dragView": true,
        "zoomView": true,
        "navigationButtons": true,
        "keyboard": true
      },

      "physics": {
        "enabled": true,
        "solver": "forceAtlas2Based",

        "forceAtlas2Based": {
          "gravitationalConstant": -50,
          "centralGravity": 0.02,
          "springLength": 140,
          "springConstant": 0.08
        },

        "minVelocity": 0.75
      },

      "edges": {
        "smooth": {
          "type": "dynamic"
        }
      }
    }
    """)

    # SAVE GRAPH
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:

        net.save_graph(tmp.name)

        html = open(tmp.name, "r", encoding="utf-8").read()

    # SHOW GRAPH
    components.html(html, height=900)

    st.markdown("---")

    # LEGEND
    st.success("""
🟢 Green = Low Risk

🟡 Yellow = Medium Risk

🟠 Orange = High Risk

🔴 Red = Critical Criminal

🔵 Blue = Cases

🔗 Red Criminal-to-Criminal Links = Shared Case Connections

📌 Larger Nodes = More Criminal Activity

🖱 Hover on nodes to inspect intelligence details
""")

    st.markdown("## 🧠 Intelligence Insights")

    col1, col2 = st.columns(2)

    # TOP OFFENDERS
    offender_counts = accused['AccusedName'].value_counts().head(5)

    with col1:

        st.warning("🚨 Top Repeat Offenders")

        for name, count in offender_counts.items():

            st.markdown(f"- **{name}** → {count} cases")

    # HOTSPOTS
    hotspot_counts = cases['Area'].value_counts().head(5)

    with col2:

        st.info("📍 Crime Hotspots")

        for area, count in hotspot_counts.items():

            st.markdown(f"- **{area}** → {count} cases")