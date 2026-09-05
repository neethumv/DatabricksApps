import streamlit as st
import time
from databricks.sdk import WorkspaceClient

st.title("HR Genie Assistant")

SPACE_ID = "01f1a7cce8341affb459c8c51394741b"

question = st.text_input(
    "Ask a question about HR data:"
)

if st.button("Ask"):

    try:

        w = WorkspaceClient()

        # Create conversation and send first message
        response = w.api_client.do(
            "POST",
            f"/api/2.0/genie/spaces/{SPACE_ID}/start-conversation",
            body={
                "content": question
            }
        )

        conversation_id = response["conversation_id"]

        st.write("Conversation Created:")
        st.write(conversation_id)

        # Give Genie a few seconds
        time.sleep(5)

        # Read conversation messages
        messages = w.api_client.do(
            "GET",
            f"/api/2.0/genie/conversations/{conversation_id}/messages"
        )

        st.subheader("Conversation")

        st.json(messages)

    except Exception as e:

        st.error(str(e))
``
