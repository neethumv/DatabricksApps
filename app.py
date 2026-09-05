import streamlit as st
import traceback
from databricks.sdk import WorkspaceClient

st.title("HR Analytics Dashboard")

try:

    w = WorkspaceClient()

    st.success("WorkspaceClient initialized")

    statement = w.statement_execution.execute_statement(
        warehouse_id="1cfe7f2931b647ba",
        statement="SELECT COUNT(*) FROM hr_catalog.hr_core.employees"
    )

    st.write("Statement object:")
    st.write(statement)

except Exception as e:

    st.error(str(e))
    st.code(traceback.format_exc())
