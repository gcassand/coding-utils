# Tooling and Platform Landscape

## Scope, cutoff, and method

This memo compares the multi-agent facilities available in Codex, Claude Code, and selected open-source/research systems. It covers subagents, background agents, Git worktrees, permission boundaries, context isolation, model routing, monitoring, cost control, and reproducibility. It describes product capabilities, not a general endorsement of multi-agent development.

The requested literature cutoff, **31 August 2026**, is eight days after the actual search date. The **actual search cutoff is 23 August 2026 (Europe/Paris)**; no claim is made about material published from 24–31 August 2026.

Searches targeted official product documentation, first-party repositories, original papers, and publisher proceedings. Codex claims were limited to official OpenAI documentation on `learn.chatgpt.com` and `developers.openai.com`, and every cited page was opened rather than inferred from a search snippet. Claude Code claims use official Anthropic documentation. Open-source claims use project-owned documentation/repositories and original papers. Product pages are treated as high-quality evidence of *documented capability* but low-quality evidence of *effectiveness*. No result was inferred from an abstract alone; where a full paper could not be inspected, that limitation is stated.

## Executive memo

The tools now expose three distinct forms of parallelism, which should not be conflated. First, a **hub-and-spoke subagent workflow** gives workers separate context windows and returns summaries to a coordinator. Codex enables subagents by default and exposes each thread; custom agents can set instructions, models, reasoning effort, sandbox mode, MCP servers, and a concurrency cap. Codex explicitly warns that subagents multiply token use and recommends starting with independent, read-heavy exploration, tests, triage, and summarization because simultaneous code editing creates conflicts and coordination overhead ([OpenAI, “Subagents,” undated living documentation, accessed 2026-08-23](https://learn.chatgpt.com/docs/agent-configuration/subagents)). Claude Code offers an analogous subagent facility with separate context, per-agent tool/model definitions, optional persistent memory, background execution, turn caps, and optional worktree isolation ([Anthropic, “Create custom subagents,” undated living documentation, accessed 2026-08-23](https://code.claude.com/docs/en/sub-agents)).

Second, **independent background sessions** expose parallel tasks directly to the user. Codex uses per-chat agent threads and can place chats or scheduled tasks in Git worktrees; its desktop worktrees start detached, can be promoted to branches, and can be handed back to the local checkout ([OpenAI, “Worktrees,” undated living documentation, accessed 2026-08-23](https://learn.chatgpt.com/docs/environments/git-worktrees)). Claude Code's agent view is a research preview for dispatching and monitoring background sessions and automatically isolates editing sessions in worktrees; Anthropic documents roughly proportional quota use as sessions are added ([Anthropic, “Manage multiple agents with agent view,” undated living documentation, accessed 2026-08-23](https://code.claude.com/docs/en/agent-view)). These are well suited to work that can be reviewed and integrated as separate changes.

Third, a **communicating team** gives workers direct messaging and shared coordination state. Claude Code agent teams provide a fixed lead, independent teammate contexts, a shared task list, mailboxes, dependency tracking, and plan-approval gates. They remain experimental and disabled by default, cannot be nested, do not restore in-process teammates on resume, sometimes leave task status stale, and do **not** isolate teammates in separate worktrees; Anthropic therefore advises disjoint file ownership and warns against sequential, same-file, or dependency-heavy work ([Anthropic, “Orchestrate teams of Claude Code sessions,” documentation as of v2.1.178+, accessed 2026-08-23](https://code.claude.com/docs/en/agent-teams)). Codex's documented product surface is currently closer to coordinator/subagent fan-out and independent worktree chats than to Claude's peer-messaging team topology.

The permission models differ in detail but share an important property: worker autonomy remains bounded by a parent/session policy. Codex subagents inherit the current sandbox and permission mode; non-interactive actions that need a new approval fail back to the parent. The local sandbox constrains files and network access, while approval policy governs boundary crossings ([OpenAI, “Sandbox,” undated living documentation, accessed 2026-08-23](https://learn.chatgpt.com/docs/sandboxing)). Claude teammates begin with the lead's permission settings, and its auto mode applies classifier checks to delegation, each subagent action, and the return result; classifier calls add tokens and latency ([Anthropic, “Choose a permission mode,” undated living documentation, accessed 2026-08-23](https://code.claude.com/docs/en/permission-modes)). Neither design makes autonomous output trustworthy by itself; both are control mechanisms, not correctness evidence.

Model routing is explicit in both products. Codex can inherit or override model and reasoning effort per custom agent and recommends cheaper/faster tiers for bounded scans while reserving stronger models/higher effort for demanding reasoning ([OpenAI, “Subagents”](https://learn.chatgpt.com/docs/agent-configuration/subagents)). Claude Code supports model fields on subagents and model selection for teammates; its cost guide recommends smaller teams and lower-cost models for routine workers, noting roughly proportional token growth with active teammates ([Anthropic, “Manage costs effectively,” undated living documentation, accessed 2026-08-23](https://code.claude.com/docs/en/costs)). These are vendor recommendations, not controlled demonstrations that heterogeneous routing preserves quality.

Open-source systems expose more programmable orchestration but require more engineering. The OpenHands SDK supports resumable sequential delegation, experimental parallel tool/subagent execution, file-defined specialist agents, per-agent model profiles and permission modes, OpenTelemetry traces, and per-call token/cost/latency metrics ([OpenHands, “Task Tool Set”](https://docs.openhands.dev/sdk/guides/task-tool-set); [“Parallel Tool Execution”](https://docs.openhands.dev/sdk/guides/parallel-tool-execution); [“Observability & Tracing”](https://docs.openhands.dev/sdk/guides/observability); all undated living documentation, accessed 2026-08-23). Its ICLR 2025 platform paper describes sandboxing, event streams, delegation, and benchmarks, but the reported SWE-bench result is for a generalist CodeAct agent and does not isolate a multi-agent advantage ([Wang et al., 2024/ICLR 2025](https://arxiv.org/abs/2407.16741)).

AutoGen established conversable-agent and programmable topology patterns, but its official repository is now in maintenance mode and directs new users to Microsoft Agent Framework, whose graph workflows add explicit execution order, state, middleware, telemetry, and human-in-the-loop control ([Wu et al., COLM 2024](https://www.microsoft.com/en-us/research/publication/autogen-enabling-next-gen-llm-applications-via-multi-agent-conversation-framework/); [Microsoft, AutoGen repository](https://github.com/microsoft/autogen); [Microsoft Agent Framework overview](https://learn.microsoft.com/en-us/agent-framework/overview/)). MetaGPT and ChatDev provide important role/SOP and staged-dialogue designs, but their software-generation evidence uses earlier models and largely prototype-style tasks. ChatDev's own paper reports materially greater time/token use and says the technology is more suitable for prototypes than complex real-world applications ([Qian et al., ACL 2024](https://aclanthology.org/2024.acl-long.810/)).

**Bottom line.** The strongest evidence in this scope supports an operational rule, not a universal productivity claim: use multiple agents only when work can be partitioned into independently verifiable outputs; isolate write-heavy workers with worktrees; keep permissions least-privilege; record topology, prompts, models, base commits, environments, traces, and test results; and impose a single integration authority. Claims that multi-agent tooling is generally faster or more correct remain emerging because vendor documents are capability descriptions and the peer-reviewed software-generation studies do not represent current repository-scale industrial work.

## Capability comparison

| Dimension | Codex | Claude Code | Open-source/research systems | Evidence status |
|---|---|---|---|---|
| Delegation topology | Coordinator spawns subagents and consolidates results; custom `worker`, `explorer`, or project agents | Subagents; independent background sessions; experimental lead/teammate teams with shared tasks and messages | OpenHands sequential or fan-out delegation; Microsoft Agent Framework graphs; MetaGPT/ChatDev role pipelines | Documented capability: high; comparative effectiveness: low–medium |
| Context isolation | Each subagent has its own thread; summaries return to parent | Each subagent/teammate has its own context; team lead history does not carry over; project instructions reload | OpenHands persists per-task conversations; graph/event systems make state explicit | High for mechanics; low for effects on correctness |
| Background execution and monitoring | Subagent panels/threads in app, CLI, IDE; worktree chats and scheduled background work | Agent view research preview, `/tasks`, `/agents`, direct attach/steer; teammate notifications | OpenHands terminal visualizer and OTEL traces; framework-specific dashboards | High for presence, no controlled usability comparison |
| File isolation | Desktop chats and scheduled tasks can use Git worktrees; handoff supports integration | `--worktree`, subagent `isolation: worktree`, automatic worktrees in agent view; agent teams themselves share files | OpenHands workspace/runtime isolation is configurable; framework users must design VCS isolation | High for documented behavior |
| Permissions | Subagents inherit sandbox/permission mode; custom agent may narrow sandbox/tool configuration | Subagent tool allow/deny lists and permission modes; teammates start from lead policy; auto classifier checks delegated actions | OpenHands per-agent permission mode and sandbox runtime; MAF requires application-specific controls | High for capability; security efficacy not established here |
| Model routing | Parent inheritance plus per-agent model and reasoning overrides; session concurrency cap | Per-subagent/team model selection, effort inheritance, organization allowlist fallback | OpenHands provider abstraction and per-agent profiles; MAF is multi-provider | High for mechanics; vendor-sponsored guidance on optimal tiers |
| Cost controls | Concurrency cap; visible agent threads; explicit warning that subagents use more tokens | `/usage`, workspace spend limits, model routing, small-team guidance; token use scales with teammate count | OpenHands metrics and per-provider cost accounting; framework-specific budgets | High for measurement controls; medium/low for cost-benefit claims |
| Reproducibility | Project agent TOML, `AGENTS.md`, worktree/base commit; mutable product/model behavior remains | Versioned agent definitions, `CLAUDE.md`, task/transcript state, worktrees; experimental features evolve quickly | Source-controlled configs, graph definitions, event traces, pinned environments/models possible | Mechanisms exist; exact run reproducibility is not demonstrated |

## Actionable findings

The “action” column is an explicitly labeled inference from the cited evidence, not a claim made by the source.

| ID | Evidence | Quality | Actionable inference |
|---|---|---:|---|
| T1 | Both [Codex](https://learn.chatgpt.com/docs/agent-configuration/subagents) and [Claude Code](https://code.claude.com/docs/en/agent-teams) say parallel agents add tokens/coordination overhead and are best on independent work. | High for documentation; low for effectiveness | Require an independence test before spawning: separate questions, test suites, modules, or competing hypotheses. Stay single-agent for sequential/same-file work. |
| T2 | Codex advises beginning with read-heavy tasks; Claude distinguishes focused subagents from communicating teams. | High | Use hub-and-spoke subagents for exploration, review, tests, and evidence gathering. Escalate to a communicating team only when workers genuinely need peer messaging/shared task state. |
| T3 | [Codex worktrees](https://learn.chatgpt.com/docs/environments/git-worktrees) and [Claude worktrees](https://code.claude.com/docs/en/worktrees) isolate concurrent edits; Claude agent teams do not automatically isolate teammates. | High | Give every write-capable independent worker a separate worktree/branch, or enforce disjoint file ownership. Never assume “separate context” means separate filesystem. |
| T4 | Codex subagents inherit sandbox/permissions; Claude teammates start with the lead policy and auto mode evaluates subagent actions. | High | Set the parent to the least privilege every worker needs; create read-only explorer/reviewer roles; do not let a broad lead policy silently expand all workers. |
| T5 | Codex and Claude both allow cheaper/faster worker models, while stronger models can be reserved for synthesis or difficult reasoning. | High for capability; low for optimality | Route bounded scans and mechanical checks to economical tiers, but validate the routing on representative tasks before institutionalizing it. |
| T6 | Claude documents roughly proportional token/quota growth; Codex states each subagent performs separate model/tool work. | High | Cap concurrency and stop idle workers. Include total tokens, wall time, and integration/review time in any pilot; do not optimize on wall-clock time alone. |
| T7 | Claude agent teams have stale-task, resumption, shutdown, fixed-lead, and no-nesting limitations; agent view is a research preview. | High | Treat team state as advisory. Maintain external acceptance criteria and checkpoints; use a human-controlled recovery path rather than depending on automatic resume. |
| T8 | OpenHands exposes per-step/tool/LLM traces and cost metrics; Microsoft Agent Framework provides explicit graph control and telemetry. | High for capability | For repeatable production workflows, prefer explicit orchestration and retained traces over free-form agent conversation alone. |
| T9 | [ChatDev](https://aclanthology.org/2024.acl-long.810/) improved its prototype-generation measures but took about 148 seconds/22,949 tokens versus 15.6 seconds/7,183 tokens for GPT-Engineer and acknowledged weak real-world coverage. | Medium | Do not cite early role-play systems as proof that contemporary multi-agent coding is broadly superior. Treat roles/SOPs as design hypotheses to test. |
| T10 | The [OpenHands platform paper](https://arxiv.org/abs/2407.16741) evaluates strong software agents, but its main SWE-bench result does not isolate delegation as the causal factor. | Medium | Demand single-agent baselines and ablations when evaluating a multi-agent workflow; framework benchmark scores alone do not establish a multi-agent benefit. |
| T11 | AutoGen is in [maintenance mode](https://github.com/microsoft/autogen); Microsoft directs new work to [Agent Framework](https://learn.microsoft.com/en-us/agent-framework/overview/). | High | Avoid selecting a framework from historical papers alone. Record the supported runtime/version and a migration path as part of platform evaluation. |
| T12 | All platforms provide configuration/state artifacts, but none of the inspected sources demonstrates bit-for-bit replay across changing model aliases and hosted services. | Medium inference | Record exact model identifiers, client/framework version, agent definitions, prompts, permissions, base commit, dependency lockfiles, task graph, traces, and test outputs. Call the result auditable rather than deterministic unless replay is verified. |

## Evidence versus inference

### Robustly documented

- Separate agent contexts, explicit delegation, monitoring surfaces, model assignment, permission inheritance, and Git worktree isolation exist in current Codex and Claude Code releases.
- Token use grows with additional active agents; vendors explicitly warn about coordination overhead and same-file conflicts.
- Claude agent teams are experimental; its agent view is a research preview. OpenHands parallel tool execution is experimental. AutoGen is in maintenance mode.
- Current open-source frameworks can expose explicit workflows, persistent state, traces, and per-call usage/cost metrics.

### Emerging or weakly supported

- That any platform's multi-agent mode reliably improves correctness, mergeability, or end-to-end developer throughput over a strong single agent on current repository-level tasks.
- That role specialization itself causes better output, independent of extra tokens, iterative refinement, tool access, or model differences.
- That cheaper worker models plus a stronger coordinator preserve quality across task types.
- That agent-to-agent messaging is superior to coordinator-only summaries for real software teams.
- That recorded transcripts and configuration are sufficient for exact reproducibility when hosted models, prompts, and platform releases change.

## Annotated bibliography

### E1. Codex subagents

- **Title:** [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- **Authors/organization:** OpenAI
- **Date:** Undated living documentation; accessed 23 August 2026
- **Source type:** Official product documentation
- **Evidence quality:** **High** for current documented behavior; **low** for effectiveness
- **Flags:** Vendor-authored; rapidly evolving surface; no controlled comparison
- **Finding:** Codex can spawn parallel specialist agents with separate threads, route models/reasoning per agent, cap concurrent threads, expose agent monitoring, and inherit sandbox/permission policy. The page explicitly warns that agents multiply tokens and advises read-heavy parallelism before write-heavy workflows.
- **Scopes supported:** subagents, context isolation, model routing, monitoring, cost, permissions, coordination limits

### E2. Codex worktrees

- **Title:** [Worktrees](https://learn.chatgpt.com/docs/environments/git-worktrees)
- **Authors/organization:** OpenAI
- **Date:** Undated living documentation; accessed 23 August 2026
- **Source type:** Official product documentation
- **Evidence quality:** **High** for capability
- **Flags:** Vendor-authored; desktop-specific behavior can change
- **Finding:** Codex can create per-chat Git worktrees for parallel/background work, start from a selected branch in detached HEAD state, promote work to a branch, and hand a chat between worktree and local checkout. Scheduled tasks can use dedicated background worktrees.
- **Scopes supported:** worktrees, background work, isolation, integration, reproducibility inputs

### E3. Codex sandbox

- **Title:** [Sandbox](https://learn.chatgpt.com/docs/sandboxing)
- **Authors/organization:** OpenAI
- **Date:** Undated living documentation; accessed 23 August 2026
- **Source type:** Official security/product documentation
- **Evidence quality:** **High** for mechanism; **low** for measured security efficacy
- **Flags:** Vendor-authored; platform-native enforcement differs by operating system
- **Finding:** The sandbox bounds filesystem and network access for local commands, while approval policy separately governs boundary crossings. Spawned commands inherit those boundaries, providing a technical control rather than relying solely on agent intent.
- **Scopes supported:** permissions, sandboxing, autonomy boundaries, security

### E4. OpenAI current model guidance

- **Title:** [Model guidance: Using GPT-5.6](https://developers.openai.com/api/docs/guides/latest-model)
- **Authors/organization:** OpenAI
- **Date:** Undated living documentation; accessed 23 August 2026
- **Source type:** Official API/model documentation
- **Evidence quality:** **High** for availability/configuration; **low** for vendor performance claims
- **Flags:** Vendor-authored; multi-agent API capability is beta; model aliases can move
- **Finding:** OpenAI documents a beta multi-agent capability for GPT-5.6 and a Sol/Terra/Luna tiering intended to trade capability, latency, and cost. The page says multi-agent can reduce wall time on complex tasks that divide cleanly, but provides no controlled software-engineering study on the page.
- **Scopes supported:** model routing, multi-agent API, cost/latency tradeoff, maturity

### E5. Claude Code parallel-work overview

- **Title:** [Run agents in parallel](https://code.claude.com/docs/en/agents)
- **Authors/organization:** Anthropic
- **Date:** Undated living documentation; accessed 23 August 2026
- **Source type:** Official product documentation
- **Evidence quality:** **High** for capability; **low** for effectiveness
- **Flags:** Vendor-authored
- **Finding:** Anthropic distinguishes subagents, agent view, agent teams, and dynamic workflows by coordinator, communication pattern, and isolation needs. It states worktrees isolate edits and that agent teams should partition file ownership because teammates are not automatically worktree-isolated.
- **Scopes supported:** topology selection, background agents, worktrees, coordination

### E6. Claude Code agent teams

- **Title:** [Orchestrate teams of Claude Code sessions](https://code.claude.com/docs/en/agent-teams)
- **Authors/organization:** Anthropic
- **Date:** Undated living documentation describing v2.1.178 and later; accessed 23 August 2026
- **Source type:** Official experimental-feature documentation
- **Evidence quality:** **High** for current mechanics; **low** for effectiveness
- **Flags:** Vendor-authored; **experimental and disabled by default**; known resumption, task-state, and shutdown limitations
- **Finding:** A fixed lead coordinates independent teammate contexts through shared tasks, dependency state, and direct messages; permissions initially inherit from the lead, and plan approval can gate implementation. The documentation warns of higher token use, coordination overhead, diminishing returns, no nested teams, stale task status, and unsuitable same-file/sequential work.
- **Scopes supported:** communicating teams, coordination topology, context isolation, permissions, model routing, monitoring, limitations

### E7. Claude Code custom subagents

- **Title:** [Create custom subagents](https://code.claude.com/docs/en/sub-agents)
- **Authors/organization:** Anthropic
- **Date:** Undated living documentation; accessed 23 August 2026
- **Source type:** Official product documentation
- **Evidence quality:** **High** for capability
- **Flags:** Vendor-authored; some fields and inheritance rules are version-sensitive
- **Finding:** Subagent definitions can control system prompt, tools, model, effort, maximum turns, background execution, worktree isolation, skills, MCP servers, memory scope, and permission mode. Parent modes can override the subagent's declared permissions.
- **Scopes supported:** specialization, model routing, context/memory, permissions, worktrees, stop conditions

### E8. Claude Code worktrees

- **Title:** [Run parallel sessions with worktrees](https://code.claude.com/docs/en/worktrees)
- **Authors/organization:** Anthropic
- **Date:** Undated living documentation; accessed 23 August 2026
- **Source type:** Official product documentation
- **Evidence quality:** **High** for capability
- **Flags:** Vendor-authored; Git-specific defaults
- **Finding:** Claude Code provides a `--worktree` mode and `isolation: worktree` for subagents, with setup/copy and cleanup rules. It explicitly presents worktrees as protection against parallel file collisions.
- **Scopes supported:** branch/worktree strategy, isolation, integration hygiene

### E9. Claude Code agent view

- **Title:** [Manage multiple agents with agent view](https://code.claude.com/docs/en/agent-view)
- **Authors/organization:** Anthropic
- **Date:** Undated living documentation with version history through v2.1.239; accessed 23 August 2026
- **Source type:** Official research-preview documentation
- **Evidence quality:** **High** for capability; **low** for usability/effectiveness
- **Flags:** Vendor-authored; **research preview**; local sessions stop if the machine shuts down
- **Finding:** Agent view dispatches, monitors, attaches to, steers, and cleans up background sessions, using worktrees for editing sessions. The page says ten parallel agents consume quota roughly ten times as fast as one and documents lifecycle/recovery limitations.
- **Scopes supported:** background agents, monitoring, worktrees, cost, recovery

### E10. Claude Code cost controls

- **Title:** [Manage costs effectively](https://code.claude.com/docs/en/costs)
- **Authors/organization:** Anthropic
- **Date:** Undated living documentation; accessed 23 August 2026
- **Source type:** Official product/cost documentation
- **Evidence quality:** **High** for available controls; **low** for recommended model-quality tradeoffs
- **Flags:** Vendor-authored; pricing and model guidance are time-sensitive
- **Finding:** Claude Code exposes session usage, organizational spend reporting/limits, context compaction guidance, and model routing. Agent-team tokens scale roughly with active teammates, so Anthropic recommends focused prompts, small teams, cheaper teammate models, and explicit shutdown.
- **Scopes supported:** cost control, monitoring, model routing, stop conditions

### E11. Claude Code permission modes

- **Title:** [Choose a permission mode](https://code.claude.com/docs/en/permission-modes)
- **Authors/organization:** Anthropic
- **Date:** Undated living documentation; accessed 23 August 2026
- **Source type:** Official security/product documentation
- **Evidence quality:** **High** for mechanism; **low** for measured security efficacy
- **Flags:** Vendor-authored; auto classifier consumes tokens and adds latency
- **Finding:** Auto mode checks the delegated task, subagent actions, and the returned history, with parent rules taking precedence. The mechanism treats inter-agent approval claims as untrusted and documents both cost and latency overhead.
- **Scopes supported:** permissions, security, agent-to-agent trust, cost/latency

### E12. OpenHands task delegation

- **Title:** [Task Tool Set](https://docs.openhands.dev/sdk/guides/task-tool-set)
- **Authors/organization:** OpenHands
- **Date:** Undated living documentation; accessed 23 August 2026
- **Source type:** Official open-source project documentation
- **Evidence quality:** **High** for capability
- **Flags:** No comparative effectiveness evaluation on the page
- **Finding:** A parent can launch a specialized subagent synchronously, persist its conversation, and resume it by task ID. The design explicitly isolates subtask complexity from parent context and supports observable task IDs/status.
- **Scopes supported:** delegation, context isolation, persistence, monitoring, reproducibility inputs

### E13. OpenHands parallel execution

- **Title:** [Parallel Tool Execution](https://docs.openhands.dev/sdk/guides/parallel-tool-execution)
- **Authors/organization:** OpenHands
- **Date:** Undated living documentation; accessed 23 August 2026
- **Source type:** Official open-source project documentation
- **Evidence quality:** **High** for documented capability; **low** for production readiness
- **Flags:** **Experimental**; project warns about races, deadlocks, resource exhaustion, shared state, and same-file writes
- **Finding:** The SDK can run tool calls and subagent delegation concurrently with configurable limits. Its own guidance restricts use to independent operations and discourages ordered or shared-file workflows.
- **Scopes supported:** parallelism, concurrency caps, failure modes, stop/avoid conditions

### E14. OpenHands observability and model layer

- **Title:** [Observability & Tracing](https://docs.openhands.dev/sdk/guides/observability) and [LLM architecture](https://docs.openhands.dev/sdk/arch/llm)
- **Authors/organization:** OpenHands
- **Date:** Undated living documentation; accessed 23 August 2026
- **Source type:** Official open-source project documentation
- **Evidence quality:** **High** for capability
- **Flags:** Some tracing backends are third-party; cost estimates depend on configured provider rates
- **Finding:** OpenHands instruments agent steps, tool executions, LLM calls, and conversation lifecycle through OpenTelemetry, grouping spans by conversation/session. Its provider abstraction tracks token use, cost, latency, errors, and retries across many model providers.
- **Scopes supported:** observability, cost control, model routing, auditability, reproducibility inputs

### E15. OpenHands platform paper

- **Title:** [OpenHands: An Open Platform for AI Software Developers as Generalist Agents](https://arxiv.org/abs/2407.16741)
- **Authors/organization:** Xingyao Wang, Boxuan Li, Yufan Song, Frank F. Xu, Xiangru Tang, Mingchen Zhuge, Jiayi Pan, Yueqi Song, Bowen Li, Jaskirat Singh, Hoang H. Tran, Fuqiang Li, Ren Ma, Mingzhang Zheng, Bill Qian, Yanjun Shao, Niklas Muennighoff, Yizhe Zhang, Binyuan Hui, Junyang Lin, Robert Brennan, Hao Peng, Heng Ji, and Graham Neubig
- **Date:** 23 July 2024; published at ICLR 2025
- **Source type:** Original peer-reviewed platform paper (arXiv full text inspected; OpenReview page was challenge-blocked)
- **Evidence quality:** **Medium** for software-engineering performance; **high** for described architecture
- **Flags:** The evaluation emphasizes individual agent implementations; it does not isolate the causal benefit of multi-agent delegation
- **Finding:** The platform combines a Docker sandbox, event stream, tools, delegation, evaluation harness, and cost/state tracking. Its reported SWE-bench result establishes that an OpenHands agent can perform repository repair, not that multiple agents outperform one.
- **Scopes supported:** open platform, sandbox, event/state architecture, evaluation, causal limitation

### E16. AutoGen and current maintenance status

- **Title:** [AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation](https://www.microsoft.com/en-us/research/publication/autogen-enabling-next-gen-llm-applications-via-multi-agent-conversation-framework/) and [microsoft/autogen](https://github.com/microsoft/autogen)
- **Authors/organization:** Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu, Beibin Li, Erkang Zhu, Li Jiang, Xiaoyun Zhang, Shaokun Zhang, Ahmed Awadallah, Ryen W. White, Doug Burger, and Chi Wang; Microsoft Research
- **Date:** August 2024 (COLM paper); repository status accessed 23 August 2026
- **Source type:** Original peer-reviewed framework paper plus official repository
- **Evidence quality:** **Medium** for pilot effectiveness; **high** for architecture and maintenance status
- **Flags:** Original experiments span heterogeneous pilot tasks rather than current production software engineering; repository is now in maintenance mode
- **Finding:** AutoGen formalized customizable conversable agents and programmable multi-agent interaction patterns. The current official repository says no new features are planned and directs new users to Microsoft Agent Framework.
- **Scopes supported:** orchestration patterns, message passing, framework lifecycle, platform selection

### E17. Microsoft Agent Framework

- **Title:** [Microsoft Agent Framework overview](https://learn.microsoft.com/en-us/agent-framework/overview/)
- **Authors/organization:** Microsoft
- **Date:** Last updated 10 August 2026; accessed 23 August 2026
- **Source type:** Official open-source framework documentation
- **Evidence quality:** **High** for capability; **low** for effectiveness
- **Flags:** Vendor-authored; users remain responsible for permissions, safety, evaluation, and third-party data flows
- **Finding:** The AutoGen/Semantic Kernel successor offers explicit graph workflows, session state, type safety, middleware, telemetry, multi-provider support, and human-in-the-loop control. Its documentation advises functions for deterministic tasks and workflows when multiple agents/functions need explicit coordination.
- **Scopes supported:** explicit orchestration, state, telemetry, governance, platform lifecycle

### E18. MetaGPT

- **Title:** [MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework](https://arxiv.org/abs/2308.00352) and [FoundationAgents/MetaGPT](https://github.com/FoundationAgents/MetaGPT)
- **Authors/organization:** Sirui Hong, Mingchen Zhuge, Jiaqi Chen/Jonathan Chen, Xiawu Zheng, Yuheng Cheng, Ceyao Zhang, Jinlin Wang, Zili Wang, Steven Ka Shing Yau, Zijuan Lin, Liyang Zhou, Chenyu Ran, Lingfeng Xiao, Chenglin Wu, and Jürgen Schmidhuber; FoundationAgents
- **Date:** 1 August 2023 preprint; ICLR 2024 publication; repository accessed 23 August 2026
- **Source type:** Original peer-reviewed research system plus official repository
- **Evidence quality:** **Medium** for the SOP/role architecture; **low–medium** for general software-engineering effectiveness
- **Flags:** OpenReview full page was inaccessible behind a challenge; arXiv abstract and official repository were inspected, so no uninspected detailed result is used here
- **Finding:** MetaGPT encodes software-company roles and standardized operating procedures into an assembly-line workflow. It is evidence that an explicit role/SOP topology is implementable, not current proof that role simulation beats simpler agent loops on repository work.
- **Scopes supported:** role specialization, SOPs, staged artifacts, evidence limitation

### E19. ChatDev

- **Title:** [ChatDev: Communicative Agents for Software Development](https://aclanthology.org/2024.acl-long.810/)
- **Authors/organization:** Chen Qian, Wei Liu, Hongzhang Liu, Nuo Chen, Yufan Dang, Jiahao Li, Cheng Yang, Weize Chen, Yusheng Su, Xin Cong, Juyuan Xu, Dahai Li, Zhiyuan Liu, and Maosong Sun
- **Date:** August 2024
- **Source type:** Peer-reviewed ACL long paper; full PDF inspected
- **Evidence quality:** **Medium** for its evaluated prototype tasks; **low** for contemporary repository-scale generalization
- **Flags:** Used ChatGPT-3.5; bespoke completeness/executability/embedding metrics; authors state complex real-world suitability is limited; substantially higher time/token use than the single-agent baseline
- **Finding:** On the authors' software-generation dataset, ChatDev reported executability 0.88 versus 0.358 for GPT-Engineer and 0.415 for MetaGPT, while taking about 148 seconds and 22,949 tokens versus 15.6 seconds and 7,183 tokens for GPT-Engineer. The paper cautions that agents produced simple, low-information-density logic and were better suited to prototypes than complex real systems.
- **Scopes supported:** staged dialogue, roles, measured benefit, cost/latency, threats to validity

## Handoff notes for synthesis

- Treat **E1–E14 and E17** as evidence that controls and workflow primitives exist, not as proof that teams improve software outcomes.
- Treat **E15, E16, E18, and E19** as architecture/prototype evidence with limited causal or contemporary validity. E19 supplies the clearest within-paper single-versus-multi comparison in this memo, but its older model, custom metrics, and toy/project-generation setting preclude universal recommendations.
- The main platform-independent inference is: **fan out only independent, testable work; isolate writers; centralize integration; bound permissions and concurrency; and retain audit artifacts.**

**Source count:** 22 unique primary-source URLs across 19 annotated entries (three entries intentionally pair an original paper with its directly related official repository/documentation).
