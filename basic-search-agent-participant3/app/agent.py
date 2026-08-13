import logging
import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.apps.app import App
from google.adk.tools import google_search

load_dotenv()

root_agent = Agent(
    name="basic-search-agent-participant3",
    model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
    description="Agent to answer questions using Google Search.",
    instruction="I can answer your questions by searching the internet. Just ask me anything!",
    tools=[google_search],
)

app = App(root_agent=root_agent, name="app")
