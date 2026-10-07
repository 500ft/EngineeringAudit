# Roadmap: evidence sufficiency

Updated 2026-10-06. This is the repository's active plan.

## Adopted question

Can an automated reviewer recognize when passing evidence cannot verify the
claimed property, and select checks that resolve it within a fixed budget?

The owner authorized this bounded software implementation on 2026-10-06.
[The decision record](docs/OPEN_QUESTIONS.md) limits adoption to this question
and records superseded work. Physical readiness and model spending are not part
of that decision.

## Executed current step

The [first result](reports/evidence-sufficiency/matrix.md) is a development
verification example for a uniform axial bar under force and displacement
loading. The full check menu was executed for every artifact. Independent
closed-form answers and a separately assembled stiffness system check labels
before any selector is scored. Correct controls, benign partition changes,
nuisance density changes and seeded faults are included. The comparator smoke
test isolates policy inputs and reports errors, abstention and cost at matched
coverage. It makes no claim of policy superiority on unseen defects.

The [FEA correction](reports/fea-interpretation.json) separates completion,
reference agreement and mesh stability using preserved original records. CAD
machinery and previous calculation-verifier results remain accessible through
[history](docs/history/README.md).

## Finish line and remaining work

A benchmark result needs independently qualified problem specifications,
predeclared check costs, a complete outcome matrix, and a frozen evaluation
protocol with whole defect families held out before selection-policy tuning.
Report errors at matched coverage and cost, and coverage at matched error;
keep seeded and natural failures separate and cluster any uncertainty by base
problem. Two loading configurations of one bar are not independent base problems.

Next: qualify a genuinely different analytic family with a separate derivation
and implementation, then grow toward the v2 target only where reference validity
and coverage justify it. A NAFEMS or Code_Aster case needs the exact geometry,
constraints, load, stress component and reference rights/source checked first.
A published scalar alone is insufficient. No such case is claimed here.

Before a confirmatory result, freeze reserved defect families and opaque reviewer
inputs. The published development matrix cannot serve as a hidden evaluation
set. Candidate LLM policies remain optional until references and the holdout
protocol are independently reviewed; no model calls or recruitment are planned
in this task. If a fixed checklist matches the candidate on held-out families,
report that result. If labels disagree, stop policy evaluation and fix references.

The old wild-capture schedule is superseded, not completed. See
[its preserved roadmap](docs/history/roadmap-before-v2-2026-10-06.md).
