"""Five expert agents run in parallel, blind to the decision-maker's chat context
(docs/protocol.md, Branch A).

V0 IMPORTANT: `_mock_agent_call` returns clearly fake placeholder data. It exists
so the pipeline (agents -> verifier -> fusion) can be wired and tested end-to-end
before real research is plugged in. It is NOT a simulation of what a real agent
would find — do not treat its output as research. Replacing it with a real call
(web search + LLM synthesis) is the actual V0 deliverable; see TODO below.
"""

import asyncio
from typing import Any

from .models import AgentName, AgentReport, Source

AGENTS: tuple[AgentName, ...] = (
    "PRATICIEN",
    "ACADEMIQUE",
    "SCEPTIQUE",
    "ECONOMISTE",
    "HISTORIEN",
)

_PROMPTS: dict[AgentName, str] = {
    "PRATICIEN": (
        "Tu es LE PRATICIEN pour : {topic}. Tu travailles ce sujet au quotidien. "
        "Fais de la vraie recherche web (sources récentes, études de cas, retours "
        "d'opérateurs). Produis : a) un résumé opérationnel, b) 6-10 points "
        "concrets, c) 6 références réelles (URL + citation courte)."
    ),
    "ACADEMIQUE": (
        "Tu es L'ACADÉMIQUE pour : {topic}. Tu te fies aux preuves évaluées par "
        "les pairs, pas aux anecdotes. Fais de la vraie recherche web (études "
        "revues par les pairs, méta-analyses). Produis : a) synthèse des preuves, "
        "b) lacunes méthodologiques, c) 6 références principales."
    ),
    "SCEPTIQUE": (
        "Tu es LE SCEPTIQUE pour : {topic}. Tu penses que la vue dominante est "
        "surestimée ou fausse. Construis le steelman le plus solide du scénario "
        "pessimiste. Fais de la vraie recherche web pour trouver contre-exemples, "
        "limites et biais. Produis : a) arguments contraires, b) scénarios où ça "
        "casse, c) 6 références."
    ),
    "ECONOMISTE": (
        "Tu es L'ÉCONOMISTE pour : {topic}. Tu suis l'argent. Fais de la vraie "
        "recherche web sur revenus, valorisations, taille de marché, unit "
        "economics. Produis : a) chiffres de marché, b) acteurs clés, c) 6 "
        "références (rapports financiers, études de marché)."
    ),
    "HISTORIEN": (
        "Tu es L'HISTORIEN pour : {topic}. Tu as déjà vu des cycles de "
        "disruption et tu cherches les motifs. Fais de la vraie recherche web "
        "pour trouver de vrais parallèles historiques. Produis : a) analogies "
        "pertinentes, b) cycles comparables, c) 6 références historiques."
    ),
}


class StormAgents:
    """Orchestrates the 5 expert agents in parallel."""

    def __init__(self, topic: str, reader_role: str):
        self.topic = topic
        self.reader_role = reader_role

    async def run_all(self) -> list[AgentReport]:
        tasks = [self._run_agent(name) for name in AGENTS]
        return await asyncio.gather(*tasks)

    async def _run_agent(self, agent_name: AgentName) -> AgentReport:
        prompt = _PROMPTS[agent_name].format(topic=self.topic)
        # TODO(V0 real deliverable): replace this mock with a real research call
        # (web_search + LLM synthesis, or an Agent SDK tool call). The prompt
        # above is already production-shaped; only the execution is mocked.
        result = await self._mock_agent_call(prompt, agent_name)
        return AgentReport(
            agent_name=agent_name,
            summary=result["summary"],
            key_points=result["key_points"],
            sources=[Source(**s) for s in result["sources"]],
        )

    async def _mock_agent_call(self, prompt: str, agent_name: AgentName) -> dict[str, Any]:
        """Placeholder execution. Returns clearly fake data — see module docstring."""
        return {
            "summary": f"[MOCK — non-implémenté] Résumé de {agent_name} sur {self.topic}",
            "key_points": [f"[MOCK] Point {i + 1}" for i in range(3)],
            "sources": [
                {
                    "url": f"https://example.invalid/mock-source-{i + 1}",
                    "title": f"[MOCK] Source {i + 1}",
                    "excerpt": "[MOCK] Aucune recherche réelle effectuée.",
                }
                for i in range(2)
            ],
        }
