from agents.deadbase_agent import DeadBaseAgent


agent = DeadBaseAgent()

queries = [
    "What was played on 1977/05/08?",
    "When was Dark Star first played?",
    "Tell me about Winterland"
]

for query in queries:

    print("\n" + "=" * 80)
    print(query)
    print("=" * 80)

    result = agent.execute(query)

    print(result)