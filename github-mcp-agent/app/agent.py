# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.apps.app import App
from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams
import os
from pathlib import Path

# Define o caminho para o arquivo .env dentro da pasta app
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)


# 1. Fetch and validate GitHub Token
GITHUB_TOKEN = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("Error: GITHUB_PERSONAL_ACCESS_TOKEN is not configured in your .env file.")

# 2. Define the MCP Toolset for GitHub
# This toolset dynamically fetches and mounts tools exposed by the GitHub MCP server.
mcp_tools = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="https://api.githubcopilot.com/mcp/",
        headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
        },
    ),
    # Optional: Limit the tools exposed to the agent to keep the context clean
    tool_filter=[
        "search_repositories",
        "search_issues",
        "list_issues",
        "get_issue",
        "list_pull_requests",
        "get_pull_request",
    ],
)

# 3. Initialize the Root Agent
root_agent = Agent(
    name="github_mcp_agent",
    model=os.getenv("MODEL_NAME", "gemini-2.5-flash"),
    description="A GitHub assistant that interacts with repositories using Model Context Protocol (MCP).",
    instruction="""You are a highly skilled GitHub technical assistant.
    - Use your MCP tools to search for repositories, read issue lists, and analyze pull requests.
    - When asked about a repository, always run search_repositories first to ensure you have the correct name and owner.
    - Provide clear, bulleted summaries of issues and pull requests.
    - Always include direct markdown links to the GitHub UI when presenting results.
    - Be precise and concise in your summaries.""",
    tools=[mcp_tools],
)

# 4. Expose the app for ADK execution and deployment
app = App(root_agent=root_agent, name="app")
