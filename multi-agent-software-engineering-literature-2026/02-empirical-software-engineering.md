# Empirical software-engineering evidence

## Scope, cutoff, and search method

- **Assigned scope:** controlled studies, repository-level and SWE-bench-style evaluations, industrial field evidence, and direct single-agent/multi-agent comparisons. This memo does not survey coordination theory or product documentation except where needed to interpret an experiment.
- **Actual search cutoff:** **23 August 2026**. The requested 31 August 2026 cutoff is eight days in the future and therefore cannot be satisfied. No claim is made about material published after the actual cutoff.
- **Method:** searched scholarly indexes and the open web for full papers, proceedings pages, official benchmark repositories, replication packages, and official technical audits. Material claims below were checked in full text or an inspectable primary repository; search-result snippets and secondary summaries were not used as evidence. Sixteen primary-source records are annotated (15 core sources plus one supplemental low-confidence result).
- **Quality scale:** **high** = peer-reviewed or randomized field evidence with a relevant comparator and transparent methods; **medium** = credible benchmark experiment or accepted paper with important ecological/comparability limits; **low** = preprint, small ablation, vendor/self-evaluation, or materially incomplete independent validation. “High” does not mean directly transferable to production.

## Executive memo

### What the evidence supports

There is evidence that role separation can improve measured correctness, but the effect is conditional rather than a general “more agents is better” law. On function-level HumanEval/MBPP tasks, AgentCoder’s controlled comparison raised pass@1 from 71.3% to 79.9% and 79.4% to 89.9%, respectively, when programming and test design were separated; test accuracy and coverage also rose ([Huang et al.](https://arxiv.org/pdf/2312.13010)). On repository issue resolution, CodeR’s 50-task ablation fell from 22% to 10% when its multi-agent/task-graph layer was removed, but the full system used roughly 48% more tokens and 51% more model requests ([Chen et al.](https://arxiv.org/pdf/2406.01304)). MAGIS resolved 13.94% of a 25% SWE-bench subset versus 1.74% for direct GPT-4, and removing its QA role reduced resolution by 3.31 percentage points without hints ([Tao et al.](https://proceedings.neurips.cc/paper_files/paper/2024/file/5d1f02132ef51602adf07000ca5b6138-Paper-Conference.pdf)). These studies support specialized localization, testing, and review loops—not arbitrary parallel coding.

The strongest recent same-model repository evidence also rejects monotonic scaling. BOAD improved Seed-OSS-36B SWE-agent from 49.8% to 53.2% on SWE-bench Verified and from 12.3% to 20.0% on SWE-bench Live; a manually designed multi-agent variant was worse than the single agent (47.4% Verified), and Live performance peaked with **two** subagents, falling with three to five ([Xu et al.](https://arxiv.org/pdf/2512.23631)). BOAD’s qualitative audit found both multi-site/localized-edit advantages and a new failure mode: an orchestrator accepts a bad handoff and propagates the error. A separate, vendor-run controlled experiment on 50 SWE-bench Verified issues found a 36/50 tie between a multi-agent “Squad” and matched standalone agent, with each solving three unique issues ([Squad repository](https://github.com/tamirdresher/squad-swe-bench)). This last result is low-quality but directionally consistent: atomic bug fixing may not repay coordination overhead.

Negative evidence is task-specific but consequential. In 180 repository-documentation tasks, a single RAG agent slightly exceeded a multi-agent workflow on ROUGE-L (0.2007 versus 0.1964), used 7,840 rather than 56,242 tokens, and ran in 40 rather than 78 seconds. The multi-agent system did improve structural precision (98.2% versus 77.6% on a 20-repository manual subsample), while a human-authored plan gave the best overall quality at still higher cost ([Saleh et al.](https://arxiv.org/pdf/2606.30524)). In DevEval’s greenfield, full-lifecycle tasks, adding an LLM review role did not improve GPT-4-Turbo implementation (3.0% acceptance-test pass in both conditions) and reduced unit-test oracle correctness from 35.1% to 22.6%; execution feedback, not review alone, raised implementation acceptance-test pass to 8.9% ([Li et al.](https://aclanthology.org/2025.coling-main.502.pdf)).

Simple scaffolds remain strong controls. Peer-reviewed Agentless used a fixed localize–repair–validate workflow and achieved 32.0% (96/300) on SWE-bench Lite at about $0.70 per issue, outperforming the more complex open-source agents tested at submission time ([Xia et al.](https://doi.org/10.1145/3715754)). SWE-agent’s own controlled ACI ablation gained 10.7 percentage points over a plain-shell agent, showing that tools and interface design can explain substantial gains without multiple agents ([Yang et al.](https://proceedings.neurips.cc/paper_files/paper/2024/file/5a7c947568c1b1328ccc5230172e1e7c-Paper-Conference.pdf)).

### What production evidence does—and does not—show

No located randomized field study directly compared multi-agent and single-agent coding in a production organization. The closest productivity evidence concerns human use of single assistants. Three workplace RCTs covering 4,867 developers found a pooled 26.08% increase (SE 10.3%) in completed tasks among Copilot users, with noisy individual experiments and larger effects for less-experienced developers ([Cui et al.](https://demirermert.github.io/Papers/Demirer_AI_productivity.pdf)). In contrast, METR randomized 246 real tasks performed by 16 experienced maintainers in repositories they knew well and found early-2025 AI tools increased completion time by 19%, despite developers believing they were faster ([Becker et al.](https://metr.org/Early_2025_AI_Experienced_OS_Devs_Study-paper.pdf)). A smaller lab RCT found a 55.8% speedup for one bounded JavaScript task ([Peng et al.](https://arxiv.org/abs/2302.06590)). These are not multi-agent evaluations; they establish that task novelty, repository familiarity, developer experience, and outcome definition materially change measured value.

### Limits on inference

SWE-bench results are not project-delivery results: tasks are predominantly Python issue patches, success is test passage, and systems often differ in model, hints, tools, attempt counts, and budgets. Agent diversity may provide portfolio value—across ten agents, 10.2% of 500 Verified issues were solved by only one system—but passing patches sometimes changed different code than the human patch, exposing test-coverage risk ([Chen and Jiang](https://arxiv.org/abs/2410.12468)). More importantly, OpenAI’s 2026 audit found material specification/test problems in 59.4% of 138 persistently difficult Verified tasks and evidence of training exposure; it recommends retiring Verified for frontier comparisons ([OpenAI](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/)). Therefore, older leaderboard deltas are historical evidence about scaffolds, not durable estimates of present-day production reliability.

### Evidence-led inference

The defensible inference is a threshold model: one well-tooled agent is the control condition; add a small number of agents only when the work contains genuinely separable information or verification roles and objective handoff checks exist. Current evidence is most supportive of independent test/review or localization roles, weaker for peer-like discussion, and negative on increasing team size without validated incremental benefit. There is insufficient empirical evidence to prescribe agent counts for large cross-cutting features or greenfield products with high confidence.

## Actionable findings

| Scope / condition | Evidence (measured) | Actionable inference (explicitly not direct evidence) | Quality |
|---|---|---|---|
| Small, atomic bug fix | Matched Squad/standalone run tied at 72% on 50 Verified issues; Agentless beat more complex agents on Lite at lower cost. | Default to one well-tooled agent; require a local benchmark before adding coordination. | Low–medium |
| Function-level implementation with generated tests | Separating programmer and test designer improved AgentCoder pass@1 by 8.6 pp on HumanEval and 10.5 pp on MBPP; test accuracy/coverage improved more. | A second, context-independent test role is plausible when executable oracles exist. Do not generalize from toy functions to repositories. | Medium (preprint; synthetic tasks) |
| Repository bug with uncertain location | CodeR’s multi-agent/task-graph ablation was +12 pp on 50 issues; MAGIS and BOAD associate gains with localization and bounded role specialization. | Decomposition has the best empirical case when localization, reproduction, editing, and validation are distinct and machine-checkable. | Medium |
| Multi-file repository change | BOAD’s audit found fewer over-edits and better multi-site coverage, but also handoff error propagation. | Validate each handoff (locations, invariants, tests) before downstream agents consume it. | Medium–high |
| More agents | BOAD Live peaked at two subagents (20.0%); 3/4/5 scored 16.3/16.7/13.7%. Manual roles underperformed the single agent on Verified. | Treat agent count as a tuned variable with a stop rule, not a proxy for capability. | High for tested scaffold; narrow external validity |
| Review role without external feedback | DevEval’s Normal-Review did not improve implementation and reduced GPT-4 unit-test oracle score; execution feedback improved implementation. | Prefer executable feedback over ungrounded reviewer dialogue. | High–medium |
| Structured documentation | Single agent matched/slightly exceeded multi-agent lexical quality with 86% fewer tokens; multi-agent improved structural precision. | Use multiple roles only if structural completeness is valuable enough to justify roughly 7.1× tokens; a small human plan may outperform autonomous planning. | Medium |
| Greenfield/full lifecycle | GPT-4-Turbo achieved under 10% repository implementation in DevEval; tests were often non-executable, although executable tests could attain high coverage. | Do not infer end-to-end product autonomy from issue-fix or function benchmarks; retain stage-specific acceptance gates. | High–medium |
| Human productivity | Real-world studies range from +26.08% completed tasks (pooled field RCTs) to 19% slower (experienced maintainers); a bounded lab task showed 55.8% faster. | Measure cycle time and accepted outcomes in the target team; subjective speed and benchmark scores are inadequate proxies. | High, but single-assistant only |
| Benchmark choice | OpenAI found residual broken tasks and training exposure in Verified; Live was designed for fresh tasks. | Prefer fresh/private, contamination-resistant tasks and matched models/tools/budgets for single-vs-multi tests. | Medium–high |
| Patch acceptance | Ten-agent analysis found complementary wins, but divergent test-passing patches and over-modification. | Use portfolio diversity for candidate generation only when independent regression/security/maintainability review can reject unsafe patches. | Medium (preprint) |

## Annotated bibliography

### 1. SWE-bench: Can Language Models Resolve Real-World GitHub Issues?

- **Authors / organization:** Carlos E. Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, Karthik Narasimhan; Princeton University / University of Chicago.
- **Date:** 2024 (ICLR 2024; initial preprint October 2023).
- **URL:** https://openreview.net/forum?id=VTF8yNQM66
- **Evidence type:** Peer-reviewed benchmark paper; 2,294 issue/PR pairs from 12 Python repositories.
- **Evidence quality:** **High** for the original benchmark construction; **medium** for production generalization.
- **Flags:** Public historical issues create later contamination risk; issue quality and tests were subsequently audited.
- **Finding:** Initial retrieval-and-generate systems solved at most 1.96% of issues, and increasing retrieved context could reduce resolution despite higher oracle-file recall. This establishes repository localization/context as a distinct difficulty, but does not compare agent counts.

### 2. SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering

- **Authors / organization:** John Yang, Carlos E. Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik Narasimhan, Ofir Press; Princeton Language and Intelligence.
- **Date:** December 2024 (NeurIPS 2024).
- **URL:** https://proceedings.neurips.cc/paper_files/paper/2024/file/5a7c947568c1b1328ccc5230172e1e7c-Paper-Conference.pdf
- **Evidence type:** Peer-reviewed repository benchmark plus controlled interface ablations.
- **Evidence quality:** **High–medium**.
- **Flags:** Primarily Python issue repair; historical models and benchmark; not multi-agent.
- **Finding:** GPT-4 Turbo SWE-agent resolved 12.47% of full SWE-bench, and its custom agent-computer interface improved Lite resolution by 10.7 percentage points over a plain Linux-shell agent. Agent architecture and tools are major confounders in purported multi-agent gains.

### 3. MAGIS: LLM-Based Multi-Agent Framework for GitHub Issue ReSolution

- **Authors / organization:** Wei Tao, Yucheng Zhou, Yanlin Wang, Wenqiang Zhang, Hongyu Zhang, Yu Cheng; Fudan University and collaborators.
- **Date:** December 2024 (NeurIPS 2024).
- **URL:** https://proceedings.neurips.cc/paper_files/paper/2024/file/5d1f02132ef51602adf07000ca5b6138-Paper-Conference.pdf
- **Evidence type:** Peer-reviewed repository-level evaluation and component ablations.
- **Evidence quality:** **Medium**.
- **Flags:** Uses only the 25% SWE-bench subset used for GPT-4 and supplies files to modify; some conditions use pre-resolution PR comments (“hints”).
- **Finding:** MAGIS resolved 13.94% versus 1.74% for direct GPT-4; without hints and QA it resolved 8.71%, and adding QA raised resolution to 10.28%. The result supports a review role within this scaffold but does not isolate every role or cost.

### 4. CodeR: Issue Resolving with Multi-Agent and Task Graphs

- **Authors / organization:** Dong Chen, Shaoxin Lin, Muhan Zeng, Daoguang Zan, Jian-Gang Wang, Anton Cheshkov, Jun Sun, Hao Yu, Guoliang Dong, Artem Aliev, Jie Wang, Xiao Cheng, Guangtai Liang, Yuchi Ma, Pan Bian, Tao Xie, Qianxiang Wang; Huawei and academic collaborators.
- **Date:** 11 June 2024 (arXiv v3).
- **URL:** https://arxiv.org/pdf/2406.01304
- **Evidence type:** Preprint; SWE-bench Lite evaluation and 50-task controlled ablation.
- **Evidence quality:** **Medium–low**.
- **Flags:** Preprint-only; small ablation; some environment restarts; full-system reported/reproduced counts differ; $8 cap per issue.
- **Finding:** Full CodeR resolved 27.33% in the authors’ rerun (reported submission 28.33%) at 299K tokens/$3.09 per issue. Removing multi-agent/task graphs reduced 50-task resolution from 22% to 10%, while tokens fell from 295K to 200K and requests from 30.4 to 18.46.

### 5. MASAI: Modular Architecture for Software-engineering AI Agents

- **Authors / organization:** Daman Arora, Atharv Sonwane, Nalin Wadhwa, Abhav Mehrotra, Saiteja Utpala, Ramakrishna Bairi, Aditya Kanade, Nagarajan Natarajan.
- **Date:** 17 June 2024.
- **URL:** https://arxiv.org/abs/2406.11638
- **Evidence type:** Preprint; five-role modular agent evaluated on 300 SWE-bench Lite tasks.
- **Evidence quality:** **Medium–low**.
- **Flags:** Preprint-only; one model (GPT-4o); several leaderboard comparators had unequal hints/setup; benchmark limited to test-verifiable Python issues.
- **Finding:** MASAI resolved 28.33%. Five repair samples increased oracle availability from 23.33% to 35%, but LLM selection without tests achieved only 23.33%; test-informed ranking reached 28.33%, showing candidate diversity is useful only with a discriminating verifier.

### 6. AgentCoder: Multi-Agent-based Code Generation with Iterative Testing and Optimisation

- **Authors / organization:** Dong Huang, Jie M. Zhang, Michael Luck, Qingwen Bu, Yuhao Qing, Heming Cui.
- **Date:** 20 December 2023 (revised 2024).
- **URL:** https://arxiv.org/pdf/2312.13010
- **Evidence type:** Preprint; controlled function-level benchmark and ablations.
- **Evidence quality:** **Medium–low**.
- **Flags:** Preprint-only; HumanEval/MBPP are small synthetic functions, not repository work; repeated benchmark exposure is possible.
- **Finding:** Separate programmer/test agents outperformed one agent doing both in the same conversation: 79.9% versus 71.3% HumanEval pass@1 and 89.9% versus 79.4% MBPP. Test accuracy rose from 61.0%/51.8% to 87.8%/89.9%.

### 7. Demystifying LLM-Based Software Engineering Agents (Agentless)

- **Authors / organization:** Chunqiu Steven Xia, Yinlin Deng, Soren Dunn, Lingming Zhang; University of Illinois Urbana-Champaign.
- **Date:** July 2025 (FSE 2025).
- **URL:** https://doi.org/10.1145/3715754
- **Evidence type:** Peer-reviewed repository-level benchmark with a fixed non-agentic workflow.
- **Evidence quality:** **High–medium**.
- **Flags:** Up to many sampled candidates and filtering complicate comparisons with one-attempt agents; SWE-bench Lite is narrow and historical.
- **Finding:** The simple localization–repair–validation workflow resolved 32.0% (96/300) of Lite at about $0.70 per issue and outperformed tested open-source autonomous agents at submission time. Complexity was not necessary for that benchmark.

### 8. BOAD: Discovering Hierarchical Software Engineering Agents via Bandit Optimization

- **Authors / organization:** Iris Xu, Guangtao Zeng, Zexue He, Charles Jin, Aldo Pareja, Dan Gutfreund, Chuang Gan, Zhang-Wei Hong; MIT, MIT-IBM Watson AI Lab, Stanford, UMass Amherst, collaborators.
- **Date:** January 2026; accepted ICLR 2026.
- **URL:** https://arxiv.org/pdf/2512.23631
- **Evidence type:** Peer-reviewed same-model single/manual-multi/optimized-multi comparison on 500 Verified and 300 Live tasks.
- **Evidence quality:** **High–medium**.
- **Flags:** Twelve Verified tasks used for design; LLM-as-judge used for subagent credit; discovered roles transfer only partly across models; Verified contamination caveat.
- **Finding:** BOAD improved the 36B baseline from 49.8% to 53.2% Verified and 12.3% to 20.0% Live; manual subagents scored 47.4% Verified. Two subagents were best on Live; adding three to five reduced success, and bad handoffs caused error propagation.

### 9. The Illusion of Agentic Complexity in README.md Generation

- **Authors / organization:** Abu Saleh, Tesfay Welegebreal Tesfay, Phuong T. Nguyen, Juri Di Rocco, Muhammad Umar Zeshan, Davide Di Ruscio; University of L’Aquila, Åbo Akademi, University of Pisa.
- **Date:** 1 July 2026; accepted ICSME 2026.
- **URL:** https://arxiv.org/pdf/2606.30524
- **Evidence type:** Accepted empirical study; matched single-agent, multi-agent, and developer-planned RAG workflows over 180 repositories.
- **Evidence quality:** **Medium**.
- **Flags:** Proceedings publication was future/pending at cutoff; only 20 repositories received manual/LLM-judge structural analysis; documentation task; gpt-5.1-specific.
- **Finding:** Single-agent lexical quality matched/slightly beat autonomous multi-agent while using 86% fewer tokens and roughly half the time. Multi-agent achieved higher structural precision; developer-authored plans achieved the best overall quality at the highest cost.

### 10. Prompting Large Language Models to Tackle the Full Software Development Lifecycle: A Case Study (DevEval)

- **Authors / organization:** Bowen Li, Wenhan Wu, Ziwei Tang, Lin Shi, John Yang, Jinyang Li, Shunyu Yao, Chen Qian, Binyuan Hui, Qicheng Zhang, Zhiyin Yu, He Du, Ping Yang, Dahua Lin, Chao Peng, Kai Chen; Shanghai AI Laboratory and collaborators.
- **Date:** January 2025 (COLING 2025).
- **URL:** https://aclanthology.org/2025.coling-main.502.pdf
- **Evidence type:** Peer-reviewed full-lifecycle/greenfield benchmark across 22 repositories and four languages.
- **Evidence quality:** **High–medium**.
- **Flags:** Small repository set; extended ChatDev baseline; only one review pass; historical models; parts of design scoring use LLM judges.
- **Finding:** GPT-4-Turbo’s repository implementation passed only 8.9% of weighted acceptance tests with execution feedback. Normal reviewer dialogue alone left implementation at 3.0% and reduced unit-test oracle score from 35.1% to 22.6%, so review without grounded feedback was not reliably helpful.

### 11. The Effects of Generative AI on High-Skilled Work: Evidence from Three Field Experiments with Software Developers

- **Authors / organization:** Kevin Zheyuan Cui, Mert Demirer, Sonia Jaffe, Leon Musolff, Sida Peng, Tobias Salz; Princeton, MIT, Microsoft Research, Wharton.
- **Date:** 27 February 2026 (Management Science; experiments in 2022–2023).
- **URL:** https://doi.org/10.1287/mnsc.2025.00535
- **Evidence type:** Peer-reviewed randomized field experiments at Microsoft, Accenture, and a Fortune 100 company (4,867 developers).
- **Evidence quality:** **High**.
- **Flags:** Vendor-associated authors/data; treatment was older Copilot autocomplete, not agents; individual experiments were noisy; completed-task counts are organization-defined.
- **Finding:** Pooled instrumental-variable estimates attribute a 26.08% increase (SE 10.3%) in weekly completed tasks to tool use; less-experienced developers adopted more and gained more. This bounds real-world assistant effects but says nothing direct about multi-agent coordination.

### 12. Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity

- **Authors / organization:** Joel Becker, Nate Rush, Beth Barnes, David Rein; Model Evaluation & Threat Research (METR).
- **Date:** 10 July 2025.
- **URL:** https://metr.org/Early_2025_AI_Experienced_OS_Devs_Study-paper.pdf
- **Evidence type:** Randomized controlled trial; 16 experienced maintainers, 246 real tasks in familiar mature repositories.
- **Evidence quality:** **High** for its population and tools; limited external breadth.
- **Flags:** Preprint/nonprofit report; small participant count; early-2025 Cursor and Claude; treatment mixed multiple AI workflows, not multi-agent orchestration.
- **Finding:** Allowing AI increased completion time by 19%, while developers forecast a 24% speedup before and believed in a 20% speedup afterward. Perceived productivity is therefore an unreliable outcome measure in this setting.

### 13. The Impact of AI on Developer Productivity: Evidence from GitHub Copilot

- **Authors / organization:** Sida Peng, Eirini Kalliamvakou, Peter Cihon, Mert Demirer; Microsoft Research / GitHub collaborators.
- **Date:** 13 February 2023.
- **URL:** https://arxiv.org/abs/2302.06590
- **Evidence type:** Randomized controlled lab study; 95 professional freelancers, one JavaScript HTTP-server task.
- **Evidence quality:** **Medium–high**.
- **Flags:** Preprint; vendor-associated; one bounded task; no code-quality or maintenance outcome; non-agent autocomplete.
- **Finding:** Copilot users completed the task 55.8% faster (95% CI 21%–89%); success-rate difference was not statistically significant. The result does not generalize by itself to repository or multi-agent work.

### 14. Evaluating Software Development Agents: Patch Patterns, Code Quality, and Issue Complexity in Real-World GitHub Scenarios

- **Authors / organization:** Zhi Chen, Lingxiao Jiang.
- **Date:** 16 October 2024.
- **URL:** https://arxiv.org/abs/2410.12468
- **Evidence type:** Preprint repository-mining study of 4,892 patches from ten agents over 500 SWE-bench Verified issues.
- **Evidence quality:** **Medium–low**.
- **Flags:** Preprint-only; heterogeneous agents/models; SonarQube proxies do not measure all quality; Verified now has contamination/specification concerns.
- **Finding:** No single system dominated: 51 issues were solved by only one of ten agents and 170 by none. Some test-passing patches diverged substantially from human patches and some over-modified code, so test passage did not fully establish maintainability or safety.

### 15. Why SWE-bench Verified no longer measures frontier coding capabilities

- **Authors / organization:** OpenAI Frontier Evals and Human Data teams.
- **Date:** 23 February 2026.
- **URL:** https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/
- **Evidence type:** Official technical audit of 138 persistently difficult benchmark tasks, with at least six experienced reviewers per case and repeated model runs.
- **Evidence quality:** **Medium–high** for benchmark diagnosis.
- **Flags:** Vendor-authored, targeted rather than random audit, not peer-reviewed; exact contamination exposure cannot be fully observed.
- **Finding:** The audit found material test/specification problems in 59.4% of reviewed tasks and evidence that frontier models had seen some gold patches or statement details. OpenAI stopped reporting Verified and recommended SWE-bench Pro, substantially weakening universal claims from historical Verified scores.

### Supplemental low-confidence primary result: Squad controlled comparison

- **Authors / organization:** Tamir Dresher / Squad project.
- **Date:** June–July 2026.
- **URL:** https://github.com/tamirdresher/squad-swe-bench
- **Evidence type:** Public vendor/project repository with a matched 50-instance Verified ablation and raw outputs.
- **Evidence quality:** **Low**.
- **Flags:** Self-evaluation; small selected sample; not peer-reviewed; uses a contaminated/deprecated benchmark; broader 66% Lite claim lacks a same-model control.
- **Finding:** Squad-on and Squad-off both resolved 36/50 tasks, with three unique wins per arm. It is a useful null result for atomic bug fixing but not sufficient to estimate production effects.

## Bottom line for synthesis

Robust findings are limited to: (1) tool/interface and execution feedback matter greatly; (2) specialized, independently verifiable roles can improve certain coding tasks; (3) more agents do not monotonically improve outcomes; and (4) benchmark success and human productivity vary sharply by task and population. Claims about large-feature or greenfield delivery, optimal parallel agent counts, merge quality, and long-term maintainability remain **emerging practice**, not established empirical fact.
