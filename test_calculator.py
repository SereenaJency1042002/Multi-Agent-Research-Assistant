from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio

async def test():
    server = StdioServerParameters(
        command="python",
        args=["calculator_server.py"]
    )
    
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            print("Tools found:", [t.name for t in tools.tools])
            
            # Call calculate tool
            result = await session.call_tool("calculate", {"expression": "10 * 5 + 3"})
            print("10 * 5 + 3 =", result.content[0].text)

asyncio.run(test())