# Research plan: multi-agent software engineering literature review

## Purpose and decision question

This review evaluates when and how multiple coding agents should be used for four scopes of software work: small features and bug fixes, medium features, large or cross-cutting features, and greenfield products. The intended output is a decision framework grounded in traceable evidence rather than a catalogue of product claims.

## Dates and cutoff

- Requested literature cutoff: **31 August 2026**.
- Actual search cutoff: **23 August 2026** (Europe/Paris), the date the searches were run.
- Limitation: 31 August 2026 is in the future at execution time. No claim is made to cover sources published from 24–31 August 2026. A final update search after the requested date would be required for literal compliance with that cutoff.

## Research questions

1. Which task properties make multi-agent decomposition beneficial or harmful?
2. What controlled or repository-level evidence compares single-agent and multi-agent software work?
3. Which coordination, context, review, testing, isolation, and rollback patterns are supported by evidence?
4. How should operating models change across small, medium, large, and greenfield scopes?
5. Which current platform features make these patterns practical, and which claims remain vendor evidence or emerging practice?
6. What failure modes, security risks, validity threats, cost, and latency effects constrain recommendations?

## Parallel workstreams and file ownership

Each research agent has a non-overlapping primary scope and writes only its assigned file. Shared sources may appear in more than one memo; the coordinator deduplicates them in the evidence register.

| Agent | Scope | Exclusive output |
|---|---|---|
| A | Foundations and theory: multi-agent systems, decomposition, coordination, planning, communication, memory/context, and failure modes | [`01-foundations-and-theory.md`](01-foundations-and-theory.md) |
| B | Empirical software-engineering evidence: controlled studies, benchmarks, repository experiments, and industrial cases | [`02-empirical-software-engineering.md`](02-empirical-software-engineering.md) |
| C | Small and medium feature practice: bug fixes, refactors, tests, localized API/UI changes, and delegation overhead | [`03-small-medium-features.md`](03-small-medium-features.md) |
| D | Large-feature and product practice: architecture, cross-service work, migrations, greenfield products, integration, and rollback | [`04-large-features-greenfield-products.md`](04-large-features-greenfield-products.md) |
| E | Tooling and platform landscape: Codex, Claude Code, and relevant open-source/research systems | [`05-tooling-and-platform-landscape.md`](05-tooling-and-platform-landscape.md) |
| F | Critical review/red team: negative results, coordination tax, security, conflicts, contamination, cost, and organizational risk | [`06-red-team-limitations.md`](06-red-team-limitations.md) |
| Coordinator | Protocol, normalized evidence register, final index, completeness and traceability audit | `00`, `07`, and `README.md` |
| Synthesis agent | Cross-memo synthesis and decision framework after A–F finish | [`08-synthesis-decision-framework.md`](08-synthesis-decision-framework.md) |

## Common research protocol

Every research memo must:

1. State the actual search cutoff and search scope.
2. Prefer full-text primary sources: original papers, official benchmark papers/repositories, official product documentation, and first-party industrial reports with disclosed methods.
3. Use secondary surveys mainly for discovery and triangulation, not as sole support for material claims when primary evidence is available.
4. Never infer a result from a search snippet or abstract alone. If full text is inaccessible, label the source **inaccessible/unverified** and do not use it as decisive evidence.
5. Separate reported evidence from the agent's inference.
6. For every material source record title, authors or organization, publication date, absolute URL, evidence type, 1–2 sentence finding, evidence quality (high/medium/low), and disclosure flags such as preprint-only or vendor-sponsored.
7. Return an executive memo of no more than 1,200 words, an actionable-findings table, and an annotated bibliography.
8. Avoid unsupported implementation advice and avoid turning benchmark success into claims about production effectiveness without an explicit bridge.

## Evidence-quality rubric

| Rating | Criteria |
|---|---|
| **High** | Peer-reviewed or otherwise rigorous primary study with transparent methods, relevant baselines, reproducible artifacts or sufficient detail, and a direct fit to the supported claim; or authoritative official documentation used only for a product-capability claim. |
| **Medium** | Relevant primary preprint, benchmark report, repository, or industrial study with useful methods but material limitations such as weak external validity, incomplete reproducibility, vendor involvement, or indirect fit. |
| **Low** | Anecdotal case, vendor marketing claim without adequate method, non-reproducible demonstration, secondary commentary, or evidence only indirectly related to the claim. Low-quality evidence may identify hypotheses but cannot alone support a universal recommendation. |

Quality is claim-relative: official documentation is high quality for whether a feature exists, but low quality for whether that feature improves software-engineering outcomes.

## Independence and reconciliation

- Agents receive their scope and the common protocol but do not edit or coordinate through one another's files.
- The coordinator normalizes source records after all six memos are complete.
- The synthesis agent reads all numbered inputs, checks citation traceability, identifies contradictions, and labels findings as **robust**, **promising/emerging**, or **insufficient evidence**.
- Where sources disagree, the synthesis records differences in task, model, scaffold, benchmark, metric, and experimental design instead of averaging incompatible results.

## Planned synthesis outputs

The synthesis must include:

- an executive summary;
- a four-scope decision matrix;
- for each scope: recommended agent count, roles, topology, model tier, context sharing, branch/worktree strategy, review gates, testing gates, stop conditions, and situations in which not to use multiple agents;
- default operating models for Codex and Claude Code, clearly distinguishing documented capability from outcome evidence;
- evidence assessment, limitations, contradictions, research gaps, and a source-linked bibliography.

## Validation checklist

Before delivery, the coordinator will verify that all ten required Markdown files exist, are non-empty, and contain valid Markdown headings; that internal links are relative; that external source links are absolute; and that citations used in synthesis are represented in the normalized evidence register.
