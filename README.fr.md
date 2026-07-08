# StormGrill — Orchestrateur d'Intelligence Décisionnelle

[🇬🇧 English version](README.md)

> Rendre la décision stratégique plus chère à mal prendre.

StormGrill est un orchestrateur open-source à double protocole qui combine une **recherche multi-agents vérifiée** (la Storm) et un **interrogatoire adversarial en temps réel** (le Grill) pour aider les décideurs — CTO, Lead Architect, Head of Product — à confronter une décision aux faits plutôt qu'à l'intuition.

## Pourquoi

La plupart des décisions stratégiques reposent sur un mélange d'intuition, de recherche incomplète et de biais de confirmation. StormGrill ne remplace pas le décideur. Il :

- Rend visibles les biais de confirmation en temps réel
- Force la confrontation entre l'intuition et les faits vérifiés
- Documente la chaîne de preuve de chaque décision
- Fournit un compte-rendu exécutable (actions datées, questions de frontière)

## Fonctionnement

```text
┌─────────────┐     cache (pipeline en sablier)     ┌─────────────┐
│    STORM     │ ───────────────────────────────▶  │    GRILL     │
│ 5 agents      │  passerelle filtrée, sens unique    │ interrogatoire│
│ experts,       │  (la Storm ne voit jamais le chat ;  │ adversarial   │
│ recherche       │  le Grill ne voit que la Storm       │ sur votre plan │
│ parallèle        │  vérifiée)                            │                │
└─────────────┘                                        └─────────────┘
        │                                                      │
        └─────────────────────┬────────────────────────────────┘
                               ▼
                      ┌─────────────────┐
                      │      FUSION       │
                      │  rapport HTML       │
                      │  unique, fin de       │
                      │  session, < 60s         │
                      └─────────────────┘
```

**Principes fondamentaux validés en conception** (voir [docs/protocol.md](docs/protocol.md)) :

| Branche | Décision | Garantie |
|---|---|---|
| A — Isolation des contextes | La Storm recherche à l'aveugle ; le Grill consomme la Storm via une passerelle filtrée | Pas de contamination croisée ; les pivots explicites déclenchent Kill & Fork |
| B — Restitution asynchrone | Rapport HTML fusionné unique en fin de session, assemblage < 60s | Fusion par section (Enseignements, Guide, Action) |
| C — Priorisation des ressources | Le Grill a préemption réseau absolue ; la Storm tourne en « Pipeline en Sablier » | Contrainte de latence < 8s sur les tours du Grill |
| D — Résolution des contradictions | Les faits de la Storm sont injectés de façon asynchrone, au tour suivant — jamais en cours de tour | Triage par criticité : SLA > Performance > Coût |

## État du projet

🚧 **Pré-V0 / scaffold.** Architecture définie, protocole validé par stress-test et une exécution réelle. L'implémentation démarre au [V0](docs/roadmap.md#v0--proof-of-concept).

## Feuille de route

Voir [docs/roadmap.md](docs/roadmap.md) pour le plan complet V0 → V3.

| Phase | Livrable | Critère de succès |
|---|---|---|
| V0 | Orchestrateur CLI, Storm 5 agents sur un sujet fixe + vérification Phase 4b | Rapport HTML vérifié en < 5 min |
| V1 | Module Grill (arbre de décision, 4 stress-tests, audit de fatigue) | Session interactive de 30 min avec un CTO test |
| V2 | Rapport HTML unifié Storm + Grill | Le rapport contient la trace du grill et les faits vérifiés |
| V3 | Mode web, profils configurables, export PDF, intégration CI/CD | Utilisé par 5 équipes en beta fermée |

## Installation

```bash
git clone git@github.com:valorisa/stormgrill.git
cd stormgrill
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Démarrage rapide (à partir du V0)

```bash
stormgrill storm "état de l'art des bases de données vectorielles en production, 2026" --agents 5 --out reports/
stormgrill grill --plan ma_decision.yaml
stormgrill fuse --storm reports/latest.json --grill sessions/latest.json --out rapport.html
```

## Structure du projet

```text
stormgrill/
├── src/stormgrill/
│   ├── core/          # Orchestrateur, Pipeline en Sablier, Sentinelle de Cadrage, Kill & Fork
│   ├── grill/           # Moteur adversarial, arbre de décision, audit de fatigue
│   ├── storm/            # Recherche multi-agents, vérification des sources (Phase 4b)
│   ├── fusion/             # Génération du rapport HTML (Jinja2)
│   └── monitoring/          # Audit de fuite de contexte, journal des pivots
├── templates/               # Templates HTML/CSS (charte Navy/Orange/Cream)
├── tests/
└── docs/
```

## Documentation

- [Spécification du protocole](docs/protocol.md) — les quatre branches de décision et leurs résultats de stress-test
- [Feuille de route](docs/roadmap.md)
- [Contribuer](CONTRIBUTING.md)

## Licence

MIT — voir [LICENSE](LICENSE).

## Auteur

Bertrand ([@valorisa](https://github.com/valorisa)) — conçu par méta-analyse en double boucle : un stress-test du protocole d'orchestration lui-même, suivi d'une exécution réelle.
