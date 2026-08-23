# Multi-agent software engineering: synthesis and decision framework

## Scope, date, and traceability

This synthesis covers evidence located and checked through **23 August 2026 (Europe/Paris)**. The requested cutoff, **31 August 2026**, was eight days in the future when the searches were run. It is therefore impossible to claim literal coverage through that date: sources published from 24–31 August 2026 require a follow-up search after 31 August.

The synthesis reads the [research plan](00-research-plan.md), all six independent evidence memos ([foundations](01-foundations-and-theory.md), [empirical software engineering](02-empirical-software-engineering.md), [small and medium work](03-small-medium-features.md), [large and greenfield work](04-large-features-greenfield-products.md), [tooling](05-tooling-and-platform-landscape.md), and [red team](06-red-team-limitations.md)), and the coordinator’s [normalized evidence register](07-evidence-register.md). Every external source cited below appears in both at least one memo bibliography and the evidence register. Evidence-register IDs are included to make that relationship auditable.

## Executive summary

The literature does not support “use more agents for bigger tasks” as a general rule. It supports a narrower decision rule:

> Use multiple coding agents only when the work exposes at least two independently executable, independently verifiable queues whose expected value exceeds coordination, integration, review, and inference costs.

The control condition is **one strong, well-tooled agent using an explicit localize/plan–edit–execute–validate loop**. Simple scaffolds remain competitive: Agentless reached 32% on SWE-bench Lite with a fixed localization–repair–validation workflow, and SWE-agent’s interface ablation showed that tool design alone can produce material gains ([Xia et al., 2025, E028](https://doi.org/10.1145/3715754); [Yang et al., 2024, E061](https://proceedings.neurips.cc/paper_files/paper/2024/file/5a7c947568c1b1328ccc5230172e1e7c-Paper-Conference.pdf)). Multi-agent gains cannot therefore be attributed to agent count unless model, tools, prompts, attempts, and budget are matched.

The strongest positive mechanism is **specialization around artifacts and executable feedback**. In bounded studies, separate localization, testing, implementation, and QA stages improved selected function- and repository-level outcomes; test-informed selection outperformed language-model ranking without tests ([AgentCoder, E002](https://arxiv.org/pdf/2312.13010); [MAGIS, E040](https://proceedings.neurips.cc/paper_files/paper/2024/file/5d1f02132ef51602adf07000ca5b6138-Paper-Conference.pdf); [MASAI, E041](https://arxiv.org/pdf/2406.11638)). BOAD’s same-model comparison improved over its single-agent baseline on SWE-bench Verified and Live, but a manually designed multi-agent variant was worse and Live peaked at two subagents ([Xu et al., 2026, E010](https://arxiv.org/pdf/2512.23631)). This is evidence for task/scaffold fit, not monotonic scaling.

The strongest negative mechanism is **coupling**. CooperBench’s paired, overlapping features performed 30% worse with two cooperating agents on average, with duplicated work and divergent architecture prominent ([Khatua et al., 2026, E026](https://arxiv.org/pdf/2601.13295)). A broader controlled preprint found benefits on a decomposable task but 39–70% degradation on sequential planning and worse efficiency per token for multi-agent configurations ([Kim et al., 2026, E070](https://arxiv.org/pdf/2512.08296)). Those exact magnitudes are benchmark-bound, but they align with formal work showing that decentralization and partial information add genuine planning difficulty ([Bernstein et al., 2002, E065](https://pubsonline.informs.org/doi/10.1287/moor.27.4.819.297)) and with MAST’s observed failures in system design, inter-agent alignment, verification, and termination ([Cemri et al., 2025, E074](https://proceedings.neurips.cc/paper_files/paper/2025/file/b1041e52d3be19f0a9bc491657488e4a-Paper-Datasets_and_Benchmarks_Track.pdf)).

Accordingly:

- **Small fixes:** use one agent by default. A second agent is justified mainly for independent diagnosis, test generation, or risk-focused review—not overlapping implementation.
- **Medium features:** start with one agent. Use two or three only after freezing a testable contract and assigning disjoint responsibilities, such as backend, UI, and black-box tests.
- **Large/cross-cutting features:** separate architecture and dependency planning from implementation. A practical initial topology is one accountable lead plus two or three workers/verifiers, isolated in branches/worktrees; scale only when the task graph contains additional ready work and integration is not the bottleneck.
- **Greenfield products:** multi-agent work is plausible but not autonomous product development. Begin with product/architecture contracts and executable acceptance tests, then use a small lead-and-workers topology. Human product and architecture ownership, staged integration, observability, security review, and rollback remain mandatory.

Consensus is not a correctness oracle. Majority voting often explains debate gains, group conformity makes agent judgments correlated, and hidden-information teams can converge while missing uniquely held evidence ([Choi et al., 2025, E027](https://papers.nips.cc/paper_files/paper/2025/hash/934252acd87f254d5d4672fbde283bd2-Abstract-Conference.html); [Choi et al., 2025, E006](https://aclanthology.org/2025.findings-acl.265/); [Li et al., 2026, E064](https://arxiv.org/abs/2505.11556)). Prefer compilers, tests, static analysis, security tools, traces, and accountable human review.

Codex and Claude Code now document subagents, context isolation, model routing, permissions, monitoring, and worktree mechanisms. Claude Code additionally documents experimental communicating agent teams. These are **capabilities**, not evidence that either product’s multi-agent mode improves delivery outcomes. The platform defaults below use those controls while keeping the empirical burden of proof on local, matched evaluation.

## Decision rule before agent count

Answer these questions in order. A “no” at steps 1–4 normally means stay with one agent.

1. **Baseline:** Can one strong agent with the relevant tools, a clean environment, and an explicit validation loop solve the task within the time/risk budget?
2. **Decomposability:** Are at least two work items ready now, with low coupling and stable input/output contracts?
3. **Independent verification:** Can each item be accepted or rejected without trusting the producing agent’s explanation?
4. **Isolation:** Can write sets be separated by file/module/service and, for concurrent edits, by branch/worktree and runnable environment?
5. **Integration capacity:** Is one accountable integrator available, with enough review and test capacity to absorb outputs?
6. **Economics:** Under a matched model/tool budget, is expected wall-clock or quality benefit likely to exceed additional tokens, merge work, review time, and failure recovery?

This rule operationalizes Contract Net’s explicit allocation and reporting and SharedPlans’ joint commitments without assuming that chat creates shared understanding ([Smith, 1980, E066](https://www.eecs.ucf.edu/~lboloni/Teaching/EEL6788_2008/papers/The_Contract_Net_Protocol_Dec-1980.pdf); [Grosz and Kraus, 1996, E025](https://u.cs.biu.ac.il/~sarit/data/articles/20.pdf)). The shared state should be a compact set of authoritative artifacts—objective, contracts, dependencies, owners, base commits, tests, and decisions—not a copied transcript.

## Literature-backed decision matrix

“Default” means the starting configuration, not an asserted optimum. No study establishes a universal agent count by project size.

| Scope | Default agent count and roles | Topology and model tier | Context and branch/worktree strategy | Review and testing gates | Stop conditions | Do **not** use multiple agents when… |
|---|---|---|---|---|---|---|
| **Small feature / bug fix** | **1** implementation agent. Optional **+1** read-only diagnostician, test author, or risk reviewer when ambiguity/risk is material. | Single context. If a second agent is used, hub-and-spoke with one write owner. Use the strongest practical coding model for diagnosis/implementation; an economical model is acceptable only for bounded search or mechanical checks validated locally. | Give the writer the issue, relevant code, baseline result, and acceptance tests. Preserve independent first-pass review context. Same checkout for one writer; separate worktree only if a second agent writes a non-overlapping test artifact. | Reproduce failure; targeted tests; affected-package tests; lint/type/static checks; diff review. Security-specific oracle for privileged or security-sensitive code. Human approval where operational/security impact is material. | Stop fan-out on duplicate diagnosis, same-file edits, changing assumptions, no new evidence, or when coordination time approaches the remaining implementation estimate. | The fix is localized/sequential; one agent already has a reliable reproduction and solution path; the second worker would touch the same code; no trustworthy oracle exists. |
| **Medium feature** | Start with **1**. If the work passes the independence test, use **2–3 total**: coordinator/integrator plus one or two workers, commonly implementation + black-box tests, or backend + UI behind a frozen contract. | Hub-and-spoke or staged pipeline, not free-form peers. Frontier/high-reasoning model for contract, integration, and ambiguous code; economical/standard tier for bounded search, fixtures, documentation, or mechanical validation after local qualification. | A versioned contract contains API/schema, invariants, affected modules, acceptance criteria, and dependency order. Each write-capable worker gets a branch/worktree when running concurrently; keep coupled files/shared types under one owner. | Contract review before fan-out; per-slice clean build and targeted tests; independent test/review evidence; integration build; regression and acceptance tests. Reviewer findings must cite code/test evidence, not agreement. | Stop or collapse to one writer when interface churn begins, workers repeatedly clarify shared context, work overlaps a core file, test failures cannot be localized, integration queue grows, or marginal success/token declines. | Work is one dependency chain; API/UX decisions remain unresolved; changes converge on shared types or one central file; environment/setup is unstable; review capacity is the bottleneck. |
| **Large / cross-cutting feature** | Initial **3–5 total**, usually one human-accountable lead/coordinator, **2–3** contract-bounded implementation workers, and an independent verifier/reviewer (a role may be sequential, not continuously active). More than four concurrent workers requires evidence of additional ready queues. | Centralized coordinator over a dependency graph; staged fan-out/fan-in. Use the strongest reasoning tier for architecture, dependency analysis, integration, and adversarial verification; route bounded migrations, searches, or test generation to cheaper tiers only after representative validation. | Before writes: impact/dependency plan, architecture decision records, versioned API/schema contracts, ownership map, migration/rollback plan. Per-worker branch/worktree and runnable environment; no shared writable checkout. Share certified artifacts and verified observations, not raw discussion. Integrate in dependency order through small commits/PRs. | Human architecture/contract gate; per-slice build/static/tests; compatibility and consumer-contract tests; independent security/performance/data checks as applicable; combined integration/end-to-end/full regression in a clean environment; review of migration and rollback. Passing legacy tests alone is insufficient. | Stop adding workers when no dependency-free items remain, merge/review queues dominate, agents collide, the same failure appears across workers, architecture assumptions diverge, regressions rise, or cost/time budget is exceeded. Collapse the disputed dependency chain to one owner. | One unresolved architecture choice controls all work; a shared central subsystem dominates; acceptance/compatibility oracles are missing; release/rollback cannot be made reversible; accountable integration or human review is unavailable. |
| **Greenfield product** | Discovery starts with **1 lead + 1–2 independent researchers/prototypers**. After contracts and acceptance harness exist, use **3–5 total**: human product/architecture owner, coordinator/integrator, 2–3 module workers, and independent test/security/review roles activated at gates. Scale only from measured queue and integration data. | Human-led hub-and-spoke over product milestones and dependency graph. Parallel exploration may precede a single decision; implementation begins only after that decision is recorded. Frontier/high-reasoning tier for product/architecture/integration and critical review; standard/economical tier for bounded implementation and test tasks proven safe by gates. | Versioned product specification, architecture decisions, API/schema contracts, threat model, acceptance tests, observability requirements, and non-functional budgets are authoritative. Isolated worktree/environment per writer; small PRs; trunk integration behind flags. Retain prompts/config, model IDs, base commits, traces, and test outputs for audit. | Human product/architecture approval; executable vertical-slice acceptance before broad fan-out; per-module tests; integration/end-to-end; security, performance, accessibility, data-migration, observability, and operational-readiness gates as relevant; canary/feature flags and tested rollback before release. | Stop autonomous expansion when acceptance criteria change faster than implementation, core architecture churns, agents produce code faster than it can be reviewed, cleanup/rework grows, defects repeat across modules, non-functional gates fail, or rollback is unproven. | The product problem or architecture is still being discovered; success is primarily tacit/subjective; no runnable end-to-end harness exists; production credentials/data would require broad agent permissions; the organization cannot own maintenance and incidents. |

### Why the matrix changes by scope

For small work, the empirical prior favors simplicity. CooperBench supplies direct negative evidence for overlapping feature work, a matched 50-issue vendor run found a tie between one and multiple agents, and Agentless shows that a disciplined simple scaffold can outperform more elaborate systems ([E026](https://arxiv.org/pdf/2601.13295); [Squad, E060](https://github.com/tamirdresher/squad-swe-bench); [E028](https://doi.org/10.1145/3715754)). The optional second agent is therefore a source of **independent evidence**, not a second co-author of the same patch.

For medium work, limited positive evidence appears when roles map to separable functions with executable outputs. MAGIS’s QA role and MASAI’s test-informed ranking helped within their scaffolds, while Co-Coder’s small preprint found dependency-cohesive partitions better than naive file-level parallelism on 28 generation tasks ([E040](https://proceedings.neurips.cc/paper_files/paper/2024/file/5d1f02132ef51602adf07000ca5b6138-Paper-Conference.pdf); [E041](https://arxiv.org/pdf/2406.11638); [Yang et al., 2026, E073](https://arxiv.org/abs/2606.00953)). The matrix accordingly permits a small team only behind a frozen boundary.

For large work, dependency planning precedes staffing. CodePlan’s planner passed validity checks on five of seven repository-wide changes spanning 2–97 files while context-matched non-planning baselines passed none; it was not a multi-agent study, so the supported conclusion is “plan dependencies,” not “spawn workers” ([Bairi et al., 2024, E020](https://doi.org/10.1145/3643757)). CAID provides emerging direct evidence for a central manager, dependency graph, worktree isolation, and executable verification on two long-horizon benchmarks, but also finds higher cost, sequential integration, and non-monotonic returns to engineer count ([Geng and Neubig, 2026, E029](https://arxiv.org/pdf/2603.21489)).

For greenfield products, prototype papers demonstrate artifact pipelines but not durable autonomous delivery. DevEval and ProjectEval report low project-level success; in DevEval, conversational second-agent review did not improve implementation, while execution feedback did ([Li et al., 2025, E053](https://aclanthology.org/2025.coling-main.502/); [Liu et al., 2025, E051](https://aclanthology.org/2025.findings-acl.1036/)). Anthropic’s compiler and OpenAI’s internal greenfield case show that high agent counts can produce large artifacts when surrounded by isolation, tests, structural constraints, review, and cleanup, but neither has a single-agent control or independent production-quality audit ([Carlini, 2026, E011](https://www.anthropic.com/engineering/building-c-compiler); [Lopopolo, 2026, E033](https://openai.com/index/harness-engineering/)). They justify investing in a harness; they do not justify autonomous swarms.

## Default coordination and handoff protocol

The following protocol is a concrete synthesis, not a directly validated universal workflow.

1. **Define the unit of value.** Record the user-visible outcome, non-goals, baseline behavior, acceptance oracle, risk class, and budget.
2. **Build a dependency graph.** Nodes must have an owner, inputs, outputs, touched surface, acceptance command, and dependencies. Do not create workers for blocked nodes.
3. **Allocate explicitly.** Each task packet states the base commit, allowed write set, interface version, acceptance criteria, permissions, model tier, time/token limit, and required return artifact.
4. **Isolate writers.** Use one branch/worktree and runnable environment per concurrent writer. Read-only explorers may share the repository if permissions prevent writes.
5. **Return evidence, not confidence.** A handoff includes commit/diff, changed contracts, commands run, results, remaining uncertainty, and any discovered conflict with the plan.
6. **Validate before consumption.** The coordinator or independent verifier checks the handoff’s schema and executable oracle before another worker builds on it. Failed handoffs are repaired or abandoned locally.
7. **Integrate centrally.** One owner merges in dependency order, runs combined tests, and records any decision or contract change. A clean Git merge is not proof of semantic compatibility.
8. **Stop deliberately.** End or consolidate the team when the ready queue empties, integration becomes critical path, repeated failures carry no new evidence, or the predefined economic/risk budget is exhausted.

This “certified artifact” approach is consistent with RTADev’s checked intermediate repository and with blackboard/shared-plan foundations, but RTADev’s evaluation is small-app and model-specific ([Liu et al., 2025, E057](https://aclanthology.org/2025.findings-acl.80/); [Nii, 1986, E009](https://onlinelibrary.wiley.com/doi/10.1609/aimag.v7i2.537)). Treat it as an auditable operating hypothesis and measure it locally.

## Practical default operating model for Codex

### Documented capabilities

Official Codex documentation says subagents have separate threads, can inherit or override model/reasoning configuration, can be monitored, and inherit sandbox/permission boundaries; it also warns that they multiply token/tool usage and recommends beginning with independent, read-heavy work ([OpenAI, “Subagents,” E023](https://learn.chatgpt.com/docs/agent-configuration/subagents)). Codex desktop can isolate parallel chats and scheduled work in Git worktrees that begin detached and can later be promoted or handed off ([OpenAI, “Worktrees,” E024](https://learn.chatgpt.com/docs/environments/git-worktrees)). The sandbox bounds filesystem/network access separately from approval policy ([OpenAI, “Sandbox,” E022](https://learn.chatgpt.com/docs/sandboxing)). OpenAI documents model tier and reasoning choices, but not a controlled software-engineering result proving that a particular routing policy is optimal ([OpenAI model guidance, E045](https://developers.openai.com/api/docs/guides/latest-model)).

### Recommended default

1. Keep the **main Codex task as coordinator and integration authority**. Store the objective, dependency graph, contracts, and acceptance commands in repository Markdown or issue artifacts.
2. For small work, do not delegate by default. If needed, spawn one **read-only explorer/test reviewer**; the coordinator remains sole writer.
3. For medium work, use at most two specialist subagents initially. Give each a non-overlapping packet and return format. Prefer subagents for search, tests, review, and evidence; use separate worktree chats for concurrent implementation.
4. For large/greenfield work, create one worktree per write-capable task, each from a recorded base commit. Use the main task for architecture decisions and merge order. Do not have several subagents edit a shared checkout.
5. Use the strongest available coding/reasoning tier for planning, ambiguous implementation, integration, and security review. Route bounded repository scans, fixtures, documentation, and mechanical validation to faster/economical tiers only after testing them on representative tasks.
6. Narrow the parent sandbox/permissions before delegation; a worker should receive only required filesystem, network, command, and credential access. Escalations return to the accountable coordinator/human.
7. Set a concurrency cap and per-task budget. Record model identifier, reasoning level, agent instructions, base commit, permissions, commands, token/cost data, and results. Hosted-model replay is auditable, not necessarily deterministic.
8. Merge only after local tests and independent review; then run integration and regression gates in the target worktree. Stop spawning when no independent ready item remains or integration/review becomes the critical path.

**Evidence status:** high for the existence and stated mechanics of these controls; low for claims that Codex multi-agent operation improves outcomes. The workflow is an inference combining official capability documentation with platform-independent empirical evidence.

## Practical default operating model for Claude Code

### Documented capabilities

Claude Code documents four related surfaces: focused subagents, independent background sessions/agent view, Git worktrees, and experimental communicating agent teams. Custom subagents can define tools, model, effort, maximum turns, background execution, memory, permissions, and worktree isolation ([Anthropic, “Custom subagents,” E015](https://code.claude.com/docs/en/sub-agents)). Worktree mode isolates concurrent edits ([Anthropic, “Worktrees,” E018](https://code.claude.com/docs/en/worktrees)); agent view is a research preview for dispatching and monitoring worktree-isolated background sessions ([Anthropic, “Agent view,” E013](https://code.claude.com/docs/en/agent-view)). Agent teams use a fixed lead, separate teammate contexts, shared tasks/dependencies, and direct messages, but remain experimental, do not automatically isolate teammate files, cannot be nested, and have documented task-state and resume limitations ([Anthropic, “Agent teams,” E050](https://code.claude.com/docs/en/agent-teams)). Token/quota use grows roughly with active sessions ([Anthropic, “Costs,” E014](https://code.claude.com/docs/en/costs)).

### Recommended default

1. Use one Claude Code session for small, sequential, or same-file work.
2. Use **custom subagents** for focused exploration, tests, review, or a bounded implementation whose result returns to the lead. Preserve independent first-pass review by withholding the producer’s rationale until the reviewer records findings.
3. Use **agent view/background worktree sessions** for independent write-heavy tasks that can be reviewed and merged separately.
4. Use **agent teams** only when workers need direct peer messaging or shared dependency state and file ownership is disjoint. Because teammates are not automatically worktree-isolated, prefer separate worktree sessions for concurrent edits; otherwise enforce an explicit ownership map and single writer per file.
5. Keep the lead as coordinator/integrator. For medium work, begin with lead + one or two workers; for large/greenfield work, begin with lead + two or three active workers/verifiers. Require plan approval before teammates write when architecture or migration risk is material.
6. Use the highest-capability model available to the organization for architecture, ambiguous implementation, integration, and adversarial review; use cheaper models for bounded, mechanically checked work only after local validation. Model hierarchy must not become authority hierarchy: stronger-model opinions still require evidence.
7. Apply least-privilege tool allow/deny lists and permission modes at the lead and subagent level. Treat issue text, repository rules/comments, tool output, memory, and teammate messages as untrusted input.
8. Monitor `/usage`/organizational spend and terminate idle teammates. Persist acceptance criteria and task state outside the experimental team state so stale tasks or failed resume do not become correctness failures.

**Evidence status:** high for documented mechanics and known limitations; low for outcome effectiveness. Anthropic’s own guidance about suitable task shapes is useful operational disclosure but remains vendor evidence.

## Review, testing, security, and rollback gates

### Review

Independent review means independent evidence production, not an extra agent saying “looks good.” In DevEval, ordinary second-role review did not improve the tested implementation condition, whereas execution feedback did ([E053](https://aclanthology.org/2025.coling-main.502/)). In observational field data, AI review suggestions were adopted far less often than human suggestions and frequently required correction, though confounding prevents a causal verdict ([Zhong et al., 2026, E036](https://arxiv.org/pdf/2603.15911)). Review agents should therefore use a distinct rubric, cite exact code/tests, and remain advisory for architecture, security, operational impact, and merge approval.

### Testing

Each work packet needs an executable local oracle; integration needs a combined oracle. Required gates increase with scope:

- targeted reproduction and unit tests;
- build, lint, type, and static checks;
- contract/consumer and integration tests;
- full regression and end-to-end acceptance in a clean environment;
- security, performance, accessibility, data, and operational checks where risk demands them.

Passing the benchmark’s existing tests is not sufficient. UTBoost found 345 erroneous SWE-bench patches that existing tests had accepted ([Yu et al., 2025, E071](https://aclanthology.org/2025.acl-long.189/)). Security also requires a separate oracle: SecureVibeBench found that functionally correct coding-agent outputs frequently remained insecure in its C/C++ tasks ([Chen et al., 2026, E059](https://arxiv.org/pdf/2509.22097)).

### Permissions and untrusted context

Every additional agent is another principal, tool caller, and communication channel. AgentDojo demonstrates indirect prompt-injection failures in tool-using agents, while Prompt Infection demonstrates propagation between agents in proof-of-concept systems ([Debenedetti et al., 2024, E003](https://proceedings.neurips.cc/paper_files/paper/2024/file/97091a5177d8dc64b1da8bf3e1f6fb54-Paper-Datasets_and_Benchmarks_Track.pdf); [Lee and Tiwari, 2024, E052](https://arxiv.org/pdf/2410.07283)). Use least privilege; separate read, write, network, secret, and deployment authority; and stop on instructions from repository/tool/agent content that expand scope or request secrets.

### Rollback

No located controlled study measures multi-agent rollback, canary safety, database recovery, or incident outcomes. Therefore, the recommendation—small reversible commits, backward-compatible expand/contract migrations, feature flags, canaries, and a tested recovery path—is conservative software-release practice, **not a demonstrated multi-agent benefit**. Worktree isolation reduces pre-merge blast radius but does not constitute production rollback.

## Robust findings, emerging practice, and unsupported claims

| Status | Findings |
|---|---|
| **Robust within studied settings** | Decomposition and decentralization add coordination complexity; architecture must fit task dependencies. Tool/interface quality is a major confounder. Executable feedback is stronger than conversational review. Shared writable state and overlapping edits create conflicts and semantic loss. Verification and termination failures are recurrent. Existing test suites can accept incorrect patches. Public benchmark scores require validity, contamination, cost, and variance caveats. |
| **Promising / emerging** | Coordinator-plus-specialists for independently verifiable stages; dependency-cohesive module partitioning; worktree-isolated branch-and-merge; certified handoff artifacts; independent localization/test/security roles; selective lower-tier model routing; small agent teams for long-horizon work. Evidence is benchmark-bound, preprint-heavy, or vendor case evidence. |
| **Insufficient evidence** | A universal optimal agent count; peer messaging outperforming hub-and-spoke coordination; role-play/job titles causing gains; multiple agents improving production developer throughput, defect escape, incidents, or maintainability; autonomous cross-service migration or product delivery; exact reproducibility on mutable hosted models; consensus as verification. |

## Contradictions and reconciliation

Apparently conflicting findings are mostly differences in task, model, scaffold, metric, or experimental design rather than logical contradictions.

| Apparent contradiction | Reconciliation |
|---|---|
| AgentCoder, MAGIS, CodeR, and BOAD report gains, while CooperBench and the scaling study report losses. | Positive systems specialize localization/testing/QA or optimize a hierarchy and often add search/attempts/tools. CooperBench deliberately pairs overlapping features; the scaling result is highly task-dependent. The causal variable is architecture–task fit and verified handoffs, not “multi-agent” as a binary label. |
| Co-Coder reports better cost and latency, while CAID reports higher cost and little wall-clock improvement. | Co-Coder uses 28 compact Python generation tasks and dependency-cohesive parallel files; CAID studies long-horizon work where central integration remains sequential. Critical-path shape and integration cost differ. Both are preprints. |
| Debate papers report gains, while voting/conformity/HiddenBench show weak or harmful communication. | Early debate comparisons can include ensemble/sample gains. Later work isolates majority voting and distributed-information failures. Communication helps only when it surfaces decision-relevant unique evidence and aggregation can recognize it; ordinary discussion does not create an oracle. |
| Large vendor projects demonstrate many-agent production, while controlled coding benchmarks show non-monotonic scaling. | The vendor projects invest heavily in containers/worktrees, tests, task locks, structural rules, human steering, and cleanup, and lack matched controls. They demonstrate feasibility under a large harness, not marginal benefit per additional agent. |
| Human productivity studies range from a pooled 26.08% increase in completed tasks to a 19% slowdown for experienced maintainers. | These are single-assistant, not multi-agent studies. The populations, repositories, task familiarity, tools, dates, and outcomes differ ([Cui et al., 2026, E067](https://doi.org/10.1287/mnsc.2025.00535); [Becker et al., 2025, E042](https://metr.org/Early_2025_AI_Experienced_OS_Devs_Study-paper.pdf)). They establish the need for local field measurement, not a pooled multi-agent effect. |
| SWE-bench improvements appear precise, while later audits question the benchmark. | Scores are historical evidence about systems on that harness. OpenAI found material test/specification flaws and exposure in a difficult Verified subset and estimated substantial brokenness in public SWE-bench Pro tasks ([E075](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/); [E062](https://openai.com/index/separating-signal-from-noise-coding-evaluations/)). Do not convert leaderboard deltas into production reliability. |

## Evaluation plan for an organization

Before standardizing a multi-agent workflow, run a matched pilot on private or time-split tasks representative of each intended scope:

- same base model(s), tools, repository snapshot, hints, attempts, and permission envelope;
- one-agent baseline versus the proposed topology;
- success judged by hidden acceptance/regression/security tests plus blinded human maintainability review;
- report task-level outcomes and variance, not only averages;
- measure wall-clock time, total tokens/cost, human steering and review time, merge conflicts, regressions, rework, escaped defects, and rollback/incident outcomes;
- preserve prompts, agent definitions, exact model identifiers, framework versions, base commits, dependency locks, traces, and outputs;
- predefine stop thresholds and include failed/non-completing runs.

This follows the cost-and-reproducibility critique in *AI Agents That Matter* ([Kapoor et al., 2025, E005](https://openreview.net/pdf?id=Zy4uFzMviZ)) and addresses the measurement failure METR reported when concurrent-agent time and task selection became hard to account for ([Becker et al., 2026, E072](https://metr.org/blog/2026-02-24-uplift-update/)).

## Evidence assessment and limitations

The most credible evidence consists of peer-reviewed formal foundations, repository benchmark construction/audits, controlled component ablations, and MAST’s failure taxonomy. Even these are narrow: many software studies use Python, historical public issues, small generated applications, older models, and pass/fail tests rather than maintainability or operations. The best direct current comparisons include BOAD, CooperBench, CAID, Co-Coder, and the 2026 scaling study, but several are preprints and their tasks/topologies differ.

Official Codex and Claude Code documentation is authoritative for what controls existed on 23 August 2026. It is low-quality evidence for productivity, correctness, or optimal team shape. Anthropic and OpenAI engineering cases disclose valuable mechanisms and costs but are vendor-sponsored, uncontrolled, and not independently audited. Their practices must remain hypotheses until replicated in the target environment.

The review found no randomized production comparison of one versus multiple coding agents; no controlled multi-agent study of cross-repository/service migrations, canary/rollback outcomes, incident rate, or long-term ownership; and no stable dose-response curve for agent count. Benchmark contamination, hidden-test defects, different compute definitions, LLM judges, changing model aliases, publication bias, and rapidly evolving tools all limit quantitative synthesis. A meta-analytic pooled effect would be misleading because the treatments and outcomes are not commensurate.

Finally, this is a literature review through the actual cutoff, not an assurance case for any deployment. Security-sensitive, safety-critical, regulated, data-destructive, or production-privileged work requires domain controls and accountable human authority beyond this framework.

## Research gaps

1. Randomized or credible quasi-experimental production studies comparing matched single- and multi-agent workflows over months, including human review time, defect escape, incidents, and maintainability.
2. Dose-response studies varying agent count, topology, model tier, communication, and compute independently on current private/time-split repository tasks.
3. Cross-repository, cross-service, migration, data, infrastructure, mobile, frontend, and non-Python benchmarks with operational and rollback outcomes.
4. Tests of whether independent model families, prompts, tools, or evidence sources reduce correlated review error and conformity.
5. Security evaluations of multi-agent permission graphs, prompt-injection propagation, poisoned shared memory, compromised workers, and secret/deployment boundaries.
6. Measures of integration load, semantic conflict, reviewer queueing, cleanup debt, architecture drift, and ownership transfer—not merely patch acceptance.
7. Reproducibility standards for mutable hosted models, including versioned prompts/configuration, environment capture, traces, and replay tolerances.
8. Decision-theoretic selectors that predict when a task should remain single-agent, use independent samples, use a coordinator, or use a communicating team under a cost/risk budget.

## Annotated source-linked bibliography

This is the deduplicated core supporting the decision framework; the complete 76-source bibliography is the [evidence register](07-evidence-register.md), with full annotations in the six scope memos.

### Foundations and failure mechanisms

- **Smith, Reid G. (1980), “The Contract Net Protocol” ([E066](https://www.eecs.ucf.edu/~lboloni/Teaching/EEL6788_2008/papers/The_Contract_Net_Protocol_Dec-1980.pdf)).** Peer-reviewed protocol paper. Explicit announcement, bidding, award, and reporting provide a durable allocation model; transfer to LLM coding agents is conceptual.
- **Grosz, Barbara J., and Sarit Kraus (1996), “Collaborative Plans for Complex Group Action” ([E025](https://u.cs.biu.ac.il/~sarit/data/articles/20.pdf)).** Peer-reviewed formalism. Collaboration requires a joint recipe and commitments, not merely parallel individual plans.
- **Bernstein, Daniel S., et al. (2002), “The Complexity of Decentralized Control of Markov Decision Processes” ([E065](https://pubsonline.informs.org/doi/10.1287/moor.27.4.819.297)).** Peer-reviewed theory. Partial observability and decentralized control can be fundamentally harder than centralized planning; not an LLM experiment.
- **Cemri, Mert, et al. (2025), “Why Do Multi-Agent LLM Systems Fail?” ([E074](https://proceedings.neurips.cc/paper_files/paper/2025/file/b1041e52d3be19f0a9bc491657488e4a-Paper-Datasets_and_Benchmarks_Track.pdf)).** Peer-reviewed trace taxonomy over seven systems. Failures span system design, inter-agent alignment, and verification/termination; scaled labeling retains judge dependence.
- **Choi, Hyeong Kyu, Xiaojin Zhu, and Yixuan Li (2025), “Debate or Vote” ([E027](https://papers.nips.cc/paper_files/paper/2025/hash/934252acd87f254d5d4672fbde283bd2-Abstract-Conference.html)).** Peer-reviewed benchmark and formal study. Independent majority voting explained most gains of ordinary debate in tested NLP settings; repository transfer is inferential.
- **Li, Yuxuan, Aoi Naito, and Hirokazu Shirado (2026), HiddenBench ([E064](https://arxiv.org/abs/2505.11556)).** Peer-reviewed ICML study. Agents performed poorly when decision-relevant information was distributed; structured evidence exchange helped in a small ablation.

### Direct and adjacent software-engineering evidence

- **Xia, Chunqiu Steven, et al. (2025), “Demystifying LLM-Based Software Engineering Agents” / Agentless ([E028](https://doi.org/10.1145/3715754)).** Peer-reviewed repository benchmark. A fixed localize–repair–validate workflow was a strong, low-cost control, showing complexity is not necessary by itself.
- **Tao, Wei, et al. (2024), MAGIS ([E040](https://proceedings.neurips.cc/paper_files/paper/2024/file/5d1f02132ef51602adf07000ca5b6138-Paper-Conference.pdf)).** Peer-reviewed repository experiment. Manager/developer/QA specialization improved selected SWE-bench outcomes, but files/hints, historical models, and scaffold confounds limit generalization.
- **Xu, Iris, et al. (2026), BOAD ([E010](https://arxiv.org/pdf/2512.23631)).** ICLR 2026 same-model comparison. An optimized hierarchy beat its single baseline, a manual hierarchy did not, and performance peaked at a small number of subagents.
- **Khatua, Arpandeep, et al. (2026), CooperBench ([E026](https://arxiv.org/pdf/2601.13295)).** Controlled open preprint on paired repository features. Cooperative agents underperformed solo execution on compact overlapping work; preprint and task construction bound the claim.
- **Geng, Jiayi, and Graham Neubig (2026), CAID ([E029](https://arxiv.org/pdf/2603.21489)).** Controlled long-horizon preprint. Central planning, worktrees, branch/merge, and executable verification helped on two benchmarks, while cost rose and agent-count returns were non-monotonic.
- **Bairi, Ramakrishna, et al. (2024), CodePlan ([E020](https://doi.org/10.1145/3643757)).** Peer-reviewed repository-level planning study. Dependency-aware planning outperformed context-matched non-planning baselines on seven cross-cutting changes; it is not a multi-agent comparison.
- **Li, Bowen, et al. (2025), DevEval full-lifecycle study ([E053](https://aclanthology.org/2025.coling-main.502/)).** Peer-reviewed study across 22 repositories. Project-level success was low; execution feedback helped while ordinary second-role review did not in the reported subset.
- **Yu, Boxi, et al. (2025), UTBoost ([E071](https://aclanthology.org/2025.acl-long.189/)).** Peer-reviewed benchmark audit. Additional tests rejected hundreds of patches previously labeled passed, demonstrating test-suite insufficiency.
- **Kapoor, Sayash, et al. (2025), “AI Agents That Matter” ([E005](https://openreview.net/pdf?id=Zy4uFzMviZ)).** Peer-reviewed evaluation critique. Agent studies must report cost, standardized controls, holdouts, and reproducibility rather than accuracy alone.

### Platform capabilities and operational cases

- **OpenAI, Codex “Subagents,” “Worktrees,” and “Sandbox” ([E023](https://learn.chatgpt.com/docs/agent-configuration/subagents), [E024](https://learn.chatgpt.com/docs/environments/git-worktrees), [E022](https://learn.chatgpt.com/docs/sandboxing)).** Official living documentation, accessed 23 August 2026. High-quality capability evidence for isolated contexts, worktrees, permissions, monitoring, and routing; low-quality outcome evidence.
- **Anthropic, Claude Code “Custom subagents,” “Worktrees,” “Agent view,” “Agent teams,” and “Costs” ([E015](https://code.claude.com/docs/en/sub-agents), [E018](https://code.claude.com/docs/en/worktrees), [E013](https://code.claude.com/docs/en/agent-view), [E050](https://code.claude.com/docs/en/agent-teams), [E014](https://code.claude.com/docs/en/costs)).** Official living documentation, accessed 23 August 2026. High-quality evidence of mechanics and documented limitations, not comparative productivity.
- **Carlini, Nicholas / Anthropic (2026), “Building a C Compiler with a Team of Parallel Claudes” ([E011](https://www.anthropic.com/engineering/building-c-compiler)).** Detailed uncontrolled vendor stress test. It illustrates isolation, test-based task splitting, high cost, regression, and integration limits, not optimal staffing.
- **Lopopolo, Ryan / OpenAI (2026), “Harness Engineering” ([E033](https://openai.com/index/harness-engineering/)).** Uncontrolled first-party greenfield case. Repository-local decisions, structural lints, per-worktree environments, review, and cleanup enabled scale; no counterfactual establishes the effect of multiple agents.

### Security and field boundaries

- **Debenedetti, Edoardo, et al. (2024), AgentDojo ([E003](https://proceedings.neurips.cc/paper_files/paper/2024/file/97091a5177d8dc64b1da8bf3e1f6fb54-Paper-Datasets_and_Benchmarks_Track.pdf)).** Peer-reviewed tool-agent security benchmark. Indirect prompt injection compromises utility/security tradeoffs; not specific to coding teams.
- **Chen, Junkai, et al. (2026), SecureVibeBench ([E059](https://arxiv.org/pdf/2509.22097)).** Repository security preprint. Functional correctness frequently coexisted with vulnerabilities on C/C++ tasks, supporting separate security gates.
- **Cui, Kevin Zheyuan, et al. (2026), “The Effects of Generative AI on High-Skilled Work” ([E067](https://doi.org/10.1287/mnsc.2025.00535)).** Peer-reviewed field experiments found a pooled increase in completed tasks with single assistants; not a multi-agent evaluation.
- **Becker, Joel, et al. (2025), experienced-maintainer RCT ([E042](https://metr.org/Early_2025_AI_Experienced_OS_Devs_Study-paper.pdf)).** Randomized field study found a slowdown with early-2025 AI tools among experienced maintainers on familiar repositories. It demonstrates setting sensitivity, not a permanent or multi-agent effect.

## Traceability and validation note

All external works cited in this synthesis are normalized in [07-evidence-register.md](07-evidence-register.md) and annotated in at least one of [01](01-foundations-and-theory.md), [02](02-empirical-software-engineering.md), [03](03-small-medium-features.md), [04](04-large-features-greenfield-products.md), [05](05-tooling-and-platform-landscape.md), or [06](06-red-team-limitations.md). Duplicate works are cited once conceptually and distinguished where companion official pages or repositories supply capability rather than outcome evidence. The synthesis does not rely on inaccessible, abstract-only, or unregistered sources.
