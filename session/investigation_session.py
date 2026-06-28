from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

@dataclass
class InvestigationSession:
    """
    Shared execution state for a single historical investigation.

    The Investigation Session persists context between the
    Planning Agent, Agent Skills, MCP tools, and Synthesis Agent.

    It is created when an investigation begins and discarded
    after the final report is generated.
    """

    question: str

    created_at: datetime = field(default_factory=datetime.utcnow)

    selected_skills: list[str] = field(default_factory=list)

    tool_calls: list[dict[str, Any]] = field(default_factory=list)

    evidence: list[dict[str, Any]] = field(default_factory=list)

    execution_trace: list[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)

    final_report: str | None = None

    def add_skill(self, skill: str) -> None:
        self.selected_skills.append(skill)

    def add_tool_call(
        self,
        tool: str,
        arguments: dict[str, Any]
    ) -> None:
        self.tool_calls.append(
            {
                "tool": tool,
                "arguments": arguments,
                "timestamp": datetime.utcnow().isoformat()
            }
        )

    def add_evidence(
        self,
        source: str,
        payload: dict[str, Any]
    ) -> None:
        self.evidence.append(
            {
                "source": source,
                "payload": payload
            }
        )

    def trace(self, message: str) -> None:
        self.execution_trace.append(message)

    def set_report(self, report: str) -> None:
        self.final_report = report

    def summary(self) -> dict[str, Any]:
        return {
        "question": self.question,
        "created_at": self.created_at.isoformat(),
        "selected_skills": self.selected_skills,
        "tool_calls": self.tool_calls,
        "evidence": self.evidence,
        "execution_trace": self.execution_trace,
        "metadata": self.metadata,
        "report_generated": self.final_report is not None
    }