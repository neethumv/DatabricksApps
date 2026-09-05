import streamlit as st
from databricks.sdk import WorkspaceClient

st.title("Genie Test")

try:
    w = WorkspaceClient()

    SPACE_ID = "01f1a7cce8341affb459c8c51394741b"

    conversation = w.api_client.do(
        "POST",
        f"/api/2.0/genie/spaces/{SPACE_ID}/start-conversation"
    )

    st.write("Conversation Response")
    st.json(conversation)

except Exception as e:
    st.error(str(e))
