from orchestration.parallel_runner import run_all_agents
from orchestration.synthesis_agent import synthesize

from rag.retriever import retrieve_documents

from p3.personalization import personalize_user


def run_pipeline(
    user_id,
    ticker,
    current_prices
):
    """
    Run the complete HackVerse AI pipeline.
    """

    # ==================================================
    # 1. RUN MARKET AGENTS
    # ==================================================

    agent_results = run_all_agents(ticker)

    # ==================================================
    # 2. RAG RETRIEVAL
    # ==================================================

    query = (
        f"{ticker} financial performance "
        f"investment outlook"
    )

    try:

        retrieved_documents = retrieve_documents(
            query,
            top_k=3
        )

    except Exception as error:

        print(
            f"RAG retrieval failed: {error}"
        )

        retrieved_documents = []

    # ==================================================
    # 3. SYNTHESIS
    # ==================================================

    synthesis_result = synthesize(
        agent_results,
        retrieved_documents
    )

    # ==================================================
    # 4. PERSONALIZATION
    # ==================================================

    personalization_result = personalize_user(
        user_id=user_id,
        ticker=ticker,
        agent_results=agent_results,
        current_prices=current_prices,
        synthesis_result=synthesis_result
    )

    # ==================================================
    # 5. FINAL RESPONSE
    # ==================================================

    return {
        "ticker": ticker,

        "market_analysis":
            synthesis_result,

        "personalization":
            personalization_result,

        "agent_results":
            agent_results
    }


if __name__ == "__main__":

    result = run_pipeline(
        user_id="U001",

        ticker="TCS",

        current_prices={
            "TCS": 3500,
            "INFY": 1500,
            "RELIANCE": 2500
        }
    )

    print("\n")
    print("=" * 60)
    print("HACKVERSE FINAL PIPELINE")
    print("=" * 60)

    print("\nFINAL RESULT:\n")

    print(result)