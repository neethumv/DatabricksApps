import time
import pandas as pd
import streamlit as st

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import ChatMessage, ChatMessageRole

# --------------------------------------------------
# Configuration
# --------------------------------------------------

SPACE_ID = "01f1a7cce8341affb459c8c51394741b"

MODEL_NAME = "databricks-meta-llama-3-3-70b-instruct"

WAREHOUSE_ID = "1cfe7f2931b647ba"

# --------------------------------------------------
# Page Setup
# --------------------------------------------------

st.set_page_config(
    page_title="HR AI Assistant",
    layout="wide"
)

st.title("HR AI Assistant")

# --------------------------------------------------
# Databricks Client
# --------------------------------------------------

w = WorkspaceClient()

# --------------------------------------------------
# Tabs
# --------------------------------------------------

tab1, tab2, tab3 = st.tabs(
    [
        "Genie Assistant",
        "Model Assistant",
        "Leave Balances"
    ]
)

# ==================================================
# TAB 1 - GENIE ASSISTANT
# ==================================================

with tab1:

    st.header("HR Genie Assistant")

    genie_question = st.text_input(
        "Ask a question about HR data",
        placeholder="How many active employees do we have?",
        key="genie_question"
    )

    if st.button(
        "Ask Genie",
        key="ask_genie"
    ):

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
                "Genie is processing your question..."
            ):

                for _ in range(30):

                    time.sleep(2)

                    message = w.api_client.do(
                        "GET",
                        f"/api/2.0/genie/spaces/{SPACE_ID}/conversations/{conversation_id}/messages/{message_id}"
                    )

                    status = message.get("status")

                    if status == "COMPLETED":

                        for attachment in message.get(
                            "attachments",
                            []
                        ):

                            if "text" in attachment:

                                answer = (
                                    attachment["text"]
                                    .get("content")
                       
