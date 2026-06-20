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

st.markdown("---")
st.write("Or, describe a project idea and the agent will plan the whole thing:")

idea = st.text_input("Project idea (e.g. 'Build a food delivery app'):")
if st.button("Generate Workspace") and idea:
    with st.spinner("Agent is planning the project and generating a full workspace..."):
        from feature4_workspace_generator import process_workspace_idea
        summary = process_workspace_idea(idea)
    st.success(summary)
st.markdown("---")
st.write("### Chat with your Workspace (RAG)")
st.write("Ask questions about your research and PRDs.")

rag_query = st.text_input("Ask a question:")
if st.button("Ask Notionaire") and rag_query:
    with st.spinner("Reading Notion databases and generating answer..."):
        from feature5_rag_chat import process_rag_chat
        answer = process_rag_chat(rag_query)
    st.info(answer)

st.markdown("---")
st.write("### Project Monitor")
st.write("Scan your tasks for any high-priority scheduling conflicts.")

if st.button("Run Conflict Monitor"):
    with st.spinner("Scanning tasks for conflicts..."):
        from feature3_monitor import get_open_tasks, detect_conflicts, post_alert
        tasks = get_open_tasks()
        alerts = detect_conflicts(tasks)
        if alerts:
            for alert in alerts:
                post_alert(alert)
                st.warning(alert)
            st.error(f"Found {len(alerts)} conflicts and logged them to Notion.")
        else:
            st.success("No scheduling conflicts detected! Your workspace is healthy.")
