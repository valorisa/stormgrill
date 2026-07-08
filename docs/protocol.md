# Protocol Specification / Spécification du protocole

*English below / Anglais plus bas.*

## FR — Les quatre branches de décision

### A — Isolation des contextes

La Storm mène sa recherche **sans jamais voir le fil de discussion** du décideur : elle reçoit uniquement le sujet initial et opère à l'aveugle. Le Grill, à l'inverse, ne reçoit les résultats de la Storm qu'à travers une **passerelle filtrée** (faits vérifiés + score de fiabilité, jamais le raisonnement brut).

- **Pivot explicite** (ex. changement de fournisseur cloud annoncé par le décideur) → **Kill & Fork** : les agents Storm en cours sont interrompus, un nouveau cadrage est émis, de nouveaux agents sont lancés.
- **Angle mort documenté** : un pivot *implicite* (le décideur change d'avis sans le formuler explicitement) n'est pas détecté par la Sentinelle de Cadrage. C'est une limite connue du protocole, pas un bug caché.

### B — Restitution asynchrone

Un seul livrable : un rapport HTML fusionné, produit en fin de session, dans un budget de **60 secondes** d'assemblage.

- La fusion se fait **par section** (Enseignements clés, Guide de communication, Plan d'action) plutôt que par flux continu — ce qui rend le budget de 60s tenable même si une section est plus longue à générer.
- Le temps d'assemblage est une **promesse à surveiller en production**, pas une garantie mathématique : elle dépend de la latence des agents Storm les plus lents.

### C — Priorisation des ressources

Le Grill a **préemption absolue** sur les outils réseau (recherche web, API externes) pendant une session active. La Storm tourne selon le modèle du **Pipeline en Sablier** : elle prend de l'avance pendant que le décideur cadre encore le sujet avec le Grill, puis livre depuis un cache dès que le Grill la sollicite.

- Contrainte stricte : **< 8 secondes** de latence perçue sur un tour du Grill, même si la Storm tourne en tâche de fond.
- **Paradoxe de la simultanéité** (le Grill a besoin d'un fait Storm qui n'est pas encore prêt) : résolu par le cache d'avance — le Grill utilise le dernier état connu et marque le fait comme "en cours de vérification" plutôt que de bloquer.

### D — Résolution des contradictions

Quand un fait vérifié par la Storm contredit une hypothèse du décideur, l'injection se fait **de façon asynchrone, au tour suivant** — jamais en interrompant le tour en cours du Grill.

- **Triage par criticité** : SLA (contraintes contractuelles/légales) > Performance (données techniques) > Coût (données économiques).
- **Biais documenté** : le protocole priorise systématiquement la disponibilité de l'information sur son coût d'obtention ("Disponibilité > Coût"). C'est une hypothèse de conception assumée, pas un artefact accidentel — elle mérite d'être révisée si le coût de recherche devient un facteur dominant dans un déploiement donné.

## FR — Tests globaux de robustesse

| Test | Scénario | Résolution |
|---|---|---|
| Pire scénario | Panne réseau totale | Bascule en « Grill à l'Ancienne » — raisonnement pur, sans recherche externe |
| Inversion | Consensus absolu entre décideur et Storm | Déclenchement automatique de l'« Avocat du Diable » — stress des marges de la décision |
| Contrainte | Fatigue cognitive du décideur | Détection proactive par audit sémantique (ratio de mots, temps de saisie, simplification syntaxique) |
| Ignorance | Pivot philosophique (le vrai problème n'est pas celui apporté au départ) | Requalification en « Rapport de Rupture Préliminaire » + nouveau sujet proposé pour la Storm suivante |

## FR — Implémentation du module Storm (V0)

### Architecture

```text
src/stormgrill/storm/
├── models.py       # Source, Verdict, AgentReport, StormResult
├── cache.py         # Pipeline en Sablier (TTL cache + Kill & Fork via invalidate())
├── agents.py         # Orchestration des 5 agents experts (exécution MOCKÉE en V0)
├── verifier.py         # Phase 4b : vérification réelle de joignabilité HTTP
├── pipeline.py           # run_storm() : assemble agents + verifier -> StormResult
└── cli.py                 # `stormgrill storm search <sujet>`
```

### Ce qui est réel en V0

- **Le cache** (`cache.py`) est une vraie implémentation TTL, persistée sur disque de façon
  atomique.
- **Le vérificateur** (`verifier.py`) fait une vraie requête HTTP (HEAD puis GET en repli) sur
  chaque URL source et rend un verdict basé sur la réponse réelle du serveur. Il ne compare
  **pas encore** le texte de la claim au contenu de la source — cette comparaison sémantique,
  qui est le vrai cœur de la Phase 4b, est prévue pour le V1.
- **Le pipeline** (`pipeline.py`) et la **CLI** orchestrent réellement agents + vérificateur et
  produisent un JSON exploitable.

### Ce qui est mocké en V0 (explicitement, pas silencieusement)

- **Les agents** (`agents.py`) ne font pas de recherche réelle : `_mock_agent_call` retourne des
  données placeholder clairement préfixées `[MOCK]`. Le prompt de chaque agent est
  production-shaped ; seule l'exécution (appel LLM + recherche web réelle) reste à brancher.
- **La synthèse inter-agents** (cartographie des contradictions, résultat universel, question de
  frontière) n'existe pas encore — `universal_result` et `frontier_question` sont des
  placeholders `[MOCK]`.

Un rapport JSON généré en V0 aujourd'hui contient donc : de vrais verdicts de joignabilité, mais
des résumés et sources fictifs. Ne pas utiliser un rapport V0 comme source d'information réelle.

## FR — Limites connues

- Angle mort sur les pivots implicites (voir Branche A)
- Temps d'assemblage non garanti au-delà de 60s en cas de latence Storm anormale
- Biais d'ingénierie « Disponibilité > Coût » non configurable en V0
- Validité externe non testée au-delà d'un seul cas réel (bases de données vectorielles, 2026)

---

## EN — The four decision branches

### A — Context isolation

The Storm conducts research **without ever seeing the decision-maker's chat thread**: it receives only the initial topic and operates blind. The Grill, conversely, only receives Storm results through a **filtered gateway** (verified facts + reliability score, never raw reasoning).

- **Explicit pivot** (e.g. the decision-maker announces a cloud vendor change) → **Kill & Fork**: in-flight Storm agents are interrupted, a new framing is issued, new agents are launched.
- **Documented blind spot**: an *implicit* pivot (the decision-maker changes their mind without stating it) is not caught by the Framing Sentinel. This is a known protocol limitation, not a hidden bug.

### B — Async delivery

A single deliverable: a fused HTML report, produced at session end, within a **60-second** assembly budget.

- Fusion happens **per section** (Key Insights, Communication Guide, Action Plan) rather than as a continuous stream — which keeps the 60s budget realistic even when one section takes longer to generate.
- Assembly time is a **promise to monitor in production**, not a mathematical guarantee: it depends on the slowest Storm agent's latency.

### C — Resource priority

The Grill has **absolute preemption** over network tools (web search, external APIs) during an active session. The Storm runs on the **Hourglass Pipeline** model: it gets ahead while the decision-maker is still framing the topic with the Grill, then serves from cache once the Grill needs it.

- Strict constraint: **< 8 seconds** perceived latency on a Grill turn, even while the Storm runs in the background.
- **Simultaneity paradox** (the Grill needs a Storm fact that isn't ready yet): resolved by the ahead-cache — the Grill uses the latest known state and flags the fact as "verification in progress" instead of blocking.

### D — Contradiction resolution

When a Storm-verified fact contradicts a decision-maker's assumption, injection happens **asynchronously, on the next turn** — never by interrupting the Grill's current turn.

- **Criticality triage**: SLA (contractual/legal constraints) > Performance (technical data) > Cost (economic data).
- **Documented bias**: the protocol systematically prioritizes information availability over acquisition cost ("Availability > Cost"). This is an accepted design assumption, not an accidental artifact — it deserves review if research cost becomes a dominant factor in a given deployment.

## EN — Global robustness tests

| Test | Scenario | Resolution |
|---|---|---|
| Worst case | Total network outage | Fallback to "Old-School Grill" — pure reasoning, no external research |
| Inversion | Absolute consensus between decision-maker and Storm | Automatic "Devil's Advocate" trigger — stresses the decision's margins |
| Constraint | Decision-maker cognitive fatigue | Proactive detection via semantic audit (word ratio, typing time, syntactic simplification) |
| Ignorance | Philosophical pivot (the real problem isn't the one originally brought) | Requalification into a "Preliminary Breakdown Report" + a new topic proposed for the next Storm run |

## EN — Storm module implementation (V0)

### Architecture

```text
src/stormgrill/storm/
├── models.py       # Source, Verdict, AgentReport, StormResult
├── cache.py         # Hourglass Pipeline (TTL cache + Kill & Fork via invalidate())
├── agents.py         # 5 expert agents orchestration (MOCKED execution in V0)
├── verifier.py         # Phase 4b: real HTTP reachability verification
├── pipeline.py           # run_storm(): wires agents + verifier -> StormResult
└── cli.py                 # `stormgrill storm search <topic>`
```

### What's real in V0

- **The cache** (`cache.py`) is a genuine TTL implementation, persisted to disk atomically.
- **The verifier** (`verifier.py`) makes a real HTTP request (HEAD, falling back to GET) against
  each source URL and returns a verdict based on the server's actual response. It does **not
  yet** compare the claim's text against the source's content — that semantic check, the real
  heart of Phase 4b, is planned for V1.
- **The pipeline** (`pipeline.py`) and **CLI** genuinely orchestrate agents + verifier and
  produce a usable JSON report.

### What's mocked in V0 (explicitly, not silently)

- **Agents** (`agents.py`) do not perform real research: `_mock_agent_call` returns placeholder
  data clearly prefixed `[MOCK]`. Each agent's prompt is production-shaped; only the execution
  (real LLM call + web research) remains to be wired in.
- **Cross-agent synthesis** (contradiction mapping, universal result, frontier question) doesn't
  exist yet — `universal_result` and `frontier_question` are `[MOCK]` placeholders.

A JSON report generated by V0 today therefore contains real reachability verdicts, but fictional
summaries and sources. Do not treat a V0 report as a real information source.

## EN — Known limitations

- Blind spot on implicit pivots (see Branch A)
- Assembly time not guaranteed beyond 60s under abnormal Storm latency
- "Availability > Cost" engineering bias not configurable in V0
- External validity untested beyond a single real case (vector databases, 2026)
