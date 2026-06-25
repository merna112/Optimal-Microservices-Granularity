# Granulify

**Granularity Optimization Decision Framework (GODF) for smarter microservice boundaries.**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Build](https://img.shields.io/badge/build-passing-brightgreen.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-3776AB.svg)
![Status](https://img.shields.io/badge/status-prototype-orange.svg)

Granulify is a modular Python framework for analyzing, scoring, and optimizing
microservice granularity. It helps architecture teams decide whether service
boundaries should be **split**, **merged**, or **maintained** by combining three
critical signals:

- 🧩 **Structural signals** from source-code dependencies and coupling.
- ⚡ **Runtime signals** from traces, latency, call frequency, and reliability.
- 👥 **Organizational signals** from Git authorship and team ownership.

The current implementation includes a runnable mock simulation for **ShopFlow**,
an e-commerce platform, so the framework works out of the box while remaining
easy to extend with real static analysis, observability, and Git data.

---

## Project Overview

Modern microservice systems often drift away from their original design. A
service that once represented a clean business capability may become overloaded,
over-coupled, or owned by too many teams. Granulify addresses this problem by
turning architectural signals into repeatable, evidence-driven decisions.

Granulify evaluates candidate service boundaries using the **Granularity
Optimization Decision Framework (GODF)**:

1. **Ingest** structural, runtime, and organizational data.
2. **Score** each service boundary using DDD alignment, technical coupling,
   team autonomy, Relative Variation Index (RVI), and elasticity.
3. **Recommend** a formal architectural action: `SPLIT`, `MERGE`, or `MAINTAIN`.

---

## Core Features

- ✅ Mock static dependency analysis for service-to-service structural coupling.
- ✅ Simulated Prometheus/Jaeger-style runtime metrics.
- ✅ Git authorship analysis for team-boundary alignment.
- ✅ Hybrid scoring engine with DDD, coupling, autonomy, RVI, and elasticity.
- ✅ Decision analyzer that produces ranked architectural recommendations.
- ✅ Out-of-the-box ShopFlow e-commerce simulation.
- ✅ Clean, typed, modular Python codebase designed for production extension.

---

## Architecture

```text
                          Granulify / GODF
+------------------------------------------------------------------+
|                                                                  |
|  +----------------------+                                        |
|  |      Ingestion       |                                        |
|  +----------------------+                                        |
|  | static_parser.py     |-- Structural Coupling --+              |
|  | runtime_monitor.py   |-- Runtime Coupling -----+--+           |
|  | git_analyzer.py      |-- Team Alignment -------+  |           |
|  +----------------------+                           |            |
|                                                     v            |
|  +------------------------------------------------------------+  |
|  |                    Scoring Engine                         |  |
|  +------------------------------------------------------------+  |
|  | DDD Alignment | Technical Coupling | Team Autonomy         |  |
|  | Relative Variation Index (RVI) | Elasticity | Hybrid Score |  |
|  +------------------------------------------------------------+  |
|                                                     |            |
|                                                     v            |
|  +------------------------------------------------------------+  |
|  |                   Decision Analyzer                       |  |
|  +------------------------------------------------------------+  |
|  |              SPLIT | MERGE | MAINTAIN                     |  |
|  +------------------------------------------------------------+  |
|                                                                  |
+------------------------------------------------------------------+
```

### Repository Structure

```text
.
|-- decision/
|   |-- __init__.py
|   `-- analyzer.py
|-- ingestion/
|   |-- __init__.py
|   |-- git_analyzer.py
|   |-- runtime_monitor.py
|   `-- static_parser.py
|-- scoring/
|   |-- __init__.py
|   `-- engine.py
|-- main.py
`-- README.md
```

---

## Signal Comparison

| Signal Type | Data Source | Metric Extracted | Impact on Decision |
|---|---|---|---|
| 🧩 **Structural** | Static code dependencies, imports, package references, service contracts | Coupling Index, dependency count, domain affinity | Identifies services that are technically intertwined or poorly separated by domain boundaries. |
| ⚡ **Runtime** | Jaeger traces, Prometheus metrics, network latency, call frequency, error rates | Runtime coupling, latency pressure, Relative Variation Index, elasticity | Reveals whether services are operationally chatty, fragile, or under runtime stress. |
| 👥 **Organizational** | Git logs, commit history, authorship metadata, team ownership records | Ownership map, shared team ratio, team autonomy score | Detects whether service boundaries align with team responsibilities and Conway's Law. |

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/<your-org>/granulify.git
cd granulify
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it:

```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install Dependencies

Granulify currently runs with the Python standard library only.

```bash
python --version
```

Recommended Python version:

```text
Python 3.10+
```

### 4. Run the ShopFlow Simulation

```bash
python main.py
```

---

## Usage & CLI Examples

Running the built-in simulation prints ranked recommendations for candidate
service boundaries in the ShopFlow platform.

```bash
python main.py
```

Example output:

```text
Granulify - Granularity Optimization Decision Framework
Simulation: ShopFlow e-commerce platform
====================================================================

Boundary: checkout -> payment
Recommendation: MERGE
Confidence: 0.908
Scores: DDD=0.910, Technical=1.000, TeamAutonomy=0.279, RVI=0.422, Elasticity=0.527, Hybrid=0.694
Rationale: High domain alignment, high technical coupling, and overlapping ownership suggest the services behave as one capability.

Boundary: support -> orders
Recommendation: SPLIT
Confidence: 0.749
Scores: DDD=0.380, Technical=0.242, TeamAutonomy=1.000, RVI=0.696, Elasticity=0.796, Hybrid=0.492
Rationale: Signal variation and low domain/team alignment suggest the boundary should be decomposed or reassigned.
```

### Recommendation Types

| Recommendation | Meaning |
|---|---|
| **SPLIT** | The service boundary is too broad, misaligned, or internally unstable. |
| **MERGE** | Two services behave like one cohesive capability and may be over-separated. |
| **MAINTAIN** | The current boundary is acceptable under the observed signals. |

---

## How Scoring Works

Granulify calculates a hybrid boundary pressure score from multiple dimensions:

- **DDD Alignment:** Estimates how closely the services belong to the same
  business capability.
- **Technical Coupling:** Blends static dependency strength and runtime
  communication pressure.
- **Team Autonomy:** Measures whether the services are owned by independent
  teams or shared contributors.
- **Relative Variation Index (RVI):** Placeholder signal for disagreement or
  instability across structural, runtime, and organizational dimensions.
- **Elasticity:** Placeholder runtime adaptability score based on latency,
  error rate, and load.

These scores are interpreted by the decision analyzer to produce a formal
architectural recommendation.

---

## Project Roadmap

- [x] Define GODF-inspired modular project structure.
- [x] Add mock structural dependency ingestion.
- [x] Add mock runtime trace and latency ingestion.
- [x] Add mock Git authorship and team-boundary analysis.
- [x] Implement hybrid scoring engine.
- [x] Implement `SPLIT`, `MERGE`, and `MAINTAIN` recommendation logic.
- [x] Add runnable ShopFlow simulation.
- [ ] Add real static analysis using AST/import graph parsing.
- [ ] Integrate with Jaeger, OpenTelemetry, or Prometheus APIs.
- [ ] Parse real Git history using repository metadata.
- [ ] Add YAML/JSON configuration for thresholds and weights.
- [ ] Export recommendations as JSON, CSV, and architecture reports.
- [ ] Add automated tests and CI workflows.
- [ ] Build a visualization dashboard for boundary evolution.

---

## Contributors

| Name |
|---|
| Basant Awad |
| Nadira Mohamed |
| Merna Adel |
| Ahmed Adel |
| Mohamed Alsariti |
| Ahmed Yahia |

---

## License

This project is currently prepared with a placeholder **MIT License** badge.
Add a `LICENSE` file before publishing the repository publicly.

---

## Acknowledgements

Granulify is inspired by modern microservice architecture practices, Domain-
Driven Design, observability engineering, Conway's Law, and continuous
architecture evaluation.
