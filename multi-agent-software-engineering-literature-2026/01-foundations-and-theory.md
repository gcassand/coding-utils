# Foundations and theory of multi-agent software engineering

## Scope, cutoff, and search method

**Assigned scope.** Foundations of multi-agent systems (MAS) as they bear on agentic software engineering: task decomposition and allocation, collaborative planning, coordination topology, communication, shared memory/context, verification, and failure modes. This memo treats implementation guidance as an inference unless a cited study directly tested it.

**Actual search cutoff: 23 August 2026 (Europe/Paris).** The requested cutoff, 31 August 2026, is eight days in the future and therefore cannot be covered. Searches and source checks were completed on 23 August 2026; no claim is made about work published from 24–31 August 2026.

**Method.** I searched the ICLR, NeurIPS, ICML/PMLR, ACL Anthology, AAAI, ACM, IEEE/INFORMS, institutional repositories, arXiv, and official project repositories using combinations of *multi-agent*, *software engineering*, *task decomposition*, *hierarchical planning*, *coordination*, *communication*, *shared plans*, *shared memory*, *debate*, *failure*, *verification*, and *scaling*. I read primary full text or the publisher's complete article page; I did not derive findings from search snippets or abstracts alone. A peer-reviewed survey was used to cross-check coverage, not to establish causal claims. Peer-reviewed theory and controlled evaluations are prioritized. Preprints and vendor-affiliated work are flagged. Quality is claim-relative: **high** means a peer-reviewed formal result or unusually well-controlled multi-model study; **medium** means peer-reviewed but narrow/synthetic, or a strong yet unreviewed controlled study; **low** means unverified, inaccessible, or materially under-controlled evidence. No inaccessible source supports a material claim below.

## Executive memo

The durable foundation is not “more agents,” but **distributed problem solving under information and dependency constraints**. The Contract Net protocol formalized dynamic task allocation through announcement, bidding, award, and result reporting, while SharedPlans formalized collaboration as agreement on a recipe, commitment to the joint activity and partners' success, and coordinated subsidiary plans ([Smith 1980](https://www.eecs.ucf.edu/~lboloni/Teaching/EEL6788_2008/papers/The_Contract_Net_Protocol_Dec-1980.pdf); [Grosz & Kraus 1996](https://u.cs.biu.ac.il/~sarit/data/articles/20.pdf)). These are complementary: allocation answers *who does what*; a collaborative plan answers *what agents mutually believe, intend, and monitor*. **Evidence quality: high.**

Decomposition is not automatically simplification. Hierarchical task-network (HTN) planning is expressive, but its decidability and complexity depend sharply on ordering and restrictions on non-primitive tasks ([Erol, Hendler & Nau 1994](https://euro.ecom.cmu.edu/program/courses/tcr854/2001/readings/Hendler_Nau_AAAI-94.pdf)). Under partial observability, even finite-horizon decentralized control with only two agents is NEXP-hard, unlike centralized counterparts ([Bernstein et al. 2002](https://pubsonline.informs.org/doi/10.1287/moor.27.4.819.297)). **Evidence quality: high.** Inference for coding agents: decomposition helps only when interfaces reduce coupling; otherwise it relocates reasoning into coordination and integration.

Communication architecture determines both information flow and failure propagation. Blackboard systems provide a common evolving problem state for independent knowledge sources ([Nii 1986](https://onlinelibrary.wiley.com/doi/10.1609/aimag.v7i2.537)); modern role-based systems encode sequential workflows and intermediate artifacts, as in MetaGPT and ChatDev ([Hong et al. 2024](https://proceedings.iclr.cc/paper_files/paper/2024/hash/6507b115562bb0a305f1958ccc87355a-Abstract-Conference.html); [Qian et al. 2024](https://aclanthology.org/2024.acl-long.810/)). **Evidence quality: medium** for transfer to real repositories: the architectural patterns are clear, but those papers' software tasks and evaluators are narrower than production engineering.

Memory is an active control component, not just a transcript. Generative Agents showed that retrieval, reflection, and planning ablations each mattered to believable behavior; Reflexion showed that compact verbal feedback retained across episodes can improve later attempts; ReAct showed the value of interleaving reasoning with external action and observations ([Park et al. 2023](https://dl.acm.org/doi/10.1145/3586183.3606763); [Shinn et al. 2023](https://papers.nips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html); [Yao et al. 2023](https://arxiv.org/abs/2210.03629)). **Evidence quality: medium** for software engineering because these are mostly single-agent or simulation studies. Inference: shared context should contain selected state, decisions, interfaces, and verified observations—not every dialogue turn.

Recent evidence rejects unqualified claims that deliberation creates correctness. Early multi-agent debate improved some math, strategy, and factuality benchmarks ([Du et al. 2024](https://proceedings.mlr.press/v235/du24e.html)), but a later NeurIPS study found that majority voting over independent samples explained most gains across seven NLP benchmarks; under its formal model, ordinary debate is a martingale and does not improve expected correctness by itself ([Choi, Zhu & Li 2025](https://papers.nips.cc/paper_files/paper/2025/hash/934252acd87f254d5d4672fbde283bd2-Abstract-Conference.html)). **Evidence quality: high for the tested protocols; external validity to repository work is medium.** Diversity is valuable only if aggregation can recognize correctness.

Coordination is a distinct capability. LLM-Coordination found agents stronger when choices follow environmental variables than when success requires modeling a partner's beliefs and intentions ([Agashe et al. 2025](https://aclanthology.org/2025.findings-naacl.448/)). HiddenBench found 30.1% accuracy with information distributed among agents versus 80.7% for a single agent given all information; agents prematurely converged on shared facts, while a structured “exchange evidence and challenge the front-runner, then decide” protocol sharply improved a small ablation ([Li, Naito & Shirado 2026](https://arxiv.org/abs/2505.11556)). **Evidence quality: high for the benchmark phenomenon; medium for the small protocol ablation.** More messages or agents did not fix latent information asymmetry.

Failure analysis converges on system-level causes. MAST identified 14 modes across 1,642 traces, grouped into specification/system design, inter-agent misalignment, and verification/termination; explicit verifiers helped but were not sufficient ([Cemri et al. 2025](https://arxiv.org/abs/2503.13657)). A controlled 2026 study across 260 configurations found benefits on decomposable work but 39–70% degradation on sequential planning, a tool-coordination penalty, and less error amplification with centralized verification ([Kim et al. 2026](https://arxiv.org/abs/2512.08296)). **Evidence quality: high for MAST's taxonomy; medium for the unreviewed, Google-affiliated scaling study.**

**Bottom line (inference, not a directly tested universal law):** use multiple coding agents when a task can be represented as a dependency graph with genuinely separable nodes, explicit input/output contracts, and independent evidence-producing work. Prefer a coordinator-plus-specialists topology when outputs must converge. Keep tightly sequential reasoning in one context. Treat agent count, communication rounds, and shared transcript volume as costs to justify, not default sources of quality.

## Actionable findings

| Finding | Direct evidence | Software-engineering inference | Quality / boundary |
|---|---|---|---|
| Decompose by low-coupling work units, not by role labels alone. | HTN complexity changes with task ordering and non-primitive-task restrictions ([Erol et al. 1994](https://euro.ecom.cmu.edu/program/courses/tcr854/2001/readings/Hendler_Nau_AAAI-94.pdf)); decentralized partial-information planning is NEXP-hard even for two agents ([Bernstein et al. 2002](https://pubsonline.informs.org/doi/10.1287/moor.27.4.819.297)). | Parallelize components with stable contracts; retain one reasoning locus for chains where each decision changes the next. | **High** theory; transfer is inference. |
| Make allocation explicit and revisable. | Contract Net uses announcement, bidding, award, and reporting to allocate tasks under distributed capabilities ([Smith 1980](https://www.eecs.ucf.edu/~lboloni/Teaching/EEL6788_2008/papers/The_Contract_Net_Protocol_Dec-1980.pdf)). | Give delegated coding tasks acceptance criteria and a return artifact; permit reassignment when prerequisites or capability assumptions fail. | **High** protocol evidence; modern LLM transfer untested. |
| Maintain a joint plan, not just parallel TODOs. | SharedPlans requires agreement on a recipe, commitments to collaborators' success, and coordinated subsidiary plans under partial knowledge ([Grosz & Kraus 1996](https://u.cs.biu.ac.il/~sarit/data/articles/20.pdf)). | Record shared objective, interfaces, dependencies, ownership, and completion/abandonment conditions before parallel execution. | **High** formal foundation; implementation is inference. |
| Prefer structured artifacts over unconstrained chat. | MetaGPT uses SOPs and intermediate structured outputs; ChatDev uses phase/subtask chat chains ([Hong et al. 2024](https://proceedings.iclr.cc/paper_files/paper/2024/hash/6507b115562bb0a305f1958ccc87355a-Abstract-Conference.html); [Qian et al. 2024](https://aclanthology.org/2024.acl-long.810/)). | Handoffs should be diffs, tests, schemas, decisions, and evidence summaries with explicit consumers. | **Medium**; peer-reviewed but synthetic software tasks. |
| Share selected state; do not assume transcript sharing equals common understanding. | Blackboard architecture centralizes evolving solution state ([Nii 1986](https://onlinelibrary.wiley.com/doi/10.1609/aimag.v7i2.537)); memory retrieval/reflection/planning components affected behavior ([Park et al. 2023](https://dl.acm.org/doi/10.1145/3586183.3606763)). | Use an authoritative project state plus per-agent local context; summarize decisions and verified facts rather than copying all dialogue. | **Medium** for LLM transfer. |
| Require agents to surface unique evidence before convergence. | HiddenBench agents underused distributed facts; an exchange-then-decide protocol improved all three tested model families in an 18-task ablation ([Li et al. 2026](https://arxiv.org/abs/2505.11556)). | Before integration, require each agent to report new evidence, uncertainty, and one challenge to the current plan. | **High** phenomenon, **medium** intervention due small ablation. |
| Do not use debate as a substitute for a correctness oracle. | Majority voting explained most gains of multi-agent debate across seven NLP benchmarks ([Choi et al. 2025](https://papers.nips.cc/paper_files/paper/2025/hash/934252acd87f254d5d4672fbde283bd2-Abstract-Conference.html)). | Prefer executable tests, static analysis, traceable sources, or human review over “agent consensus.” | **High** tested setting; repository transfer is inference. |
| Centralize integration and verification when outputs converge. | MAST finds verification/termination failures across systems ([Cemri et al. 2025](https://arxiv.org/abs/2503.13657)); controlled scaling work reports lower error amplification with centralized coordination ([Kim et al. 2026](https://arxiv.org/abs/2512.08296)). | One coordinator should own merge order, conflict resolution, system tests, and stop decisions; verifier independence is desirable but not sufficient. | **High** taxonomy; **medium** scaling result (preprint/vendor-affiliated). |
| Stop adding agents when the task is sequential, tool-dense, or already solved reliably by one strong agent. | All tested MAS variants degraded sequential planning by 39–70%; tool-heavy tasks incurred greater coordination overhead under matched budgets ([Kim et al. 2026](https://arxiv.org/abs/2512.08296)). | Benchmark one-agent success first; add agents only for separable search, independent verification, or distinct context partitions. | **Medium**: controlled but preprint and cross-domain. |

## Annotated bibliography

### 1. The Contract Net Protocol: High-Level Communication and Control in a Distributed Problem Solver

- **Authors / organization:** Reid G. Smith; Stanford/Schlumberger research lineage.
- **Date:** December 1980.
- **URL:** https://www.eecs.ucf.edu/~lboloni/Teaching/EEL6788_2008/papers/The_Contract_Net_Protocol_Dec-1980.pdf
- **Source / evidence type:** Peer-reviewed *IEEE Transactions on Computers* protocol paper with a distributed-sensing demonstration.
- **Evidence quality:** **High** for task-allocation concepts.
- **Flags:** Historical non-LLM system; implementation assumptions differ from probabilistic language agents.
- **Finding:** A manager announces a task, potential contractors bid, the manager awards a contract, and results are reported. Negotiation distributes control and enables capability-sensitive allocation without a fixed central executor.

### 2. Blackboard Systems, Part One: The Blackboard Model of Problem Solving and the Evolution of Blackboard Architectures

- **Authors / organization:** H. Penny Nii; Stanford Knowledge Systems Laboratory.
- **Date:** Summer 1986.
- **URL:** https://onlinelibrary.wiley.com/doi/10.1609/aimag.v7i2.537
- **Source / evidence type:** Peer-reviewed *AI Magazine* architecture review grounded in implemented systems including HEARSAY-II.
- **Evidence quality:** **High** for the historical architecture; **medium** for LLM-agent transfer.
- **Flags:** Historical; not an experiment comparing modern agent-memory strategies.
- **Finding:** Blackboard systems coordinate heterogeneous knowledge sources through a shared, incrementally updated solution space plus control mechanisms. This provides a durable alternative to sending every intermediate thought directly among all agents.

### 3. HTN Planning: Complexity and Expressivity

- **Authors / organization:** Kutluhan Erol, James A. Hendler, Dana S. Nau; University of Maryland.
- **Date:** 1994.
- **URL:** https://euro.ecom.cmu.edu/program/courses/tcr854/2001/readings/Hendler_Nau_AAAI-94.pdf
- **Source / evidence type:** Peer-reviewed AAAI formal complexity analysis.
- **Evidence quality:** **High**.
- **Flags:** Theoretical worst-case results; not an LLM evaluation.
- **Finding:** HTN decomposition is more expressive than STRIPS-style planning, and decidability/complexity depend strongly on ordering and constraints on non-primitive tasks. Hierarchy is therefore a representational commitment, not a free reduction in difficulty.

### 4. Collaborative Plans for Complex Group Action

- **Authors / organization:** Barbara J. Grosz (Harvard University), Sarit Kraus (Bar-Ilan University / University of Maryland).
- **Date:** 1996.
- **URL:** https://u.cs.biu.ac.il/~sarit/data/articles/20.pdf
- **Source / evidence type:** Peer-reviewed *Artificial Intelligence* journal formalism (SharedPlans).
- **Evidence quality:** **High**.
- **Flags:** Formal model; empirical effectiveness in LLM systems was not tested.
- **Finding:** Collaborative action requires more than coordinated individual actions: agents need agreement on a recipe, intentions that partners' constituent actions succeed, and compatible individual/subgroup plans. The formalism explicitly accommodates partial knowledge and evolving incomplete plans.

### 5. The Complexity of Decentralized Control of Markov Decision Processes

- **Authors / organization:** Daniel S. Bernstein, Robert Givan, Neil Immerman, Shlomo Zilberstein; University of Massachusetts Amherst and Purdue University.
- **Date:** 1 November 2002.
- **URL:** https://pubsonline.informs.org/doi/10.1287/moor.27.4.819.297
- **Source / evidence type:** Peer-reviewed *Mathematics of Operations Research* complexity theorem.
- **Evidence quality:** **High**.
- **Flags:** Formal Dec-MDP/Dec-POMDP setting; does not measure LLM agents.
- **Finding:** Finite-horizon decentralized control is NEXP-hard even for two agents; under standard complexity assumptions it can require superexponential time. Partial observability and distributed control create a fundamental difficulty beyond centralized planning.

### 6. ReAct: Synergizing Reasoning and Acting in Language Models

- **Authors / organization:** Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao; Princeton University and Google Research.
- **Date:** ICLR 2023.
- **URL:** https://arxiv.org/abs/2210.03629
- **Source / evidence type:** Peer-reviewed ICLR experiments across question answering and interactive decision tasks.
- **Evidence quality:** **High** for single-agent reasoning/action interleaving; **medium** for MAS design.
- **Flags:** Primarily single-agent; transfer to multi-agent software engineering is inferential.
- **Finding:** Interleaving reasoning traces with environment actions lets observations update plans and helps handle exceptions. This grounds the view that agent plans should be revised from tool feedback rather than executed as static scripts.

### 7. Reflexion: Language Agents with Verbal Reinforcement Learning

- **Authors / organization:** Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, Shunyu Yao; Northeastern University, MIT, and Princeton University.
- **Date:** NeurIPS 2023.
- **URL:** https://papers.nips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html
- **Source / evidence type:** Peer-reviewed NeurIPS experiments on sequential decision making, programming, and reasoning.
- **Evidence quality:** **High** for episodic verbal feedback; **medium** for shared multi-agent memory.
- **Flags:** Mostly single-agent self-reflection; some benchmarks have since become easier for frontier models.
- **Finding:** Converting environmental or simulated feedback into compact verbal reflections stored for subsequent attempts improved performance over baseline agents. The result supports retaining distilled failure lessons, not raw history alone.

### 8. Generative Agents: Interactive Simulacra of Human Behavior

- **Authors / organization:** Joon Sung Park, Joseph C. O'Brien, Carrie J. Cai, Meredith Ringel Morris, Percy Liang, Michael S. Bernstein; Stanford University and Google Research.
- **Date:** 29 October 2023 (UIST 2023).
- **URL:** https://dl.acm.org/doi/10.1145/3586183.3606763
- **Source / evidence type:** Peer-reviewed ACM UIST system study with component ablations.
- **Evidence quality:** **Medium** for memory architecture.
- **Flags:** Evaluation target was believable simulated behavior, not task correctness or software delivery; partly Google-affiliated.
- **Finding:** An architecture combining a natural-language memory stream, relevance/recency/importance retrieval, reflection, and planning produced more believable individual and emergent behavior; ablations indicated each component contributed. It demonstrates selective retrieval and synthesis, not a shared-context guarantee.

### 9. Improving Factuality and Reasoning in Language Models through Multiagent Debate

- **Authors / organization:** Yilun Du, Shuang Li, Antonio Torralba, Joshua B. Tenenbaum, Igor Mordatch; MIT and OpenAI.
- **Date:** ICML 2024.
- **URL:** https://proceedings.mlr.press/v235/du24e.html
- **Source / evidence type:** Peer-reviewed ICML controlled experiments on math, strategic reasoning, and factual generation.
- **Evidence quality:** **Medium**.
- **Flags:** OpenAI-affiliated author; mostly static benchmarks; debate and aggregation choices limit generalization.
- **Finding:** Multiple model instances proposing and revising answers over debate rounds improved selected reasoning and factuality measures over the paper's baselines. Later work below shows that much apparent benefit can come from ensembling rather than communication.

### 10. AgentVerse: Facilitating Multi-Agent Collaboration and Exploring Emergent Behaviors

- **Authors / organization:** Weize Chen, Yusheng Su, Jingwei Zuo, Cheng Yang, Chenfei Yuan, Chi-Min Chan, Heyang Yu, Yaxi Lu, Yi-Hsin Hung, Chen Qian, Yujia Qin, Xin Cong, Ruobing Xie, Zhiyuan Liu, Maosong Sun, Jie Zhou; Tsinghua University, BUPT, and Tencent.
- **Date:** ICLR 2024.
- **URL:** https://proceedings.iclr.cc/paper_files/paper/2024/hash/578e65cdee35d00c708d4c64bce32971-Abstract-Conference.html
- **Source / evidence type:** Peer-reviewed ICLR multi-domain framework evaluation.
- **Evidence quality:** **Medium**.
- **Flags:** Tencent-affiliated; benchmarks span heterogeneous tasks and do not isolate all architecture confounds.
- **Finding:** AgentVerse separates expert recruitment, collaborative decision making, action execution, and evaluation, and reports gains over a single agent on several tested tasks. It is evidence for modular orchestration patterns, not for universal multi-agent superiority.

### 11. MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework

- **Authors / organization:** Sirui Hong, Mingchen Zhuge, Jonathan Chen, Xiawu Zheng, Yuheng Cheng, Jinlin Wang, Ceyao Zhang, Zili Wang, Steven Ka Shing Yau, Zijuan Lin, Liyang Zhou, Chenyu Ran, Lingfeng Xiao, Chenglin Wu, Jürgen Schmidhuber; multi-institution team led by DeepWisdom/KAUST.
- **Date:** ICLR 2024.
- **URL:** https://proceedings.iclr.cc/paper_files/paper/2024/hash/6507b115562bb0a305f1958ccc87355a-Abstract-Conference.html
- **Source / evidence type:** Peer-reviewed ICLR framework paper and software-generation evaluation.
- **Evidence quality:** **Medium**.
- **Flags:** Framework authors evaluate their own system; benchmark and coherence judgments are narrower than repository-level correctness.
- **Finding:** MetaGPT encodes standard operating procedures as prompt sequences, assigns specialized roles, and requires structured intermediate artifacts. It directly addresses cascading inconsistencies from naively chaining LLM outputs, while not proving that role multiplicity itself causes the gains.

### 12. ChatDev: Communicative Agents for Software Development

- **Authors / organization:** Chen Qian, Wei Liu, Hongzhang Liu, Nuo Chen, Yufan Dang, Jiahao Li, Cheng Yang, Weize Chen, Yusheng Su, Xin Cong, Juyuan Xu, Dahai Li, Zhiyuan Liu, Maosong Sun; Tsinghua University, University of Sydney, BUPT, and ModelBest.
- **Date:** August 2024.
- **URL:** https://aclanthology.org/2024.acl-long.810/
- **Source / evidence type:** Peer-reviewed ACL framework and controlled ablation/evaluation paper.
- **Evidence quality:** **Medium**.
- **Flags:** Vendor-affiliated author; generated small applications, not long-lived production repositories.
- **Finding:** ChatDev decomposes development into sequential design, coding, review, and testing subtasks, with two-agent instructor/assistant dialogues and clarification prompts. The paper found natural-language exchanges useful for design and code-language exchange useful for debugging within its task set.

### 13. LLM-Coordination: Evaluating and Analyzing Multi-agent Coordination Abilities in Large Language Models

- **Authors / organization:** Saaket Agashe, Yue Fan, Anthony Reyna, Xin Eric Wang; University of California Santa Cruz.
- **Date:** April 2025.
- **URL:** https://aclanthology.org/2025.findings-naacl.448/
- **Source / evidence type:** Peer-reviewed Findings of NAACL benchmark: four pure-coordination games and 198 CoordQA questions.
- **Evidence quality:** **High** for the tested coordination constructs.
- **Flags:** Games are abstractions rather than software projects; several conclusions depend on simulated partners.
- **Finding:** LLM agents coordinated relatively well when choices depended on environmental variables, but struggled when success required considering partners' beliefs and intentions; joint planning and theory-of-mind reasoning remained weak. Zero-shot coordination with unseen partners was comparatively robust.

### 14. Why Do Multi-Agent LLM Systems Fail?

- **Authors / organization:** Mert Cemri, Melissa Z. Pan, Shuyi Yang, Lakshya A. Agrawal, Bhavya Chopra, Rishabh Tiwari, Kurt Keutzer, Aditya Parameswaran, Dan Klein, Kannan Ramchandran, Matei Zaharia, Joseph E. Gonzalez, Ion Stoica; UC Berkeley and collaborators.
- **Date:** NeurIPS 2025 Datasets and Benchmarks track; manuscript v3 dated 26 October 2025.
- **URL:** https://arxiv.org/abs/2503.13657
- **Source / evidence type:** Peer-reviewed failure-taxonomy study; 1,642 annotated traces from seven MAS frameworks, with expert agreement studies and released data.
- **Evidence quality:** **High** for taxonomy and observed failure incidence; **medium** for cross-system causal claims.
- **Flags:** Most large-scale labels use a validated LLM annotator; frameworks were run on different benchmarks and their failure rates are not directly comparable.
- **Finding:** Fourteen failure modes cluster into specification/system-design failures, inter-agent misalignment, and verification/termination. Clearer prompts or topology changes were inconsistent fixes; systems with explicit verification had fewer failures, but verifiers still missed substantive defects.

### 15. Debate or Vote: Which Yields Better Decisions in Multi-Agent Large Language Models?

- **Authors / organization:** Hyeong Kyu Choi, Xiaojin (Jerry) Zhu, Yixuan (Sharon) Li; University of Wisconsin–Madison.
- **Date:** NeurIPS 2025.
- **URL:** https://papers.nips.cc/paper_files/paper/2025/hash/934252acd87f254d5d4672fbde283bd2-Abstract-Conference.html
- **Source / evidence type:** Peer-reviewed NeurIPS experiments across seven NLP benchmarks plus a formal stochastic model.
- **Evidence quality:** **High** for the studied debate protocols.
- **Flags:** Mostly question-answering/static tasks; the martingale theorem depends on the stated belief-update assumptions and is not a universal impossibility result.
- **Finding:** Majority voting over initial independent answers matched or exceeded multi-round debate in most tested settings. Under the paper's model, ordinary debate preserves expected belief in the correct answer; targeted mechanisms that weight correct signals are needed to make communication add value.

### 16. Towards a Science of Scaling Agent Systems

- **Authors / organization:** Yubin Kim, Ken Gu, Chanwoo Park, Chunjong Park, Samuel Schmidgall, A. Ali Heydari, Yao Yan, Zhihan Zhang, Yuchen Zhuang, Yun Liu, Mark Malhotra, Paul Pu Liang, Hae Won Park, Yuzhe Yang, Xuhai Xu, Yilun Du, Shwetak Patel, Tim Althoff, Daniel McDuff, Xin Liu; Google Research, Google DeepMind, and MIT.
- **Date:** arXiv v3, 8 April 2026.
- **URL:** https://arxiv.org/abs/2512.08296
- **Source / evidence type:** Controlled multi-model, multi-benchmark preprint; 260 configurations, five topologies, three model families, matched tools/prompts/compute, including SWE-bench Verified and Terminal-Bench.
- **Evidence quality:** **Medium**.
- **Flags:** **Preprint-only and vendor-sponsored/affiliated**; the cross-validated model explains a limited share of variance and software-specific results should be inspected separately before adoption.
- **Finding:** Architecture–task fit, not agent count, predicted benefit: +80.8% on a decomposable financial task but −39% to −70% on sequential planning; tool density imposed overhead, and centralized verification reduced measured trace-error amplification from 17.2× to 4.4×. The architecture selector chose the best topology for 87% of held-out configurations in the study.

### 17. Systematic Failures in Collective Reasoning under Distributed Information in Multi-Agent LLMs (HiddenBench)

- **Authors / organization:** Yuxuan Li, Aoi Naito, Hirokazu Shirado; Carnegie Mellon University, Institute of Science Tokyo, and JSPS.
- **Date:** ICML 2026; manuscript v4 dated 13 May 2026.
- **URL:** https://arxiv.org/abs/2505.11556
- **Source / evidence type:** Peer-reviewed ICML benchmark study: 65 hidden-profile tasks, 15 frontier models, controlled information distribution, human/task validation, and protocol ablations.
- **Evidence quality:** **High** for the coordination failure; **medium** for the mitigation ablation.
- **Flags:** Many tasks were generated then filtered with GPT-4.1; the structured-protocol ablation used 18 tasks, four agents, three models, and five runs.
- **Finding:** Multi-agent accuracy with distributed information averaged 30.1% versus 80.7% for a single agent with complete information; adding agents or discussion did not close the gap and could worsen it. Requiring agents to exchange decision-relevant unique facts, challenge the front-runner, then summarize uncertainty improved accuracy sharply in the small ablation.

### 18. A Survey on LLM-Based Multi-Agent Systems: Workflow, Infrastructure, and Challenges

- **Authors / organization:** Xinyi Li, Sai Wang, Siqi Zeng, Yu Wu, Yi Yang; Wuhan University and Zhejiang University.
- **Date:** 8 October 2024.
- **URL:** https://doi.org/10.1007/s44336-024-00009-2
- **Source / evidence type:** Peer-reviewed open-access review in *Vicinagearth*.
- **Evidence quality:** **Medium** as a coverage/taxonomy source; not used as causal evidence.
- **Flags:** Secondary source; rapidly dated in a fast-moving field and includes many preprints among the works surveyed.
- **Finding:** The review organizes LLM-MAS work into profile, perception, self-action (including memory/reasoning/planning), mutual interaction, and evolution, and separates problem-solving from world-simulation applications. It was used here to check that major architectural dimensions were not omitted; all material efficacy and failure claims in this memo are tied to original studies above.

## Evidence-to-inference boundary

Robust foundations support explicit allocation, structured decomposition, shared-state representations, commitments/termination conventions, and objective verification. Emerging LLM evidence supports centralized verification for convergent work and structured information exchange under asymmetry. It does **not** yet establish a universal optimal agent count, prove that human job-title roleplay adds value, or show that unconstrained debate improves repository-level correctness. Those decisions require task-specific measurements against a strong single-agent baseline.
