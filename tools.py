from bs4 import BeautifulSoup
from langchain_core.tools import tool
from tavily import TavilyClient

import os
import requests

from dotenv import load_dotenv


load_dotenv()


TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY is not set in .env")


tavily = TavilyClient(
    api_key=TAVILY_API_KEY
)


@tool
def web_search(query: str) -> str:
    """
    Search the web for recent and reliable information on a topic.

    Returns titles, URLs, and content snippets from the top search
    results. Use this tool when you need to find information on
    the web.
    """

    try:
        response = tavily.search(
            query=query,
            max_results=5
        )

        results = response.get("results", [])

        if not results:
            return "No search results were found."

        formatted_results = []

        for index, result in enumerate(results, start=1):
            formatted_results.append(
                f"""
SOURCE {index}

Title: {result.get("title", "N/A")}
URL: {result.get("url", "N/A")}
Content: {result.get("content", "N/A")}
"""
            )

        return "\n".join(formatted_results)

    except Exception as e:
        return f"Web search failed: {str(e)}"


@tool
def scrape_url(url: str) -> str:
    """
    Scrape the readable text from a given webpage URL.

    Removes scripts, styles, navigation, headers, footers and
    sidebars. Returns the first 6000 characters of readable content.
    """

    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/154.0 Safari/537.36"
                )
            }
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for tag in soup(
            [
                "script",
                "style",
                "nav",
                "footer",
                "header",
                "aside",
                "noscript"
            ]
        ):
            tag.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        return text[:6000]

    except Exception as e:
        return f"Scraping failed for {url}: {str(e)}"