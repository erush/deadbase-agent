# scripts/test_research_agent.py

from agents.research_agent import execute


def main():

    result = execute(
        "1977/05/08"
    )

    print()
    print(result["answer"])
    print()


if __name__ == "__main__":
    main()