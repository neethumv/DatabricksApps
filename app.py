import streamlit as st
import traceback
from databricks.sdk import WorkspaceClient

st.title("Genie Test")

try:
    w = WorkspaceClient()

    SPACE_ID = "01f1a7cce8341affb459c8c51394741b"

    response = w.api_client.do(
        "POST",
        f"/api/2.0/genie/spaces/{SPACE_ID}/start-conversation",
        body={
            "content": "test"
        }
    )

    st.json(response)

except Exception as e:
    st.error(str(e))
    st.code(traceback.format_exc())
