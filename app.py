import time
import requests
import streamlit as st
from databricks.sdk import WorkspaceClient

# --------------------------------------------------
# Configuration
# --------------------------------------------------

SPACE_ID = "01f1a7cce8341affb459c8c51394741b"

MODEL_NAME = "system.ai.meta-llama-3-3-70b-instruct"

HOST = "https://dbc-7f6f174c-ac08.cloud.databricks.com"

# --------------------------------------------------
# Setup
# --------------------------------------------------

st.set_page_config(
    page_title="HR AI Assistant",
    layout="wide"
)

st.title("HR AI Assistant")

w = WorkspaceClient()

tab1, tab2 = st.tabs(
    ["Genie Assistant", "Model Assistant"]
)

# ==================================================
# TAB 1 - GENIE
# ==================================================

with tab1:

    st.header("HR Genie Assistant")

    genie_question = st.text_input(
        "Ask a question about HR data",
        placeholder="How many active employees do we have?",
        key="genie_question"
    )

    if st.button("Ask Genie"):

        if not genie_question.strip():
            st.warning("Please enter a question.")
            st.stop()

        try:

            response = w.api_client.do(
                "POST",
                f"/api/2.0/genie/spaces/{SPACE_ID}/start-conversation",
                body={
                    "content": genie_question
                }
            )

            conversation_id = response["conversation_id"]
            message_id = response["message_id"]

            answer = None

            with st.spinner(
                "Genie is processing..."
            ):

                for _ in range(30):

                    time.sleep(2)

                    message = w.api_client.do(
                        "GET",
                        f"/api/2.0/genie/spaces/{SPACE_ID}/conversations/{conversation_id}/messages/{message_id}"
                    )

                    if message.get("status") == "COMPLETED":

                        for attachment in message.get(
                            "attachments",
                            []
                        ):

                            if "text" in attachment:

                                answer = attachment["text"]["content"]
                                break

                        break

            st.subheader("Question")
            st.write(genie_question)

            st.subheader("Answer")

            if answer:
                st.success(answer)
            else:
                st.warning("No answer returned.")

        except Exception as e:

            st.error(f"Genie error: {e}")

# ==================================================
# TAB 2 - FOUNDATION MODEL
# ==================================================

with tab2:

    if st.button("Debug Config"):

        st.write("Host:")
        st.write(w.config.host)

        st.write("Auth Type:")
        st.write(type(w.config))
