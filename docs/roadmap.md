# Roadmap / Feuille de route

*English below / Anglais plus bas.*

## FR

### V0 — Proof of Concept

**Objectif** : prouver que l'orchestrateur peut produire un rapport HTML vérifié en moins de 5 minutes sur un sujet donné.

- [ ] Orchestrateur CLI (`stormgrill storm <sujet>`)
- [ ] 5 agents experts paramétrables : Praticien, Académique, Sceptique, Économiste, Historien
- [ ] Vérification Phase 4b : chaque citation confrontée à sa source primaire
- [ ] Score de fiabilité 1-10 (hiérarchie : causal évalué > donnée officielle > rapport > sondage > analogie > preprint)
- [ ] Bannière de vérification (X inventée, Y corrigée, Z rétrogradée)
- [ ] Export HTML simple (sans Grill)

**Critère de succès** : rapport HTML vérifié en < 5 min sur un sujet donné.

### V1 — Le Grill

**Objectif** : une session interactive de 30 minutes tenable avec un décideur réel.

- [ ] Extraction automatique de l'arbre de décision à partir du plan du décideur
- [ ] Moteur de stress-test (pire scénario, inversion, contrainte, ignorance)
- [ ] Audit de fatigue cognitive en temps réel
- [ ] Bouton d'éjection (mode dégradé)

**Critère de succès** : session interactive de 30 min avec un CTO test.

### V2 — La Fusion

**Objectif** : un rapport unique où les faits vérifiés et les décisions stressées sont croisés.

- [ ] Pipeline en Sablier (Storm en avance pendant le cadrage)
- [ ] Sentinelle de Cadrage + Kill & Fork
- [ ] Template HTML enrichi (Résumé 60s, Enseignements avec score de fiabilité, Guide Sûr/Réserve/Éviter, Plan d'action, Question de frontière)
- [ ] Journal de bord du Grill (décisions qui ont tenu/cédé)
- [ ] Mode « Rapport de Rupture »

**Critère de succès** : le rapport d'une session contient à la fois la trace du grill et les faits de la Storm.

### V3 — Production

**Objectif** : adoption réelle par plusieurs équipes.

- [ ] Mode web (au-delà du CLI)
- [ ] Configurations paramétrables (agents custom, seuils de fatigue, biais ajustables)
- [ ] Export PDF
- [ ] Intégration CI/CD (déclenchement de session depuis une PR ou un ticket)

**Critère de succès** : utilisé par 5 équipes en beta fermée.

---

## EN

### V0 — Proof of Concept

**Goal**: prove the orchestrator can produce a verified HTML report in under 5 minutes on a given topic.

- [ ] CLI orchestrator (`stormgrill storm <topic>`)
- [ ] 5 configurable expert agents: Practitioner, Academic, Skeptic, Economist, Historian
- [ ] Phase 4b verification: every citation checked against its primary source
- [ ] 1-10 reliability score (hierarchy: evaluated causal > official data > report > survey > analogy > preprint)
- [ ] Verification banner (X fabricated, Y corrected, Z downgraded)
- [ ] Simple HTML export (no Grill)

**Success criterion**: verified HTML report in < 5 min on a given topic.

### V1 — The Grill

**Goal**: a sustainable 30-minute interactive session with a real decision-maker.

- [ ] Automatic decision-tree extraction from the decision-maker's plan
- [ ] Stress-test engine (worst case, inversion, constraint, ignorance)
- [ ] Real-time cognitive fatigue audit
- [ ] Eject button (degraded mode)

**Success criterion**: 30-min interactive session with a test CTO.

### V2 — The Fusion

**Goal**: a single report where verified facts and stress-tested decisions are cross-referenced.

- [ ] Hourglass Pipeline (Storm gets ahead during framing)
- [ ] Framing Sentinel + Kill & Fork
- [ ] Enriched HTML template (60s Summary, Insights with reliability score, Safe/Caution/Avoid guide, Action Plan, Frontier Question)
- [ ] Grill session log (decisions that held/gave way)
- [ ] "Breakdown Report" mode

**Success criterion**: a session's report contains both the grill trace and the Storm facts.

### V3 — Production

**Goal**: real adoption across multiple teams.

- [ ] Web mode (beyond CLI)
- [ ] Configurable profiles (custom agents, fatigue thresholds, adjustable bias)
- [ ] PDF export
- [ ] CI/CD integration (session triggered from a PR or ticket)

**Success criterion**: used by 5 teams in closed beta.
