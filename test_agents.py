from agents.run_agents import run_all_agents


ticker = "TCS.NS"

results = run_all_agents(ticker)


for result in results:

    print("\n================================")
    print(result.agent_name)
    print("================================")

    print(result.model_dump_json(indent=2))