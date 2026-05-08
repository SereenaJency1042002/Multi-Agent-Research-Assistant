from mcp.server.fastmcp import FastMCP
import urllib.request
import urllib.parse
import json
import re

mcp = FastMCP("Research Tools Server")

# TOOL 1- calculator
@mcp.tool()
def calculate(expression: str) -> str:
    """Evaluate a math expression. Example: Calculate('2 + 2')"""
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"


# TOOL 2- search the web
@mcp.tool()
def web_search(query: str) -> str:
    """Search the web and return top results for a query."""
    try:
        encoded = urllib.parse.quote(query)
        url = f"https://api.duckduckgo.com/?q={encoded}&format=json&no_html=1"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req,timeout=10) as response:
            data = json.loads(response.read().decode())

        results = []

        if data.get("AbstractText"):
            results.append(f"Summary: {data['AbstractText']}")
            results.append(f"Source: {data.get('AbstractURL','')}")

        for topic in data.get("RelatedTopics",[])[:5]:
            if isinstance(topic, dict) and topic.get("Text"):
                results.append(f"-{topic['Text']}")

        if results:
            return "\n".json(results)
        else:
            return f"No results found for: {query}"

    except Exception as e:
        return f"Search error: {str(e)}"


# TOOL 3 - read a webpage

@mcp.tool()
def fetch_url(url: str) -> str:
    """Fetch a webpage and return clean readable text."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode("utf-8", errors="ignore")

        # Remove scripts and styles
        html = re.sub(r"<scripts[^>]*>.*?</scripts>","",html, flags=re.DOTALL)
        html = re.sub(r"<style[^>]*>.*?</style>","",html, flags=re.DOTALL)

        # Remove all HTML tags
        text = re.sub(r"<[^>]+>"," ",html)

        #Clean whitespace
        text = re.sub(r"\s+"," ",text).strip()

        return text[:2000]

    except Exception as e:
        return f"Fetch error: {str(e)}"


if __name__ == "__main__":
    print("Research MCP Server starting...")
    print("Tool available: calculate,web_search,fetch_url")
    mcp.run(transport="stdio")