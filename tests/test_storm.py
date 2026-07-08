"""Tests for the Storm module: models, cache, agents (mock), and pipeline wiring.

Network-dependent verifier behavior is tested with a local httpx MockTransport,
not with live requests, to keep tests fast, deterministic, and sandbox-safe.
"""

import httpx
import pytest

from stormgrill.storm.agents import AGENTS, StormAgents
from stormgrill.storm.cache import StormCache
from stormgrill.storm.models import AgentReport, Source, Verdict
from stormgrill.storm.pipeline import _slugify, run_storm
from stormgrill.storm.verifier import SourceVerifier


def test_models_construct():
    source = Source(url="https://example.com", title="Test", excerpt="Test excerpt")
    assert source.url == "https://example.com"

    verdict = Verdict(claim="Test claim", source=source, status="VERIFIE_ACCESSIBLE")
    assert verdict.status == "VERIFIE_ACCESSIBLE"

    report = AgentReport(
        agent_name="PRATICIEN", summary="s", key_points=["a"], sources=[source]
    )
    assert report.agent_name == "PRATICIEN"


def test_cache_set_get_invalidate(tmp_path):
    cache = StormCache(cache_dir=tmp_path)
    cache.set("k", {"value": "v"})
    assert cache.get("k") == {"value": "v"}

    cache.invalidate("k")
    assert cache.get("k") is None


def test_cache_persists_across_instances(tmp_path):
    cache = StormCache(cache_dir=tmp_path)
    cache.set("k", {"value": "v"})

    reloaded = StormCache(cache_dir=tmp_path)
    reloaded.load()
    assert reloaded.get("k") == {"value": "v"}


def test_cache_expired_entry_returns_none(tmp_path):
    cache = StormCache(cache_dir=tmp_path)
    cache.set("k", {"value": "v"}, ttl_seconds=-1)
    assert cache.get("k") is None


async def test_storm_agents_run_all_returns_five_reports():
    agents = StormAgents(topic="test topic", reader_role="Lead Architect")
    reports = await agents.run_all()
    assert len(reports) == len(AGENTS)
    assert {r.agent_name for r in reports} == set(AGENTS)
    # Mock output must be unambiguously fake — see agents.py docstring.
    assert all("[MOCK" in r.summary for r in reports)


async def test_verifier_marks_reachable_source_pending_review():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200)

    transport = httpx.MockTransport(handler)
    verifier = SourceVerifier()

    # Patch the client construction to use the mock transport.
    async def fake_verify_all(claims):
        async with httpx.AsyncClient(transport=transport) as client:
            return await __import__("asyncio").gather(
                *[verifier._verify_single(client, claim, source) for claim, source in claims]
            )

    source = Source(url="https://example.com/ok", title="OK", excerpt="")
    verdicts = await fake_verify_all([("claim", source)])
    assert verdicts[0].status == "VERIFIE_ACCESSIBLE"

    summary = verifier.summarize(verdicts)
    assert summary["accessible"] == 1
    assert summary["pending_review"] == 1


async def test_verifier_marks_unreachable_source_inaccessible():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500)

    transport = httpx.MockTransport(handler)
    verifier = SourceVerifier()

    async def fake_verify_all(claims):
        async with httpx.AsyncClient(transport=transport) as client:
            return await __import__("asyncio").gather(
                *[verifier._verify_single(client, claim, source) for claim, source in claims]
            )

    source = Source(url="https://example.com/down", title="Down", excerpt="")
    verdicts = await fake_verify_all([("claim", source)])
    assert verdicts[0].status == "INACCESSIBLE"

    summary = verifier.summarize(verdicts)
    assert summary["inaccessible"] == 1
    assert summary["accessible"] == 0


def test_slugify():
    assert _slugify("État de l'art : Bases Vectorielles ?") == "état-de-lart-bases-vectorielles"


@pytest.mark.parametrize("monkeypatch_transport", [None])
async def test_run_storm_end_to_end_uses_mock_transport(monkeypatch, monkeypatch_transport):
    """Full pipeline wiring, with the verifier's real HTTP client swapped for a mock."""

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200)

    original_client = httpx.AsyncClient

    def patched_client(*args, **kwargs):
        kwargs["transport"] = httpx.MockTransport(handler)
        return original_client(*args, **kwargs)

    monkeypatch.setattr(httpx, "AsyncClient", patched_client)

    result = await run_storm(topic="sujet de test", reader_role="Lead Architect")

    assert len(result.reports) == len(AGENTS)
    assert result.verification_summary["accessible"] > 0
    assert result.verification_summary["inaccessible"] == 0
    assert all(r.verdicts for r in result.reports)
