import streamlit as st
from databricks.sdk import WorkspaceClient

SPACE_ID = "01f1a7cce8341affb459c8c51394741b"

st.set_page_config(
    page_title="HR Genie Assistant",
    layout="wide"
)

st.title("HR Genie Assistant")

question = st.text_input(
    "Ask a question about HR data:",
    placeholder="How many active employees do we have?"
)

if st.button("Ask"):

    if not question.strip():
        st.warning("Please enter a question.")
    else:

        try:

            w = WorkspaceClient()

            response = w.api_client.do(
                "POST",
                f"/api/2.0/genie/spaces/{SPACE_ID}/start-conversation",
                body={
                    "content": question
                }
            )

            message_id = response["message_id"]

            # Get completed Genie response
            message = w.api_client.do(
                "GET",
                f"/api/2.0/genie/spaces/{SPACE_ID}/messages/{message_id}"
            )

            answer = "No answer returned"

            for attachment in message.get("attachments", []):

                if "text" in attachment:
                    answer = attachment["text"]["content"]
                    break

            st.subheader("Question")
            st.write(question)

            st.subheader("Answer")
            st.success(answer)

        except Exception as e:
            st.error(str(e))
``
