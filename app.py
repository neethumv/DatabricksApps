import streamlit as st
from databricks.sdk import WorkspaceClient

st.set_page_config(
    page_title="HR Genie Assistant",
    layout="wide"
)

SPACE_ID = "01f1a7cce8341affb459c8c51394741b"

st.title("HR Genie Assistant")

question = st.text_input(
    "Ask a question about HR data:",
    placeholder="How many active employees do we have?"
)

if st.button("Ask"):

    if not question.strip():
        st.warning("Please enter a question.")
        st.stop()

    try:

        w = WorkspaceClient()

        response = w.api_client.do(
            "POST",
            f"/api/2.0/genie/spaces/{SPACE_ID}/start-conversation",
            body={
                "content": question
            }
        )

        conversation_id = response.get("conversation_id")

        st.success("Question submitted to Genie")

        st.subheader("Question")
        st.write(question)

        st.subheader("Conversation ID")
        st.code(conversation_id)

        if "message" in response:

            st.subheader("Submission Status")

            status = response["message"].get(
                "status",
                "Unknown"
            )

            st.write(status)

        st.subheader("Genie Response Payload")

        st.json(response)

    except Exception as e:

        st.error(str(e))
