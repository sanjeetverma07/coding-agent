from benchmark import BenchmarkManager


manager = BenchmarkManager(
    r"G:\agentic\agent_evals"
)

manager.reset()

print(
    "Commit:",
    manager.current_commit()
)

print(
    "Status:",
    manager.status()
)