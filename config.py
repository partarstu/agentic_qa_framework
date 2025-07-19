# SPDX-FileCopyrightText: 2025 Taras Paruta (partarstu@gmail.com)
#
# SPDX-License-Identifier: Apache-2.0

"""
Centralized configuration for the application.
"""

from dotenv import load_dotenv
import os

load_dotenv()

# Logging
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()

# URLs
ORCHESTRATOR_HOST = os.environ.get("ORCHESTRATOR_HOST", "localhost")
ORCHESTRATOR_PORT = int(os.environ.get("ORCHESTRATOR_PORT", "8000"))
ORCHESTRATOR_URL = os.environ.get("ORCHESTRATOR_URL", f"http://{ORCHESTRATOR_HOST}:{ORCHESTRATOR_PORT}")
JIRA_MCP_SERVER_URL = os.environ.get("MCP_SERVER_URL", "http://localhost:9000/sse")
ZEPHYR_BASE_URL = os.environ.get("ZEPHYR_BASE_URL")

# Webhook URLs
NEW_REQUIREMENTS_WEBHOOK_URL = f"{ORCHESTRATOR_URL}/new-requirements-available"
STORY_READY_FOR_TEST_CASE_GENERATION_WEBHOOK_URL = f"{ORCHESTRATOR_URL}/story-ready-for-test-case-generation"
EXECUTE_TESTS_WEBHOOK_URL = f"{ORCHESTRATOR_URL}/execute-tests"

# Secrets
JIRA_WEBHOOK_SECRET = os.environ.get("JIRA_WEBHOOK_SECRET")
ZEPHYR_API_TOKEN = os.environ.get("ZEPHYR_API_TOKEN")

# Agent
AGENT_BASE_URL = "http://localhost"
AGENT_HOST = os.environ.get("AGENT_HOST", "localhost")
ATTACHMENTS_REMOTE_FOLDER_PATH = "/tmp"
ATTACHMENTS_LOCAL_FOLDER_PATH = "D://temp"
REMOTE_EXECUTION_AGENTS_URLS = os.environ.get("REMOTE_EXECUTION_AGENTS_URLS")
AGENT_DISCOVERY_PORTS = os.environ.get("AGENT_DISCOVERY_PORTS")

# Test Management System
ZEPHYR_COMMENTS_CUSTOM_FIELD_NAME = "Review Comments"
ZEPHYR_CLIENT_TIMEOUT_SECONDS = 15
ZEPHYR_CUSTOM_FIELDS_JSON_FIELD_NAME = "customFields"
TEST_MANAGEMENT_SYSTEM = os.environ.get("TEST_MANAGEMENT_SYSTEM", "zephyr").lower()

# Test Reporting
TEST_REPORTER = os.environ.get("TEST_REPORTER", "allure").lower()
ALLURE_RESULTS_DIR = "allure-results"
ALLURE_REPORT_DIR = "allure-report"

# OpenTelemetry
OPEN_TELEMETRY_URL = os.environ.get('OTEL_EXPORTER_OTLP_ENDPOINT')

# Common model config
TOP_P = 1.0
TEMPERATURE = 0.0


# Orchestrator
class OrchestratorConfig:
    AUTOMATED_TC_LABEL = "automated"
    AGENTS_DISCOVERY_INTERVAL_SECONDS = 3000
    TASK_EXECUTION_TIMEOUT = 500.0
    AGENT_DISCOVERY_TIMEOUT_SECONDS = 3.0
    MODEL_NAME = "google-gla:gemini-2.5-flash"


# Requirements Review Agent
class RequirementsReviewAgentConfig:
    THINKING_BUDGET = 10000
    OWN_NAME = "Jira Requirements Reviewer"
    PORT = 8001
    PROTOCOL = "http"
    MODEL_NAME = "google-gla:gemini-2.5-pro"


# Test Case Classification Agent
class TestCaseClassificationAgentConfig:
    THINKING_BUDGET = 2000
    OWN_NAME = "Test Case Classification Agent"
    PORT = 8003
    PROTOCOL = "http"
    MODEL_NAME = "google-gla:gemini-2.5-flash"


# Test Case Generation Agent
class TestCaseGenerationAgentConfig:
    THINKING_BUDGET = 0
    OWN_NAME = "Test Case Generation Agent"
    PORT = 8002
    PROTOCOL = "http"
    MODEL_NAME = "google-gla:gemini-2.5-flash"


# Test Case Review Agent
class TestCaseReviewAgentConfig:
    THINKING_BUDGET = 10000
    REVIEW_COMPLETE_STATUS_NAME = "Review Complete"
    OWN_NAME = "Test Case Review Agent"
    PORT = 8004
    PROTOCOL = "http"
    MODEL_NAME = "google-gla:gemini-2.5-pro"
