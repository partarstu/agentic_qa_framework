# Agentic QA Framework

A framework for building and orchestrating AI agents, focusing on automating software testing processes starting with
software requirements review and up to generating test execution reports.

The corresponding article on Medium can be
found [here](https://medium.com/@partarstu/the-next-evolution-in-software-testing-from-automation-to-autonomy-1bd7767802e1).

## Demo

Watch a demo of the project in action:

[Agentic QA Framework Demo](https://youtu.be/jd8s0fLdxLA)

## Features

* **Modular Agent Architecture:** Includes specialized agents for:
    * Requirements Review
    * Test Case Generation
    * Test Case Classification
    * Test Case Review
* **A2A and MCP - compliant:** Adheres to the specifications of Agent2Agent and Model Context protocols.
* **Orchestration Layer:** A central orchestrator manages agent registration, task routing, and workflow execution.
* **Integration with External Systems:** Supports integration with Jira by utilizing its MCP server.
* **Test Management System Integration:** Integrates with Zephyr for operations related to test case management.
* **Test Reporting:** Generates detailed Allure reports for test execution results.
* **Extensible:** Designed for easy addition of new agents, tools, and integrations.

## Architecture

The orchestrator acts as the central hub, managing the lifecycle and interactions of various specialized agents. Agents
expose details about their capabilities to the orchestrator and allow it to identify the tasks they can handle.

When an event occurs (e.g., a Jira webhook indicating new requirements), the orchestrator:

1. Receives the event.
2. Identifies the appropriate agent(s) based on the task description and registered agent capabilities.
3. Routes the task to the selected agent(s).
4. Monitors the task execution and collects results.
5. Triggers subsequent agents or workflows as needed (e.g., after test case generation, trigger test case
   classification).

For a visual representation of the system's architecture and data flow, please refer to the following diagrams:

* [Architectural Diagram](architectural_diagram.html)
* [Flow Diagram](flow_diagram.html)

## Getting Started

### Prerequisites

* Python 3.13+
* `pip` (Python package installer)
* `virtualenv` (or `conda` for environment management)

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/partarstu/agentic-qa-framework.git
   cd agentic-qa-framework
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Docker Images

The project utilizes Docker for containerization of the orchestrator and agent services. All services are built upon the
`python:3.13-slim` base image.

Each service runs using `gunicorn` as the WSGI server. The command for agents is
`gunicorn -w 1 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT agents.<agent_name>.main:app`, and for the
orchestrator, it is `gunicorn -w 1 -k uvicorn.workers.UvicornWorker orchestrator.main:orchestrator_app`. Note that
`$PORT` refers to the internal port the agent listens on, while the `AgentCard` will use the `EXTERNAL_PORT` for its
URL.

### Environment Variables

Create a `.env` file in the project root and configure the following environment variables. These variables control the
behavior of the orchestrator and agents.

```
# Logging
LOG_LEVEL=INFO # Default: INFO. Controls the verbosity of logging.
GOOGLE_CLOUD_LOGGING_ENABLED=False # Default: False. Set to "True" to enable Google Cloud Logging.

# Orchestrator
ORCHESTRATOR_HOST=localhost # Default: localhost. The host where the orchestrator runs.
ORCHESTRATOR_PORT=8000 # Default: 8000. The port the orchestrator listens on.
ORCHESTRATOR_URL=http://localhost:8000 # Default: http://localhost:8000. The full URL of the orchestrator.
JIRA_MCP_SERVER_URL=http://localhost:9000/sse # Default: http://localhost:9000/sse. The URL of the Jira MCP server.

# Zephyr Test Management System
ZEPHYR_BASE_URL=YOUR_ZEPHYR_BASE_URL # Required. The base URL of your Zephyr instance.

ZEPHYR_API_TOKEN=YOUR_ZEPHYR_API_TOKEN # Required. API token for Zephyr authentication.

# Jira Webhook Secret (for security)
JIRA_WEBHOOK_SECRET=YOUR_JIRA_WEBHOOK_SECRET # Required. Secret key for validating Jira webhooks. Must match the one configured in the MCP server.

# Agent Configuration
AGENT_BASE_URL=http://localhost # Default: http://localhost. Base URL for agents.
PORT=8001 # Default: 8001. The internal port an agent listens on.
EXTERNAL_PORT=443 # Default: 443. The externally accessible port for the agent (e.g., for cloud deployments).

# Agent Discovery (for remote agents)
REMOTE_EXECUTION_AGENT_HOSTS=http://localhost # Default: http://localhost. Comma-separated URLs of remote agent hosts.
AGENT_DISCOVERY_PORTS=8001-8005 # Default: 8001-8005. Port range for agent discovery.

# Google Cloud Storage (for attachments)
USE_GOOGLE_CLOUD_STORAGE=False # Default: False. Is set to "True" if running in the Google Cloud.
GOOGLE_CLOUD_STORAGE_BUCKET_NAME=YOUR_BUCKET_NAME # Required if USE_GOOGLE_CLOUD_STORAGE is True. The name of the GCS 
                                 bucket in which downloaded by Jira MCP server attachments are stored.

# OpenTelemetry (for tracing and metrics)
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317 # Default: http://localhost:4317. Endpoint for OpenTelemetry collector.

# Test Management System
TEST_MANAGEMENT_SYSTEM=zephyr # Default: zephyr. Specifies the test management system in use.

# Test Reporting
TEST_REPORTER=allure # Default: allure. Specifies the test reporting tool.
ALLURE_RESULTS_DIR=allure-results # Default: allure-results. Directory for Allure test results.
ALLURE_REPORT_DIR=allure-report # Default: allure-report. Directory for generated Allure reports.

# Common Model Configuration
TOP_P=1.0 # Default: 1.0. Top-p sampling parameter for models.
TEMPERATURE=0.0 # Default: 0.0. Temperature parameter for models.

# Specific Agent Model Names (example values, adjust as needed)
# These specify the AI model to be used by each component.
# Refer to your model provider's documentation for available model names.
ORCHESTRATOR_MODEL_NAME=google-gla:gemini-2.5-flash
REQUIREMENTS_REVIEW_AGENT_MODEL_NAME=google-gla:gemini-2.5-pro
TEST_CASE_CLASSIFICATION_AGENT_MODEL_NAME=google-gla:gemini-2.5-flash
TEST_CASE_GENERATION_AGENT_MODEL_NAME=google-gla:gemini-2.5-flash
TEST_CASE_REVIEW_AGENT_MODEL_NAME=google-gla:gemini-2.5-pro
```

### Jira MCP Server Setup

The Agentic Framework integrates with Jira via a Model Context Protocol (MCP) server. This server acts as an
intermediary, handling communication between Jira webhooks and the orchestrator.

To run the Jira MCP server, you will need Docker installed.

1. **Create a `.env` file for the MCP server:**
   The MCP server uses its own `.env` file for configuration. Create a file named `.env` in the `mcp/jira/` directory
   with the following content:

   ```
   JIRA_URL=YOUR_JIRA_INSTANCE_URL
   JIRA_API_TOKEN=YOUR_JIRA_API_TOKEN
   JIRA_USERNAME=YOUR_JIRA_USERNAME   
   ```
    * `JIRA_URL`: The base URL of your Jira instance (e.g., `https://your-company.atlassian.net`).
    * `JIRA_API_TOKEN`: A Jira API token for authentication. You can generate one in your Atlassian account settings.
    * `JIRA_USERNAME`: The email address associated with your Jira account.

2. **Run the MCP Server using Docker:**
   Navigate to the `mcp/jira/` directory and execute the `start_mcp_server.bat` script (valid only for Windows
   platform):

   ```bash
   cd mcp/jira
   start_mcp_server.bat
   ```
   This command will start the Docker container for the MCP server, mapping port `9000` on your host to the container's
   port `9000`. It also mounts a local directory (`D:\temp` in the example, corresponding to
   `ATTACHMENTS_DESTINATION_FOLDER_PATH` in your main `.env` file) to `/tmp` inside the container (corresponding to
   `MCP_SERVER_ATTACHMENTS_FOLDER_PATH`). Ensure this local directory exists and has appropriate permissions. Such an
   approach is needed because the current implementation of Jira MCP server only downloads the attachments locally on
   the server and doesn't transfer them to the agent. That's why those downloaded attachments need to be retrieved and
   volume mapping is the current solution for that. Within the cloud setup, a cloud storage could be mapped to the
   docker
   container and then downloaded attachments could be retrieved by the agent from the cloud storage.

### Starting agents locally

1. **Start Individual Agents:**
   Open separate terminal windows for each agent you want to run:

    * **Requirements Review Agent:**
      ```bash
      python agents/requirements_review/main.py
      ```
    * **Test Case Generation Agent:**
      ```bash
      python agents/test_case_generation/main.py
      ```
    * **Test Case Classification Agent:**
      ```bash
      python agents/test_case_classification/main.py
      ```
    * **Test Case Review Agent:**
      ```bash
      python agents/test_case_review/main.py
      ```

2. **Start the Orchestrator:**
   ```bash
   python orchestrator/main.py
   ```

### Deployment to Google Cloud Run

This project is already configured for deployment to Google Cloud Run. The `cloudbuild.yaml` file orchestrates the
building of Docker images and their deployment as separate services. The deployment process is fully automatic, all you
need is existing Cloud Storage bucket and setting up the **following secrets in the Google Secrets Manager with
corresponding values**:

* `GOOGLE_API_KEY`
* `JIRA_API_TOKEN`
* `JIRA_USERNAME`
* `JIRA_URL`
* `ZEPHYR_API_TOKEN`
* `ZEPHYR_BASE_URL`
* `JIRA_MCP_SERVER_URL`

After having all secrets set up, you can execute the following command:

```bash
gcloud builds submit --config 'cloudbuild.yaml' --substitutions "`^;`^_BUCKET_NAME=<YOUR_BUCKET_NAME>;_REQUIREMENTS_REVIEW_AGENT_BASE_URL=<YOUR_REQUIREMENTS_REVIEW_AGENT_URL>;_TEST_CASE_GENERATION_AGENT_BASE_URL=<YOUR_TEST_CASE_GENERATION_AGENT_URL>;_TEST_CASE_CLASSIFICATION_AGENT_BASE_URL=<YOUR_TEST_CASE_CLASSIFICATION_AGENT_URL>;_TEST_CASE_REVIEW_AGENT_BASE_URL=<YOUR_TEST_CASE_REVIEW_AGENT_URL>;_REMOTE_EXECUTION_AGENT_HOSTS=<YOUR_REMOTE_EXECUTION_AGENT_HOSTS>" .
```

**Substitution Variables:**

* `_BUCKET_NAME`: The name of the Google Cloud Storage bucket used for storing attachments downloaded by Jira MCP
  server.
* `_REQUIREMENTS_REVIEW_AGENT_BASE_URL`: The URL of the deployed Requirements Review Agent.
* `_TEST_CASE_GENERATION_AGENT_BASE_URL`: The URL of the deployed Test Case Generation Agent.
* `_TEST_CASE_CLASSIFICATION_AGENT_BASE_URL`: The URL of the deployed Test Case Classification Agent.
* `_TEST_CASE_REVIEW_AGENT_BASE_URL`: The URL of the deployed Test Case Review Agent.
* `_REMOTE_EXECUTION_AGENT_HOSTS`: A comma-separated list of URLs for all deployed agents that the orchestrator will
  interact with.

**Important**: Before the initial deployment of the framework into Google Cloud Run it's quite hard to know which URL
will be assigned to each agent and orchestrator. That's why most probably you'll have to run the deployment command
once, then identify the assigned URL of each service, update the substitution values in the command and run it again.

## Invoking Orchestrator Workflows

### Triggering Workflows via Jira Webhooks

The orchestrator listens for webhooks from Jira or CI/CD systems to initiate automated workflows.

* **New Requirements Available (Requirements Review):**
  Send a POST request to `/new-requirements-available` with a JSON payload containing the `issue_key` of the Jira user
  story.

  Example payload:
  ```json
  {
      "issue_key": "SCRUM-1"
  }
  ```

* **Story Ready for Test Case Generation:**
  Send a POST request to `/story-ready-for-test-case-generation` with a JSON payload containing the `issue_key` of the
  Jira user story. This triggers the test case generation, classification, and review workflows.

  Example payload:
  ```json
  {
      "issue_key": "SCRUM-1"
  }
  ```

### Executing Automated Tests

You can trigger the execution of automated tests for a specific project.

* **Execute Tests:**
  Send a POST request to `/execute-tests` with a JSON payload containing the `project_key` of the Jira project. This
  will execute all test cases labeled as "automated" within that project.

  Example payload:
  ```json
  {
      "project_key": "SCRUM"
  }
  ```
  The results will be reported back to Zephyr and an Allure report will be generated.

## Contributing

We welcome contributions to the Agentic Framework! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on
how to contribute.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
