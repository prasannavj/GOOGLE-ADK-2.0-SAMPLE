
from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import (
    StreamableHTTPConnectionParams,
)

# Connect to already running MCP server
mcp_tools = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="http://127.0.0.1:9000/mcp",
        timeout=30,
    )
)

# Google ADK agent
root_agent = Agent(
    name="mcp_client_agent",
    model="gemini-3.6-flash",
    instruction="""
    You are an assistant connected to an MCP server.

    Use the MCP tools to:
    - Add numbers
    - Multiply numbers
    - Retrieve employee information

    Always call the appropriate tool.
    """,
    tools=[mcp_tools],
)
