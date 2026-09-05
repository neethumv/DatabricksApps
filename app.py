import streamlit as st
from databricks.sdk import WorkspaceClient

st.title("HR Analytics Dashboard")

try:

    w = WorkspaceClient()

    response = w.statement_execution.execute_statement(
        warehouse_id="1cfe7f2931b647ba",
        statement="""
        SELECT COUNT(*)
        FROM hr_catalog.hr_core.employees
        """
    )

    employee_count = response.result.data_array[0][0]

    st.metric(
        "Employee Count",
        employee_count
    )

except Exception as e:
    st.error(str(e))
