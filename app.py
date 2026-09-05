import streamlit as st
from databricks.sdk import WorkspaceClient

st.set_page_config(
    page_title="HR Genie Assistant",
    layout="wide"
)

st.title("HR Genie Assistant")

st.write(
    "Ask a question about the HR Genie Space."
)

SPACE_ID = "01f1a7cce8341affb459c8c51394741b"

question = st.text_input(
    "Question",
    placeholder="How many active employees do we have?"
)

if st.button("Ask"):

    if not question.strip():
        st.warning("Please enter a question.")
    else:

        try:

            w = WorkspaceClient()

            # Creates a conversation and submits the question
            response = w.api_client.do(
                "POST",
                f"/api/2.0/genie/spaces/{SPACE_ID}/start-conversation",
                body={
                    "content": question
                }
            )

            st.success("Question submitted successfully")

            st.subheader("Conversation ID")
            st.code(response.get("conversation_id", "Not Returned"))

            st.subheader("Response")

            if "message" in response:
                message = response["message"]

                st.write("Submitted Question:")
                st.info(message.get("content", question))

                st.write("Status:")
                st.write(message.get("status", "Unknown"))

            with st.expander("Raw API Response"):
                st.json(response)

        except Exception as e:
            st.error(str(e))
