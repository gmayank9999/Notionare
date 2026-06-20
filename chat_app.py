import streamlit as st
from feature1_task_creator import process_user_input

st.title("Notionaire Agent")
st.write("Welcome to your Notionaire Workspace! Use the input below to automatically add tasks to your Notion database.")

user_text = st.text_input("Tell the agent what's on your plate:")
if st.button("Run Agent") and user_text:
    with st.spinner("Agent is extracting tasks and writing to Notion..."):
        summary = process_user_input(user_text)
    st.success(summary)
