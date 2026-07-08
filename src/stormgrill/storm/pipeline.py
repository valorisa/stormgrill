"""End-to-end Storm pipeline: run agents, verify sources, produce a StormResult.

Phase mapping (see docs/protocol.md):
  Phase 1 — deploy the 5 expert agents in parallel
  Phase 2 — (V1) map contradictions between agents; stubbed in V0
  Phase 3 — synthesize (stubbed in V0, see TODO)
  Phase 4b — verify source reachability (real, not mocked — see verifier.py)
"""

import json
import re
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path

from .agents import StormAgents
from .models import Source, StormResult
from .verifier import SourceVerifier


def _slugify(topic: str, max_len: int = 50) -> str:
    slug = topic.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    return slug[:max_len].strip("-")


async def run_storm(topic: str, reader_role: str, agent_count: int = 5) -> StormResult:
    """Run the full V0 Storm pipeline for a topic.

    `agent_count` is accepted for interface stability with the roadmap but V0
    always runs the fixed 5-agent panel; partial panels land later if needed.
    """
    agents = StormAgents(topic, reader_role)
    reports = await agents.run_all()

    # TODO(V1): real contradiction mapping between agent reports.
    universal_result = (
        "[MOCK — non-implémenté] Synthèse inter-agents non disponible en V0."
    )
    frontier_question = (
        "[MOCK — non-implémenté] Question de frontière non générée en V0."
    )

    verifier = SourceVerifier()
    claims: list[tuple[str, Source]] = [
        (f"[MOCK] Claim non extraite — source de {report.agent_name}", source)
        for report in reports
        for source in report.sources
    ]
    verdicts = await verifier.verify_all(claims)
    verification_summary = verifier.summarize(verdicts)

    # Attach verdicts back to their originating report, in source order.
    cursor = 0
    for report in reports:
        n = len(report.sources)
        report.verdicts = verdicts[cursor : cursor + n]
        cursor += n

    return StormResult(
        topic=topic,
        topic_slug=_slugify(topic),
        reader_role=reader_role,
        timestamp=datetime.now(UTC).isoformat(),
        reports=reports,
        universal_result=universal_result,
        frontier_question=frontier_question,
        verification_summary=verification_summary,
    )


def save_result(result: StormResult, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{result.topic_slug}-storm-result.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(asdict(result), f, indent=2, ensure_ascii=False)
    return output_file
