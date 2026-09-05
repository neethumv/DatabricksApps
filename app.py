import streamlit as st
import pandas as pd
from databricks import sql
import os

st.title("HR Analytics Dashboard")

try:

    conn = sql.connect(
        server_hostname="dbc-7f6f174c-ac08.cloud.databricks.com",
        http_path="/sql/1.0/warehouses/1cfe7f2931b647ba",
        access_token=os.environ["DATABRICKS_TOKEN"]
    )

    query = """
    SELECT *
    FROM hr_catalog.hr_core.employees
    LIMIT 10
    """

    cursor = conn.cursor()
    cursor.execute(query)

    rows = cursor.fetchall()

    columns = [col[0] for col in cursor.description]

    df = pd.DataFrame(rows, columns=columns)

    st.subheader("Employee Data")

    st.dataframe(df)

except Exception as e:
    st.error(f"Error executing query: {e}")
