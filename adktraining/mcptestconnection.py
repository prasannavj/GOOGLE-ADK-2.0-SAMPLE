
import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


async def main():

    MCP_URL = "http://127.0.0.1:9000/mcp"

    # Connect to running MCP server
    async with streamable_http_client(MCP_URL) as (
        read,
        write,
    ):

        async with ClientSession(read, write) as session:

            # Initialize MCP session
            await session.initialize()

            # Discover available tools
            tools = await session.list_tools()

            print("\nAvailable MCP Tools:")

            for tool in tools.tools:
                print(f" - {tool.name}")

            # Invoke addition MCP tool
            result = await session.call_tool(
                "add",
                arguments={"a": 10, "b": 20},
            )

            print("\nAddition Result:")
            print(result.content)

            # Invoke employee MCP tool
            employee = await session.call_tool(
                "get_employee",
                arguments={"employee_id": 102},
            )

            print("\nEmployee Result:")
            print(employee.content)


if __name__ == "__main__":
    asyncio.run(main())
