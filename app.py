import streamlit as st
from databricks.sdk import WorkspaceClient

st.title("HR Genie Assistant")

question = st.text_input(
    "Ask a question about HR data:"
)

if st.button("Ask"):

    try:

        w = WorkspaceClient()

        SPACE_ID = "01f1a7cce8341affb459c8c51394741b"

        # Start conversation
        conv = w.api_client.do(
            "POST",
            f"/api/2.0/genie/spaces/{SPACE_ID}/start-conversation"
        )

        conversation_id = conv["conversation_id"]

        # Send question
        response = w.api_client.do(
            "POST",
            f"/api/2.0/genie/conversations/{conversation_id}/messages",
            body={
                "message": question
            }
        )

        st.subheader("Answer")

        st.write(response)

    except Exception as e:

        st.error(str(e))
