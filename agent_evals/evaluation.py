from dataclasses import dataclass, field


@dataclass
class EvaluationResult:
    case_id: str
    category: str

    success: bool = False

    duration_seconds: float = 0.0

    changed_files: list[str] = field(default_factory=list)
    expected_files: list[str] = field(default_factory=list)

    expected_files_changed: bool = False

    tests: list[dict] = field(default_factory=list)

    agent_result: str | None = None

    error: str | None = None