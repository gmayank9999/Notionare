import streamlit as st
from feature1_task_creator import process_user_input
from feature2_research_agent import process_research_goal

st.title("Notionaire Agent")
st.write("Welcome to your Notionaire Workspace! Use the input below to automatically add tasks to your Notion database.")

user_text = st.text_input("Tell the agent what's on your plate:")
if st.button("Run Task Agent") and user_text:
    with st.spinner("Agent is extracting tasks and writing to Notion..."):
        summary = process_user_input(user_text)
    st.success(summary)

st.markdown("---")
st.write("Or, ask the agent to research a topic for you:")

research_goal = st.text_input("Research goal:")
if st.button("Run Research Agent") and research_goal:
    with st.spinner("Agent is searching the web and compiling a Notion page..."):
        summary = process_research_goal(research_goal)
    st.success(summary)
