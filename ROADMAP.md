# Roadmap: evidence sufficiency

## Question and finish line

Can a reviewer recognize when passing evidence cannot verify a specific claim,
and select the least-cost applicable check or combination that settles the
claim within a stated budget?

This is the only active plan. The [owner decision](docs/OPEN_QUESTIONS.md)
authorizes its adoption, repository cleanup and the completed M1.1 software
implementation. Model spending, recruitment, host experiments and publication
require separate authorization.

The core finish line is a reproducible, independently labeled benchmark with
claim-specific decisions, executed check outcomes, cost-matched non-LLM
baselines, a qualified reviewer pilot if separately authorized, and a write-up
whose claims match the completed evaluation. Without the pilot, the deliverable
is explicitly a benchmark and baseline result; reviewer performance remains
unanswered. A negative comparison is a valid result.

## Verified foundation: done

Prerequisites were an explicit axial-bar specification, analytic answers and a
separate stiffness implementation. Completion evidence is the public
[development matrix](reports/evidence-sufficiency/matrix.md), its
[source and derivation](studies/evidence_sufficiency/README.md), and
[reference tests](tests/test_evidence_sufficiency.py). The result covers one
mechanics family under force and displacement loading, with correct, benign,
nuisance and seeded-fault artifacts. Its claim is the full response tuple;
its costs are abstract tokens. It is not a private evaluation set or a qualified
measure of total verification effort.

The [FEA interpretation](reports/fea-interpretation.json) and
[record regressions](tests/test_fea_interpretation.py) separately establish
completion, correlation agreement and mesh-stability status. The global sweep
fails the declared stability criterion; refined single-mesh records leave
convergence unknown. Retained CAD/FEA assets are indexed in [history](docs/history/README.md).

## Dependency order

Claim definition -> qualified references and controls -> frozen truth and
reserved families -> full applicable-check matrix -> non-LLM baselines and
verified discriminating checks -> authorized reviewer pilot -> scoped write-up.

Freezing reserved families precedes reviewer or selection-policy tuning.
Extensions depend on the base result and a separate frozen evaluation design.
The M1.1 implementation reuses public development inputs; later milestones
retain their qualification and authorization prerequisites.

## M1. Claim-specific foundation: current, incomplete

**Prerequisite:** the reproduced development foundation above. Start with the
claim definition; do not expand a case whose reference or decision is unresolved.

### M1.1 Define the decision and evidence boundary: done

The [claim contract and derivation](studies/evidence_sufficiency/claims/README.md)
declare observable, units, inclusive absolute tolerance, loading convention,
assumptions and a finite set of implementation explanations. Artifact correctness
is agreement with the independent specification for that claim. Evidence
sufficiency is unanimity of correctness decisions across compatible explanations;
empty support is inconsistent evidence.

**Completion evidence:** the [executed claim matrix](reports/claim-sufficiency/matrix.md)
and [regressions](tests/test_claim_sufficiency.py) show the same force-controlled
stress evidence resolving stress agreement while allowing opposite deflection
decisions. Displacement control changes compatibility as independently derived.
Tests cover boundaries, separate evidence tolerances, name invariance and
stiffness cross-checks. The historical full-tuple result remains reproducible.
This completes the public bar claim definition within the declared explanation
set; independently qualified problems and label review remain incomplete.

### M1.2 Qualify independent problems: next, incomplete

**Prerequisite:** M1.1's claim contract. The provisional benchmark target is
**10 independently qualified base problems in total, including 2 published-reference
problems**, not additional reference cases. This is a coverage target subject
to qualification, not a sample-size justification or a claim that cases exist.

- Select distinct problems across applicable axial, bending, pressure-vessel,
  holed-plate and conduction physics. Parameter variants and loading variants
  do not by themselves create independent problems.
- Derive answers and cross-check using a separately implemented method such as
  stiffness assembly, energy or conservation. Record assumptions and source
  rights. A NAFEMS or Code_Aster candidate needs its exact geometry, load,
  constraints, observable and convention; no isolated published stress value
  is an answer key for an unspecified case.
- Arrange an independent collaborator review with scope and discrepancies
  recorded. Reviewer availability is an unresolved input. Resolve disagreements
  before admitting a problem or evaluating policies.

**Completion evidence:** admitted problem specifications, derivations, independent
cross-checks and review records, with exclusions and actual coverage stated.
Revise the target explicitly if it cannot be qualified; do not fill it with
nominal variants.

### M1.3 Controls, truth and exposure freeze

**Prerequisite:** qualified claims and references from M1.1–M1.2.

- Match faults to applicable physics: elastic modulus for elasticity, thermal
  conductivity for conduction, and boundary, unit or reference-convention
  defects only where meaningful. Include correct controls, benign changes and
  uncertainties that cannot change the claim's decision.
- Define truth from specifications and independent references, never from a
  sensitivity selector or mutation name. For claimed insufficiency, construct
  two allowed explanations consistent with available evidence but giving
  opposite claim decisions. If no such pair exists, do not label the evidence
  insufficient by assertion.
- Register the split and reserve whole defect families before any reviewer or
  policy tuning. Freeze labels, hashes, exposure rules and opaque identifiers;
  keep reserved answers and outcomes unavailable to tuning. Public development
  artifacts stay in development. No existing holdout is to be opened for setup.

**Completion evidence:** reviewed labels, compatible-explanation witnesses,
a frozen manifest and exposure protocol. Unsupported labels stop expansion.

## M2. Outcome matrix and non-LLM baselines: future

**Prerequisite:** M1's qualified specifications, labels and exposure freeze.

### M2.1 Execute the applicable menu

- Declare applicability and costs for candidate stress, displacement, reaction,
  energy, re-drive, mesh-refinement and specification checks. A check can be
  inapplicable; record why instead of treating it as a pass or failure.
- Include setup and execution costs, shared setup reuse and units. Declare how
  costs are measured or estimated and how combinations are charged. The current
  equal-token demonstration is not this cost model.
- Execute every applicable check on every artifact in the outcome-generation
  harness. Preserve failures and inapplicability. Restrict reviewer access to
  purchased observations and protect reserved outcomes from developers tuning
  policies.

**Completion evidence:** complete outcome matrix bound to frozen inputs,
execution records and a reproducible cost ledger, with missing outcomes explicit.

### M2.2 Baselines and discriminating checks

**Prerequisite:** M2.1's outcomes and costs; M1.3's exposure rules remain in force.

- Compare a dependency rule table, sensitivity policy, fixed expert checklist
  and random equal-cost selection on development inputs.
- For each insufficient case, verify that a proposed informative check actually
  distinguishes its two compatible explanations in the executed matrix. Allow
  combinations and multiple equally useful choices. Claim least cost only
  within the declared applicable menu and cost model.
- Score wrong accepts, wrong rejects, useful acceptance, abstention and total
  cost at matched decision coverage/budget. Report coverage at matched error;
  accepting, rejecting or abstaining on everything must not masquerade as a
  useful solution. Keep seeded and natural failures separate.

**Completion evidence:** reproducible baseline scores and witness/check outcomes,
with residual ambiguity reported when no affordable check resolves the claim.
Identical observations with opposite truth require abstention, not guessing.

## M3. Reviewer pilot: future, authorization and review gates unresolved

**Prerequisites:** M1–M2 complete, independent label review, frozen reviewer
exposure and scoring protocol, and owner authorization for the model run and
its resources. The present task authorizes no model calls.

- Implement a claim-and-evidence interface that reveals only purchased checks;
  hide mutation descriptions, filenames and reference answers.
- Qualify the harness on development artifacts. Pin model versions, prompts,
  tool behavior and budgets and retain complete transcripts. Model count and
  pilot size are design targets to justify from coverage and paired variation,
  not a guarantee of power.
- Evaluate under the predeclared split without retuning on reserved families.
  Report per-base-problem results and cluster uncertainty by independent base
  problem where the sample supports it, not by check or time sample.

**Completion evidence:** authorized run records, exposure audit and reproducible
scores against M2 baselines. If the rule table or checklist matches reviewers
at matched coverage and cost, narrow the claim. If references or the harness
fail, repair and requalify before interpreting reviewer performance.

## M4. Write-up: future

**Prerequisites:** M2 complete and M3 complete if reviewer-performance claims are
made. If the pilot remains blocked, explicitly limit the report to the executed
benchmark and baseline result.

- Report the question, admitted cases, references, outcomes, costs, comparisons
  and limitations. Distinguish seed detection from natural failures and software
  verification from physical validation.
- Verify relevant prior work before positioning novelty; candidate literature
  includes MooseBench, ALL-FEM, CADTests and CADEngBench. Inclusion here does not
  establish what those works demonstrate.
- Link figures to executed numeric sources and provide reproduction commands.

**Completion evidence:** a reproducible report with claims bounded by the actual
comparison, including negative results and unresolved scope. Publication remains
an owner decision.

## Conditional extensions

**Prerequisite for each:** the base benchmark result and a separately frozen
extension design before exposure. These are optional, not blockers for the
scoped benchmark and baseline write-up.

- **CAD/FEA:** qualify exact model/reference pairs for mesh stability, material,
  convention or import defects. Reuse retained machinery. Completion evidence
  is independent claim truth and executed applicable checks. Historical solver
  success and stress agreement alone do not supply it; host execution needs
  separate authorization and resources.
- **Broader family transfer:** admit genuinely new families and freeze their
  evaluation before tuning. Completion evidence is a held-out comparison with
  coverage and cost reported. This adds to the initial holdout requirement.
- **Human comparison:** requires the institution's determination and separate
  owner authorization, resources and recruitment protocol before recruitment.
  Completion evidence would be an authorized study and its scoped analysis.

No hardware readiness, funding, purchase, reviewer availability, naming or
publication decision is inferred from this plan. Next work is M1.2; pilot and
physical-study gates remain unresolved in [open questions](docs/OPEN_QUESTIONS.md).
