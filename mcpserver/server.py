
from mcp.server.fastmcp import FastMCP

# Initialize MCP Server
mcp = FastMCP(
    "MyLocalMCPServer",
    host="127.0.0.1",
    port=9000
)

# TOOL 1: Add two numbers
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers and return the result."""
    return a + b


# TOOL 2: Multiply two numbers
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers and return the result."""
    return a * b


# TOOL 3: Employee information
@mcp.tool()
def get_employee(employee_id: int) -> dict:
    """Retrieve information about an employee."""
    employees = {
        101: {"name": "John", "department": "AI"},
        102: {"name": "David", "department": "Data Science"},
        103: {"name": "Sarah", "department": "Engineering"}
    }

    return employees.get(
        employee_id,
        {"error": "Employee not found"}
    )


# RESOURCE: Expose information
@mcp.resource("greeting://{name}")
def greeting(name: str) -> str:
    """Return a personalized greeting."""
    return f"Hello {name}, welcome to MCP!"


# PROMPT: Reusable prompt template
@mcp.prompt()
def explain_topic(topic: str) -> str:
    """Generate an instruction to explain a topic."""
    return (
        f"Explain {topic} in simple terms "
        "with a practical example."
    )


# Start MCP server
if __name__ == "__main__":
        mcp.run(transport="streamable-http")

