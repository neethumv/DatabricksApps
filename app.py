import streamlit as st
import time
from databricks.sdk import WorkspaceClient

SPACE_ID = "01f1a7cce8341affb459c8c51394741b"

st.title("HR Genie Assistant")

question = st.text_input(
    "Ask a question about HR data:"
)

if st.button("Ask"):

    try:

        w = WorkspaceClient()

        response = w.api_client.do(
            "POST",
            f"/api/2.0/genie/spaces/{SPACE_ID}/start-conversation",
            body={
                "content": question
            }
        )

        conversation_id = response["conversation_id"]
        message_id = response["message_id"]

        st.write("Waiting for Genie response...")

        answer = None

        # Poll for completion
        for _ in range(15):

            time.sleep(2)

            try:

                msg = w.api_client.do(
                    "GET",
                    f"/api/2.0/genie/spaces/{SPACE_ID}/conversations/{conversation_id}/messages/{message_id}"
                )

                if "attachments" in msg:

                    for attachment in msg["attachments"]:

                        if "text" in attachment:

                            answer = attachment["text"]["content"]
                            break

                if answer:
                    break

            except Exception:
                pass

        st.subheader("Question")
        st.write(question)

        st.subheader("Answer")

        if answer:
            st.success(answer)
        else:
            st.warning(
                "Genie response not yet available."
            )

    except Exception as e:

        st.error(str(e))
