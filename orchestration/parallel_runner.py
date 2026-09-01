from concurrent.futures import ThreadPoolExecutor


def volatility_agent():
    return {
        "agent": "volatility",
        "signal": "BEARISH",
        "confidence": 0.85,
        "reasoning": "High volatility detected."
    }


def volume_agent():
    return {
        "agent": "volume",
        "signal": "BULLISH",
        "confidence": 0.78,
        "reasoning": "Trading volume is above average."
    }


def news_agent():
    return {
        "agent": "news",
        "signal": "BEARISH",
        "confidence": 0.72,
        "reasoning": "Recent news contains negative signals."
    }


def run_all_agents():

    with ThreadPoolExecutor(max_workers=3) as executor:

        futures = [
            executor.submit(volatility_agent),
            executor.submit(volume_agent),
            executor.submit(news_agent)
        ]

        results = [
            future.result()
            for future in futures
        ]

    return results


if __name__ == "__main__":

    results = run_all_agents()

    print("\n===== AGENT RESULTS =====")

    for result in results:
        print(result)