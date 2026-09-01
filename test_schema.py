from agents.news_agent import news_agent

result = news_agent("TCS.NS")

print(result.model_dump_json(indent=2))