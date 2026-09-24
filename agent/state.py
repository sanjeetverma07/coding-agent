from dataclasses import dataclass, field


@dataclass
class AgentState:
    task: str
    plan: list[str] = field(default_factory=list)
    current_step: int = 0
    files_inspected: list[str] = field(default_factory=list)
    changes_made: list[dict] = field(default_factory=list)
    tests_run: list[dict] = field(default_factory=list)
    completed: bool = False
    failed: bool = False