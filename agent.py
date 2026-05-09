import asyncio
import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_tavily import TavilySearch
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import StdioServerParameters, ClientSession
from mcp.client.stdio import stdio_client

load_dotenv()

async def run_agent(question: str):

    server = StdioServerParameters(
        command="python",
        args=["research_mcp_server.py"]
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Load MCP tools (calculate, fetch_url)
            mcp_tools = await load_mcp_tools(session)

            # Add Tavily as proper search tool
            tavily = TavilySearch(
                max_results=3,
                api_key=os.getenv("TAVILY_API_KEY")
            )

            # Combine all tools
            all_tools = mcp_tools + [tavily]
            print(f"Tools available: {[t.name for t in all_tools]}")

            llm = ChatGroq(
                model="llama-3.3-70b-versatile",
                api_key=os.getenv("GROQ_API_KEY"),
                temperature=0
            )

            llm_with_tools = llm.bind_tools(all_tools)

            print(f"\nQuestion: {question}")
            print("Agent thinking...\n")

            messages = [HumanMessage(content=question)]
            response = await llm_with_tools.ainvoke(messages)

            if response.tool_calls:
                for tool_call in response.tool_calls:
                    print(f"Agent calling: {tool_call['name']}")
                    print(f"With args: {tool_call['args']}")

                    for tool in all_tools:
                        if tool.name == tool_call['name']:
                            tool_result = await tool.ainvoke(tool_call['args'])

                            messages.append(response)
                            messages.append(ToolMessage(
                                content=str(tool_result),
                                tool_call_id=tool_call['id']
                            ))

                            final = await llm_with_tools.ainvoke(messages)
                            print(f"\nFinal Answer:\n{final.content}")
            else:
                print(f"Direct Answer:\n{response.content}")

asyncio.run(run_agent("What is 25 multiplied by 4?"))
# asyncio.run(run_agent("What is ROS2 and what is it used for?"))