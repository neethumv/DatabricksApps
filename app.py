import streamlit as st
import time
from databricks.sdk import WorkspaceClient

# --------------------------------------------------
# Configuration
# --------------------------------------------------

SPACE_ID = "01f1a7cce8341affb459c8c51394741b"
aimport streamlit as st
import time
from databricks.sdk import WorkspaceClient

# --------------------------------------------------
# Configuration
# --------------------------------------------------

SPACE_ID = "01f1a7cce8341affb459c8c51394741b"

st.set_page_config(
    page_title="HR Genie Assistant",
    layout="wide"
)

# --------------------------------------------------
# UI
# --------------------------------------------------

st.title("HR Genie Assistant")

question = st.text_input(
    "Ask a question about HR data:",
    placeholder="How many active employees do we have?"
)

# --------------------------------------------------
# Ask Genie
# --------------------------------------------------

if st.button("Ask"):

    if not question.strip():
        st.warning("Please enter a question.")
        st.stop()

    try:

        w = WorkspaceClient()

        # Submit question to Genie
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

        # Poll until Genie finishes processing
        for _ in range(30):

            time.sleep(2)

            message = w.api_client.do(
                "GET",
                f"/api/2.0/genie/spaces/{SPACE_ID}/conversations/{conversation_id}/messages/{message_id}"
            )

            status = message.get("status")

            if status == "COMPLETED":

                for attachment in message.get("attachments", []):

                    if "text" in attachment:
                        answer = attachment["text"]["content"]
                        break

                break

            elif status in ["FAILED", "ERROR"]:
                st.error(
                    f"Genie request failed with status: {status}"
                )
                st.stop()

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
        st.error(f"Error: {str(e)}")
st.set_page_config(
    page_title="HR Genie Assistant",
    layout="wide"
)

# --------------------------------------------------
# UI
# --------------------------------------------------

st.title("HR Genie Assistant")

question = st.text_input(
    "Ask a question about HR data:",
    placeholder="How many active employees do we have?"
)

# --------------------------------------------------
# Ask Genie
# --------------------------------------------------

if st.button("Ask"):

    if not question.strip():
        st.warning("Please enter a question.")
        st.stop()

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
        message_id = response["message_id"]

        st.subheader("Question")
        st.write(question)

        st.write(f"Conversation ID: {conversation_id}")
        st.write(f"Message ID: {message_id}")

        answer = None

        # Poll Genie for completion
        for i in range(30):

            time.sleep(2)

            try:

                message = w.api_client.do(
                    "GET",
                    f"/api/2.0/genie/spaces/{SPACE_ID}/conversations/{conversation_id}/messages/{message_id}"
                )

                status = message.get("status")

                st.write(f"Poll #{i+1} | Status: {status}")

                # Debug - expand to inspect response
                with st.expander(f"Response #{i+1}"):
                    st.json(message)

                if status == "COMPLETED":

                    attachments = message.get(
                        "attachments",
                        []
                    )

                    for attachment in attachments:

                        if "text" in attachment:

                            answer = attachment["text"].get(
                                "content"
                            )

                            break

                    break

                elif status in ["FAILED", "ERROR"]:

                    st.error(
                        f"Genie request failed: {status}"
                    )
                    break

            except Exception as poll_error:

                st.error(
                    f"Polling error: {poll_error}"
                )
                break

        # --------------------------------------------------
        # Display Answer
        # --------------------------------------------------

        st.subheader("Answer")

        if answer:

            st.success(answer)

        else:

            st.warning(
                "Genie did not return an answer within the timeout period."
            )

    except Exception as e:

        st.error(f"Error: {str(e)}")
