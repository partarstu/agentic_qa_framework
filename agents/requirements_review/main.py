# SPDX-FileCopyrightText: 2025 Taras Paruta (partarstu@gmail.com)
#
# SPDX-License-Identifier: Apache-2.0

from pydantic_ai.mcp import MCPServerSSE

import config
from agents.agent_base import AgentBase, ATTACHMENTS_REMOTE_FOLDER_PATH
from agents.requirements_review.prompt import RequirementsReviewSystemPrompt
from common import utils
from common.models import JiraUserStory, RequirementsReviewFeedback

logger = utils.get_logger("reviewer_agent")
jira_mcp_server = MCPServerSSE(url=config.JIRA_MCP_SERVER_URL)


class RequirementsReviewAgent(AgentBase):
    def __init__(self):
        atlassian_mcp_server = jira_mcp_server
        instruction_prompt = RequirementsReviewSystemPrompt(
            attachments_remote_folder_path=ATTACHMENTS_REMOTE_FOLDER_PATH
        )
        super().__init__(
            agent_name=config.RequirementsReviewAgentConfig.OWN_NAME,
            host=config.AGENT_HOST,
            port=config.RequirementsReviewAgentConfig.PORT,
            protocol=config.RequirementsReviewAgentConfig.PROTOCOL,
            model_name=config.RequirementsReviewAgentConfig.MODEL_NAME,
            output_type=RequirementsReviewFeedback,
            instructions=instruction_prompt.get_prompt(),
            mcp_servers=[atlassian_mcp_server],
            deps_type=JiraUserStory,
            description="Agent which does the review of requirements including Jira user stories",
            tools=[self._get_media_file_content]
        )

    def get_thinking_budget(self) -> int:
        return config.RequirementsReviewAgentConfig.THINKING_BUDGET


if __name__ == "__main__":
    RequirementsReviewAgent().start_as_server()
