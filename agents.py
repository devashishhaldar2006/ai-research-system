import os

from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI

from tools import web_search, scrape_url


load_dotenv()


MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

if not MISTRAL_API_KEY:
    raise ValueError("MISTRAL_API_KEY is not set in .env")


llm = ChatMistralAI(
    model="mistral-medium-latest",
    temperature=0.2,
    max_tokens=3000,
    api_key=MISTRAL_API_KEY
)


def build_search_agent():

    return create_agent(
        model=llm,
        tools=[web_search]
    )


def build_scrape_agent():

    return create_agent(
        model=llm,
        tools=[scrape_url]
    )


# ==============================
# Writer
# ==============================

writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an expert research writer.

Your job is to transform raw research material into
a clear, factual and well-structured research report.

Rules:

- Use only information provided in the research.
- Do not invent facts.
- Preserve important source URLs.
- Distinguish facts from uncertainty.
- Do not make unsupported claims.
- Prefer concise and informative writing.
"""
    ),
    (
        "human",
        """
Research topic:

{topic}

Research material:

{research}

Write a comprehensive research report using this structure:

# Title

## Executive Summary

## Key Findings

## Detailed Analysis

## Limitations

## Sources

The Sources section must contain the URLs found in the research.
"""
    )
])


writer_chain = (
    writer_prompt
    | llm
    | StrOutputParser()
)


# ==============================
# Critic
# ==============================

critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a rigorous research critic.

Evaluate the research report for:

- Unsupported claims
- Missing information
- Contradictions
- Weak reasoning
- Source quality
- Possible factual problems
- Areas requiring further research

Do not rewrite the report.

Provide specific and actionable feedback.
"""
    ),
    (
        "human",
        """
Research topic:

{topic}

Research report:

{report}

Provide a structured critique with:

1. Overall assessment
2. Potential factual issues
3. Missing information
4. Source concerns
5. Recommended improvements
"""
    )
])


critic_chain = (
    critic_prompt
    | llm
    | StrOutputParser()
)