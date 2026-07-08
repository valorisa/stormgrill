"""Phase 4b verification.

V0 IMPORTANT: this checks that a source URL is reachable over HTTP. It does
NOT compare the claim's text against the source's actual content — that
semantic check (the real point of Phase 4b) requires fetching and reading the
page, which is a V1 deliverable. Do not read VERIFIE_ACCESSIBLE as "claim
confirmed": it only means "the source exists and responded". Everything
reachable is marked EN_ATTENTE_REVUE until semantic comparison lands, so the
verification banner never overstates what V0 actually checked.

This intentionally does NOT use randomness to fabricate verdicts. A prior
draft of this module simulated Phase 4b with `random.choices(...)`, which
would have produced verdicts indistinguishable from real verification while
checking nothing. That defeats the purpose of Phase 4b and was rejected.
"""

import asyncio

import httpx

from .models import Source, Verdict


class SourceVerifier:
    """Checks source reachability. See module docstring for V0 scope."""

    def __init__(self, timeout_seconds: float = 8.0):
        self.timeout_seconds = timeout_seconds

    async def verify_all(self, claims: list[tuple[str, Source]]) -> list[Verdict]:
        async with httpx.AsyncClient(
            timeout=self.timeout_seconds, follow_redirects=True
        ) as client:
            tasks = [self._verify_single(client, claim, source) for claim, source in claims]
            return await asyncio.gather(*tasks)

    async def _verify_single(
        self, client: httpx.AsyncClient, claim: str, source: Source
    ) -> Verdict:
        try:
            response = await client.head(source.url)
            if response.status_code >= 400:
                # Some servers reject HEAD; retry with GET before giving up.
                response = await client.get(source.url)
            if response.status_code < 400:
                return Verdict(
                    claim=claim,
                    source=source,
                    status="VERIFIE_ACCESSIBLE",
                    http_status=response.status_code,
                    note="Source jointe. Comparaison sémantique claim/contenu : V1.",
                )
            return Verdict(
                claim=claim,
                source=source,
                status="INACCESSIBLE",
                http_status=response.status_code,
            )
        except httpx.HTTPError as exc:
            return Verdict(
                claim=claim,
                source=source,
                status="INACCESSIBLE",
                note=f"Erreur réseau : {exc.__class__.__name__}",
            )

    def summarize(self, verdicts: list[Verdict]) -> dict[str, int]:
        summary = {"accessible": 0, "inaccessible": 0, "pending_review": 0}
        for v in verdicts:
            if v.status == "VERIFIE_ACCESSIBLE":
                summary["accessible"] += 1
                summary["pending_review"] += 1  # accessible != semantically confirmed
            elif v.status == "INACCESSIBLE":
                summary["inaccessible"] += 1
        return summary
