# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added

- Initial project scaffold: package structure, bilingual README, protocol spec, roadmap
- CI workflow (markdownlint + Python lint/tests, matrix 3.11/3.12)
- CLI stub for `grill`, `fuse` commands (V1/V2, raise `NotImplementedError`)
- HTML report template (Navy/Orange/Cream)
- Storm module (`stormgrill storm search <topic>`): data models, TTL cache
  (Hourglass Pipeline / Kill & Fork primitive), agent orchestration, and a
  Phase 4b verifier that performs **real HTTP reachability checks** against
  source URLs (no randomized/simulated verdicts)
- 10 passing tests covering models, cache, agents, verifier (via `httpx.MockTransport`,
  no live network calls), and end-to-end pipeline wiring

### Known limitations (see `docs/protocol.md`)

- Agent research execution is mocked (`_mock_agent_call`); prompts are
  production-shaped but no real web search / LLM call is wired in yet
- Verifier confirms source reachability only, not claim/content match
  (semantic comparison is a V1 deliverable)
- No HTML export yet for Storm-only reports (JSON only)
