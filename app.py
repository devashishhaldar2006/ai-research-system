import streamlit as st

from pipelines import run_research_pipeline


st.set_page_config(
    page_title="AI Research System",
    page_icon="🔎",
    layout="wide"
)


# ========================================
# CUSTOM CSS
# ========================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        color: #777;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    .agent-card {
        padding: 1rem;
        border: 1px solid rgba(128,128,128,0.25);
        border-radius: 12px;
        margin-bottom: 1rem;
    }

    .source-box {
        padding: 1rem;
        border-radius: 10px;
        background: rgba(128,128,128,0.08);
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ========================================
# HEADER
# ========================================

st.markdown(
    '<div class="main-title">AI Research System</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    Multi-agent web research powered by Mistral, Tavily,
    BeautifulSoup and LangChain.
    </div>
    """,
    unsafe_allow_html=True
)


# ========================================
# SIDEBAR
# ========================================

with st.sidebar:

    st.header("Research Pipeline")

    st.markdown(
        """
        **1. Search Agent**

        Finds relevant sources using Tavily.

        **2. Scrape Agent**

        Extracts information from webpages.

        **3. Writer Agent**

        Synthesizes the collected research.

        **4. Critic Agent**

        Evaluates the final report.
        """
    )

    st.divider()

    st.caption(
        "AI Research System • Multi-Agent Architecture"
    )


# ========================================
# INPUT
# ========================================

topic = st.text_area(
    "Research topic",
    placeholder=(
        "Example: Recent advancements in "
        "AI agent architectures"
    ),
    height=120
)


research_button = st.button(
    "🔎 Start Research",
    type="primary",
    use_container_width=True
)


# ========================================
# RUN PIPELINE
# ========================================

if research_button:

    if not topic.strip():

        st.warning(
            "Please enter a research topic."
        )

    else:

        try:

            with st.status(
                "Running research pipeline...",
                expanded=True
            ) as status:

                st.write(
                    "🔎 Search Agent: finding sources..."
                )

                result = run_research_pipeline(
                    topic.strip()
                )

                st.write(
                    "🌐 Scrape Agent: extracting webpage content..."
                )

                st.write(
                    "✍️ Writer Agent: generating report..."
                )

                st.write(
                    "🔬 Critic Agent: reviewing report..."
                )

                status.update(
                    label="Research completed",
                    state="complete"
                )


            # ========================================
            # REPORT
            # ========================================

            st.divider()

            st.header("Research Report")

            st.markdown(
                result["writer_output"]
            )


            # ========================================
            # CRITIQUE
            # ========================================

            st.divider()

            st.header("Research Critique")

            st.markdown(
                result["critic_output"]
            )


            # ========================================
            # RAW RESEARCH
            # ========================================

            with st.expander(
                "View raw search results"
            ):

                st.text(
                    result["search_results"]
                )


            with st.expander(
                "View scraped research"
            ):

                st.text(
                    result["scrape_results"]
                )


        except Exception as e:

            st.error(
                f"Research pipeline failed: {str(e)}"
            )