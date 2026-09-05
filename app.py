import streamlit as st
from databricks.sdk import WorkspaceClient

st.title("HR Analytics Dashboard")

try:

    w = WorkspaceClient()

    st.success("WorkspaceClient initialized")

except Exception as e:

    st.error(str(e))
