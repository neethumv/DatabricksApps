# HR AI Assistant

A Streamlit-based Databricks App demonstrating AI, governance, and application development capabilities.

## Scenarios Completed

### 1. Minimal Deployable App
- Created and deployed a basic Streamlit application.
- Verified successful deployment and application access.

### 2. Front-End for Genie
- Integrated the app with a Databricks Genie Space.
- Allowed users to ask natural-language questions about HR data.
- Displayed AI-generated responses.

### 3. Model Serving Integration
- Integrated with the Databricks Foundation Model:
  `system.ai.llama_v3_3_70b_instruct`
- Accepted user prompts and displayed generated responses.
- Implemented error handling for failures and timeouts.

### 4. Access Control Test
- Configured a Unity Catalog row filter on `leave_balances`.
- Validated different results for different users using the same query.
- Demonstrated that data access is enforced by Unity Catalog, not application logic.

### 5. Live Iteration
Implemented three incremental enhancements:

1. Region Filter
2. Region-wise Bar Chart
3. CSV Export Button

Each change was deployed and validated before proceeding to the next enhancement.

## Technologies Used

- Databricks Apps
- Streamlit
- Databricks Genie
- Databricks Foundation Models
- Unity Catalog
- Databricks SDK
- Pandas

## Outcome

Successfully built and deployed an AI-powered HR analytics application demonstrating:
- Databricks App deployment
- Genie integration
- Foundation Model integration
- Unity Catalog row-level security
- Iterative feature development
