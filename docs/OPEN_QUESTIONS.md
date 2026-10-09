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
  Obsolete schedules were removed in the owner-directed cleanup;
  [history](history/README.md) links their pre-cleanup source. Captures remain intact.
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

[PR #5](https://github.com/500ft/evidence-sufficiency-benchmark/pull/5) contains only CodeQL,
Dependency Review and Dependabot configuration. Its diff and recorded successful
checks were inspected on 2026-10-06 at head
`f27458001d304cc179f05a1b99fef4bf6866d300`. Live inspection on 2026-10-07
confirmed that PR #5 and the substantive pivot [PR #10](https://github.com/500ft/evidence-sufficiency-benchmark/pull/10)
are merged. CI maintenance is not research evidence.
No new review of its action versions or rerun of its historical checks is claimed.

## AUD-4: dependency plan and cleanup adoption, 2026-10-07

The owner requested an active roadmap with no dates or schedule estimates,
prerequisites and completion evidence, plus actual removal of obsolete active
code and documentation. [ROADMAP.md](../ROADMAP.md) adopts that dependency plan
and is the sole active task list. This implements section 1 of the external
`ROADMAPS_20261007.md` handoff with the project-specific corrections.

The benchmark target in the roadmap includes its published-reference cases.
It remains subject to independent qualification. Holdout freezing moves before
reviewer or policy tuning. Applicability and setup plus execution costs are
required; defects must match the physics. The existing public bar example is
development evidence, not a qualified claim-specific or hidden benchmark.

The cleanup removes the old capture CLI, obsolete schedules, prompt-hardening
instructions and active requests to fill old capture slots. The
[history index](history/README.md) records the consumer checks and specific
retentions. This adoption does not authorize running the proposed experiments.

## AUD-5: bounded M1.1 implementation

The owner authorized implementation of the axial-bar claim contract and a
scoped review PR. The [executed claim matrix](../reports/claim-sufficiency/matrix.md)
separates artifact correctness from evidence sufficiency. It demonstrates
compatible explanations with opposite deflection decisions while resolving
stress agreement under force control. The
[derivation and tests](../studies/evidence_sufficiency/claims/README.md) include
the loading convention and decision boundaries. The original full-tuple
development result remains reproducible.

This authorization ends at M1.1. It supplies no independent problem review,
source reuse rights, model spending, host execution or reserved-case expansion.

## Remaining inputs and decisions

- Next uncompleted technical step: M1.2's independently qualified problems and
  review. M1.1 adds claim-relative development labels for the existing bar;
  no additional base problem or reviewer pilot was executed.
- Independent collaborator review and reviewer availability remain unresolved.
  Stiffness cross-checks are software verification, not a second human review.
- Model pilot execution and resources require separate owner authorization.
- Human comparison is optional and requires the institution's determination
  and separate authorization before recruitment.
- Host CAD/FEA execution, physical study, hardware, funding, purchases, naming
  and publication have no new approval here. Useful CAD position checks and
  latency questions remain outside this cleanup; see [CAD limitations](cad_fea_loop.md).
- Reserved families must remain unexposed until the registered evaluation.
  No existing holdout was opened or used in this task.
