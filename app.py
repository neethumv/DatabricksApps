import time
import pandas as pd
import streamlit as st

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import ChatMessage, ChatMessageRole
from databricks import sql

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

SPACE_ID = "01f1a7cce8341affb459c8c51394741b"

MODEL_NAME = "databricks-meta-llama-3-3-70b-instruct"

SERVER_HOSTNAME = "dbc-7f6f174c-ac08.cloud.databricks.com"

HTTP_PATH = "/sql/1.0/warehouses/1cfe7f2931b647ba"

# --------------------------------------------------
# PAGE SETUP
# --------------------------------------------------

st.set_page_config(
    page_title="HR AI Assistant",
    layout="wide"
)

st.title("HR AI Assistant")

w = WorkspaceClient()

# --------------------------------------------------
# TABS
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
        placeholder="How many active employees do we have?"
    )

    if st.button("Ask Genie"):

        if genie_question.strip():

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

                                    answer = attachment[
                                        "text"
                                    ].get(
                                        "content"
                                    )

                                    break

                            break

                st.subheader("Question")
                st.write(genie_question)

                st.subheader("Answer")

                if answer:
                    st.success(answer)

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
        placeholder="Explain GDPR in one sentence."
    )

    if st.button("Generate Response"):

        if prompt.strip():

            try:

                with st.spinner(
                    "Generating response..."
                ):

                    response = w.serving_endpoints.query(
                        name=MODEL_NAME,
                        messages=[
                            ChatMessage(
                                role="user",
                                content=prompt
                            )
                        ]
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

# ==================================================
# TAB 3 - ACCESS CONTROL TEST
# ==================================================

with tab3:

    st.header("Leave Balances Access Control Test")

    st.write("""
    This demonstrates Unity Catalog row-level security.

    The same query is executed for every user.
    Any differences in results come from Unity Catalog permissions,
    not application logic.
    """)

    if st.button("Load Leave Balance Data"):

        try:

            response = w.statement_execution.execute_statement(
                warehouse_id=WAREHOUSE_ID,
                statement="""
                SELECT
                region,
                COUNT(*) AS employee_count
                FROM hr_catalog.hr_core.leave_balances
                GROUP BY region
                ORDER BY region
                """,
                wait_timeout="30s"
            )

            st.success("Query executed successfully")

            st.json(response.as_dict())

        except Exception as e:

            st.error(str(e))
