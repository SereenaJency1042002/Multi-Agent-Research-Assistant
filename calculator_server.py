from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Calculator Server")

@mcp.tool()
def calculate(expression: str) -> str:
    """Evaluate a math expression. Example: Calculate('2 + 2')"""
    try:
        result = eval(expression)
        return f"Result:{result}"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    print("Calculator MCP Server starting...")
    print("Tool available: calculate")
    mcp.run(transport="stdio")