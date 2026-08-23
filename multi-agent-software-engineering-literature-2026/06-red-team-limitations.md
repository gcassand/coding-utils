# Critical Review and Red-Team Limitations

## Scope, cutoff, and search method

This memo independently tests the case for multi-agent software development against negative, null, and boundary evidence. It covers coordination tax, duplicated work, false or socially induced consensus, security and permissions, prompt injection, merge and semantic conflicts, benchmark contamination, cost and latency, reproducibility, human oversight, and organizational risk. It does not inspect or rely on the other research memos.

The requested cutoff, **31 August 2026**, is in the future. The actual search cutoff is **23 August 2026 (Europe/Paris)**; no source published after that date is represented. Searches combined title/keyword queries across arXiv, OpenReview, NeurIPS proceedings, ACL Anthology, official benchmark repositories, and official research/engineering sites. Candidate claims were retained only after inspecting full text or a first-party page with disclosed methods. Search terms included combinations of *multi-agent*, *coding agents*, *coordination failure/tax*, *cooperation*, *worktree/merge*, *SWE-bench contamination*, *prompt injection/infection*, *secure code*, *cost*, *latency*, *reproducibility*, *code review*, and *developer productivity*. Secondary summaries and abstract-only claims were excluded from the evidentiary core.

Quality labels mean: **high** = peer-reviewed primary empirical work with disclosed methods/artifacts; **medium** = primary preprint, field experiment, or first-party audit/production study with important scope or independence limits; **low** = relevant first-party observational/vendor evidence that cannot establish the multi-agent claim causally. “High” is never shorthand for universal external validity.

## Executive memo

### Bottom line

The evidence does **not** support “more agents” as a general software-engineering default. It supports a conditional mechanism: parallel agents can add useful compute and independent context only when the work has genuinely separable branches and an explicit integration protocol. On sequential, tool-heavy, context-coupled, or conflict-prone work, coordination can erase the gain or make outcomes worse.

The most direct negative coding result is [CooperBench](https://arxiv.org/pdf/2601.13295) (Khatua et al., 26 January 2026; 652 two-feature tasks): two cooperating agents averaged 30% lower success than a solo agent handling the same workload; GPT-5 and Claude Sonnet 4.5 were roughly 50% lower in the cooperative condition. Work overlap (33.2%) and divergent architecture (29.7%) dominated observed failure symptoms; in a manual root-cause sample of 50 failed traces, expectation, commitment, and communication failures accounted for 42%, 32%, and 26%. Communication reduced raw textual conflicts but had a near-zero to slightly negative effect after merge resolution. This is a preprint and deliberately concentrates compact, overlapping changes, so it is strong evidence of a coordination boundary, not of all multi-agent coding.

A broader controlled [agent-scaling study](https://arxiv.org/pdf/2512.08296) (Kim et al., 8 April 2026; 260 configurations, six benchmarks, equal reasoning-token budgets) found multi-agent changes ranging from +80.8% on decomposable financial analysis to −70% on sequential planning. On its 20-instance SWE-bench Verified subset, every multi-agent topology was worse than the single agent (−2.1% to −14.9%). Aggregate coordination overhead was 58% for independent agents, 263–285% for decentralized/centralized systems, and 515% for hybrid systems; success per 1,000 tokens was 2.8–5.0 times worse than single-agent. However, only capability saturation survived both cluster-robust and multiple-comparison scrutiny; coding cells had typical bootstrap intervals of about ±20 points and used a subsequently discredited benchmark. Treat the exact thresholds and topology rankings as emerging, not robust laws.

Positive long-horizon evidence contains its own warning. [CAID](https://arxiv.org/pdf/2603.21489) (Geng and Neubig, 8 July 2026) improved scores on Commit0-Lite and PaperBench using a central manager, dependency graph, isolated worktrees, branch-and-merge, and executable verification. Yet its multi-agent runs consistently cost more and did not substantially reduce wall-clock time because integration remained sequential and test-gated. Soft isolation fell below the single-agent PaperBench score (55.5 vs. 57.2), while worktree isolation reached 63.3; four engineers beat two on Commit0-Lite, but eight performed worse, and more than two brought little PaperBench gain while cost and runtime rose. The study is a preprint, uses only two benchmarks, and PaperBench partly relies on an LLM judge. It supports disciplined branch-and-merge for specific long tasks—not swarms.

Failure is systemic, not merely a bad prompt. The peer-reviewed [MAST study](https://proceedings.neurips.cc/paper_files/paper/2025/file/b1041e52d3be19f0a9bc491657488e4a-Paper-Datasets_and_Benchmarks_Track.pdf) (Cemri et al., NeurIPS 2025) reports 41–86.7% failure across seven multi-agent systems and derives 14 failure modes from 150 deeply reviewed traces: system design (44.2%), inter-agent misalignment (32.3%), and verification (23.5%). Its scaled 1,642-trace labels use an o1 judge calibrated to human labels (κ=0.77), so prevalence estimates retain judge and sampling dependence. Together with CooperBench, this rejects the idea that role prompts or more conversation alone make collaboration reliable.

“Consensus” is not independent verification. In more than 2,500 debates, the peer-reviewed [group-conformity study](https://aclanthology.org/2025.findings-acl.265/) (Choi et al., July 2025) found neutral agents significantly followed numerical majorities and higher-capability agents; under a two-agent superior majority, conformity reached 83.17%. The domain was contentious-topic debate, not code, so applying this to code review is an inference. Still, it is direct evidence that agreement among related LLM instances is not statistically independent corroboration. Artifact-based tests and genuinely independent review carry more evidential weight than votes or mutually reinforcing prose.

The security boundary worsens with autonomy and communication. Peer-reviewed [AgentDojo](https://proceedings.neurips.cc/paper_files/paper/2024/file/97091a5177d8dc64b1da8bf3e1f6fb54-Paper-Datasets_and_Benchmarks_Track.pdf) (Debenedetti et al., NeurIPS 2024) shows tool-using agents are vulnerable to indirect prompt injection across 97 tasks and 629 security cases. [Prompt Infection](https://arxiv.org/pdf/2410.07283) (Lee and Tiwari, 9 October 2024) demonstrates self-replicating injections spreading between agents, including through local communication and memory. It is preprint-only and uses older models, but the propagation mechanism is specifically multi-agent. [SecureVibeBench](https://arxiv.org/pdf/2509.22097) (Chen et al., 6 June 2026) found the best tested coding-agent/model combination produced only 23.8% solutions that were both correct and secure across 105 C/C++ repository tasks; over half of correct outputs in many combinations remained insecure. More agents are therefore additional principals and trust channels, not a substitute for least privilege or independent security tests.

Benchmark evidence itself is fragile. OpenAI’s [SWE-bench Verified audit](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/) (23 February 2026) found material flaws in 59.4% of 138 audited hard cases and evidence that all tested frontier models had encountered some gold patches or problem details. Its later [SWE-bench Pro audit](https://openai.com/index/separating-signal-from-noise-coding-evaluations/) (8 July 2026) estimated about 30% of the public tasks were broken. Both are first-party vendor audits, but they directly invalidate treating leaderboard deltas as field productivity or product-quality estimates. The TMLR paper [AI Agents That Matter](https://openreview.net/pdf?id=Zy4uFzMviZ) (Kapoor et al., June 2025) independently shows that cost-blind, non-standardized agent evaluations can reward unnecessary complexity and lack reproducibility or adequate holdouts.

Real-work productivity is unsettled. METR’s randomized [early-2025 developer study](https://metr.org/Early_2025_AI_Experienced_OS_Devs_Study-paper.pdf) (Becker et al., 10 July 2025; 16 experienced developers, 246 tasks) found AI access increased completion time by 19% even though developers believed it made them 20% faster. This was not a multi-agent comparison and used early-2025 tools. METR later [withdrew a strong interpretation of its late-2025 follow-up](https://metr.org/blog/2026-02-24-uplift-update/) because selection effects and concurrent-agent time accounting made the signal unreliable. The honest conclusion is uncertainty, not permanent slowdown. Anthropic’s production report says multi-agent research used about 15 times the tokens of chat, explicitly notes most coding tasks have fewer parallel branches, and reports its 90.2% gain only on an internal research evaluation—not coding.

### Evidence/inference boundary

**Evidence:** current systems exhibit coordination deficits, superlinear communication growth, duplicate work, semantic conflicts after clean merges, weak verification, non-monotonic gains with agent count, prompt-injection propagation, insecure code, benchmark contamination, and high cost. These effects recur across independent controlled benchmarks, trace studies, and first-party production disclosures.

**Inference for software-development policy:** make single-agent execution the prior for localized or tightly coupled changes; admit multiple agents only after demonstrating decomposability and measurable value; isolate writes; integrate through one accountable owner; require executable and security-aware gates; and stop scaling when marginal success, wall-clock time, or review burden no longer improves. These are bounded deductions from the evidence, not universally validated operating procedures.

## Actionable findings

| Finding | Evidence | Bounded action / stop condition | Strength |
|---|---|---|---|
| Small fixes and overlapping edits carry high coordination tax. | CooperBench: −30% average cooperative success; 33.2% work overlap and 29.7% divergent architecture. Scaling study: SWE-bench MAS −2.1% to −14.9%. | Start with one agent. Do not add another unless the second task has a non-overlapping artifact or provides independent, artifact-grounded verification. Stop on duplicate edits or changing interface assumptions. | **Medium**, direct but benchmark-bound. |
| Parallelism is non-monotonic. | CAID improved from two to four engineers on Commit0-Lite, then declined at eight; more than two added little on PaperBench while cost/runtime rose. Scaling study finds diminishing returns above moderate team sizes. | Cap initial teams at the smallest count that saturates independent work. Add an agent only if a ready, dependency-free work item exists; stop when queues idle or integration dominates elapsed time. | **Medium**, two preprints with controlled ablations. |
| Shared writable state is unsafe as a coordination mechanism. | CAID soft isolation scored 55.5 on PaperBench versus 57.2 single-agent and 63.3 with worktrees; CooperBench documents silent semantic loss even after conflict-free merges. | Use separate branches/worktrees and a single integration authority. Treat a clean merge as necessary, never sufficient; run combined tests after every integration. | **Medium**, direct SWE experiments. |
| Conversation is not a state store or a verifier. | CooperBench communication had −0.5 point average final effect after merge resolution; MAST identifies ignored input, withholding, repetition, history loss, and incorrect/incomplete verification. | Encode ownership, interfaces, dependencies, completion evidence, and current commit IDs in checkable artifacts. Stop a handoff that lacks a diff/commit and test evidence. | **High-to-medium**, peer-reviewed trace taxonomy plus direct coding preprint. |
| Agent agreement can be correlated error. | Choi et al. found statistically significant majority/capability conformity across 2,500+ debates; MAST found verifier failures material. | Preserve independent first-pass analysis and adjudicate against tests/specifications. Do not accept majority vote or fluent consensus as a review gate. | **Medium**; conformity-to-code transfer is explicitly an inference. |
| Permissions and communication multiply attack paths. | AgentDojo establishes indirect-injection risk in tool agents; Prompt Infection shows cross-agent propagation; RepoGuardBench finds repository comments/rule files can redirect coding agents. | Give each worker only the files, commands, credentials, and network access required for its task. Treat repository text, issue text, tool output, memory, and agent messages as untrusted; stop on instructions that expand scope or request secrets. | **High** for tool-agent injection; **medium/low** for coding-specific and propagation generality. |
| Functional tests do not establish security. | SecureVibeBench’s best combination reached 23.8% correct-and-secure; many functionally correct solutions remained vulnerable. | Add independent security oracles for security-relevant changes and retain human approval for privileged/deployment actions. Stop if only functional tests exist for a security-sensitive diff. | **Medium**, direct repository preprint, C/C++ only. |
| Automated review does not replace accountable review. | Zhong et al.: AI review suggestions were adopted 16.6% vs. 56.5% for humans; over half of unadopted AI suggestions were incorrect or fixed differently. | Use reviewer agents for triage, not sole approval, when architectural intent, testing adequacy, security, or operational impact is material. | **Medium/low**, large observational preprint with confounding. |
| Reported success must include cost, latency, and variance. | Anthropic: multi-agent research ≈15× chat tokens. Scaling study: 2.8–5× worse success/token. CAID: higher API cost and little wall-clock reduction. Kapoor et al.: agent results often lack standardized cost and error bars. | Predefine a budget and compare against the same-model single-agent baseline on success, wall-clock, dollars/tokens, regressions, and human review time. Stop at budget or negative marginal value. | **High-to-medium** across peer review, preprints, and vendor production data. |
| Public benchmark deltas are not product evidence. | OpenAI audits find 59.4% issues in a difficult SWE-bench Verified subset and ≈30% broken SWE-bench Pro public tasks, plus contamination evidence. | Require private, time-split, repository-representative evaluations and human audit of a failure/pass sample before rollout. Do not use a leaderboard delta alone to justify agent count. | **Medium**, first-party audits with disclosed method; vendor interest flagged. |
| Team-level delivery can worsen while local output feels faster. | METR’s RCT found 19% slowdown despite perceived 20% speedup; DORA associates higher AI use with reduced throughput/stability and larger batches. | Measure lead time, escaped defects, rollback/rework, and review queues rather than lines or task counts. Stop expansion if batch size or downstream review load rises without delivered-value improvement. | **Medium/low**; neither study isolates multi-agent use and DORA is correlational. |

## Threats to validity and unresolved contradictions

- **Rapid model drift:** 2024–early-2026 results may age quickly. METR’s failed follow-up shows that changing adoption also changes who and what can be measured.
- **Benchmark mismatch:** CooperBench intentionally creates overlapping compact features; CAID targets long-horizon greenfield/reproduction work. Their opposite results are compatible with task-structure dependence, not proof that one architecture wins generally.
- **Contaminated or broken coding benchmarks:** the scaling paper’s software result uses only 20 SWE-bench Verified instances, a benchmark OpenAI later deemed unsuitable. Its reported cell confidence intervals are wide.
- **Unequal notions of compute:** equal token/iteration budgets, equal dollars, equal wall-clock time, and equal human attention answer different questions. Some “multi-agent gains” are simply more inference.
- **LLM judges:** PaperBench, MAST’s scaled annotations, CooperBench symptom coding, and the review study use LLM-assisted evaluation. Human calibration helps but does not remove correlated-model bias.
- **Publication and sponsorship:** CooperBench, CAID, Prompt Infection, SecureVibeBench, the code-review and oversight studies, METR’s RCT, and the scaling paper are preprints or non-journal first-party reports. CAID discloses Fujitsu support; Anthropic/OpenAI/DORA report on ecosystems in which they have commercial interests.
- **Security transfer:** AgentDojo is not a coding benchmark; SecureVibeBench is C/C++-specific; RepoGuardBench uses mostly small open-weight models and inert payloads. They establish attack mechanisms and boundary failures, not precise production incident rates.
- **Missing organizational experiments:** no included study randomizes software teams to one versus multiple coding agents and measures months-long delivery, maintainability, incidents, and ownership. No robust evidence fixes an optimal agent count for “small,” “medium,” “large,” or “greenfield” categories.

## Annotated bibliography

### 1. CooperBench

- **Title:** *CooperBench: Why Coding Agents Cannot Be Your Teammates Yet*
- **Authors/organization:** Arpandeep Khatua, Hao Zhu, Peter Tran, Arya Prabhudesai, Frederic Sadrieh, Johann K. Lieberwirth, Xinkai Yu, Yicheng Fu, Michael J. Ryan, Jiaxin Pei, Diyi Yang; Stanford University and SAP Labs US
- **Date:** 26 January 2026 (arXiv v2)
- **URL:** https://arxiv.org/pdf/2601.13295
- **Source type:** Primary controlled repository benchmark; open code/data; preprint
- **Evidence quality:** **Medium**
- **Scopes supported:** Small/medium features; coordination tax; duplicate work; merge/semantic conflicts; communication failure
- **Flags:** Preprint-only as of cutoff; intentionally compact and conflict-prone tasks; one OpenHands-derived cooperative scaffold; LLM-assisted symptom labeling (96% agreement on 50 human checks).
- **Finding:** Across 652 task pairs in 12 repositories/four languages, cooperative agents averaged 30% lower success than one agent doing both features. Communication reduced raw merge conflicts but did not improve final success after resolution; clean merges could still erase functionality.

### 2. Agent-system scaling

- **Title:** *Towards a Science of Scaling Agent Systems*
- **Authors/organization:** Yubin Kim, Ken Gu, Chanwoo Park, Chunjong Park, Samuel Schmidgall, A. Ali Heydari, Yao Yan, Zhihan Zhang, Yuchen Zhuang, Yun Liu, Mark Malhotra, Paul Pu Liang, Hae Won Park, Yuzhe Yang, Xuhai Xu, Yilun Du, Shwetak Patel, Tim Althoff, Daniel McDuff, Xin Liu; Google Research, Google DeepMind, MIT
- **Date:** 8 April 2026 (arXiv v3)
- **URL:** https://arxiv.org/pdf/2512.08296
- **Source type:** Primary controlled cross-benchmark experiment; preprint
- **Evidence quality:** **Medium**
- **Scopes supported:** Agent count; topology; cost/latency; task decomposability; error propagation; coding benchmark result
- **Flags:** Preprint; only 20 SWE-bench Verified tasks per cell with ≈±20-point typical CIs; benchmark later found contaminated/flawed; several effects lose cluster-robust significance.
- **Finding:** Across 260 configurations with matched reasoning-token budgets, multi-agent performance ranged from +80.8% to −70% by task. Coordination turns grew superlinearly; independent systems had 17.2× trace-level error amplification versus 4.4× centralized, but capability saturation was the only result robust to both key statistical corrections.

### 3. CAID

- **Title:** *Effective Strategies for Asynchronous Software Engineering Agents*
- **Authors/organization:** Jiayi Geng and Graham Neubig; Carnegie Mellon University
- **Date:** 8 July 2026 (arXiv v2)
- **URL:** https://arxiv.org/pdf/2603.21489
- **Source type:** Primary repository-level experiment with ablations and open implementation; preprint
- **Evidence quality:** **Medium**
- **Scopes supported:** Large features/greenfield; worktrees; branch/merge; dependency-aware delegation; cost, latency, conflicts
- **Flags:** Preprint; two benchmarks; PaperBench uses a model judge and Code-Dev protocol; Fujitsu-supported; model/API prices and capabilities can drift.
- **Finding:** Centralized, isolated branch-and-merge improved Commit0-Lite and PaperBench scores, while soft shared-workspace isolation could underperform a single agent. Gains were non-monotonic with engineer count; API cost rose and wall-clock time was not substantially reduced because integration stayed sequential.

### 4. MAST failure taxonomy

- **Title:** *Why Do Multi-Agent LLM Systems Fail?*
- **Authors/organization:** Mert Cemri, Melissa Z. Pan, Shuyi Yang, Lakshya A. Agrawal, Bhavya Chopra, Rishabh Tiwari, Kurt Keutzer, Aditya Parameswaran, Dan Klein, Kannan Ramchandran, Matei Zaharia, Joseph E. Gonzalez, Ion Stoica; UC Berkeley and Intesa Sanpaolo
- **Date:** 2025
- **URL:** https://proceedings.neurips.cc/paper_files/paper/2025/file/b1041e52d3be19f0a9bc491657488e4a-Paper-Datasets_and_Benchmarks_Track.pdf
- **Source type:** Peer-reviewed NeurIPS 2025 Datasets and Benchmarks paper; trace study and open dataset
- **Evidence quality:** **High**
- **Scopes supported:** System design, inter-agent misalignment, verification, termination, reproducibility
- **Flags:** Taxonomy was grounded in 150 deeply reviewed traces; most of the 1,642-trace dataset was labeled by an o1 judge (κ=0.77 to human labels); diverse tasks but not exclusively coding.
- **Finding:** Seven systems showed 41–86.7% failure. Fourteen modes clustered into system design (44.2%), inter-agent misalignment (32.3%), and verification (23.5%), showing that failures arise throughout the workflow and are not solved consistently by prompt/role tweaks.

### 5. Cost-aware agent evaluation

- **Title:** *AI Agents That Matter*
- **Authors/organization:** Sayash Kapoor, Benedikt Stroebl, Zachary S. Siegel, Nitya Nadgir, Arvind Narayanan; Princeton University
- **Date:** June 2025
- **URL:** https://openreview.net/pdf?id=Zy4uFzMviZ
- **Source type:** Peer-reviewed Transactions on Machine Learning Research paper; benchmark audit and empirical case studies
- **Evidence quality:** **High**
- **Scopes supported:** Cost control; baseline design; benchmark overfitting; reproducibility
- **Flags:** General agent evaluation, not a direct single-versus-multi coding trial.
- **Finding:** Accuracy-only evaluation can reward needlessly complex and costly agents; inadequate holdouts, inconsistent evaluation choices, high run cost, and missing error bars undermine claimed improvements. The paper demonstrates joint cost/accuracy optimization and calls for downstream-specific evaluation.

### 6. Anthropic production disclosure

- **Title:** *How We Built Our Multi-Agent Research System*
- **Authors/organization:** Anthropic engineering
- **Date:** 13 June 2025
- **URL:** https://www.anthropic.com/engineering/multi-agent-research-system
- **Source type:** First-party production engineering report with internal evaluations
- **Evidence quality:** **Medium**
- **Scopes supported:** Cost/latency; orchestration; context isolation; coding-fit boundary
- **Flags:** Vendor-sponsored; internal evaluation and task set not independently reproduced; positive result is research, not software engineering.
- **Finding:** Anthropic reports ≈15× chat token use for its multi-agent research system and says token use explained most BrowseComp variance. It explicitly identifies coding as less parallelizable and context/dependency-heavy work as a poor current fit.

### 7. Experienced-developer RCT

- **Title:** *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity*
- **Authors/organization:** Joel Becker, Nate Rush, Beth Barnes, David Rein; Model Evaluation & Threat Research (METR)
- **Date:** 10 July 2025
- **URL:** https://metr.org/Early_2025_AI_Experienced_OS_Devs_Study-paper.pdf
- **Source type:** Randomized controlled field experiment; preprint/report
- **Evidence quality:** **Medium**
- **Scopes supported:** Productivity; review/interaction overhead; perception bias; mature repositories
- **Flags:** Not a multi-agent comparison; 16 developers/246 tasks; early-2025 Cursor and Claude; experienced maintainers on familiar repositories; limited generalizability.
- **Finding:** AI-allowed tasks took 19% longer (95% interval reported as +2% to +39%) even though participants believed AI made them 20% faster after the study. It is strong evidence that perceived speed is an unreliable proxy in this narrow setting, not that newer agents always slow developers.

### 8. METR follow-up design failure

- **Title:** *We Are Changing Our Developer Productivity Experiment Design*
- **Authors/organization:** Joel Becker, Nate Rush, Tom Cunningham, David Rein, Khalid Mahamud; METR
- **Date:** 24 February 2026
- **URL:** https://metr.org/blog/2026-02-24-uplift-update/
- **Source type:** First-party methodological update on a randomized field study
- **Evidence quality:** **Medium** for the validity warning; **low** for productivity magnitude
- **Scopes supported:** Multi-agent time accounting; selection bias; measurement risk
- **Flags:** Unreliable central effect by the authors’ own assessment; not a publishable estimate of multi-agent uplift.
- **Finding:** Opt-out, task selection, concurrent agent use, and inconsistent time reporting made the late-2025 uplift estimate unreliable. This directly illustrates why concurrent-agent productivity requires instrumentation beyond self-reported active time.

### 9. SWE-bench Verified audit

- **Title:** *Why SWE-bench Verified No Longer Measures Frontier Coding Capabilities*
- **Authors/organization:** OpenAI
- **Date:** 23 February 2026
- **URL:** https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/
- **Source type:** First-party benchmark audit with multi-reviewer human analysis
- **Evidence quality:** **Medium**
- **Scopes supported:** Benchmark contamination; test validity; evaluation threats
- **Flags:** Vendor-sponsored and not peer-reviewed; audit targets a difficult 27.6% subset rather than a random full-set sample.
- **Finding:** At least 59.4% of 138 audited frequently failed tasks had material test/specification defects, and all tested frontier models reproduced some gold-patch or problem-specific content consistent with exposure. OpenAI stopped using the benchmark for frontier launches.

### 10. SWE-bench Pro audit

- **Title:** *Separating Signal from Noise in Coding Evaluations*
- **Authors/organization:** OpenAI
- **Date:** 8 July 2026
- **URL:** https://openai.com/index/separating-signal-from-noise-coding-evaluations/
- **Source type:** First-party benchmark audit with agent-assisted and five-engineer review
- **Evidence quality:** **Medium**
- **Scopes supported:** Broken tasks; hidden-test validity; benchmark-to-practice transfer
- **Flags:** Vendor-sponsored and not peer-reviewed; public split only.
- **Finding:** The automated pipeline flagged 27.4% and the human campaign 34.1% of 731 public SWE-bench Pro tasks as broken, leading to an ≈30% estimate. Failure and pass rates can therefore reflect evaluation defects as well as capability.

### 11. AgentDojo

- **Title:** *AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents*
- **Authors/organization:** Edoardo Debenedetti, Jie Zhang, Mislav Balunović, Luca Beurer-Kellner, Marc Fischer, Florian Tramèr; ETH Zurich and Invariant Labs
- **Date:** 2024
- **URL:** https://proceedings.neurips.cc/paper_files/paper/2024/file/97091a5177d8dc64b1da8bf3e1f6fb54-Paper-Datasets_and_Benchmarks_Track.pdf
- **Source type:** Peer-reviewed NeurIPS 2024 Datasets and Benchmarks paper; dynamic security benchmark
- **Evidence quality:** **High**
- **Scopes supported:** Tool permissions; indirect prompt injection; security/utility trade-offs
- **Flags:** Single-agent tool-use environments rather than coding teams; older model versions; synthetic but executable harms.
- **Finding:** Across 97 realistic tasks and 629 security cases, leading agents failed benign tasks and prompt-injection defenses preserved neither complete utility nor complete security. The work demonstrates that untrusted tool data can cause actions on the user’s behalf.

### 12. Prompt Infection

- **Title:** *Prompt Infection: LLM-to-LLM Prompt Injection within Multi-Agent Systems*
- **Authors/organization:** Donghyun Lee and Mo Tiwari
- **Date:** 9 October 2024
- **URL:** https://arxiv.org/pdf/2410.07283
- **Source type:** Primary multi-agent security experiment; preprint
- **Evidence quality:** **Medium**
- **Scopes supported:** Cross-agent propagation; shared/local messaging; memory poisoning; systemic compromise
- **Flags:** Preprint-only; GPT-4o/GPT-3.5-era models and basic topologies; proof-of-concept scenarios, not coding repositories.
- **Finding:** Self-replicating malicious instructions propagated across communicating agents and generally outperformed non-replicating injections, including where agents lacked a global transcript. The proposed tagging defense reduced attacks in tested settings but was not established against adaptive production adversaries.

### 13. RepoGuardBench

- **Title:** *RepoGuardBench: Repository-Borne Prompt Injection Attacks and Lightweight Defenses for Local Coding Agents*
- **Authors/organization:** Daoyuan Li
- **Date:** 2026
- **URL:** https://github.com/DaoyuanLi2816/RepoGuardBench
- **Source type:** Open benchmark artifact and ICML 2026 DL4C workshop paper
- **Evidence quality:** **Low**
- **Scopes supported:** Repository prompt injection; rules/comments; sandbox/action gates
- **Flags:** Non-archival workshop; 80 simple core tasks and 14 applied tasks; mostly Qwen2.5-Coder models; inert attacks; optional Claude data excluded from headline aggregate.
- **Finding:** Code comments and agent-rule files were the most effective injection carriers in matched clean/poisoned tests; simple path gates still allowed semantic test deletion. Strict sandbox completion was low but non-zero, so file-location controls alone did not establish safety.

### 14. SecureVibeBench

- **Title:** *SecureVibeBench: Benchmarking Secure Vibe Coding of AI Agents via Reconstructing Vulnerability-Introducing Scenarios*
- **Authors/organization:** Junkai Chen, Huihui Huang, Yunbo Lyu, Junwen An, Jieke Shi, Chengran Yang, Ting Zhang, Haoye Tian, Yikun Li, Zhenhao Li, Xin Zhou, Xing Hu, David Lo; SMU, NUS, Monash, Aalto, York, Zhejiang
- **Date:** 6 June 2026 (arXiv v5)
- **URL:** https://arxiv.org/pdf/2509.22097
- **Source type:** Primary repository-level security benchmark; preprint
- **Evidence quality:** **Medium**
- **Scopes supported:** Secure coding; functional-test insufficiency; cost/time trade-offs
- **Flags:** Preprint; 105 C/C++ memory-safety tasks from 41 projects; not multi-agent; static/dynamic oracle coverage is necessarily incomplete.
- **Finding:** Across five agents and five LLMs, the best combination reached 23.8% correct-and-secure; in many combinations more than half of functionally correct outputs still had security issues. Higher performance generally required more processing time, and scaffold choice materially changed cost-effectiveness.

### 15. Group conformity

- **Title:** *An Empirical Study of Group Conformity in Multi-Agent Systems*
- **Authors/organization:** Min Choi, Keonwoo Kim, Sungwon Chae, Sangyeop Baek
- **Date:** July 2025
- **URL:** https://aclanthology.org/2025.findings-acl.265/
- **Source type:** Peer-reviewed ACL Findings paper; controlled debate simulations
- **Evidence quality:** **High** for the studied social dynamics; **medium/low** for transfer to coding
- **Scopes supported:** Hallucinated consensus; correlated review; model-tier influence
- **Flags:** Contentious social debates rather than objective coding tasks; prompted personas and moderator decisions.
- **Finding:** Across more than 2,500 debates, neutral agents conformed significantly to majorities and higher-capability peers; one higher-capability agent could outweigh a larger lower-capability group. Agreement count is thus not evidence of independent error reduction.

### 16. Agentic code review in the wild

- **Title:** *Human-AI Synergy in Agentic Code Review*
- **Authors/organization:** Suzhen Zhong, Shayan Noei, Ying Zou, Bram Adams; Queen’s University
- **Date:** 16 March 2026
- **URL:** https://arxiv.org/pdf/2603.15911
- **Source type:** Large observational mining study; preprint
- **Evidence quality:** **Medium/low**
- **Scopes supported:** Review burden; human oversight; suggestion quality; organizational risk
- **Flags:** Preprint; observational confounding; bot identity and merge outcome are proxies; only 928 agent-on-agent conversations and 94% were self-review; code metrics are incomplete quality proxies.
- **Finding:** In 278,790 inline conversations from 300 projects, AI-agent suggestions were adopted 16.6% versus 56.5% for human suggestions; more than half of unadopted AI suggestions were incorrect or fixed another way. Human reviewers exchanged 11.8% more rounds on agent-authored code, indicating downstream review work rather than free quality assurance.

### 17. Organizational delivery evidence

- **Title:** *Highlights from the 10th DORA Report* (2024 Accelerate State of DevOps)
- **Authors/organization:** Nathen Harvey, Derek DeBellis; DORA / Google Cloud
- **Date:** 22 October 2024
- **URL:** https://cloud.google.com/blog/products/devops-sre/announcing-the-2024-dora-report
- **Source type:** Industry cross-sectional survey report
- **Evidence quality:** **Low** for causal or multi-agent conclusions
- **Scopes supported:** Delivery throughput/stability; trust; batch-size and review risk
- **Flags:** Vendor-sponsored; self-reported/correlational; generative AI broadly, not coding agents or multi-agent systems.
- **Finding:** A 25% increase in AI adoption was associated with 1.5% lower delivery throughput and 7.2% lower stability despite reported documentation/code-quality/review-speed gains. The authors attribute the delivery pattern partly to larger batches, but the design does not establish causation.

## Red-team conclusion

The robust recommendation is a burden-of-proof rule: **do not add coding agents merely because a task is larger or because parallel execution is available**. Require evidence that the task graph has independent ready work, the integration surface is explicit, each worker is isolated and least-privileged, verification is executable and independent, and measured value exceeds added compute plus human review. Small or coupled work usually fails that test; architecture-heavy work may pass it only with centralized ownership and branch-and-merge discipline. Any universal agent-count prescription would outrun the literature available by 23 August 2026.
