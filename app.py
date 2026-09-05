import streamlit as st
from databricks.sdk import WorkspaceClient

st.set_page_config(page_title="HR Genie Assistant")

st.title("HR Genie Assistant")

question = st.text_input(
    "Ask a question about HR data:"
)

if st.button("Ask"):

    if not question.strip():
        st.warning("Please enter a question.")
    else:

        try:
            w = WorkspaceClient()

            # Replace with your Genie Space ID
            SPACE_ID = "01f1a7cce8341affb459c8c51394741b"

            # Create conversation
            conversation = w.api_client.do(
                "POST",
                f"/api/2.0/genie/spaces/{SPACE_ID}/start-conversation"
            )

            st.write("Conversation Response:")
            st.json(conversation)

            conversation_id = (
                conversation.get("conversation_id")
                or conversation.get("id")
            )

            # Submit question
            payload = {
                "content": question
            }

            response = w.api_client.do(
                "POST",
                f"/api/2.0/genie/conversations/{conversation_id}/messages",
                body=payload
            )

            st.subheader("Genie Response")
            st.json(response)

        except Exception as e:
            st.error(f"Error: {str(e)}")
