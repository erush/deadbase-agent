# scripts/test_historian_agent.py

from agents.historian_agent import execute

result = execute(
    "1977/05/08"
)

print()
print(result["answer"])
print()