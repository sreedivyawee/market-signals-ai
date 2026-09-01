from rag.retriever import retrieve_documents


def synthesize(
    results,
    retrieved_documents
):

    bullish_score = 0
    bearish_score = 0

    reasons = []

    # Process agent results
    for result in results:

        signal = result["signal"]
        confidence = result["confidence"]

        reasons.append(
            f'{result["agent"].title()}: '
            f'{signal} '
            f'({confidence:.0%}) - '
            f'{result["reasoning"]}'
        )

        if signal == "BULLISH":

            bullish_score += confidence

        elif signal == "BEARISH":

            bearish_score += confidence

    # Detect conflicting signals
    signals = [
        result["signal"]
        for result in results
    ]

    conflict = len(set(signals)) > 1

    # Calculate difference
    difference = (
        bullish_score -
        bearish_score
    )

    # Decide final signal
    if difference > 0.5:

        final_signal = "BULLISH"

    elif difference < -0.5:

        final_signal = "BEARISH"

    else:

        final_signal = "HOLD"

    # Calculate confidence
    total = (
        bullish_score +
        bearish_score
    )

    if total == 0:

        confidence = 0.0

    else:

        confidence = (
            abs(difference) / total
        )

    # Reduce confidence during conflict
    if conflict:

        confidence *= 0.85

    # Create source attribution
    sources = []

    for document in retrieved_documents:

        source = {
            "document": document["source"],
            "page": document["page"]
        }

        if source not in sources:

            sources.append(source)

    # Combine retrieved evidence
    evidence = []

    for document in retrieved_documents:

        evidence.append(
            f'Source: {document["source"]}, '
            f'Page: {document["page"]}\n'
            f'{document["text"]}'
        )

    evidence_text = "\n\n".join(
        evidence
    )

    # Final structured output
    return {

        "signal": final_signal,

        "confidence":
            round(confidence, 2),

        "reasoning":
            " | ".join(reasons),

        "conflict_detected":
            conflict,

        "sources":
            sources,

        "evidence":
            evidence_text
    }


if __name__ == "__main__":

    # --------------------------------
    # 1. Simulated specialized agents
    # --------------------------------

    test_results = [

        {
            "agent": "volatility",
            "signal": "BEARISH",
            "confidence": 0.85,
            "reasoning":
                "High volatility detected."
        },

        {
            "agent": "volume",
            "signal": "BULLISH",
            "confidence": 0.78,
            "reasoning":
                "Trading volume is above average."
        },

        {
            "agent": "news",
            "signal": "BEARISH",
            "confidence": 0.72,
            "reasoning":
                "Recent news contains negative signals."
        }
    ]

    # --------------------------------
    # 2. Retrieve RAG evidence
    # --------------------------------

    query = (
        "What is the financial "
        "investment problem described?"
    )

    print(
        "\nRetrieving relevant documents..."
    )

    retrieved_documents = (
        retrieve_documents(
            query,
            top_k=3
        )
    )

    # --------------------------------
    # 3. Synthesis
    # --------------------------------

    final_result = synthesize(
        test_results,
        retrieved_documents
    )

    # --------------------------------
    # 4. Display result
    # --------------------------------

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
        "Conflict detected:",
        final_result["conflict_detected"]
    )

    print(
        "\nReasoning:"
    )

    print(
        final_result["reasoning"]
    )

    # --------------------------------
    # 5. Display sources
    # --------------------------------

    print(
        "\n===== SOURCES ====="
    )

    for source in final_result["sources"]:

        print(
            f'📄 {source["document"]} '
            f'- Page {source["page"]}'
        )

    # --------------------------------
    # 6. Display retrieved evidence
    # --------------------------------

    print(
        "\n===== RAG EVIDENCE ====="
    )

    print(
        final_result["evidence"][:2000]
    )