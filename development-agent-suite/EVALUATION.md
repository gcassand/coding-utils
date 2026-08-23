# Evaluation guide

Agent definitions are hypotheses. Evaluate them against a matched single-agent baseline on representative private or time-split tasks before standardizing their use.

## Offline checks

Run:

```sh
python3 scripts/validate_agent_suite.py
python3 -m unittest discover -s tests
```

These checks establish adapter parity and policy invariants, not behavioral quality.

## Behavioral fixtures

Fixtures under `development-agent-suite/evals/` describe seven representative decisions. For each fixture, run:

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

