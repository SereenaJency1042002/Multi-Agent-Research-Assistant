# Dev Log — MARA
## Multi-Agent Research Assistant
Sereena Jency · TH Köln · Automation & IT · AI and Data Science

---

| Date | Day | Focus | Status |
|------|-----|-------|--------|
| 08.05.2026 | 01 | Environment setup + MCP | ✅ |
| 09.05.2026 | 02 | First MCP tool | ✅ |
| 10.05.2026 | 03 | Complete MCP server | ✅ |
| 11.05.2026 | 04 | Connected agent to LLM | ✅ |
| 12.05.2026 | 05 | Built 4-agent pipeline | ✅ |
| 13.05.2026 | 06 | LangSmith + Streamlit UI + Deployment | ✅ |

---

## Day 01 · 08.05.2026
**Focus:** Environment setup + MCP architecture

**Deliverables:**
- GitHub Codespaces running — Python 3.12.1
- MCP Python SDK installed
- MCP core primitives understood — Tools, Resources, Prompts

**Key Technical Decisions:**
- stdio transport selected for local development
- Single MCP server will expose all tools — simpler connectivity

**Blockers:**
- Official docs were overwhelming — resolved by filtering
  to only project-relevant concepts

---

## Day 02 · 09.05.2026
**Focus:** First MCP tool from scratch

**Deliverables:**
- calculate() tool built and tested
- ClientSession confirms tool discovery and execution
- calculator_server.py renamed to research_mcp_server.py

**Key Technical Decisions:**
- @mcp.tool() decorator adopted for all tools going forward
- Tool returns string — consistent interface for all agents
- stdio transport confirmed working end to end

**Blockers:** None

---

## Day 03 · 10.05.2026
**Focus:** Complete MCP server — all 3 tools

**Deliverables:**
- web_search() built via DuckDuckGo free API
- fetch_url() built with HTML stripping via re module
- All 3 tools verified via test_server.py

**Key Technical Decisions:**
- User-Agent header added to bypass bot detection
- HTML stripping pipeline: remove scripts → remove styles
  → remove tags → clean whitespace → return 2000 chars
- DuckDuckGo selected for zero-config testing phase

**Known Issues:**
- DuckDuckGo returns empty for some queries — Tavily upgrade planned

---

## Day 04 · 11.05.2026
**Focus:** Connecting MCP server to real AI agent

**Deliverables:**
- agent.py built — MCP tools connected to Groq LLM
- Agent correctly picks calculate for math questions
- Agent correctly picks Tavily for research questions
- Tool results returned to LLM via ToolMessage for final answer

**Key Technical Decisions:**
- temperature=0 added for reliable tool call generation
- Switched from DuckDuckGo to Tavily — built for AI agents
- TavilySearch replaces TavilySearchResults (deprecated in 1.x)

**Blockers:**
- LangChain 1.x removed AgentExecutor — rewrote agent approach
- llama3-groq-70b-8192-tool-use-preview decommissioned by Groq
- TavilySearchResults deprecated — migrated to langchain-tavily

---

## Day 05 · 12.05.2026
**Focus:** LangGraph 4-agent pipeline

**Deliverables:**
- research_graph.py built with 4 specialized agents
- Planner breaks question into 3 sub-tasks
- Searcher fetches web results for each sub-task
- Analyst extracts 8 key insights from results
- Writer produces structured professional report
- Full pipeline tested end to end successfully

**Key Technical Decisions:**
- ResearchState TypedDict shared across all 4 agents
- Each agent reads state, does one job, writes back to state
- LangGraph controls flow: Planner→Searcher→Analyst→Writer
- set_entry_point and add_edge define the pipeline sequence

**Self-tested:**
Pipeline verified with 3 different questions —
ROS2, AI in robotics, LangChain vs LangGraph —
all produced accurate structured reports

**Blockers:** None

---

## Day 06 · 13.05.2026
**Focus:** LangSmith tracing + Streamlit UI + Deployment

**Deliverables:**
- LangSmith integrated — all agent steps visible in dashboard
- Trace confirmed: 0% error rate, 7.83s latency
- MARA.py built — full web interface for research pipeline
- User can type any question and receive structured report
- Progress shown during agent execution via st.status()
- Sub-tasks and insights displayed in expandable sections
- MARA deployed on Streamlit Cloud
- App tested on mobile — works perfectly

**Key Technical Decisions:**
- LANGCHAIN_TRACING_V2 enables automatic tracing
- LangSmith project name organizes traces by project
- st.status() shows live progress during 30 second pipeline
- st.expander() organises sub-tasks and insights cleanly
- st.secrets used for secure API key management on cloud
- python-dotenv kept for local development

**Blockers:**
- KeyError on insights — fixed by using correct dictionary key
- TypeError on list — fixed with isinstance check
- requirements.txt missing s — fixed
- os.getenv returning None on cloud — fixed with st.secrets.get()

**What I got out of this project:**
Learned multiple frameworks from scratch in 6 days.
Understood the skeleton of agentic AI by actually building it.
Got comfortable debugging real production errors that
tutorials never show you.