# Limitations

This file states what engineering-audit's current evidence does and does not
support. It exists so that no summary of this project has to guess. Wherever a
claim about engineering-audit is made (README, resume line, talk slide), it
should be checkable against this list.

## 1. The real-world failures are elicited, not found in the wild

The gold captures are verbatim model outputs with hash-verified provenance —
but they were produced by **challenge-protocol prompts written by the operator
and run deliberately** (`capture_protocol: challenge`). No committed case yet
records a failure encountered during someone's real engineering workflow.

- Supported claim: *"engineering-audit detected genuine, reproducible
  calculation failures in unmodified frontier-model outputs, captured under a
  pre-registered protocol with cryptographic provenance."*
- Unsupported claim: *"engineering-audit has caught model failures in the
  wild."*

The gap matters because elicited prompts are chosen where failure is likely;
wild usage samples a different distribution.

## 2. Domain coverage is narrow

Verified failure detection currently covers thin-wall pressure-vessel hoop
stress, axial stress, and finite-width holed-plate stress concentration
(Kt-aware, FM-04). The taxonomy in `docs/failure_taxonomy.md` is much larger
than the implemented checker set. Beam bending, buckling, contact, bolted
joints, and fatigue are scoped but not implemented; claims about "mechanical
engineering calculations" in general are aspirational beyond the three
implemented families.

## 3. Ground truth is closed-form first

Expected results trace to standard closed-form solutions (with the tolerance
policy in `docs/tolerance_policy.md`) and, for stress concentration, to
Peterson/Roark Kt fits. In-repo FEA provides an approximate comparison, not
independent validation of those fits. There is no
physical-test ground truth anywhere in the benchmark. Where a problem admits
defensible variant conventions (inner-radius vs mean-radius), the rubric
accepts the variant rather than forcing one number.

## 4. Capture metadata is partly self-reported

Model identity/version in `source.json` is recorded from the serving CLI and
the model's own self-report (`metadata_source: self_report`). Raw output bytes
are hash-verified; the *identity* of the model that produced them relies on
the toolchain being honest. Temperature was not controlled (`temperature:
null`), so per-prompt failure rates are single-draw observations, not
probabilities.

## 5. Sample sizes are small

10 Haiku runs, 20 Codex runs, one prompt battery, one language (English), one
unit system (SI). Per-model comparisons ("model X fails where model Y passes")
are existence results, not statistics.

## 6. CAD and FEA exist, with separate evidence boundaries

`cadloop/` records parametric re-drive, volume checks, STEP/IGES exports and
MAPDL linear static plate solves. The [original records](cadloop/evidence/README.md)
and [FEA runs](cadloop/fea/runs) remain unchanged. The latest runner includes a
stress-reference comparison and contour rendering. No host run was performed
for this correction.

The [derived interpretation](reports/fea-interpretation.json) separates solver
completion, agreement with the declared correlation tolerance, and mesh stability.
The global sweep's final peak change exceeds the reporting criterion. The
hole-refined records each contain one mesh; their close peaks under different
global and local mesh settings do not establish systematic convergence. The
retrospective stability criterion is not a discretization error bound.

A scalar stress match cannot establish material correctness, displacement
accuracy, all boundary conditions or physical validity. The reference correlation
and finite restrained solid have different modeling assumptions. The historical
load is arbitrary, so its yield ratio cannot establish service readiness. Volume
alone does not constrain feature location, and host timing remains unstable.
See [FEA scope](cadloop/fea/README.md) and [CAD loop](docs/cad_fea_loop.md).

## 7. The verifier is narrow by design

Checks are limited to what is independently recomputable. engineering-audit does
not judge modeling choices, load-case selection, or safety-factor policy — the
places where real engineering judgment lives. A calculation can pass every
engineering-audit check and still be the wrong calculation for the design.

## 8. Evidence-sufficiency pilot scope

The [new result](reports/evidence-sufficiency/matrix.md) uses seeded artifacts in
one analytic family with different loading conventions. It is a verification
example, not physical validation or a completed independent-problem benchmark.
Check costs are declared abstract tokens. Labels are cross-checked by a separate
stiffness assembly, but no second human review is claimed. The published matrix
is development data; no hidden-family evaluation or natural LLM pilot was run.
The selected faults illustrate sensitivity and cannot establish a general policy
ranking. See [the protocol](studies/evidence_sufficiency/README.md).
