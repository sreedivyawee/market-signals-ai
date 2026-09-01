from concurrent.futures import ThreadPoolExecutor

from agents.volume_agent import volume_agent
from agents.volatility_agent import volatility_agent
from agents.news_agent import news_agent


def run_all_agents(ticker="TCS"):

    with ThreadPoolExecutor(max_workers=3) as executor:

        futures = {
            "volume_agent": executor.submit(
                volume_agent,
                ticker
            ),

            "volatility_agent": executor.submit(
                volatility_agent,
                ticker
            ),

            "news_agent": executor.submit(
                news_agent,
                ticker
            )
        }

        results = {}

        for name, future in futures.items():

            result = future.result()

            # Convert Pydantic model to dictionary
            results[name] = result.model_dump()

    return results


if __name__ == "__main__":

    results = run_all_agents("TCS")

    print("\n===== AGENT RESULTS =====")

    for name, result in results.items():

        print(f"\n{name}:")
        print(result)