# 🚀 Gemini Enterprise Hackathon - Full Technical Solution

This repository contains the complete reference solution for the Gemini Enterprise (GE) Hackathon across all technical tracks.

---

## 📁 Repository Structure

- **`basic-search-agent-participant1/`**: Participant 1 Basic Search Agent with `google_search` tools & ADK `App`.
- **`basic-search-agent-participant2/`**: Participant 2 Basic Search Agent.
- **`basic-search-agent-participant3/`**: Participant 3 Basic Search Agent.
- **`bq-trend-agent/`**: BigQuery Trends Analyst Agent using `BigQueryToolset` with `WriteMode.BLOCKED`, dynamic `refresh_date` Jinja2 prompt rendering, and SQL constraints.
- **`github-mcp-agent/`**: GitHub MCP Agent configured with `MCPToolset`, `StreamableHTTPConnectionParams`, and authenticated GitHub actions.
- **`ge-config/`**: Gemini Enterprise App configuration manifest (`ge_app_manifest.json`).

---

## 🛠️ Setup & Local Testing

Each agent uses `uv` for dependency management and ADK for execution:

```bash
# 1. Install dependencies
uv sync

# 2. Configure environment variables (.env)
cp app/.env.example app/.env

# 3. Test locally via ADK Web UI
uv run adk web . --port 8501 --reload_agents --allow_origins "*"

# 4. Deploy backend to Agent Engine
make backend

# 5. Register in Gemini Enterprise App
make register-gemini-enterprise
```
