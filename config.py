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
GOOGLE_CLOUD_LOGGING_ENABLED = os.environ.get("GOOGLE_CLOUD_LOGGING_ENABLED", "False").lower() in ("true", "1", "t")

# URLs
ORCHESTRATOR_HOST = os.environ.get("ORCHESTRATOR_HOST", "localhost")
ORCHESTRATOR_PORT = int(os.environ.get("ORCHESTRATOR_PORT", "8000"))
ORCHESTRATOR_URL = os.environ.get("ORCHESTRATOR_URL", f"http://{ORCHESTRATOR_HOST}:{ORCHESTRATOR_PORT}")
JIRA_MCP_SERVER_URL = os.environ.get("JIRA_MCP_SERVER_URL", "http://localhost:9000/sse")
ZEPHYR_BASE_URL = os.environ.get("ZEPHYR_BASE_URL")
JIRA_BASE_URL = os.environ.get("JIRA_URL")
JIRA_USER = os.environ.get("JIRA_USERNAME")
JIRA_TOKEN = os.environ.get("JIRA_API_TOKEN")

# Webhook URLs
NEW_REQUIREMENTS_WEBHOOK_URL = f"{ORCHESTRATOR_URL}/new-requirements-available"
STORY_READY_FOR_TEST_CASE_GENERATION_WEBHOOK_URL = f"{ORCHESTRATOR_URL}/story-ready-for-test-case-generation"
EXECUTE_TESTS_WEBHOOK_URL = f"{ORCHESTRATOR_URL}/execute-tests"

# Secrets
JIRA_WEBHOOK_SECRET = os.environ.get("JIRA_WEBHOOK_SECRET")
ZEPHYR_API_TOKEN = os.environ.get("ZEPHYR_API_TOKEN")

XRAY_BASE_URL = os.environ.get("XRAY_BASE_URL")
XRAY_CLIENT_ID = os.environ.get("XRAY_CLIENT_ID")
XRAY_CLIENT_SECRET = os.environ.get("XRAY_CLIENT_SECRET")
XRAY_PRECONDITIONS_FIELD_ID = os.environ.get("XRAY_PRECONDITIONS_FIELD_ID", "Pre-conditions")

# Agent
AGENT_BASE_URL = os.environ.get("AGENT_BASE_URL", "http://localhost")
MCP_SERVER_ATTACHMENTS_FOLDER_PATH = "/tmp"
ATTACHMENTS_DESTINATION_FOLDER_PATH = "D://temp"
REMOTE_EXECUTION_AGENT_HOSTS = os.environ.get("REMOTE_EXECUTION_AGENT_HOSTS")
AGENT_DISCOVERY_PORTS = os.environ.get("AGENT_DISCOVERY_PORTS")
USE_GOOGLE_CLOUD_STORAGE = os.environ.get("USE_CLOUD_STORAGE", "False").lower() in ("true", "1", "t")
GOOGLE_CLOUD_STORAGE_BUCKET_NAME = os.environ.get("CLOUD_STORAGE_BUCKET_NAME")
JIRA_ATTACHMENTS_CLOUD_STORAGE_FOLDER = os.environ.get("JIRA_ATTACHMENTS_CLOUD_STORAGE_FOLDER", "jira")
MCP_SERVER_TIMEOUT_SECONDS = 30

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
    AGENTS_DISCOVERY_INTERVAL_SECONDS = 300
    TASK_EXECUTION_TIMEOUT = 500.0
    AGENT_DISCOVERY_TIMEOUT_SECONDS = 30
    INCOMING_REQUEST_WAIT_TIMEOUT = AGENT_DISCOVERY_TIMEOUT_SECONDS + 5
    MODEL_NAME = "google-gla:gemini-2.5-flash"
    API_KEY = os.environ.get("ORCHESTRATOR_API_KEY")


# Requirements Review Agent
class RequirementsReviewAgentConfig:
    THINKING_BUDGET = 10000
    OWN_NAME = "Jira Requirements Reviewer"
    PORT = int(os.environ.get("PORT", "8001"))
    EXTERNAL_PORT = int(os.environ.get("EXTERNAL_PORT", "443"))
    PROTOCOL = "http"
    MODEL_NAME = "google-gla:gemini-2.5-pro"
    MAX_REQUESTS_PER_TASK = 10


# Test Case Classification Agent
class TestCaseClassificationAgentConfig:
    THINKING_BUDGET = 2000
    OWN_NAME = "Test Case Classification Agent"
    PORT = int(os.environ.get("PORT", "8003"))
    EXTERNAL_PORT = int(os.environ.get("EXTERNAL_PORT", "443"))
    PROTOCOL = "http"
    MODEL_NAME = "google-gla:gemini-2.5-flash"
    MAX_REQUESTS_PER_TASK = 5


# Test Case Generation Agent
class TestCaseGenerationAgentConfig:
    THINKING_BUDGET = 0
    OWN_NAME = "Test Case Generation Agent"
    PORT = int(os.environ.get("PORT", "8002"))
    EXTERNAL_PORT = int(os.environ.get("EXTERNAL_PORT", "443"))
    PROTOCOL = "http"
    MODEL_NAME = "google-gla:gemini-2.5-flash"
    MAX_REQUESTS_PER_TASK = 10


# Test Case Review Agent
class TestCaseReviewAgentConfig:
    THINKING_BUDGET = 10000
    REVIEW_COMPLETE_STATUS_NAME = "Review Complete"
    OWN_NAME = "Test Case Review Agent"
    PORT = int(os.environ.get("PORT", "8004"))
    EXTERNAL_PORT = int(os.environ.get("EXTERNAL_PORT", "443"))
    PROTOCOL = "http"
    MODEL_NAME = "google-gla:gemini-2.5-pro"
    MAX_REQUESTS_PER_TASK = 5
