# Agentic QA Framework

A framework for building and orchestrating AI agents, focusing on automating software testing processes starting with software requirements review and up to generating test execution reports.

## Demo

Watch a demo of the project in action:

[Agentic QA Framework Demo](https://youtu.be/jd8s0fLdxLA)

## Features

*   **Modular Agent Architecture:** Includes specialized agents for:
    *   Requirements Review
    *   Test Case Generation
    *   Test Case Classification
    *   Test Case Review
*   **A2A and MCP - compliant:** Adheres to the specifications of Agent2Agent and Model Context protocols. 
*   **Orchestration Layer:** A central orchestrator manages agent registration, task routing, and workflow execution.
*   **Integration with External Systems:** Supports webhooks for seamless integration with platforms like Jira.
*   **Test Management System Integration:** Integrates with Zephyr for comprehensive test case management.
*   **Test Reporting:** Generates detailed Allure reports for test execution results.
*   **Extensible:** Designed for easy addition of new agents, tools, and integrations.

## Architecture

The orchestrator acts as the central hub, managing the lifecycle and interactions of various specialized agents. Agents register themselves with the orchestrator, providing details about their capabilities and the tasks they can handle.

When an event occurs (e.g., a Jira webhook indicating new requirements), the orchestrator:
1.  Receives the event.
2.  Identifies the appropriate agent(s) based on the task description and registered agent capabilities.
3.  Routes the task to the selected agent(s).
4.  Monitors the task execution and collects results.
5.  Triggers subsequent agents or workflows as needed (e.g., after test case generation, trigger test case classification).

For a visual representation of the system's architecture and data flow, please refer to the following diagrams:

*   [Architectural Diagram](architectural_diagram.html)
*   [Flow Diagram](flow_diagram.html)

## Getting Started

### Prerequisites

*   Python 3.9+
*   `pip` (Python package installer)
*   `virtualenv` (or `conda` for environment management)

### Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-repo/agentic_framework.git
    cd agentic_framework
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Jira MCP Server Setup

The Agentic Framework integrates with Jira via a Model Context Protocol (MCP) server. This server acts as an intermediary, handling communication between Jira webhooks and the orchestrator.

To run the Jira MCP server, you will need Docker installed.

1.  **Create a `.env` file for the MCP server:**
    The MCP server uses its own `.env` file for configuration. Create a file named `.env` in the `mcp/jira/` directory with the following content:

    ```
    JIRA_BASE_URL=YOUR_JIRA_INSTANCE_URL
    JIRA_API_TOKEN=YOUR_JIRA_API_TOKEN
    JIRA_USERNAME=YOUR_JIRA_USERNAME
    JIRA_WEBHOOK_SECRET=YOUR_JIRA_WEBHOOK_SECRET
    ```
    *   `JIRA_BASE_URL`: The base URL of your Jira instance (e.g., `https://your-company.atlassian.net`).
    *   `JIRA_API_TOKEN`: A Jira API token for authentication. You can generate one in your Atlassian account settings.
    *   `JIRA_USERNAME`: The email address associated with your Jira account.
    *   `JIRA_WEBHOOK_SECRET`: A secret key used to secure webhooks from Jira. This must match the `JIRA_WEBHOOK_SECRET` configured in the main project's `.env` file.

2.  **Run the MCP Server using Docker:**
    Navigate to the `mcp/jira/` directory and execute the `start_mcp_server.bat` script:

    ```bash
    cd mcp/jira
    start_mcp_server.bat
    ```
    This command will start the Docker container for the MCP server, mapping port `9000` on your host to the container's port `9000`. It also mounts a local directory (`D:\temp` in the example, corresponding to `ATTACHMENTS_LOCAL_FOLDER_PATH` in your main `.env` file) to `/tmp` inside the container (corresponding to `ATTACHMENTS_REMOTE_FOLDER_PATH`). Ensure this local directory exists and has appropriate permissions.

### Environment Variables

Create a `.env` file in the project root and configure the following environment variables. These variables control the behavior of the orchestrator and agents.

```
# Logging
LOG_LEVEL=INFO # Default: INFO. Controls the verbosity of logging.

# Orchestrator
ORCHESTRATOR_HOST=localhost # Default: localhost. The host where the orchestrator runs.
ORCHESTRATOR_PORT=8000 # Default: 8000. The port the orchestrator listens on.
ORCHESTRATOR_URL=http://localhost:8000 # Default: http://localhost:8000. The full URL of the orchestrator.
JIRA_MCP_SERVER_URL=http://localhost:9000/sse # Default: http://localhost:9000/sse. The URL of the Jira MCP server.

# Zephyr Test Management System
ZEPHYR_BASE_URL=YOUR_ZEPHYR_BASE_URL # Required. The base URL of your Zephyr instance.
ZEPHYR_COMMENTS_CUSTOM_FIELD_NAME="Review Comments" # Default: "Review Comments". Custom field name for comments in Zephyr.
ZEPHYR_API_TOKEN=YOUR_ZEPHYR_API_TOKEN # Required. API token for Zephyr authentication.

# Jira Webhook Secret (for security)
JIRA_WEBHOOK_SECRET=YOUR_JIRA_WEBHOOK_SECRET # Required. Secret key for validating Jira webhooks. Must match the one configured in the MCP server.

# Agent Configuration
AGENT_BASE_URL=http://localhost # Default: http://localhost. Base URL for agents.
AGENT_HOST=localhost # Default: localhost. Host for individual agents.
ATTACHMENTS_REMOTE_FOLDER_PATH=/tmp # Default: /tmp. Remote folder path for attachments (inside Docker container for MCP).
ATTACHMENTS_LOCAL_FOLDER_PATH=D://temp # Default: D://temp. Local folder path for attachments (on your machine, mounted to MCP container).

# Agent Discovery (for remote agents)
REMOTE_EXECUTION_AGENTS_URLS=http://localhost # Default: http://localhost. Comma-separated URLs of remote agent hosts.
AGENT_DISCOVERY_PORTS=8001-8004 # Default: 8001-8004. Port range for agent discovery.

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

### Running the Application

1.  **Start the Orchestrator:**
    ```bash
    python orchestrator/main.py
    ```

2.  **Start Individual Agents:**
    Open separate terminal windows for each agent you want to run:

    *   **Requirements Review Agent:**
        ```bash
        python agents/requirements_review/main.py
        ```
    *   **Test Case Generation Agent:**
        ```bash
        python agents/test_case_generation/main.py
        ```
    *   **Test Case Classification Agent:**
        ```bash
        python agents/test_case_classification/main.py
        ```
    *   **Test Case Review Agent:**
        ```bash
        python agents/test_case_review/main.py
        ```

## Usage

### Triggering Workflows via Jira Webhooks

The orchestrator listens for webhooks from Jira to initiate automated workflows.

*   **New Requirements Available (Requirements Review):**
    Send a POST request to `/new-requirements-available` with a JSON payload containing the `issue_key` of the Jira user story.

    Example payload:
    ```json
    {
        "issue_key": "SCRUM-15"
    }
    ```

*   **Story Ready for Test Case Generation:**
    Send a POST request to `/story-ready-for-test-case-generation` with a JSON payload containing the `issue_key` of the Jira user story. This triggers the test case generation, classification, and review workflow.

    Example payload:
    ```json
    {
        "issue_key": "SCRUM-15"
    }
    ```

### Executing Automated Tests

You can trigger the execution of automated tests for a specific project.

*   **Execute Tests:**
    Send a POST request to `/execute-tests` with a JSON payload containing the `project_key` of the Jira project. This will execute all test cases labeled as "automated" within that project.

    Example payload:
    ```json
    {
        "project_key": "SCRUM"
    }
    ```
    The results will be reported back to Zephyr and an Allure report will be generated.

## Contributing

We welcome contributions to the Agentic Framework! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
