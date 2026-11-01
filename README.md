# AI Research System

A multi-agent research assistant built with Streamlit, LangChain, Mistral, Tavily, and BeautifulSoup. It searches for relevant sources, extracts useful material, and turns the results into a structured research report.

## Pipeline

1. Search the web for relevant sources.
2. Scrape and collect source content.
3. Draft a concise, source-aware report.
4. Review the draft for clarity and unsupported claims.

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file with the credentials required by the configured providers, including `MISTRAL_API_KEY` and the search-tool credentials. Start the interface with:

```bash
streamlit run app.py
```

Use the output as research assistance and verify important claims against the linked sources.