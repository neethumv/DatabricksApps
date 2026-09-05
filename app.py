import streamlit as st
import traceback
from databricks.sdk import WorkspaceClient

st.title("HR Genie Assistant")

SPACE_ID = "01f1a7cce8341affb459c8c51394741b"

question = st.text_input(
    "Ask a question about HR data:"
)

if st.button("Ask"):

    try:

        w = WorkspaceClient()

        response = w.api_client.do(
            "POST",
            f"/api/2.0/genie/spaces/{SPACE_ID}/start-conversation",
            body={"content": question}
        )

        st.success("Question submitted")

        st.subheader("Create Conversation Response")
        st.json(response)

        conversation_id = response["conversation_id"]

        st.write(f"Conversation ID: {conversation_id}")

        # Test endpoint
        test = w.api_client.do(
            "GET",
            f"/api/2.0/genie/spaces/{SPACE_ID}"
        )

        st.subheader("Space Response")
        st.json(test)

    except Exception as e:
        st.error(str(e))
        st.code(traceback.format_exc())
