from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio

async def test():
    server = StdioServerParameters(
        command="python",
        args=["research_mcp_server.py"]
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List all tools
            tools = await session.list_tools()
            print("Tools found:", [t.name for t in tools.tools])

            # Test calculate
            result = await session.call_tool("calculate", {"expression": "15 * 4"})
            print("Calculate 15*4:", result.content[0].text)

            # Test web_search
            result = await session.call_tool("web_search", {"query": "Bosch AI robotics"})
            print("Web search result:", result.content[0].text[:200])

            # Test fetch_url
            result = await session.call_tool("fetch_url", {"url": "https://wikipedia.org/wiki/Robotics"})
            print("Fetch URL result:", result.content[0].text[:200])

asyncio.run(test())