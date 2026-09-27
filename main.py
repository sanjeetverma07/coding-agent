import asyncio
from agent.agent import run_agent

async def main():

    print("=" * 60)
    print("LOCAL AI CODING AGENT")
    print("=" * 60)
    while True:
        request = input(
            "\nWhat do you want the agent to do?\n> "
        )

        result = await run_agent(request)

        print("\n")
        print("=" * 60)
        print("FINAL ANSWER")
        print("=" * 60)
        print(result)
        
        print("=" * 60)
        print("make your next step")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())