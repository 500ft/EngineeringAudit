# Decisions and open questions

## AUD-1: bounded software adoption, 2026-10-06

Adopt the evidence-sufficiency question in [ROADMAP.md](../ROADMAP.md), with the
[executed result](../reports/evidence-sufficiency/matrix.md) in the same change.
Owner instruction: implement the reviewed v2 pivot and update the repository's
questions, figures and obsolete material while keeping useful work. The reviewed
handoff permits an independently checkable minimal result before expansion.
This records no hardware readiness, purchases, funding, human recruitment or
permission for external model spending.

## Superseded active questions

- The old priority to collect wild failures and execute the week-by-week v1
  schedule is superseded by AUD-1. It is not answered by challenge captures.
  [Original roadmap](history/roadmap-before-v2-2026-10-06.md) and
  [v1 plan](v1_plan.md) are history; captures remain intact.
- FEA implementation and parametric re-drive are recorded capabilities, so
  their old "not implemented" questions are closed with links to
  [CAD records](../cadloop/evidence/README.md) and
  [FEA interpretation](../reports/fea-interpretation.json).
- Mesh convergence remains unresolved for the hole-refined runs. Their close
  peaks under simultaneously changed global and local meshes are evidence of
  agreement between those discretizations, not an error bound.

## AUD-2: working copy

Use this clean isolated clone. The separate Developer working copy, including
its modified JSON and untracked instructions, was neither read nor changed.

## AUD-3: PR #5 review

[PR #5](https://github.com/500ft/engineering-audit/pull/5) contains only CodeQL,
Dependency Review and Dependabot configuration. Its diff and recorded successful
checks were inspected on 2026-10-06 at head
`f27458001d304cc179f05a1b99fef4bf6866d300`. It remains open and untouched.
It is neither a dependency nor research evidence for this main-based change.
No new review of its action versions or rerun of its historical checks is claimed.

## Remaining qualification

- Independently review the problem specifications and labels before expansion
  or an external reviewer study. Current stiffness cross-checks are software
  verification, not a second human's review.
- Add a genuinely distinct base problem before treating variation as replication.
- Register unseen defect families and reviewer exposure rules before a held-out
  evaluation. No existing holdout was opened or used in this task.
- CAD feature-position checks and host latency remain useful engineering issues,
  outside this software result. See [CAD limitations](cad_fea_loop.md).
