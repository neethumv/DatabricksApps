from databricks.sdk import WorkspaceClient
import time

w = WorkspaceClient()

conversation_id = "01f1a9457e3012439136716f46d87549"

time.sleep(10)

result = w.api_client.do(
    "GET",
    f"/api/2.0/genie/conversations/{conversation_id}/messages"
)

result
