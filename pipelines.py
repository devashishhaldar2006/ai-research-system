from agents import (
    build_search_agent,
    build_scrape_agent,
    writer_chain,
    critic_chain
)


def get_last_message_content(result):

    messages = result.get("messages", [])

    if not messages:
        return "No response was returned."

    return messages[-1].content


def run_research_pipeline(topic: str) -> dict:

    state = {
        "topic": topic,
        "search_results": "",
        "scrape_results": "",
        "writer_output": "",
        "critic_output": ""
    }

    # ========================================
    # 1. SEARCH AGENT
    # ========================================

    print(f"\n[1/4] Running search agent for: {topic}")

    search_agent = build_search_agent()

    search_result = search_agent.invoke({
        "messages": [
            (
                "user",
                f"""
Research the following topic:

{topic}

Use the web search tool to find several reliable and
relevant sources.

Return the important findings along with the source
titles and URLs.
"""
            )
        ]
    })

    state["search_results"] = get_last_message_content(
        search_result
    )

    print("Search completed.")


    # ========================================
    # 2. SCRAPE AGENT
    # ========================================

    print("[2/4] Running scraping agent...")

    scrape_agent = build_scrape_agent()

    scrape_result = scrape_agent.invoke({
        "messages": [
            (
                "user",
                f"""
You are researching:

{topic}

Below are the results produced by another research agent:

{state["search_results"]}

Identify the most relevant URLs from these results.

Use the scrape_url tool to extract information from
the relevant webpages.

Focus on:

- Important facts
- Statistics
- Explanations
- Evidence
- Information useful for the final report

Return the extracted information and preserve the
original URLs.
"""
            )
        ]
    })

    state["scrape_results"] = get_last_message_content(
        scrape_result
    )

    print("Scraping completed.")


    # ========================================
    # 3. WRITER
    # ========================================

    print("[3/4] Generating research report...")

    research_combined = (
        f"SEARCH RESULTS:\n"
        f"{state['search_results']}\n\n"
        f"SCRAPED CONTENT:\n"
        f"{state['scrape_results']}"
    )

    state["writer_output"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    print("Research report generated.")


    # ========================================
    # 4. CRITIC
    # ========================================

    print("[4/4] Critiquing research report...")

    state["critic_output"] = critic_chain.invoke({
        "topic": topic,
        "report": state["writer_output"]
    })

    print("Critique completed.")

    return state


if __name__ == "__main__":

    topic = input(
        "\nEnter your research topic: "
    ).strip()

    if not topic:
        print("Please enter a research topic.")
    else:
        result = run_research_pipeline(topic)

        print("\n\n========== FINAL REPORT ==========\n")
        print(result["writer_output"])

        print("\n\n========== CRITIQUE ==========\n")
        print(result["critic_output"])