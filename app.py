import streamlit as st
from databricks.sdk import WorkspaceClient

st.title("Employee Table Test")

try:

    w = WorkspaceClient()

    result = w.statement_execution.execute_statement(
        warehouse_id="<YOUR_WAREHOUSE_ID>",
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
