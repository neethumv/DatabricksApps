import streamlit as st
import time
from databricks.sdk import WorkspaceClient

st.title("HR Genie Assistant")

SPACE_ID = "YOUR_SPACE_ID"

question = st.text_input(
    "Ask a question about HR data:"
)

if st.button("Ask"):

    try:

        w = WorkspaceClient()

        # Create conversation and submit question
        response = w.api_client.do(
            "POST",
            f"/api/2.0/genie/spaces/{SPACE_ID}/start-conversation",
            body={
                "content": question
            }
        )

        conversation_id = response["conversation_id"]

        st.write(f"Conversation ID: {conversation_id}")

        # Give Genie time to process
        time.sleep(5)

        # Get conversation details
        conversation = w.api_client.do(
            "GET",
            f"/api/2.0/genie/conversations/{conversation_id}"
        )

        st.subheader("Conversation Details")
        st.json(conversation)

    except Exception as e:
        st.error(str(e))
