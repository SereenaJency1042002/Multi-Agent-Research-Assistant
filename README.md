# Multi-Agent-Research-Assistant# MARA — Multi-Agent Research Assistant

> Powered by LangGraph · MCP · Groq · Tavily · LangSmith

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?style=flat&logo=streamlit)](https://multi-agent-research-assistant-mara.streamlit.app)
[![LangSmith](https://img.shields.io/badge/Traced%20with-LangSmith-1C3C3C?style=flat)](https://smith.langchain.com)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python)](https://python.org)

---

## What is MARA?

MARA is a multi-agent AI system that researches any topic autonomously. The user types a question in plain English. Four specialized AI agents collaborate to produce a structured, detailed research report — no manual searching required.

**Live demo:** [multi-agent-research-assistant-mara.streamlit.app]
(https://multi-agent-research-assistant-mara.streamlit.app/)

---

## How it works

```
User types research question
         ↓
┌─────────────────────┐
│   Planner Agent     │  Breaks question into 3 focused sub-tasks
└─────────────────────┘
         ↓
┌─────────────────────┐
│   Searcher Agent    │  Searches the web for each sub-task via Tavily
└─────────────────────┘
         ↓
┌─────────────────────┐
│   Analyst Agent     │  Extracts 8 key insights from search results
└─────────────────────┘
         ↓
┌─────────────────────┐
│   Writer Agent      │  Produces structured research report
└─────────────────────┘
         ↓
   Final report delivered to user
```

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Agent Orchestration | LangGraph | Graph-based multi-agent workflow |
| Tool Protocol | MCP (Model Context Protocol) | Connect agents to external tools |
| LLM | Groq — Llama 3.3 70B | Fast free inference |
| Web Search | Tavily API | AI-optimized search results |
| Observability | LangSmith | Trace every agent step and decision |
| UI | Streamlit | Web interface for demo and use |
| Deployment | Streamlit Cloud | Public live URL |

---

## MCP Server

A custom Python MCP server exposes 3 tools to the agents:

```python
calculate(expression: str)  # evaluates math expressions
web_search(query: str)      # searches via DuckDuckGo
fetch_url(url: str)         # fetches and cleans webpage content
```

---

## Agent State

All 4 agents share a typed state object. Each agent reads from it and writes its output back:

```python
class ResearchState(TypedDict):
    question:       str         # original user question
    sub_tasks:      List[str]   # planner output
    search_results: List[str]   # searcher output
    insights:       List[str]   # analyst output
    final_report:   str         # writer final report
```

---

## LangSmith Observability

Every agent step, LLM call, and tool use is traced in LangSmith. This provides full visibility into agent decisions and enables systematic debugging.

---

## Project Structure

```
├── MARA.py                  # Streamlit web app — main entry point
├── research_graph.py        # LangGraph 4-agent pipeline
├── research_mcp_server.py   # Custom MCP server — 3 tools
├── agent.py                 # Single agent prototype
├── requirements.txt         # Dependencies
├── DEVLOG.md                # Daily development log
└── .env                     # API keys (not committed)
```

---

## Run Locally

```bash
# Clone the repository
git clone https://github.com/SereenaJency1042002/Multi-Agent-Research-Assistant
cd Multi-Agent-Research-Assistant

# Install dependencies
pip install -r requirements.txt

# Add your API keys to .env
# Run the app
streamlit run MARA.py
```

### Required API Keys

| Key | Where to get it | Free tier |
|-----|----------------|-----------|
| `GROQ_API_KEY` | console.groq.com | ✅ Free |
| `TAVILY_API_KEY` | app.tavily.com | ✅ 1000/month |
| `LANGSMITH_API_KEY` | smith.langchain.com | ✅ Free |

---

## Author

**Sereena Jency**
Master's student — Automation and Information Technology
TH Köln, Germany

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Sereena%20Jency-0077B5?style=flat&logo=linkedin)](https://linkedin.com/in/sereena-jency-711983301)
[![GitHub](https://img.shields.io/badge/GitHub-SereenaJency1042002-181717?style=flat&logo=github)](https://github.com/SereenaJency1042002)