import streamlit as st
import os
import pprint
from app import graph

# Streamlit page config
st.set_page_config(page_title="LangGraph Planner Agent", layout="centered")

# --- Sidebar: GROQ API Key ---
st.sidebar.title("🔐 Enter GROQ API Key")
groq_api_key = st.sidebar.text_input("GROQ_API_KEY", type="password", help="Paste your GROQ key to run the agent.")

if groq_api_key:
    os.environ["GROQ_API_KEY"] = groq_api_key

# --- Main UI ---
st.title("🧠 LangGraph Planning Agent")
st.markdown("Ask me a question and I’ll break it into tasks, use tools, and return a smart response!")

user_input = st.text_input("Your question", placeholder="E.g., Who is Virat Kohli?", key="input")

# --- Submission ---
if st.button("Submit"):
    if not groq_api_key:
        st.warning("Please enter your GROQ API Key in the sidebar.")
    elif not user_input:
        st.warning("Please enter a question before submitting.")
    else:
        # Initialize state
        input_state = {
            "input": user_input,
            "task": "",
            "result": "",
            "history": []
        }

        st.subheader("🧩 Output Stream")

        output_placeholder = st.empty()
        result_str = ""

        try:
            for output in graph.stream(input_state):
                for key, value in output.items():
                    formatted = f"\n📍 **Output from node `{key}`**\n---\n{pprint.pformat(value)}\n"
                    result_str += formatted
                    output_placeholder.code(result_str, language="python")

            st.success("✅ Agent run completed!")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
