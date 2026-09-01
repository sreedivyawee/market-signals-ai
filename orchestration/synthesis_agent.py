from rag.retriever import retrieve_documents


def synthesize(results, retrieved_documents=None):

    if retrieved_documents is None:
        retrieved_documents = []

    bullish_score = 0.0
    bearish_score = 0.0

    reasons = []

    # --------------------------------------------------
    # Process P1 agent results
    # --------------------------------------------------

    for agent_name, agent_data in results.items():

        result = agent_data.get("result", {})

        classification = result.get(
            "classification",
            "UNKNOWN"
        )

        confidence = float(
            result.get("confidence", 0.0)
        )

        score = float(
            result.get("score", 0.0)
        )

        reasoning = result.get(
            "reasoning",
            []
        )

        if isinstance(reasoning, list):
            reasoning_text = " ".join(reasoning)
        else:
            reasoning_text = str(reasoning)

        reasons.append(
            f"{agent_name}: "
            f"{classification} "
            f"({confidence:.0%}) - "
            f"{reasoning_text}"
        )

        # --------------------------------------------------
        # Convert agent scores into overall signal
        # --------------------------------------------------

        if classification == "BULLISH":

            bullish_score += abs(score) * confidence

        elif classification == "BEARISH":

            bearish_score += abs(score) * confidence

        # Volatility is a risk signal rather than
        # a directional signal.
        #
        # Therefore HIGH_RISK / ELEVATED_RISK
        # contributes to bearish pressure.

        elif classification in [
            "HIGH_RISK",
            "ELEVATED_RISK"
        ]:

            bearish_score += abs(score) * confidence

    # --------------------------------------------------
    # Detect conflict
    # --------------------------------------------------

    directional_signals = []

    for agent_data in results.values():

        classification = (
            agent_data
            .get("result", {})
            .get("classification", "UNKNOWN")
        )

        if classification == "BULLISH":
            directional_signals.append("BULLISH")

        elif classification == "BEARISH":
            directional_signals.append("BEARISH")

    conflict = (
        len(set(directional_signals)) > 1
    )

    # --------------------------------------------------
    # Decide final signal
    # --------------------------------------------------

    difference = (
        bullish_score -
        bearish_score
    )

    total = (
        bullish_score +
        bearish_score
    )

    if difference > 0.10:

        final_signal = "BULLISH"

    elif difference < -0.10:

        final_signal = "BEARISH"

    else:

        final_signal = "HOLD"

    # --------------------------------------------------
    # Confidence
    # --------------------------------------------------

    if total == 0:

        confidence = 0.0

    else:

        confidence = (
            abs(difference) / total
        )

    # Reduce confidence if agents disagree
    if conflict:

        confidence *= 0.85

    confidence = round(
        min(confidence, 1.0),
        2
    )

    # --------------------------------------------------
    # RAG source attribution
    # --------------------------------------------------

    sources = []

    for document in retrieved_documents:

        source = {
            "document": document.get(
                "source",
                "Unknown"
            ),

            "page": document.get(
                "page",
                None
            )
        }

        if source not in sources:

            sources.append(source)

    # --------------------------------------------------
    # RAG evidence
    # --------------------------------------------------

    evidence = []

    for document in retrieved_documents:

        evidence.append(

            f'Source: '
            f'{document.get("source", "Unknown")}, '

            f'Page: '
            f'{document.get("page", "Unknown")}\n'

            f'{document.get("text", "")}'
        )

    evidence_text = "\n\n".join(
        evidence
    )

    # --------------------------------------------------
    # Final output
    # --------------------------------------------------

    return {

        "signal": final_signal,

        "confidence": confidence,

        "reasoning": " | ".join(reasons),

        "conflict_detected": conflict,

        "sources": sources,

        "evidence": evidence_text
    }


# --------------------------------------------------
# Standalone test
# --------------------------------------------------

if __name__ == "__main__":

    from orchestration.parallel_runner import (
        run_all_agents
    )

    print(
        "\nRunning market agents..."
    )

    agent_results = run_all_agents("TCS")

    print(
        "\nRetrieving RAG evidence..."
    )

    retrieved_documents = retrieve_documents(
        "TCS financial performance investment risk",
        top_k=3
    )

    print(
        "\nSynthesizing results..."
    )

    final_result = synthesize(
        agent_results,
        retrieved_documents
    )

    print(
        "\n===== SYNTHESIS RESULT ====="
    )

    print(
        "Signal:",
        final_result["signal"]
    )

    print(
        "Confidence:",
        final_result["confidence"]
    )

    print(
        "Conflict:",
        final_result["conflict_detected"]
    )

    print(
        "\nReasoning:"
    )

    print(
        final_result["reasoning"]
    )

    print(
        "\nSources:"
    )

    for source in final_result["sources"]:

        print(source)