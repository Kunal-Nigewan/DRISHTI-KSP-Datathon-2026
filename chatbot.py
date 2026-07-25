def show_chatbot():

    import streamlit as st
    import pandas as pd
    import google.generativeai as genai
    from dotenv import load_dotenv
    import os
    import time

    # ---------------------------------------------------
    # TYPING EFFECT
    # ---------------------------------------------------

    def typing_effect(text):

        placeholder = st.empty()

        displayed_text = ""

        for char in text:

            displayed_text += char

            placeholder.markdown(displayed_text)

            time.sleep(0.003)

        return placeholder

    # ---------------------------------------------------
    # LOAD API KEY
    # ---------------------------------------------------

    load_dotenv()

    genai.configure(
        api_key=os.getenv("GEMINI_API_KEY")
    )

    # ---------------------------------------------------
    # GEMINI MODEL
    # ---------------------------------------------------

    model = genai.GenerativeModel(
        "gemini-2.5-flash",
        generation_config={
            "temperature": 0.3
        }
    )

    # ---------------------------------------------------
    # LOAD DATA
    # ---------------------------------------------------

    accused = pd.read_csv("data/accused.csv")

    cases = pd.read_csv("data/case_master.csv")

    arrests = pd.read_csv("data/arrests.csv")

    # ---------------------------------------------------
    # UI
    # ---------------------------------------------------

    st.markdown(
        "## 🤖 DRISHTI Conversational Intelligence"
    )

    st.markdown(
        "AI Powered Criminal Intelligence Assistant"
    )

    st.markdown("---")

    # ---------------------------------------------------
    # EXAMPLE QUERIES
    # ---------------------------------------------------

    st.markdown("### 💡 Suggested Intelligence Queries")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            "Who is the most dangerous criminal?"
        )

    with col2:

        st.info(
            "Show absconding suspects"
        )

    with col3:

        st.info(
            "Drug trafficking suspects"
        )

    st.markdown("---")

    # ---------------------------------------------------
    # CHAT HISTORY
    # ---------------------------------------------------

    if "messages" not in st.session_state:

        st.session_state.messages = []

    # ---------------------------------------------------
    # INITIAL GREETING
    # ---------------------------------------------------

    if len(st.session_state.messages) == 0:

        greeting = """
🟢 **DRISHTI Intelligence Core Online**

Welcome Officer.

How may I assist your investigation today?
"""

        st.session_state.messages.append({
            "role": "assistant",
            "content": greeting
        })

    # ---------------------------------------------------
    # DISPLAY CHAT HISTORY
    # ---------------------------------------------------

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    # ---------------------------------------------------
    # CLEAR CHAT
    # ---------------------------------------------------

    if st.button("🗑️ Clear Intelligence Chat"):

        st.session_state.messages = []

        st.rerun()

    # ---------------------------------------------------
    # CHAT INPUT
    # ---------------------------------------------------

    query = st.chat_input(
        "Ask DRISHTI Intelligence System..."
    )

    # ---------------------------------------------------
    # PROCESS QUERY
    # ---------------------------------------------------

    if query:

        # ---------------------------------------------------
        # USER MESSAGE
        # ---------------------------------------------------

        st.session_state.messages.append({
            "role": "user",
            "content": query
        })

        with st.chat_message("user"):

            st.markdown(query)

        # ---------------------------------------------------
        # SMART MATCHING
        # ---------------------------------------------------

        matched_accused = accused[
            accused.astype(str).apply(
                lambda col: col.str.contains(
                    query,
                    case=False,
                    na=False
                )
            ).any(axis=1)
        ]

        matched_cases = cases[
            cases.astype(str).apply(
                lambda col: col.str.contains(
                    query,
                    case=False,
                    na=False
                )
            ).any(axis=1)
        ]

        matched_arrests = arrests[
            arrests.astype(str).apply(
                lambda col: col.str.contains(
                    query,
                    case=False,
                    na=False
                )
            ).any(axis=1)
        ]

        # ---------------------------------------------------
        # GREETING MODE
        # ---------------------------------------------------

        greetings = [
            "hi",
            "hello",
            "hey",
            "yo",
            "good morning",
            "good evening",
            "good afternoon"
        ]

        if query.lower().strip() in greetings:

            greeting_reply = """
🟢 DRISHTI Intelligence Core Active.

Hello Officer.

Available Intelligence Modules:
• Suspect Intelligence
• Criminal Network Analysis
• Threat Analytics
• FIR Intelligence
• Predictive Risk Assessment

Awaiting investigation query.
"""

            with st.chat_message("assistant"):

                typing_effect(greeting_reply)

                st.toast(
                    "🛰️ DRISHTI Core Activated",
                    icon="🚨"
                )

            st.session_state.messages.append({
                "role": "assistant",
                "content": greeting_reply
            })

            return

        # ---------------------------------------------------
        # NO RECORD FOUND
        # ---------------------------------------------------

        if (
            matched_accused.empty and
            matched_cases.empty and
            matched_arrests.empty
        ):

            no_record_reply = """
⚠️ No matching intelligence records found.

Please refine your query or check suspect details.
"""

            with st.chat_message("assistant"):

                typing_effect(no_record_reply)

                st.toast(
                    "⚠️ No intelligence records located",
                    icon="🚨"
                )

            st.session_state.messages.append({
                "role": "assistant",
                "content": no_record_reply
            })

            return

        # ---------------------------------------------------
        # CONTEXT
        # ---------------------------------------------------

        accused_context = matched_accused.to_string(
            index=False
        )

        cases_context = matched_cases.to_string(
            index=False
        )

        arrests_context = matched_arrests.to_string(
            index=False
        )

        # ---------------------------------------------------
        # PROMPT
        # ---------------------------------------------------

        prompt = f"""
You are DRISHTI AI.

An advanced criminal intelligence assistant
for Karnataka Police.

You must:
- analyze suspects
- identify threats
- explain criminal records
- answer naturally like ChatGPT
- behave professionally like police AI

IMPORTANT RULES:
- Never create fake criminals
- Use ONLY provided database
- Mention threat levels
- Mention criminal status
- Mention IPC sections if available
- Mention case counts correctly
- Be professional and intelligent

ACCUSED DATABASE:
{accused_context}

CASE DATABASE:
{cases_context}

ARREST DATABASE:
{arrests_context}

Officer Query:
{query}
"""

        # ---------------------------------------------------
        # AI RESPONSE
        # ---------------------------------------------------

        try:

            with st.chat_message("assistant"):

                with st.spinner(
                    "🛰️ Scanning criminal intelligence network..."
                ):

                    response = model.generate_content(
                        prompt
                    )

                    ai_response = response.text

                    typing_effect(ai_response)

                    st.toast(
                        "📡 Threat intelligence synchronized",
                        icon="🛰️"
                    )

                    st.toast(
                        "🟢 DRISHTI Intelligence Analysis Complete",
                        icon="🚨"
                    )

            # ---------------------------------------------------
            # SAVE RESPONSE
            # ---------------------------------------------------

            st.session_state.messages.append({
                "role": "assistant",
                "content": ai_response
            })

        except Exception as e:

            st.error(
                f"❌ Intelligence Error: {e}"
            )