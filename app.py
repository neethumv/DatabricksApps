import time
import pandas as pd
import streamlit as st

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import ChatMessage, ChatMessageRole
from databricks import sql
from databricks.sdk.core import Config
import os

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

SPACE_ID = "01f1a7cce8341affb459c8c51394741b"

MODEL_NAME = "databricks-meta-llama-3-3-70b-instruct"

SERVER_HOSTNAME = "dbc-7f6f174c-ac08.cloud.databricks.com"
WAREHOUSE_ID = "1cfe7f2931b647ba"
HTTP_PATH = "/sql/1.0/warehouses/1cfe7f2931b647ba"


def get_user_client():

    user_token = st.context.headers.get(
        "X-Forwarded-Access-Token"
    )

    cfg = Config(
        host="https://dbc-7f6f174c-ac08.cloud.databricks.com",
        token=user_token,
        auth_type="pat"
    )

    return WorkspaceClient(config=cfg)



# --------------------------------------------------
# PAGE SETUP
# --------------------------------------------------

st.set_page_config(
    page_title="HR AI Assistant",
    layout="wide"
)

st.title("HR AI Assistant")

w = WorkspaceClient()
# def get_user_client():

#     headers = st.context.headers

#     user_token = headers.get(
#         "x-forwarded-access-token"
#     )

#     if not user_token:
#         raise Exception(
#             "User token not found. Ensure User Authorization is enabled."
#         )

#     cfg = Config(
#         host=app_client.config.host,
#         token=user_token
#     )

#     return WorkspaceClient(config=cfg)

# if st.button("Show Current User"):

#     try:

#         user_client = get_user_client()

#         response = user_client.statement_execution.execute_statement(
#             warehouse_id=WAREHOUSE_ID,
#             statement="""
#             SELECT current_user() AS current_user
#             """,
#             wait_timeout="30s"
#         )

#         st.json(response.as_dict())

#     except Exception as e:

#         st.error(str(e))
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
# ==================================================
# ACCESS CONTROL TEST
# ==================================================

# ==================================================
# ITERATION 1 - REGION FILTER
# ==================================================
with tab3:

    st.header("Leave Balances Access Control Test")

    selected_region = st.selectbox(
        "Filter Region",
        ["All", "UK", "US", "PL"]
    )

    if st.button("Load Leave Balance Data"):

        try:

            user_token = st.context.headers.get(
                "X-Forwarded-Access-Token"
            )

            from databricks.sdk.core import Config

            user_client = WorkspaceClient(
                config=Config(
                    host=w.config.host,
                    token=user_token,
                    auth_type="pat"
                )
            )

            me = user_client.api_client.do(
                "GET",
                "/api/2.0/preview/scim/v2/Me"
            )

            user_email = me["emails"][0]["value"]

            st.success(
                f"Logged in as: {user_email}"
            )

            query = """
            SELECT
                region,
                COUNT(*) AS employee_count
            FROM hr_catalog.hr_core.leave_balances
            """

            if selected_region != "All":

                query += f"""
                WHERE region = '{selected_region}'
                """

            query += """
            GROUP BY region
            ORDER BY region
            """

            response = (
                user_client.statement_execution.execute_statement(
                    warehouse_id=WAREHOUSE_ID,
                    statement=query,
                    wait_timeout="30s"
                )
            )

            result_dict = response.as_dict()

            columns = [
                col["name"]
                for col in result_dict["manifest"]["schema"]["columns"]
            ]

            rows = result_dict["result"]["data_array"]

            df = pd.DataFrame(
                rows,
                columns=columns
            )

            df["employee_count"] = pd.to_numeric(
                df["employee_count"],
                errors="coerce"
            )

            st.subheader(
                "Leave Balance Summary by Region"
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            # New Feature #2
            st.subheader(
                "Employees by Region"
            )

            st.bar_chart(
                df.set_index("region")["employee_count"]
            )
            # --------------------------------
            # Iteration 3 - Download CSV
            # --------------------------------
            csv_data = df.to_csv(
                index=False)
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name="leave_balance_summary.csv",
                mime="text/csv"
            )
        except Exception as e:

            st.error(
                f"Query failed: {str(e)}"
            )
# with tab3:

#     st.header("Leave Balances Access Control Test")

#     st.write("""
#     This tab demonstrates Unity Catalog row-level security.

#     The same SQL query is executed for every user.
#     Any differences in results come from Unity Catalog
#     permissions and row filters, not application logic.
#     """)

#     # New Feature #1
#     selected_region = st.selectbox(
#         "Filter Region",
#         ["All", "UK", "US", "PL"]
#     )

#     if st.button("Load Leave Balance Data"):

#         try:

#             user_token = st.context.headers.get(
#                 "X-Forwarded-Access-Token"
#             )

#             from databricks.sdk.core import Config

#             user_client = WorkspaceClient(
#                 config=Config(
#                     host=w.config.host,
#                     token=user_token,
#                     auth_type="pat"
#                 )
#             )

#             me = user_client.api_client.do(
#                 "GET",
#                 "/api/2.0/preview/scim/v2/Me"
#             )

#             user_email = me["emails"][0]["value"]

#             st.success(
#                 f"Logged in as: {user_email}"
#             )

#             # Base query
#             query = """
#             SELECT
#                 region,
#                 COUNT(*) AS employee_count
#             FROM hr_catalog.hr_core.leave_balances
#             """

#             # Apply filter if selected
#             if selected_region != "All":

#                 query += f"""
#                 WHERE region = '{selected_region}'
#                 """

#             query += """
#             GROUP BY region
#             ORDER BY region
#             """

#             response = (
#                 user_client.statement_execution.execute_statement(
#                     warehouse_id=WAREHOUSE_ID,
#                     statement=query,
#                     wait_timeout="30s"
#                 )
#             )

#             result_dict = response.as_dict()

#             columns = [
#                 col["name"]
#                 for col in result_dict["manifest"]["schema"]["columns"]
#             ]

#             rows = result_dict["result"]["data_array"]

#             df = pd.DataFrame(
#                 rows,
#                 columns=columns
#             )

#             st.subheader(
#                 "Leave Balance Summary by Region"
#             )

#             st.dataframe(
#                 df,
#                 use_container_width=True,
#                 hide_index=True
#             )

#         except Exception as e:

#             st.error(
#                 f"Query failed: {str(e)}"
#             )
# with tab3:

#     st.header("Leave Balances Access Control Test")

#     st.write("""
#     This tab demonstrates Unity Catalog row-level security.

#     The same SQL query is executed for every user.
#     Any differences in results come from Unity Catalog
#     permissions and row filters, not application logic.
#     """)

#     if st.button("Load Leave Balance Data"):

#         try:

#             # Build a user-authorized client
#             user_token = st.context.headers.get(
#                 "X-Forwarded-Access-Token"
#             )

#             from databricks.sdk.core import Config

#             user_client = WorkspaceClient(
#                 config=Config(
#                     host=w.config.host,
#                     token=user_token,
#                     auth_type="pat"
#                 )
#             )

#             # Show the logged-in user
#             me = user_client.api_client.do(
#                 "GET",
#                 "/api/2.0/preview/scim/v2/Me"
#             )

#             user_email = me["emails"][0]["value"]

#             st.success(
#                 f"Logged in as: {user_email}"
#             )

#             # Run query as the USER
#             response = (
#                 user_client.statement_execution.execute_statement(
#                     warehouse_id=WAREHOUSE_ID,
#                     statement="""
#                     SELECT
#                         region,
#                         COUNT(*) AS employee_count
#                     FROM hr_catalog.hr_core.leave_balances
#                     GROUP BY region
#                     ORDER BY region
#                     """,
#                     wait_timeout="30s"
#                 )
#             )

#             # st.subheader("Query Response")

#             # st.json(response.as_dict())


#             result_dict = response.as_dict()
            
#             # Extract column names
#             columns = [
#                 col["name"]
#                 for col in result_dict["manifest"]["schema"]["columns"]
#             ]
            
#             # Extract rows
#             rows = result_dict["result"]["data_array"]
            
#             # Build dataframe
#             df = pd.DataFrame(rows, columns=columns)
            
#             # Convert numeric columns
#             if "employee_count" in df.columns:
#                 df["employee_count"] = pd.to_numeric(
#                     df["employee_count"],
#                     errors="coerce"
#                 )
            

#             st.subheader("Leave Balance Summary by Region")
            
#             st.dataframe(
#                 df,
#                 use_container_width=True,
#                 hide_index=True
#             )

#         except Exception as e:

#             st.error(
#                 f"Query failed: {str(e)}"
#             )
