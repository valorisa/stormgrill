"""Data models for the Storm research module.

These are the shared structures produced by expert agents and consumed by
the verifier, the cache, and the fusion/report layer.
"""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Literal

AgentName = Literal["PRATICIEN", "ACADEMIQUE", "SCEPTIQUE", "ECONOMISTE", "HISTORIEN"]

# Honest status set for V0: real network-reachability check only.
# Semantic comparison of claim vs. source content is a V1 concern (see verifier.py).
VerdictStatus = Literal["VERIFIE_ACCESSIBLE", "INACCESSIBLE", "EN_ATTENTE_REVUE"]


@dataclass
class Source:
    url: str
    title: str
    excerpt: str
    accessed_date: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


@dataclass
class Verdict:
    """Result of checking a single source in Phase 4b.

    V0 scope is honest but limited: it confirms the source URL is reachable.
    It does NOT yet compare the claim's text against the source's content —
    that semantic check is real verification and lands in V1. Do not treat
    VERIFIE_ACCESSIBLE as "claim confirmed true"; it only means "source exists
    and responded".
    """

    claim: str
    source: Source
    status: VerdictStatus
    http_status: int | None = None
    note: str | None = None


@dataclass
class AgentReport:
    agent_name: AgentName
    summary: str
    key_points: list[str]
    sources: list[Source]
    verdicts: list[Verdict] = field(default_factory=list)


@dataclass
class StormResult:
    topic: str
    topic_slug: str
    reader_role: str
    timestamp: str
    reports: list[AgentReport]
    universal_result: str
    frontier_question: str
    verification_summary: dict[str, int]  # {accessible, inaccessible, pending_review}
