import streamlit as st
import time
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
        st.stop()

    try:

        w = WorkspaceClient()

        # Submit question
        response = w.api_client.do(
            "POST",
            f"/api/2.0/genie/spaces/{SPACE_ID}/start-conversation",
            body={
                "content": question
            }
        )

        conversation_id = response["conversation_id"]
        message_id = response["message_id"]

        answer = None

        # Poll for completion (up to ~30 seconds)
        for _ in range(15):

            time.sleep(2)

            message = w.api_client.do(
                "GET",
                f"/api/2.0/genie/spaces/{SPACE_ID}/conversations/{conversation_id}/messages/{message_id}"
            )

            if message.get("status") == "COMPLETED":

                for attachment in message.get("attachments", []):

                    if "text" in attachment:
                        answer = attachment["text"]["content"]
                        break

                break

        st.subheader("Question")
        st.write(question)

        st.subheader("Answer")

        if answer:
            st.success(answer)
        else:
            st.warning(
                "Genie did not return an answer within the timeout period."
            )

    except Exception as e:
        st.error(str(e))
