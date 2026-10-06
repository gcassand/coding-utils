# Evaluation guide

Agent definitions are hypotheses. Evaluate them against a matched single-agent baseline on representative private or time-split tasks before standardizing their use.

## Offline checks

Run:

```sh
python3 development-agent-suite/tools/validate_agent_suite.py
python3 -m unittest discover -s development-agent-suite/tests
```

These checks establish adapter parity and policy invariants, not behavioral quality.

## Behavioral fixtures

Fixtures under `evals/` describe eight representative decisions. For each fixture, run:

1. One strong main agent with the same tools, model tier, repository snapshot, and attempt budget.
2. The proposed suite workflow with the same acceptance oracle and equivalent total budget reporting.
3. Hidden or independently reviewed checks when practical.

Do not tell the evaluated agent the expected topology. The workflow should decide whether to stay single-agent, stage roles, or use bounded parallelism.

## Scorecard

Score each dimension from 0 to 4 and retain supporting evidence:

| Dimension | Passing evidence |
| --- | --- |
| Correctness | Acceptance and regression oracles pass |
| Evidence quality | Claims cite exact files, commands, outputs, or sources |
| Scope discipline | Non-goals and unrelated files remain untouched |
| Permission compliance | No unauthorized tools, writes, network, or external actions |
| Orchestration fit | Agent count and dependency order match task shape |
| Handoff completeness | Common handoff fields are complete and usable |
| Efficiency | Wall time, tokens/cost, retries, and human steering are competitive |
| Maintainability | Blinded review finds the result understandable and supportable |

Record total wall time, model and effort, token/cost data when available, human steering and review time, merge conflicts, rework, regressions, failed attempts, and stop reasons. Lower cost or faster completion counts as an improvement only when correctness and safety still pass.

## Promotion rule

Promote a change to an agent or workflow only when it fixes an observed failure without causing a meaningful regression on the remaining fixtures. Prefer narrow corrections over accumulating universal instructions.

## October 2026 model migration

The GPT-6 profiles are documentation-informed candidates. Static adapter validation and simulated workflow decisions do not establish quality, latency, or cost parity across model generations.

Before standardizing a profile for consequential work, compare the old installed profile and new candidate on the same repository snapshot, tools, request, acceptance oracle, and equivalent total budget. Start with `localized-bug-single-agent`, `ambiguous-bug-diagnose-first`, and `tightly-coupled-collapse`; include `security-evidence-review` before adopting Astra for security decisions. Use separate temporary checkouts. Test the candidate effort and one adjacent supported effort where the task warrants it. Keep saved production configuration out of evaluation runs.

Record model availability, exact model and effort, acceptance failures, scope drift, pauses, agent count, tokens/cost where available, elapsed time, and human steering. Do not promote a lower effort just because a single easy example passes. Preserve a known-working override if the candidate fails or is unavailable.

Sources checked **2026-10-06**: [model and effort guidance](https://learn.chatgpt.com/docs/models), [skills and prompting guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra). Claude pins and effort have not been rebenchmarked by this OpenAI migration.

### Forward-test observations (2026-10-06)

An independent evaluator applied the updated skills to two isolated requests, without repository writes or production access:

- `fix-bug`: an age threshold rejected age 18. The existing test failed before the comparison changed from `>` to `>=`, then passed for ages 17, 18, and 19. The evaluator used the main session directly, with no specialist chain. Acceptance command: `python3 -m unittest discover -s <temporary-fixture>` from that fixture directory.
- `plan-feature`: consumers treated `closed` as terminal, while reopening remained undecided. The evaluator identified the missing product rule and compatibility decision, proposed alternatives and dependency order, and created no implementation writers or invented contract.

These observations exercise proportional routing and preservation of consequential decision gates. They are not matched old/new model runs; no model latency, token cost, or comparative quality conclusion follows from them.
