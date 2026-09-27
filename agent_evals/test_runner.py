import asyncio

from .runner import EvaluationRunner


async def main():

    runner = EvaluationRunner(
        repo_path=r"G:\agentic\agent_evals\benchmark_repo",
        cases_path=r"G:\agentic\agent_evals\cases\cases.json"
    )

    result = await runner.run_case("FEAT-001")

    print("\n")
    print("=" * 60)
    print("RESULT")
    print("=" * 60)

    print(result)


if __name__ == "__main__":
    asyncio.run(main())