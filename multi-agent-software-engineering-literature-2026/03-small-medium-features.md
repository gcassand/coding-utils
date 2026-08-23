# Small and Medium Feature Practice

## Scope, cutoff, and search method

This memo covers bug fixes, refactors, tests, localized features, and bounded API/UI work. It treats “small” as a change with one dominant implementation path and little independent work, and “medium” as a repository change with several separable phases or components but a bounded integration surface. These are operational categories, not categories consistently used in the literature.

The requested cutoff, **31 August 2026**, is in the future. The actual search cutoff is **23 August 2026 (Europe/Paris)**; no claim is made about work published from 24–31 August 2026. Searches combined terms for multi-agent coding, issue resolution, task decomposition, parallelism, bug repair, testing, refactoring, repository benchmarks, developer productivity, and worktrees. Sources were retained only when full text or detailed first-party methods/results were available. Preference order was peer-reviewed primary research, primary benchmark artifacts, preprints with inspectable methods/data, then official product documentation. Search-result snippets and secondary summaries were not used as evidence.

Evidence quality means: **high** = peer-reviewed or controlled primary evidence with clear methods; **medium** = strong primary evidence with material scope/recency or review-status limits; **low** = small/preliminary study or vendor practice documentation without controlled outcome evidence.

## Executive memo (under 1,200 words)

### Evidence

The evidence does **not** support “more agents” as a default for small changes. A peer-reviewed counterexample is **Agentless**, a fixed localization → repair → validation pipeline that deliberately removes autonomous tool planning. It resolved 32.67% (98/300) of SWE-bench Lite at a reported average cost of $0.68, outperforming the open-source agent systems compared at publication time ([Xia et al., 2025](https://doi.org/10.1145/3715754)). This does not prove that one modern coding agent always wins, but it does show that orchestration complexity is unnecessary for many bounded repository issues.

The best multi-agent results for this scope come from **functional specialization**, not unconstrained swarms. MAGIS assigns manager, repository-custodian, developer, and QA roles; on SWE-bench Lite its full configuration resolved 25.33%, versus 23.33% without QA, while the original SWE-bench experiment reported 13.94% ([Tao et al., 2024](https://proceedings.neurips.cc/paper_files/paper/2024/file/5d1f02132ef51602adf07000ca5b6138-Paper-Conference.pdf)). MASAI similarly passes typed artifacts through test-template, issue-reproduction, localization, fixing, and ranking stages, reaching 28.33% on 300 predominantly bug-fix issues at $1.96 per issue ([Arora et al., 2024](https://arxiv.org/pdf/2406.11638)). MASAI’s ranking with generated tests achieved 28.33%, compared with 23.33% for LLM ranking without a test and 22.28% for random selection. These studies support staged handoffs and executable validation; they do not isolate “agent count” from better prompts, search, sampling, or tools.

Direct evidence about parallel implementation is newer and weaker. The Co-Coder preprint compared sequential, file-per-agent, Claude Code Agent Teams, and dependency-aware partitioning on 28 Python repository-generation tasks. On compact DevEval projects (reference implementations average 3.1 files/243 LOC), Co-Coder raised average test pass rate from 56.8% sequential to 68.1%, with 1.81× wall-clock speedup and 28% lower API cost; on simple projects where a single agent already succeeded, all approaches were comparable ([Yang et al., 2026](https://arxiv.org/abs/2606.00953)). Its gain came from keeping cohesive files together and scheduling around dependencies, not one worker per file. Because this is a small, Python-only preprint and generation task rather than maintenance work, it is emerging evidence, not a universal rule.

Static decomposition can itself be worse than a monolith. Across ten runs on each of two workloads, a 2026 workshop preprint found static decomposition increased retry tokens from 703 to 933 for multi-file debugging and from 904±17 to 1,632±145 for Kubernetes root-cause analysis. Executable control flow with schema validation and selective subtask retry reduced those figures to 460 and 436±132 respectively ([Asthana et al., 2026](https://arxiv.org/abs/2605.15425)). The sample is tiny, but it directly identifies a coordination mechanism: decomposition only helps when failures can be localized and retried locally.

Input quality and executable environments are first-order constraints. In a 2026 preprint using 441 SWE-bench Verified bug reports, three models, and three runs per issue, localization cues and natural-language fix suggestions were associated with higher success odds (OR 1.52 for line cues and 2.01 for natural-language suggestions). Removing both localization and suggestions reduced success odds to 0.60 and increased attempt cost by 9–38%, depending on model ([Bruno et al., 2026](https://arxiv.org/pdf/2607.09553)). Separately, the peer-reviewed GitTaskBench found the best tested agent/framework combination solved 48.15% of 54 repository-based tasks, with more than half of failures attributed to environment setup and dependency resolution ([Ni et al., 2026](https://doi.org/10.1609/aaai.v40i38.40533)).

Benchmark scores should not be read as field productivity. SWE-bench Verified contains 196 tasks estimated below 15 minutes and only 45 above one hour, and is Python-only ([OpenAI/SWE-bench authors, 2024](https://openai.com/index/introducing-swe-bench-verified/)). OpenAI’s later audit found material test/specification problems in 59.4% of 138 frequently failed tasks and evidence of training contamination ([OpenAI, 2026](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/)). In the strongest field counterpoint, a randomized trial of 16 experienced maintainers completing 246 real tasks found early-2025 AI access increased completion time by 19% ([Becker et al., 2025](https://metr.org/Early_2025_AI_Experienced_OS_Devs_Study-paper.pdf)). METR’s 2026 follow-up produced raw speedup estimates but explicitly judged them unreliable because of participant/task selection and difficulty measuring concurrent-agent time ([Becker et al., 2026](https://metr.org/blog/2026-02-24-uplift-update/)). Neither field study isolates multi-agent use; together they warn against projecting benchmark throughput onto expert maintenance work.

### Bounded inference for practice

- **Small fixes, localized refactors, and one-file tests:** default to **one implementation agent** with a fixed reproduce/localize/edit/test loop. Add a second agent only for read-only competing diagnosis or independent review when uncertainty or risk is high. This is consistent with Agentless and with Anthropic’s own low-quality but explicit guidance that the main conversation suits quick targeted changes and that teams add token/coordination overhead ([Anthropic, undated](https://code.claude.com/docs/en/agent-teams)).
- **Medium features or bounded API/UI changes:** use **one coordinator plus one or two focused workers** only when the work has sparse, testable boundaries—for example, implementation versus black-box tests, or backend versus UI behind a frozen contract. Prefer a hub-and-spoke or staged pipeline over free peer-to-peer conversation. Require structured handoff artifacts: affected symbols, contract, patch/diff, reproduction command, and test evidence.
- **Parallelize uncertainty before writes:** competing root-cause hypotheses, repository search, test-plan generation, and review lenses are safer fan-out targets than overlapping edits. Reunite at a single decision owner before implementation.
- **Do not split by file count alone.** Keep coupled files and shared types with one owner; isolate branches/worktrees only for genuinely independent write sets. Stop parallel work when workers need repeated cross-context clarification, touch the same central file, cannot establish a clean baseline, or selective tests cannot distinguish success.

No controlled field study found here directly compares one versus multiple current coding agents by small/medium task size. The recommendations above are therefore a synthesis of repository benchmarks and operational evidence, not a measured staffing law.

## Actionable findings

| Scenario | Primary evidence | Evidence-backed action | Evidence / inference | Quality |
|---|---|---|---|---|
| One localized bug or small refactor | Agentless beat more complex open-source systems on SWE-bench Lite with a fixed three-stage pipeline ([Xia et al.](https://doi.org/10.1145/3715754)) | Start with one agent and explicit localization, minimal repair, and validation stages | Evidence supports the staged baseline; “one agent” is bounded inference because Agentless is not a modern interactive single-agent comparison | High |
| Ambiguous bug with several plausible causes | Vendor documentation recommends teams for competing hypotheses but warns against sequential/high-dependency tasks ([Anthropic](https://code.claude.com/docs/en/agent-teams)) | Fan out read-only diagnoses; appoint one owner to select a hypothesis and write the patch | Emerging vendor practice, not controlled outcome evidence | Low |
| Medium issue with distinct test/localize/fix work | MASAI’s typed pipeline reached 28.33%; test-informed ranking beat ranking without tests ([Arora et al.](https://arxiv.org/pdf/2406.11638)) | Delegate by function and pass compact, structured outputs; make tests an independent gate | Evidence for architecture; exact worker count is inference | Medium |
| Medium issue needing independent review | MAGIS gained 2 percentage points on Lite with QA and 1.57–3.31 points in reported ablations ([Tao et al.](https://proceedings.neurips.cc/paper_files/paper/2024/file/5d1f02132ef51602adf07000ca5b6138-Paper-Conference.pdf)) | Use a reviewer only when it checks the patch against issue-specific criteria/tests | Evidence for this scaffold and benchmark only | High |
| Parallel implementation across modules | Co-Coder outperformed sequential and naive file-parallel baselines on 28 tasks; simple tasks showed no clear advantage ([Yang et al.](https://arxiv.org/abs/2606.00953)) | Partition on dependency cohesion and contracts, never mechanically one agent per file | Direct but small, preprint-only evidence | Medium |
| Workflow with flaky/expensive stages | Static decomposition increased retry cost; selective subtask retry reduced it in two small workloads ([Asthana et al.](https://arxiv.org/abs/2605.15425)) | Give each stage a schema, validation check, retry budget, and stop state | Preliminary direct evidence | Low |
| Underspecified bug ticket | Removing both localization and repair suggestions cut success odds and increased cost ([Bruno et al.](https://arxiv.org/pdf/2607.09553)) | Before delegation, record likely area, expected invariant, and candidate repair direction when known | Direct preprint evidence; do not invent a suggested fix | Medium |
| Environment cannot build/test cleanly | More than half of GitTaskBench failures involved setup/dependencies ([Ni et al.](https://doi.org/10.1609/aaai.v40i38.40533)) | Establish a reproducible baseline before fan-out; stop if no reliable oracle exists | Direct general agent evidence, not multi-agent-specific | High |
| Expert maintainer already knows the code | Early-2025 RCT measured a 19% slowdown with AI access ([Becker et al.](https://metr.org/Early_2025_AI_Experienced_OS_Devs_Study-paper.pdf)) | Require a time-boxed trial and compare elapsed/review time against manual work | Direct field evidence for older tools; multi-agent extension is inference | High |
| Same-file or tightly coupled change | Anthropic warns teams add tokens/coordination and recommends single sessions for same-file or dependency-heavy work ([Anthropic](https://code.claude.com/docs/en/agent-teams)) | Keep a single write owner; use other agents only for review or tests | Vendor-sponsored practice claim | Low |

## Annotated bibliography

### 1. Demystifying LLM-Based Software Engineering Agents

- **Authors / organization:** Chunqiu Steven Xia, Yinlin Deng, Soren Dunn, Lingming Zhang; University of Illinois Urbana-Champaign
- **Publication date:** July 2025
- **URL:** https://doi.org/10.1145/3715754
- **Source type:** Peer-reviewed FSE 2025 research article; primary experiment
- **Evidence quality:** **High**
- **Flags:** Final paper is open access; benchmark is public, Python-only, and later shown to have validity/contamination limitations. “Agentless” is a fixed multi-call pipeline, not a human working without AI.
- **Finding:** A simple localization–repair–validation system resolved 32.67% (98/300) of SWE-bench Lite at a reported $0.68 average cost, outperforming compared open-source agent systems at publication. It is strong evidence that orchestration complexity is not itself necessary for bounded issue resolution.

### 2. MAGIS: LLM-Based Multi-Agent Framework for GitHub Issue ReSolution

- **Authors / organization:** Wei Tao, Yucheng Zhou, Yanlin Wang, Wenqiang Zhang, Hongyu Zhang, Yu Cheng; Fudan University, University of Macau, Sun Yat-sen University, Chongqing University, Chinese University of Hong Kong
- **Publication date:** December 2024
- **URL:** https://proceedings.neurips.cc/paper_files/paper/2024/file/5d1f02132ef51602adf07000ca5b6138-Paper-Conference.pdf
- **Source type:** Peer-reviewed NeurIPS 2024 paper; primary benchmark experiment and ablations
- **Evidence quality:** **High**
- **Flags:** Uses older GPT-4-era models and SWE-bench; architecture improvements are confounded with prompting, retrieval, hints, and workflow changes.
- **Finding:** The manager/custodian/developer/QA architecture reported 13.94% on its original SWE-bench evaluation and 25.33% on Lite in supplementary comparison. Removing QA reduced Lite performance to 23.33%; review gains were modest and benchmark-specific.

### 3. MASAI: Modular Architecture for Software-Engineering AI Agents

- **Authors / organization:** Daman Arora, Atharv Sonwane, Nalin Wadhwa, Abhav Mehrotra, Saiteja Utpala, Ramakrishna B. Bairi, Aditya Kanade, Nagarajan Natarajan; Microsoft Research India and collaborators
- **Publication date:** December 2024
- **URL:** https://arxiv.org/pdf/2406.11638
- **Source type:** NeurIPS 2024 workshop paper / preprint; primary benchmark experiment
- **Evidence quality:** **Medium**
- **Flags:** Workshop publication; one benchmark, all subagents use GPT-4o, no fixed-model agent-count ablation, $1.96 average issue cost.
- **Finding:** Five typed subagents—test template, reproducer, localizer, fixer, ranker—resolved 28.33% of 300 predominantly bug-fix issues. Generated-test-informed ranking achieved 28.33%, versus 23.33% without test evidence and 22.28% random ranking.

### 4. When Parallelism Pays Off: Cohesion-Aware Task Partitioning for Multi-Agent Coding

- **Authors / organization:** Xu Yang, Lunyiu Nie, Ethan Chandra, Stanislav Gannutin, Fangru Lin, Swarat Chaudhuri; University of Texas at Austin and University of Oxford
- **Publication date:** 31 May 2026
- **URL:** https://arxiv.org/abs/2606.00953
- **Source type:** Preprint with released code; comparative repository-generation experiments
- **Evidence quality:** **Medium**
- **Flags:** **Preprint-only**; 28 Python tasks, three runs each; generation rather than maintenance; authors’ own system; external replication not found.
- **Finding:** Dependency-cohesive partitions improved pass rate, latency, and cost over sequential and naive parallel baselines, including 56.8%→68.1%, 1.81× speedup, and 28% cost reduction on DevEval. On simple projects already solved sequentially, approaches were comparable.

### 5. Runtime-Structured Task Decomposition for Agentic Coding Systems

- **Authors / organization:** Shubhi Asthana, Bing Zhang, Chad DeLuca, Hima Patel, Ruchi Mahindru
- **Publication date:** 14 May 2026
- **URL:** https://arxiv.org/abs/2605.15425
- **Source type:** Preprint presented at an ACM AI and Agentic Systems workshop; controlled configuration comparison
- **Evidence quality:** **Low**
- **Flags:** **Preprint-only**, two workloads and ten runs per configuration; limited external validity.
- **Finding:** Static decomposition increased retry-token cost relative to monolithic execution, while executable branching, schema validation, and selective retry reduced retry cost below both. It supports localized failure recovery, not decomposition by itself.

### 6. Writing Bug Reports for Software Repair Agents: What Information Matters Most?

- **Authors / organization:** Vincenzo Luigi Bruno, Alessandro Giagnorio, Daniele Bifolco, Leon Wienges, Massimiliano Di Penta, Gabriele Bavota; USI and University of Sannio
- **Publication date:** 10 July 2026
- **URL:** https://arxiv.org/pdf/2607.09553
- **Source type:** Preprint; observational mixed-effects analysis plus controlled text ablation
- **Evidence quality:** **Medium**
- **Flags:** **Preprint-only**; one scaffold, three models, 11 Python repositories; observational associations are not causal and the 65-issue ablation is modest.
- **Finding:** Across 3,969 runs, line localization (OR 1.52) and natural-language repair suggestions (OR 2.01) were positively associated with success. Removing both cues reduced pooled success odds to 0.60 and increased per-attempt cost 9–38%.

### 7. GitTaskBench: A Benchmark for Code Agents Solving Real-World Tasks Through Code Repository Leveraging

- **Authors / organization:** Ziyi Ni, Huacan Wang, Shuo Zhang, Shuo Lu, Ziyang He, WangYou, Zhenheng Tang, Sen Hu, Bo Li, Chen Hu, Binxing Jiao, Daxin Jiang, Yuntao Du, Pin Lyu; academic and industry collaboration
- **Publication date:** 14 March 2026
- **URL:** https://doi.org/10.1609/aaai.v40i38.40533
- **Source type:** Peer-reviewed AAAI 2026 benchmark paper; primary experiments
- **Evidence quality:** **High**
- **Flags:** Only 54 tasks; comparison is across general agent frameworks, not agent counts.
- **Finding:** The best tested combination solved 48.15% of tasks; more than half of failures were attributed to environment setup and dependency resolution. Reliable execution infrastructure is therefore a prerequisite to evaluating or parallelizing coding work.

### 8. Introducing SWE-bench Verified

- **Authors / organization:** Neil Chowdhury, James Aung, Chan Jun Shern, Oliver Jaffe, Dane Sherburn, Giulio Starace, Evan Mays, Rachel Dias, Marwan Aljubeh, Mia Glaese, Carlos E. Jimenez, John Yang, Leyton Ho, Tejal Patwardhan, Kevin Liu, Aleksander Madry; OpenAI and SWE-bench collaborators
- **Publication date:** 13 August 2024 (page updated 24 February 2025)
- **URL:** https://openai.com/index/introducing-swe-bench-verified/
- **Source type:** Official benchmark construction report; 93-developer annotation campaign
- **Evidence quality:** **Medium**
- **Flags:** **Vendor-sponsored**; subsequent audit found residual validity and contamination problems.
- **Finding:** Three annotators screened each of 1,699 samples to produce 500 verified tasks; 196 were estimated below 15 minutes and 45 above one hour. The benchmark therefore mostly represents small-to-medium Python issue resolution, not large product development.

### 9. Why SWE-bench Verified No Longer Measures Frontier Coding Capabilities

- **Authors / organization:** OpenAI
- **Publication date:** 23 February 2026
- **URL:** https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/
- **Source type:** First-party benchmark audit
- **Evidence quality:** **Medium**
- **Flags:** **Vendor-sponsored**; audit focuses on 138 tasks that a model failed inconsistently, not a random sample of all 500.
- **Finding:** At least 59.4% of the audited tasks had material test/specification problems, and the authors found evidence of training exposure to public solutions. Absolute SWE-bench Verified scores should not be treated as clean field-performance estimates.

### 10. Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity

- **Authors / organization:** Joel Becker, Nate Rush, Beth Barnes, David Rein; METR
- **Publication date:** 10 July 2025
- **URL:** https://metr.org/Early_2025_AI_Experienced_OS_Devs_Study-paper.pdf
- **Source type:** Randomized controlled field trial; primary study
- **Evidence quality:** **High** for its stated setting
- **Flags:** Early-2025 models/tools; 16 developers; AI-allowed treatment was not specifically multi-agent; results should not be generalized to 2026 systems.
- **Finding:** Experienced maintainers completed 246 real tasks in repositories they knew; AI access increased completion time by 19% despite participants perceiving a speedup. It directly demonstrates that prompting, waiting, and review overhead can erase automation gains.

### 11. We Are Changing Our Developer Productivity Experiment Design

- **Authors / organization:** Joel Becker, Nate Rush, Tom Cunningham, David Rein, Khalid Mahamud; METR
- **Publication date:** 24 February 2026
- **URL:** https://metr.org/blog/2026-02-24-uplift-update/
- **Source type:** First-party methods update and preliminary field results
- **Evidence quality:** **Low**
- **Flags:** Authors explicitly label the new signal unreliable because of selection effects, changed compensation, task selection, and concurrent-agent time measurement.
- **Finding:** Raw late-2025 data suggested possible speedups, but developers increasingly declined no-AI tasks and omitted tasks with high expected AI benefit. Concurrent agents also made task-time measurement unreliable, leaving current real-world multi-agent productivity unresolved.

### 12. Orchestrate Teams of Claude Code Sessions

- **Authors / organization:** Anthropic
- **Publication date:** Undated; retrieved 23 August 2026
- **URL:** https://code.claude.com/docs/en/agent-teams
- **Source type:** Official product documentation and vendor practice guidance
- **Evidence quality:** **Low**
- **Flags:** **Vendor-sponsored**; experimental feature; no controlled outcome study supplied.
- **Finding:** Anthropic documents higher token use and coordination overhead, recommending teams for independent research/review, competing debugging hypotheses, separate modules, and cross-layer work, while recommending a single session or subagents for sequential, same-file, or dependency-heavy tasks.
