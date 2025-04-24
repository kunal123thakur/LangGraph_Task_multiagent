import streamlit as st
import pprint
from app import graph

st.set_page_config(page_title="LangGraph Planner Agent", layout="centered")

st.title("🧠 LangGraph Planning Agent")
st.markdown("Ask me a question and I’ll break it into tasks, use tools, and return a smart response!")

user_input = st.text_input("Your question", placeholder="E.g., Who is Virat Kohli?", key="input")

if st.button("Submit"):
    if not user_input:
        st.warning("Please enter a question before submitting.")
    else:
        # Set up initial state
        input_state = {
            "input": user_input,
            "task": "",
            "result": "",
            "history": []
        }

        st.subheader("🧩 Output Stream")
  
        output_placeholder = st.empty()

        result_str = ""
        for output in graph.stream(input_state):
            for key, value in output.items():
                formatted = f"\n📍 **Output from node `{key}`**\n---\n{pprint.pformat(value)}\n"
                result_str += formatted
                output_placeholder.code(result_str, language="python")
# hi