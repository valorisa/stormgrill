# StormGrill — Decision Intelligence Orchestrator

[🇫🇷 Version française](README.fr.md)

> Make bad strategic decisions expensive to make.

StormGrill is an open-source dual-protocol orchestrator that pairs **verified multi-agent research** (the Storm) with **real-time adversarial interrogation** (the Grill) to help decision-makers — CTOs, Lead Architects, Heads of Product — stress-test a decision against facts, not intuition.

## Why

Most strategic decisions are made on a mix of intuition, incomplete research, and confirmation bias. StormGrill doesn't replace the decision-maker. It:

- Surfaces confirmation bias in real time
- Forces a confrontation between intuition and verified facts
- Documents the chain of evidence behind every decision
- Produces a single, executable report (dated actions, open questions)

## How it works

```text
┌─────────────┐        cache (hourglass pipeline)        ┌─────────────┐
│    STORM    │ ─────────────────────────────────────▶  │    GRILL    │
│ 5 expert     │   filtered gateway, one-way only         │ adversarial │
│ agents,      │   (Storm never sees the chat;             │ interrogation│
│ parallel     │    Grill only sees verified Storm output) │ on your plan │
│ research     │                                           │              │
└─────────────┘                                           └─────────────┘
        │                                                         │
        └──────────────────────┬──────────────────────────────────┘
                                ▼
                       ┌─────────────────┐
                       │      FUSION      │
                       │  single HTML      │
                       │  report, end of    │
                       │  session, < 60s     │
                       └─────────────────┘
```

**Core principles validated during design (see [docs/protocol.md](docs/protocol.md)):**

| Branch | Decision | Guarantee |
|---|---|---|
| A — Context isolation | Storm researches blind; Grill consumes Storm through a filtered gateway | No cross-contamination; explicit pivots trigger Kill & Fork |
| B — Async delivery | Single fused HTML report at session end, < 60s assembly | Section-based merge (Insights, Guide, Action) |
| C — Resource priority | Grill has absolute network preemption; Storm runs in "Hourglass Pipeline" | < 8s latency constraint on Grill turns |
| D — Contradiction resolution | Storm facts injected asynchronously, next turn — never mid-turn | Triage by criticality: SLA > Performance > Cost |

## Status

🚧 **Pre-V0 / scaffold.** Architecture defined, protocol validated by stress-test and one real-world execution run. Implementation starts at [V0](docs/roadmap.md#v0--proof-of-concept).

## Roadmap

See [docs/roadmap.md](docs/roadmap.md) for the full V0 → V3 plan.

| Phase | Deliverable | Success criterion |
|---|---|---|
| V0 | CLI orchestrator, 5-agent Storm on a fixed topic + Phase 4b verification | Verified HTML report in < 5 min |
| V1 | Grill module (decision tree, 4 stress-tests, fatigue audit) | 30-min interactive session with a test CTO |
| V2 | Unified Storm + Grill HTML report | Report contains both grill trace and verified facts |
| V3 | Web mode, configurable profiles, PDF export, CI/CD integration | Used by 5 teams in closed beta |

## Installation

```bash
git clone git@github.com:valorisa/stormgrill.git
cd stormgrill
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Quick start (once V0 lands)

```bash
stormgrill storm "state of vector databases in production, 2026" --agents 5 --out reports/
stormgrill grill --plan my_decision.yaml
stormgrill fuse --storm reports/latest.json --grill sessions/latest.json --out report.html
```

## Project structure

```text
stormgrill/
├── src/stormgrill/
│   ├── core/          # Orchestrator, Hourglass Pipeline, Framing Sentinel, Kill & Fork
│   ├── grill/          # Adversarial engine, decision tree, fatigue audit
│   ├── storm/           # Multi-agent research, source verification (Phase 4b)
│   ├── fusion/            # HTML report generation (Jinja2)
│   └── monitoring/         # Context-leak audit, pivot log
├── templates/              # HTML/CSS report templates (Navy/Orange/Cream)
├── tests/
└── docs/
```

## Documentation

- [Protocol specification](docs/protocol.md) — the four decision branches and their stress-test results
- [Roadmap](docs/roadmap.md)
- [Contributing](CONTRIBUTING.md)

## License

MIT — see [LICENSE](LICENSE).

## Author

Bertrand ([@valorisa](https://github.com/valorisa)) — designed through a double-loop meta-analysis: a stress-test of the orchestration protocol itself, followed by a real-world execution run.
