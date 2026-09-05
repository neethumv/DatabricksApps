import time
import os
import streamlit as st
from databricks.sdk import WorkspaceClient
from openai import OpenAI

# --------------------------------------------------
# Configuration
# --------------------------------------------------

SPACE_ID = "01f1a7cce8341affb459c8c51394741b"

MODEL_NAME = "system.ai.meta-llama-3-3-70b-instruct"

DATABRICKS_HOST = "https://dbc-7f6f174c-ac08.cloud.databricks.com"

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
                                )

                                break

                        break

                    elif status in [
                        "FAILED",
                        "ERROR"
                    ]:

                        st.error(
                            "Genie request failed."
                        )
                        break

            st.subheader("Question")
            st.write(genie_question)

            st.subheader("Answer")

            if answer:
                st.success(answer)

            else:
                st.warning(
                    "No response received from Genie."
                )

        except Exception as e:

            st.error(
                f"Genie error: {str(e)}"
            )

# ==================================================
# TAB 2 - FOUNDATION MODEL
# ==================================================

with tab2:

    st.header("Foundation Model Assistant")

    prompt = st.text_area(
        "Enter a prompt",
        placeholder="Explain GDPR in one sentence.",
        key="model_prompt"
    )

    if st.button(
        "Generate Response",
        key="generate_response"
    ):

        if not prompt.strip():
            st.warning("Please enter a prompt.")
            st.stop()

        try:

            # Uses Databricks Apps identity
            token = os.environ.get(
                "DATABRICKS_TOKEN"
            )

            if not token:
                raise Exception(
                    "DATABRICKS_TOKEN not available."
                )

            client = OpenAI(
                api_key=token,
                base_url=f"{DATABRICKS_HOST}/ai-gateway/v1"
            )

            with st.spinner(
                "Generating response..."
            ):

                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    max_tokens=300
                )

            answer = (
                response
                .choices[0]
                .message
                .content
            )

            st.subheader("Prompt")
            st.write(prompt)

            st.subheader("Response")
            st.success(answer)

        except TimeoutError:

            st.warning(
                "Request timed out. Please try again."
            )

        except Exception as e:

            st.error(
                f"Model endpoint unavailable: {str(e)}"
            )
