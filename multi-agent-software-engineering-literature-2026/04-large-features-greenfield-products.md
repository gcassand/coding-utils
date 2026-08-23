# Large Features and Greenfield Products: Evidence Memo

## Scope, cutoff, and search method

**Assigned scope.** Architecture-heavy and cross-cutting features, repository-wide migrations, cross-service work, platform initiatives, and greenfield products; specifically orchestration, interfaces/contracts, decision ownership, integration, review, testing, rollback, and stop conditions.

**Actual search cutoff: 23 August 2026 (Europe/Paris).** The requested cutoff, 31 August 2026, is eight days in the future and therefore cannot be searched or claimed. This memo is current through the actual search date only.

**Method.** Searches covered ACL Anthology, ICLR proceedings/OpenReview, ACM/FSE and Microsoft Research publication records, arXiv, official benchmark sites and repositories, and first-party engineering reports from Anthropic and OpenAI. Searches combined terms for multi-agent software development, project-level generation, full SDLC, repository planning, migrations, code review, worktrees, integration, testing, and greenfield development. Inclusion required accessible full text or a first-party artifact with enough disclosed method to inspect the claim. Search snippets and abstract-only findings were not used as evidence. Vendor cases were retained only when methods, scale, or artifacts were disclosed and are flagged. No controlled study of multi-agent cross-repository/cross-service delivery or production rollback was found.

**Quality rubric.** **High** = peer-reviewed study with executable or public evaluation artifacts and comparatively direct measurement; **medium** = peer-reviewed but narrow/synthetic evaluation, or unusually well-documented first-party case; **low** = preprint, vendor report without controls, subjective metric, or weak external validity.

## Executive memo

The most defensible conclusion is conditional: **multiple coding agents can help with large or greenfield work when the job can be turned into independently verifiable work packets, but agent count is not itself the causal lever.** The recurring enabling variables are explicit intermediate artifacts, dependency-aware planning, isolated execution, and machine-checkable feedback. Evidence for multi-agent superiority on production-scale, cross-service delivery remains weak.

Three peer-reviewed strands support this. First, repository-wide work is a planning and dependency-propagation problem. CodePlan handled changes spanning 2–97 files and made 5/7 repositories pass validity checks, while context-matched non-planning baselines passed none. Although CodePlan is not a multi-agent experiment, it is direct evidence against assigning workers before discovering change dependencies. Second, structured multi-role pipelines can improve prototype generation. MetaGPT, ChatDev, and RTADev use PRDs, designs, plans, code, and tests as handoff artifacts; RTADev's checkpointed alignment and conditional review achieved 63.83% average functional completeness on its 120-task FSD-Bench versus 41.02% for ChatDev, at substantially higher token cost than single-agent systems. Third, full-lifecycle evaluations remain sobering: on DevEval, ordinary second-agent review did not improve GPT-4-Turbo implementation scores, while execution feedback raised acceptance-test pass from 3.0% to 8.9% and unit-test pass from 0% to 4.2%. ProjectEval likewise found very low project-level pass rates; GPT-4o's reported overall Pass@5 average was 12.49%, and OpenHands failed to finish 8 of 20 tasks.

These results shift the design question from “how many agents?” to “what contracts and oracles let work proceed independently?” For a migration, that means a dependency graph, explicit compatibility envelope, ordered change obligations, and build/static-analysis/test oracles. For a greenfield product, it means a versioned product specification, architecture boundaries, API/schema contracts, acceptance tests, and isolated runnable environments before broad parallel implementation. A reviewer that merely rereads the same context is not a reliable gate; reviewers become more useful when given distinct criteria and external evidence such as compiler output, tests, screenshots, logs, metrics, or security scanners.

Two unusually detailed vendor cases show what this can look like at scale, but neither is a controlled trial. Anthropic's 16-agent C-compiler project used per-agent containers, Git task locks, frequent merging, specialist roles, and extensive test oracles; 16 agents stopped helping when all hit the same Linux-kernel failure, and parallelism resumed only after the verifier split the failing surface. The project consumed nearly 2,000 sessions, 2 billion input tokens, 140 million output tokens, and just under $20,000; the resulting 100,000-line compiler remained below expert quality and regressions were frequent. OpenAI reports a million-line greenfield internal beta, about 1,500 merged PRs, and three initial engineers over five months. Its operating system was repository-local plans and decision logs, per-worktree runnable stacks, structural linters, agent-to-agent review, and continuous cleanup; it also reports that manual cleanup initially consumed 20% of the week. Both cases support investment in the harness, not an unconditional claim that more agents accelerate projects.

**Robust findings.** Use executable feedback; discover dependencies before parallelizing; version intermediate decisions; keep work isolated until integration gates pass; and measure functional behavior, not code volume. Tests must include both target behavior and regression preservation: UTBoost found 345 erroneous patches that SWE-bench tests had incorrectly accepted, changing many leaderboard entries.

**Emerging practice, not universal guidance.** A human-owned coordinator with specialist workers, narrow file/service ownership, contract-first handoffs, and independent verifier agents is a plausible default for genuinely separable large work. RTADev supports gated artifact alignment; the Anthropic and OpenAI cases support isolated workspaces and specialist review. No controlled evidence establishes an optimal topology or agent count. A conservative inference is to begin with one planning/architecture agent and two or three independent workers/verifiers, then add workers only when the task graph and oracle expose additional independent queues.

**When not to use multiple agents.** Do not fan out when all workers require the same evolving global context, when the next step depends on one unresolved architecture decision, when changes overlap the same core files, when no acceptance oracle exists, or when integration and review capacity is the bottleneck. Anthropic's own production multi-agent report explicitly notes that most coding tasks have fewer truly parallelizable branches than research and that multi-agent systems used about 15 times the tokens of ordinary chats in its research workload.

**Evidence gap.** No included source measures multi-agent delivery of a real cross-repository or cross-service migration against a single-agent counterfactual, and none validates canary, rollback, incident, or long-term maintainability outcomes. Rollback recommendations below are therefore conservative inferences from isolation and software-release practice, not established multi-agent findings.

## Actionable findings

| Situation | Evidence | Evidence-led action | Status / quality | Important limit |
|---|---|---|---|---|
| Repository-wide migration or refactor | CodePlan passed validity checks on 5/7 repositories spanning 2–97 edited files; matched baselines without planning passed 0/7. | Build a dependency/change-impact plan before assigning implementation slices; order work by dependencies and rerun the correctness oracle after propagation. | Robust for repository-wide edits / **high** | Not a multi-agent comparison; only seven repositories and two task families. |
| Architecture and requirements handoff | MetaGPT and RTADev use structured PRD, architecture, task-plan, code, and test artifacts; RTADev's checkpointed handoffs improved benchmark outcomes. | Make each handoff a versioned, reviewable contract with acceptance criteria; reject or repair it before downstream implementation begins. | Emerging / **medium** | Mostly small generated Python applications, not industrial services. |
| Deciding whether to fan out | In Anthropic's compiler case, 16 agents did not help when every agent encountered the same kernel failure; an oracle-based partition made independent debugging possible. | Fan out only when workers can claim distinct failing tests, components, contracts, or independently checkable milestones. | Case-supported / **medium-low** | One vendor-authored frontier-model stress test; no single-agent control. |
| Choosing agent count | RTADev used five roles; Anthropic used 16 agents at high cost; neither provides a dose-response comparison. | Start with the smallest set that covers independent queues (inference: coordinator plus 2–3 workers/verifiers); scale only after measuring queue contention and integration load. | Inference / **low** | No reliable optimum is known. |
| Decision ownership | RTADev checks each new artifact against earlier certified artifacts; OpenAI reports humans steering goals and agents executing. | Keep one human accountable for product and architecture decisions; agents may propose alternatives, but only an approved decision record becomes shared context. | Triangulated emerging practice / **medium-low** | Human-ownership benefit was not experimentally isolated. |
| Cross-service interfaces | CodePlan's change-impact analysis propagates signature changes to dependants; DevEval failures include file references, parameter use, type handling, and build configuration. | Freeze or version API/schema contracts before parallel implementation; assign compatibility tests to an independent verifier. | Evidence-backed inference / **medium** | Direct cross-service multi-agent trials were not found. |
| Shared context | RTADev's Shared Certified Repository stores approved PRD/design/plan/code; OpenAI uses repository-local indexed docs and versioned execution plans. | Share durable decisions and interfaces, not full transcripts; give workers only the slice plus links to authoritative artifacts. | Emerging / **medium-low** | OpenAI evidence is vendor-authored; RTADev's tasks are synthetic. |
| Branch/worktree integration | Anthropic used per-agent containers and clones plus task locks; OpenAI used a runnable, observable app per worktree. | Use one isolated branch/worktree/environment per implementation slice and integrate through small PRs after local verification. | Case-supported / **medium-low** | Neither case compares this strategy against alternatives. |
| Code review | On DevEval, “Normal-Review” did not improve GPT-4-Turbo implementation (3.0%/0% remained 3.0%/0%); execution feedback improved it to 8.9%/4.2%. | Do not count same-model rereading as a gate. Give reviewers distinct rubrics and executable evidence; require issue-linked findings. | Robust negative within DevEval / **high** | Small 22-repository benchmark and older models. |
| Test gates | ChatDev's ablations made testing important for executability; DevEval and ProjectEval show low end-to-end success; SWE-bench uses fail-to-pass tests in reproducible containers. | Gate each slice on targeted tests, then gate integration on full build, regression, acceptance, and end-to-end tests in a clean environment. | Robust / **high** | Passing existing tests can still accept wrong patches. |
| Test adequacy | UTBoost found 36 SWE-bench instances with insufficient tests and 345 erroneous patches previously labeled passed. | Add independently generated or human-reviewed tests, mutation/adversarial cases, and pass-to-pass regression checks before release. | Robust benchmark audit / **high** | SWE-bench is Python issue resolution, not greenfield products. |
| Rollback | The detailed cases use Git isolation and ephemeral environments but do not report controlled rollback outcomes. | Treat every agent slice as reversible: small commits, migration expand/contract phases, feature flags, and a tested rollback path before merge. | Conservative inference / **low** | No direct multi-agent rollback evidence found. |
| Stop conditions | RTADev bounds review iterations; ProjectEval reports loops and non-completion; Anthropic reports long tests and repeated regressions. | Stop fan-out when workers collide on files, repeat the same failure, lack new oracle signal, exceed cost/time budgets, or increase failing/regression tests. | Evidence-backed inference / **medium-low** | Thresholds must be calibrated locally. |

## Practice synthesis: evidence versus inference

### Orchestration and interfaces

**Evidence.** Structured, artifact-mediated pipelines outperform or ablate better than unstructured role removal in ChatDev, MetaGPT, and RTADev. CodePlan shows that dependencies and prior edits are necessary temporal context for pervasive changes. RTADev also shows that checking every handoff against all prior artifacts can improve functional completeness, while unnecessary all-hands communication increases cost.

**Inference.** For large work, use a hub-and-spoke coordinator over a dependency graph, not peer-to-peer free-for-all. The coordinator owns the plan and integration order; each worker owns a contract-bounded slice. Cross-service changes should use explicit API/schema versions and consumer/contract tests. Architecture alternatives may be explored in parallel, but one human decision owner should select and record the result before implementation fans out.

### Integration, review, and testing

**Evidence.** Isolated clones/worktrees and runnable per-change environments appear in both detailed 2026 vendor cases. DevEval provides a direct negative result for ungrounded dual-role review and a positive result for execution-grounded feedback. CodeAgent reports gains from a specialist QA-checker on code-review datasets, but its metrics are task-specific and do not establish production defect reduction. UTBoost demonstrates that repository tests can be incomplete even when an agent “passes.”

**Inference.** Integrate in dependency order through small PRs, with one integration owner and no shared writable checkout. Require a local clean build and slice tests before review; then contract, integration, end-to-end, performance/security where relevant, and full regression gates. A verifier should not edit the implementation it evaluates unless its proposed fix is reviewed in a new cycle.

### Rollback and release

**Evidence.** None of the included studies evaluates deployment rollback, canary safety, database migration reversal, or incident rate. Git/container/worktree isolation limits pre-merge blast radius but is not a production rollback strategy.

**Inference.** Large migrations should use expand/contract sequencing, backward-compatible interfaces, feature flags or traffic shadowing, small reversible commits, and explicit rollback rehearsals. Multi-agent implementation should stop before irreversible data changes unless a human approves the migration and its recovery plan. These are prudent controls, not claims established by the multi-agent literature.

## Annotated bibliography

### 1. CodePlan: Repository-Level Coding using LLMs and Planning

- **Title / URL:** [CodePlan: Repository-Level Coding using LLMs and Planning](https://doi.org/10.1145/3643757)
- **Authors / organization:** Ramakrishna Bairi, Atharv Sonwane, Aditya Kanade, Vageesh D. C., Arun Iyer, Suresh Parthasarathy, Sriram K. Rajamani, B. Ashok, Shashank Shet; Microsoft Research and collaborators
- **Publication date:** July 2024
- **Evidence type:** Peer-reviewed FSE 2024 paper; repository-level controlled comparison; [public replication package](https://github.com/microsoft/CodePlan)
- **Evidence quality:** **High**
- **Flags:** Small sample (seven repositories); not itself a multi-agent system; replication repository archived read-only in June 2026 but remains accessible.
- **Finding:** A dependency-aware adaptive plan led 5/7 repositories with 2–97 affected files to pass validity checks, while baselines with comparable context but no planning passed 0/7. This directly supports planning edits around dependency propagation for migrations and cross-cutting changes.

### 2. ChatDev: Communicative Agents for Software Development

- **Title / URL:** [ChatDev: Communicative Agents for Software Development](https://aclanthology.org/2024.acl-long.810/)
- **Authors / organization:** Chen Qian, Wei Liu, Hongzhang Liu, Nuo Chen, Yufan Dang, Jiahao Li, Cheng Yang, Weize Chen, Yusheng Su, Xin Cong, Juyuan Xu, Dahai Li, Zhiyuan Liu, Maosong Sun; Tsinghua University/OpenBMB and collaborators
- **Publication date:** August 2024
- **Evidence type:** Peer-reviewed ACL 2024 paper; prototype-generation comparison and ablations
- **Evidence quality:** **Medium**
- **Flags:** Prototype-scale tasks; bespoke quality metrics; authors explicitly say the technology is more suitable for prototypes than complex real applications.
- **Finding:** A sequential design–coding–review–testing chat chain achieved 0.88 executability versus 0.3583 for GPT-Engineer and 0.4145 for MetaGPT in the reported setup; removing roles or testing degraded outcomes. It used more time/tokens than the single-agent baseline, and its evaluation does not establish production readiness.

### 3. MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework

- **Title / URL:** [MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework](https://proceedings.iclr.cc/paper_files/paper/2024/hash/6507b115562bb0a305f1958ccc87355a-Abstract-Conference.html)
- **Authors / organization:** Sirui Hong, Mingchen Zhuge, Jonathan Chen, Xiawu Zheng, Yuheng Cheng, Jinlin Wang, Ceyao Zhang, Zili Wang, Steven Ka Shing Yau, Zijuan Lin, Liyang Zhou, Chenyu Ran, Lingfeng Xiao, Chenglin Wu, Jürgen Schmidhuber; DeepWisdom, KAUST, and collaborators
- **Publication date:** May 2024
- **Evidence type:** Peer-reviewed ICLR 2024 paper; benchmark comparison and ablations
- **Evidence quality:** **Medium**
- **Flags:** SoftwareDev evaluation is small and partly subjective; generated applications are far smaller than industrial products.
- **Finding:** Encoding standard operating procedures and structured PRD/design/task/code artifacts produced more executable prototype software and lower reported human revision cost than ChatDev, but at higher token use. The result supports reviewable handoff artifacts, not a general claim about agent-team scale.

### 4. Prompting Large Language Models to Tackle the Full Software Development Lifecycle: A Case Study

- **Title / URL:** [Prompting Large Language Models to Tackle the Full Software Development Lifecycle: A Case Study](https://aclanthology.org/2025.coling-main.502/)
- **Authors / organization:** Bowen Li, Wenhan Wu, Ziwei Tang, Lin Shi, John Yang, Jinyang Li, Shunyu Yao, Chen Qian, Binyuan Hui, Qicheng Zhang, Zhiyin Yu, He Du, Ping Yang, Dahua Lin, Chao Peng, Kai Chen; Shanghai AI Laboratory, ByteDance, Princeton, and collaborators
- **Publication date:** January 2025
- **Evidence type:** Peer-reviewed COLING 2025 case study; 22 curated repositories, four languages, full-SDLC modular evaluation
- **Evidence quality:** **High**
- **Flags:** Small repository set; GPT-4-Turbo-era models; baseline extends ChatDev rather than testing modern production agent teams.
- **Finding:** GPT-4-Turbo scored only 7.1% acceptance-test and 8.0% unit-test pass on implementation. A second-role normal review did not improve a subset, while execution feedback improved it, showing that grounded feedback is more reliable than conversational review alone.

### 5. RTADev: Intention Aligned Multi-Agent Framework for Software Development

- **Title / URL:** [RTADev: Intention Aligned Multi-Agent Framework for Software Development](https://aclanthology.org/2025.findings-acl.80/)
- **Authors / organization:** Jie Liu, Guohua Wang, Ronghui Yang, Jiajie Zeng, Mengchen Zhao, Yi Cai; South China University of Technology
- **Publication date:** July 2025
- **Evidence type:** Peer-reviewed Findings of ACL 2025 paper; 120-task FSD-Bench comparison and ablation
- **Evidence quality:** **Medium**
- **Flags:** Benchmark is generated/curated rather than industrial; Python websites, desktop apps, and games; GPT-4o-mini base; functional-completeness tests partly LLM-generated.
- **Finding:** Five roles use a Shared Certified Repository, per-artifact alignment checks, and conditional ad hoc reviews. Average functional completeness was 63.83% versus ChatDev's 41.02%; all alignment ablations were worse, but RTADev consumed 70,652.6 tokens per task versus 1,953.23 for direct GPT-4o-mini.

### 6. ProjectEval: A Benchmark for Programming Agents Automated Evaluation on Project-Level Code Generation

- **Title / URL:** [ProjectEval: A Benchmark for Programming Agents Automated Evaluation on Project-Level Code Generation](https://aclanthology.org/2025.findings-acl.1036/)
- **Authors / organization:** Kaiyuan Liu, Youcheng Pan, Yang Xiang, Daojing He, Jing Li, Yexing Du, Tianrun Gao; Harbin Institute of Technology and Pengcheng Laboratory
- **Publication date:** July 2025
- **Evidence type:** Peer-reviewed Findings of ACL 2025 benchmark paper; 20 projects and 284 user-simulation tests
- **Evidence quality:** **Medium**
- **Flags:** Python/Django-heavy, only 20 tasks, LLM-assisted benchmark construction; maintainability, efficiency, and best practices are not measured.
- **Finding:** Project generation remained difficult: GPT-4o had a 12.49% overall average Pass@5 in the reported table, and OpenHands failed to finish 8/20 tasks. Frequent failures included invalid formats, missing essential files, omissions, and loops; code-structure similarity did not reliably predict executable success.

### 7. CodeAgent: Autonomous Communicative Agents for Code Review

- **Title / URL:** [CodeAgent: Autonomous Communicative Agents for Code Review](https://aclanthology.org/2024.emnlp-main.632/)
- **Authors / organization:** Xunzhu Tang, Kisub Kim, Yewei Song, Cedric Lothritz, Bei Li, Saad Ezzini, Haoye Tian, Jacques Klein, Tegawendé F. Bissyandé; University of Luxembourg and collaborators
- **Publication date:** November 2024
- **Evidence type:** Peer-reviewed EMNLP 2024 paper; more than 3,545 real-world commits across review subtasks; ablation of supervisory QA-checker
- **Evidence quality:** **Medium**
- **Flags:** Automated/task-specific metrics do not show production defect or incident reduction; some judging relies on model-based analysis.
- **Finding:** Specialist agents plus a QA-checker improved reported vulnerability, consistency, formatting, and revision metrics over model baselines, and removing the QA-checker reduced vulnerability hit rates. This supports criterion-specific review roles as an emerging pattern, not autonomous merge approval.

### 8. SWE-bench: Can Language Models Resolve Real-World GitHub Issues?

- **Title / URL:** [SWE-bench: Can Language Models Resolve Real-World GitHub Issues?](https://www.swebench.com/original.html)
- **Authors / organization:** Carlos E. Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, Karthik R. Narasimhan; Princeton University
- **Publication date:** May 2024
- **Evidence type:** Peer-reviewed ICLR 2024 benchmark; 2,294 issue/PR instances from 12 Python repositories; reproducible containerized harness
- **Evidence quality:** **High**
- **Flags:** Issue-resolution benchmark, not greenfield or cross-service delivery; Python-only original benchmark.
- **Finding:** Evaluation applies a generated patch in a repository-specific container and runs fail-to-pass tests. It establishes a reproducible minimum integration gate, but later audit evidence shows that the supplied tests are not always sufficient.

### 9. UTBoost: Rigorous Evaluation of Coding Agents on SWE-Bench

- **Title / URL:** [UTBoost: Rigorous Evaluation of Coding Agents on SWE-Bench](https://aclanthology.org/2025.acl-long.189/)
- **Authors / organization:** Boxi Yu, Yuxuan Zhu, Pinjia He, Daniel Kang
- **Publication date:** July 2025
- **Evidence type:** Peer-reviewed ACL 2025 benchmark audit and test augmentation study
- **Evidence quality:** **High**
- **Flags:** Focused on SWE-bench Python patches; generated tests can have their own validity risks.
- **Finding:** The audit identified 36 instances with insufficient tests and 345 erroneous patches previously labeled as passed, affecting 40.9% of SWE-bench Lite and 24.4% of Verified leaderboard entries and changing rankings. Existing green tests are therefore not adequate as the sole integration oracle.

### 10. Building a C Compiler with a Team of Parallel Claudes

- **Title / URL:** [Building a C compiler with a team of parallel Claudes](https://www.anthropic.com/engineering/building-c-compiler)
- **Authors / organization:** Nicholas Carlini; Anthropic
- **Publication date:** 5 February 2026
- **Evidence type:** First-party engineering stress test with public source artifact and disclosed harness/costs
- **Evidence quality:** **Medium-low**
- **Flags:** **Vendor-sponsored**, uncontrolled, one researcher/project, frontier-model capability demonstration; not peer reviewed.
- **Finding:** Sixteen agents in isolated containers used Git task locks and frequent merges to create a 100,000-line compiler over nearly 2,000 sessions for just under $20,000. Parallelism failed when every worker hit the same kernel bug and improved only after an oracle made failures independently searchable; regressions, merge conflicts, and quality limits remained.

### 11. Harness Engineering: Leveraging Codex in an Agent-First World

- **Title / URL:** [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/)
- **Authors / organization:** Ryan Lopopolo; OpenAI
- **Publication date:** 11 February 2026
- **Evidence type:** First-party internal greenfield product case with disclosed scale and practices
- **Evidence quality:** **Medium-low**
- **Flags:** **Vendor-sponsored**, no control group, repository and raw data not public, speed estimate self-reported, longevity unknown.
- **Finding:** OpenAI reports roughly one million agent-written lines and 1,500 merged PRs over five months, initially driven by three engineers. The enabling harness included repository-local plans/decisions, structural lints, per-worktree runnable and observable environments, iterative agent review, and recurring cleanup; manual “AI slop” cleanup initially used 20% of the team's week.

### 12. How We Built Our Multi-Agent Research System

- **Title / URL:** [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- **Authors / organization:** Jeremy Hadfield, Barry Zhang, Kenneth Lien, Florian Scholz, Jeremy Fox, Daniel Ford; Anthropic
- **Publication date:** 13 June 2025
- **Evidence type:** First-party production engineering report with internal evaluations
- **Evidence quality:** **Medium-low**
- **Flags:** **Vendor-sponsored** and about research agents, not coding; internal evaluation details and raw data are unavailable.
- **Finding:** Anthropic reports that its multi-agent research system used about 15 times the tokens of chats and worked best on heavily parallel, high-value tasks. The authors explicitly caution that most coding tasks have fewer independent branches and that current agents coordinate poorly in real time; this is relevant boundary evidence, not direct software-delivery measurement.

### 13. MASAI: Modular Architecture for Software-Engineering AI Agents

- **Title / URL:** [MASAI: Modular Architecture for Software-Engineering AI Agents](https://arxiv.org/abs/2406.11638)
- **Authors / organization:** Daman Arora, Atharv Sonwane, Nalin Wadhwa, Abhav Mehrotra, Saiteja Utpala, Ramakrishna Bairi, Aditya Kanade, Nagarajan Natarajan; Microsoft Research and collaborators
- **Publication date:** 17 June 2024
- **Evidence type:** Full-text preprint; modular subagent architecture evaluated on 300 SWE-bench Lite issues
- **Evidence quality:** **Low-medium**
- **Flags:** **Preprint-only** in the sources verified here; SWE-bench Lite and older model versions; issue repair rather than large-feature delivery.
- **Finding:** Specialized test-template, reproduction, localization, fixing, and ranking modules achieved a reported 28.33% resolution rate, 75% file localization, and more than 95% patch application at under $2 per issue. It supports specialized, bounded subproblems and context isolation, but not broad parallel implementation across services.

## Research gaps for synthesis

1. No controlled single-agent versus multi-agent study on production cross-service or cross-repository features, migrations, or platform programs.
2. No reliable dose-response evidence for 2, 4, 8, or 16 coding agents, nor for model-tier routing by role.
3. No study measuring merge-conflict burden, reviewer load, defect escape, incident rate, rollback success, or long-term maintenance under multi-agent development.
4. Project-generation benchmarks remain small, synthetic, Python-heavy, and weak on non-functional requirements, organizational constraints, and real users.
5. Vendor greenfield cases disclose useful mechanisms but lack counterfactuals, independent audits, and multi-year maintainability data.
6. Test-passing is an incomplete oracle; research is needed on independently authored contract, adversarial, security, performance, migration, and rollback tests.
