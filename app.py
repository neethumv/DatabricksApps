import time
import pandas as pd
import streamlit as st

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import ChatMessage, ChatMessageRole

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

SPACE_ID = "01f1a7cce8341affb459c8c51394741b"
MODEL_NAME = "databricks-meta-llama-3-3-70b-instruct"
WAREHOUSE_ID = "1cfe7f2931b647ba"

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
# GENIE TAB
# ==================================================

with tab1:

    st.header("HR Genie Assistant")

    genie_question = st.text_input(
        "Ask a question about HR data",
        placeholder="How many active employees do we have?"
    )

    if st.button("Ask Genie"):

        if not genie_question.strip():
            st.warning("Please enter a question.")
        else:

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

                            attachments = message.get(
                                "attachments",
                                []
                            )

                            for attachment in attachments:

                                if "text" in attachment:

                                    answer = attachment[
                                        "text"
                                    ].get(
                                        "content",
                                        ""
                                    )

                                    break

                            break

                        elif status in (
                            "FAILED",
                            "ERROR"
                        ):

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
                        "No answer returned from Genie."
                    )

            except Exception as e:

                st.error(
                    f"Genie error: {str(e)}"
                )

# ==================================================
# MODEL ASSISTANT TAB
# ==================================================

with tab2:

    st.header("Foundation Model Assistant")

    prompt = st.text_area(
        "Enter a prompt",
        placeholder="Explain GDPR in one sentence."
    )

    if st.button("Generate Response"):

        if not prompt.strip():
            st.warning("Please enter a prompt.")
        else:

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
# ACCESS CONTROL TAB
# ==================================================

with tab3:

    st.header("Leave Balances by Region")

    st.write(
        """
        This tab demonstrates Unity Catalog
        row-level security. The same SQL query is
        executed for all users. Any differences in
        results come from Unity Catalog permissions,
        not application logic.
        """
    )

    if st.button("Load Leave Balance Summary"):

        try:

            with st.spinner(
                "Loading leave balance data..."
            ):

                response = w.statement_execution.execute_statement(
                                warehouse_id=WAREHOUSE_ID,
                                statement="""
                                SELECT
                                    employee_id,
                                    region,
                                    leave_balance
                                FROM hr_catalog.hr_core.leave_balances
                                LIMIT 20
                                """,
                                wait_timeout="30s"
                            )
                st.write(response)

            # rows = response.result.data_array

            # df = pd.DataFrame(
            #     rows,
            #     columns=[
            #         "Region",
            #         "Employee Count"
            #     ]
            # )

            # st.dataframe(
            #     df,
            #     use_container_width=True
            # )

        except Exception as e:

            st.error(
                f"Unable to load leave balance data: {str(e)}"
            )
