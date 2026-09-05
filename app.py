import streamlit as st
import traceback
from databricks.sdk import WorkspaceClient

st.title("HR Analytics Dashboard")

try:

    w = WorkspaceClient()

    st.success("WorkspaceClient initialized")

    response = w.statement_execution.execute_statement(
        warehouse_id="1cfe7f2931b647ba",
        statement="SELECT 1"
    )

    st.write("Response:")
    st.write(response)

except Exception as e:

    st.error(str(e))
    st.code(traceback.format_exc())
