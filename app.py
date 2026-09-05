import streamlit as st
from databricks.sdk import WorkspaceClient

st.title("Employee Table Query")

try:

    w = WorkspaceClient()

    result = w.statement_execution.execute_statement(
        warehouse_id="1cfe7f2931b647ba",
        statement="""
        SELECT COUNT(*)
        FROM hr_catalog.hr_core.employees
        """
    ).result()

    count = result.data_array[0][0]

    st.success(
        f"Employee Count: {count}"
    )

except Exception as e:

    st.error(str(e))
