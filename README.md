# 🚔 DRISHTI – Deep Recognition & Intelligence System

**AI-Powered Criminal Intelligence Platform for Karnataka State Police**

DRISHTI is an AI-powered criminal intelligence platform developed for the **Karnataka State Police Datathon 2026**. The platform addresses the challenge of fragmented crime records and time-consuming manual investigations by enabling officers to search criminal histories, identify criminal connections, analyse crime patterns, and support faster, data-driven policing through Artificial Intelligence and Machine Learning.

---

## 🚀 Key Features

- 🤖 AI Investigation Chatbot (Google Gemini)
- 🔍 Smart Criminal Search with Alias Matching
- 🕸️ Criminal Network Graph Visualization
- 🔗 Case Connection Analysis
- ⚠️ PRECOG Reoffending Risk Prediction
- 📊 Crime Analytics Dashboard
- 🕐 Crime Clock Analysis
- 🗺️ Crime Heatmap
- 📡 Live Intelligence Feed
- 🏢 Station Command Overview
- 👮 Role-Based Access Control (Constable, Inspector, DCP, Admin)

---

## 🛠️ Technology Stack

### Frontend
- Streamlit
- Custom CSS
- Streamlit Option Menu

### AI & Machine Learning
- Google Gemini 1.5 Flash
- Scikit-learn
- Pandas
- NumPy
- RapidFuzz

### Data Visualization
- Plotly
- NetworkX
- Pyvis

### Backend & Deployment
- Python
- Zoho Catalyst AppSail
- Python-dotenv

---

## 📂 Project Structure

```text
DRISHTI/
├── app.py
├── login.py
├── dashboard.py
├── chatbot.py
├── criminal_search.py
├── network_graph.py
├── case_connections.py
├── crime_clock.py
├── heatmap.py
├── precog.py
├── live_feed.py
├── all_stations.py
├── requirements.txt
└── data/
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/Kunal-Nigewan/DRISHTI-KSP-Datathon-2026.git
```

Move into the project directory:

```bash
cd DRISHTI-KSP-Datathon-2026
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root and add:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

---

## 🎯 Problem Statement

Police departments often rely on fragmented records and manual investigation processes, making it difficult to quickly identify criminal histories, connect related cases, analyse crime trends, and make timely operational decisions.

---

## 💡 Solution

DRISHTI provides an AI-powered criminal intelligence platform that centralises crime data, enables natural language criminal search, visualises criminal networks, predicts reoffending risk, analyses crime patterns, and assists officers with intelligent investigation support.

---

## 📸 Highlights

- AI-powered investigation assistant
- Intelligent criminal search with alias matching
- Interactive criminal network visualization
- Machine Learning based PRECOG Risk Prediction
- Crime Analytics Dashboard
- Crime Clock & Temporal Analysis
- Crime Heatmap
- Live Intelligence Feed
- Role-Based Police Dashboard

---

## 🚀 Future Scope

- Integration with real Karnataka Police databases
- Kannada voice assistant using Bhashini
- Mobile application for field officers
- Predictive patrol deployment
- Real-time multi-station crime intelligence

---

## 👥 Team

**Team CrimeX**

**Team Members**
- Kunal Nigewan
- Gagan HV
- Lokrannjan ND

---

## 📄 License

This project was developed for the **Karnataka State Police Datathon 2026** for educational and demonstration purposes.
