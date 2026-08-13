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
import google.auth

try:
    from dotenv import find_dotenv, load_dotenv
    load_dotenv(find_dotenv())
except ImportError:
    # dotenv is optional; environment variables can be set manually
    pass

from google.adk.agents import Agent
from google.adk.apps.app import App
from google.adk.tools.bigquery import BigQueryCredentialsConfig, BigQueryToolset
from google.adk.tools.bigquery.config import BigQueryToolConfig, WriteMode

try:
    from .utils import get_latest_refresh_date, load_nl2sql_with_few_shot_prompt
except ImportError:
    from utils import get_latest_refresh_date, load_nl2sql_with_few_shot_prompt

# Setup Google Cloud Environment Credentials
# This will pick up credentials in Cloud Shell, Vertex AI, or local ADC
credentials, project_id = google.auth.default()

os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

# Define constants for this agent
AGENT_NAME = "google_trends_bigquery_analyst"
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Configure BigQuery Tools
# FIX: Explicitly pass your project_id as the compute_project_id to avoid 403 error
tool_config = BigQueryToolConfig(
    write_mode=WriteMode.BLOCKED,
    compute_project_id=project_id 
)

# Configure credentials for the BigQuery connection
credentials_config = BigQueryCredentialsConfig(credentials=credentials)

# Instantiate the BigQuery toolset
bigquery_toolset = BigQueryToolset(
    credentials_config=credentials_config, 
    bigquery_tool_config=tool_config
)

# Prompt Engineering & Instructions
# Load and render the instruction prompt with the latest refresh date
latest_date = get_latest_refresh_date()
if not latest_date:
    latest_date = "2026-05-01"  # Fallback date if connection fails
    
agent_instruction = load_nl2sql_with_few_shot_prompt(
    refresh_date_value=latest_date
)

# Define the Agent with BigQuery Tools
root_agent = Agent(
    model=GEMINI_MODEL,
    name=AGENT_NAME,
    description=(
        "A BigQuery SQL expert that answers natural language questions about"
        " top trending and rising international terms, according to Google search queries."
    ),
    instruction=agent_instruction,
    tools=[bigquery_toolset],
)

# Expose the app for ADK execution and deployment
app = App(root_agent=root_agent, name="app")
