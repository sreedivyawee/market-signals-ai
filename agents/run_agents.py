from agents.volume_agent import volume_agent
from agents.volatility_agent import volatility_agent
from agents.news_agent import news_agent


def run_all_agents(ticker: str):

    results = [
        volume_agent(ticker),
        volatility_agent(ticker),
        news_agent(ticker)
    ]

    return results