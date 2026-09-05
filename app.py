import streamlit as st
import pandas as pd
from databricks.sdk import WorkspaceClient

st.title("HR Analytics Dashboard")

try:

    w = WorkspaceClient()

    response = w.statement_execution.execute_statement(
        warehouse_id="1cfe7f2931b647ba",
        statement="""
        SELECT *
        FROM hr_catalog.hr_core.employees
        LIMIT 10
        """
    )

    rows = response.result.data_array

    columns = [
        column.name
        for column in response.manifest.schema.columns
    ]

    df = pd.DataFrame(
        rows,
        columns=columns
    )

    st.subheader("Employee Data")

    st.dataframe(df)

except Exception as e:
    st.error(str(e))
