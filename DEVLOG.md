# Development Log
## Multi-Agent Research Assistant
Sereena Jency · TH Köln · Automation & IT Masters

---

| Date | Day | Focus | Status |
|------|-----|-------|--------|
| 08.05.2026 | 01 | Environment setup + MCP fundamentals | ✅ |
| 09.05.2026 | 02 | Calculator MCP server | ✅ |
| 10.05.2026 | 03 | Complete MCP server — 3 tools | ✅ |

---

## Day 01 · 08.05.2026
**Focus:** Development environment + MCP architecture

**Deliverables:**
- GitHub Codespaces configured — Python 3.12.1
- MCP Python SDK installed
- MCP core primitives studied — Tools, Resources, Prompts

**Key Technical Decisions:**
- Selected stdio transport for local development
- Single MCP server will expose all tools — simpler agent connectivity

**Blockers:** Information overload from official docs — resolved by
filtering to project-relevant concepts only

---

## Day 02 · 09.05.2026
**Focus:** First MCP tool implementation

**Deliverables:**
- calculate() tool implemented from scratch
- ClientSession test confirms tool discovery and execution
- Renamed calculator_server.py → research_mcp_server.py

**Key Technical Decisions:**
- @mcp.tool() decorator pattern adopted for all tools
- Tool returns string type — consistent interface for all agents
- stdio transport confirmed working end to end

**Blockers:** None

---

## Day 03 · 10.05.2026
**Focus:** Complete MCP server — all 3 tools

**Deliverables:**
- web_search() implemented via DuckDuckGo free API
- fetch_url() implemented with HTML stripping via re module
- All 3 tools verified via test_server.py

**Key Technical Decisions:**
- User-Agent header added to bypass bot detection on requests
- HTML stripping pipeline: remove scripts → remove styles →
  remove tags → clean whitespace → return 2000 chars
- DuckDuckGo selected for zero-config testing phase

**Known Issues:**
- DuckDuckGo returns empty results for some specific queries

**Planned:**
- Upgrade web_search to Tavily API on Day 5

---