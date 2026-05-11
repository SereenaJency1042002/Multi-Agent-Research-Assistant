import asyncio
import os
from dotenv import load_dotenv
from typing import TypedDict, List

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langchain_tavily import TavilySearch
from langgraph.graph import StateGraph, END

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGSMITH_PROJECT")

#SHARED STATE - MEMORY SHARED BETWEEN AGENTS; EACH AGENT READS FROM IT 
class ResearchState(TypedDict):
    question:           str             #original user question
    sub_tasks:          List[str]       #planner output
    search_results:     List[str]       #searcher output
    insights:           List[str]       #analyst output
    final_report:       str             #writer output


#LLM SETUP
llm = ChatGroq(
    model = "llama-3.3-70b-versatile",
    api_key = os.getenv("GROQ_API_KEY"),
    temperature = 0
)

#AGENT 1 : PLANNER (takes the qn nd breaks into 3 sub tasks)
async def planner_agent(state: ResearchState) -> ResearchState:
    print("\n[PLANNER] Breaking question into sub-tasks...")

    prompt = f"""Break this research question into exactly 3 specific sub-tasks.
Return ONLY a numbered list. No explanation.

Question: {state['question']}

Format:
1. sub-task one
2. sub-task two
3. sub-task three"""

    response = await llm.ainvoke([HumanMessage(content=prompt)])


    lines = response.content.strip().split('\n')
    sub_tasks = []
    for line in lines:
        line = line.strip()
        if line and line[0].isdigit():

            task = line.split('.',1)[1].strip()
            sub_tasks.append(task)

    print(f"[PLANNER] Sub-tasks created: {sub_tasks}")
    return {"sub_tasks": sub_tasks}


#AGENT 2 : SEARCHER(takes each sub-task and searches the web for information)

async def searcher_agent(state: ResearchState) -> ResearchState:
    print("\n[SEARCHER] Searching web for each sub-task...")


    tavily = TavilySearch(
        max_results=2,
        tavily_api_key = os.getenv("TAVILY_API_KEY")
    )


    all_results = []
    for task in state['sub_tasks']:
        print(f"[SEARCHER] searching: {task}")
        result = await tavily.ainvoke(task)
        all_results.append(f"Sub-task: {task}\nResult: {result}")


    print(f"[SEARCHER] Found {len(all_results)} results")
    return {"search_results": all_results}



#AGENT 3 : ANALYST(Reads all search results and extracts key insights)

async def analyst_agent(state: ResearchState) -> ResearchState:
    print("\n[ANALYST] Extracting key insights...")

    results_text = "\n\n".join(state['search_results'])

    prompt = f"""Read these search results and extract 5 key insights.
Return ONLY a numbered list of insights. Be specific and factual.

Search Result:
{results_text}

Format:
1. insight one
2. insight two
3. insight three 
4. insight four
5. insight five"""

    response = await llm.ainvoke([HumanMessage(content=prompt)])

    lines = response.content.strip().split('\n')
    insights = []
    for line in lines: 
        line = line.strip()
        if line and line[0].isdigit():
            insight = line.split('.',1)[1].strip()
            insights.append(insight)


    print(f"[ANALYST] Extracted {len(insights)} insights")
    return {"insights": insights}


#AGENT 4 : WRITER(taes all the insights and writes a structured final report)

async def writer_agent(state: ResearchState) -> ResearchState:
    print("\n[WRITER] Writing final report...")

    insights_text = "\n".join([f"-{i}" for i in state['insights']])

    prompt = f"""Write a clear, structured research report based on these insights.

Original Question: {state['question']}

Key Insights:
{insights_text}

Write a report with:
-A short introduction
-Main findings section
-A brief conclusion

Keep it professional and factual."""

    response = await llm.ainvoke([HumanMessage(content=prompt)])

    print("[WRITER] Report Complete.")
    return {"final_report": response.content}




#BUILD THE GRAPH
def build_graph():
    graph = StateGraph(ResearchState)

    #add all 4 agents as nodes
    graph.add_node("planner",  planner_agent)
    graph.add_node("searcher", searcher_agent)
    graph.add_node("analyst",  analyst_agent)
    graph.add_node("writer",  writer_agent)

    #connect them in sequence
    graph.set_entry_point("planner")
    graph.add_edge("planner", "searcher")
    graph.add_edge("searcher", "analyst")
    graph.add_edge("analyst", "writer")
    graph.add_edge("writer", END)

    return graph.compile()


#Run the pipeline
async def run_researcher(question: str):
    print(f"\nResearch Question: {question}")
    print("="*50)

    graph = build_graph()

    result = await graph.ainvoke({
        "question": question,
        "sub_tasks": [],
        "search_results": [],
        "insights": [],
        "final_report": ""
    })


    print("\n" + "="*50)
    print("FINAL REPORT:")
    print("="*50)
    print(result['final_report'])



#asyncio.run(run_researcher("What is ROS2 and how is it used in industrial robotics?"))
#asyncio.run(run_researcher("What is AI and how is it used in robotics?"))
asyncio.run(run_researcher("What is langgraph and langchain. How is it used in AI?"))