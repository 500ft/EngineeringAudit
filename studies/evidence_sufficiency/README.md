# Evidence-sufficiency development example

The [executed matrix](../../reports/evidence-sufficiency/matrix.md) demonstrates
that a passing stress check can be blind to an incorrect elastic modulus.
It also exposes a remaining blind spot for the modulus-sensitivity selector:
an area fault under displacement loading requires the reaction check.

The [active roadmap](../../ROADMAP.md) specifies the next claim-specific schema,
check applicability, setup/execution costs and exposure gates. Those features
are not implemented by this preserved full-tuple development example.

## Independent question and answer

The specification is [spec.json](spec.json). A straight uniform linear elastic
bar has its left end fixed, free lateral contraction, no gravity/body force,
no inertia, no thermal strain and small tensile deformation. The right end
has either prescribed axial force or prescribed axial displacement. The claim
is the complete tuple of axial stress, extension and reaction magnitude for
that original specification, within its declared numerical tolerance. It is
not a claim that every internal parameter in an artifact is correct.

Equilibrium gives constant axial force N. Hooke's law gives u'=N/(EA), so
u(L)=NL/(EA). Under force control, sigma=F/A and delta=FL/(EA). Under displacement
control, sigma=E delta/L and reaction=EA delta/L. Thus the logarithmic modulus
sensitivity of stress is zero under force control and one under displacement
control. These derivatives guide one selector; they do not define truth.
Dimensions: MPa=N/mm², EA/L=N/mm, force/stiffness=mm. As E grows, force-controlled
extension tends to zero; displacement-controlled stress increases. No stress
concentration, yielding, fatigue or physical safety claim is evaluated.

[reference.py](reference.py) implements the closed form. [artifact.py](artifact.py)
uses nonuniform series springs and summed compliance. The independent
[stiffness test](../../tests/test_evidence_sufficiency.py) assembles element
matrices, solves constrained DOFs and recovers reactions for every artifact
and every original specification. Reference labels compare the full output
tuple against the unmodified specification, without reading mutation names,
policy choices or sensitivity. Density is a permitted nuisance change in this
body-force-free static problem; changing the mesh partition is benign.

## Check acquisition and scoring

The fixed menu and costs are declared in the specification. Every check runs
on every artifact. Costs are abstract acquisition tokens, not runtime, money
or a calibrated measure of engineering effort. All checks compare an observable
with its specification reference except `completed`, which checks finite outputs.
The completion check intentionally says nothing about correctness.

[policies.py](policies.py) receives the loading convention and check menu for
selection, then only purchased boolean observations for its decision. It never
receives filenames, variant descriptions, answer values or correctness labels.
The scorer alone can read the truth and full matrix. The random comparator
is evaluated by exact enumeration of its equal-cost selections, avoiding noise
from a sampled random seed. A pass-accept policy can be wrong because passing
one observable does not verify the complete response tuple. A cautious policy
rejects failed stress checks and abstains otherwise.

The generated JSON records wrong accepts, wrong rejects, abstentions, decision
coverage, cost and errors among decisions, including per-configuration scores.
Groups explicitly match coverage and cost. Coverage at zero observed error can
also be read from the cautious and full-menu controls, with their different costs
shown. All-abstain has undefined decision error and cannot win on accuracy.
Multiple checks can be useful: under displacement control, stress and reaction
both detect a modulus fault, while only reaction detects the seeded area fault.

This is a comparator smoke test on seeded development artifacts. Natural model
failures are absent. Configurations are dependent members of the same mechanics
family, so no confidence intervals or independent-sample claims are made.
The matrix is public and cannot be reused as a private holdout. A future study
must freeze whole defect families before policy tuning and independently review
labels; no unseen-family performance is reported here.

## Reproduce

From the repository root:

```bash
python -m studies.evidence_sufficiency.run
pytest tests/test_evidence_sufficiency.py
# Optional figure, with matplotlib installed:
python -m studies.evidence_sufficiency.plot
```

[results.json](../../reports/evidence-sufficiency/results.json) is the numeric
result home. It binds specification and source bytes by SHA-256. The generated
Markdown table and PNG are views of these results, not separately maintained
numbers. The PNG and editable-text SVG compare control and half-modulus stress, extension
and reaction under each loading convention. Each observable uses the same scale
across both loading rows, includes zero and the original specification reference,
and labels its check outcome. No uncertainty interval is inferred.
It is a verification example, not physical validation.

The runner also writes `outcomes.csv` and `policies.csv` as full-precision views
of `results.json`. CSV coverage and decision error are fractions; the Markdown
table displays percentages. An empty decision-error CSV field means undefined
because the policy made no decisions. Artifact CSV headings include physical
units; policy costs remain abstract tokens. Controls precede faults in both
loading tables. The figure shows the modulus comparison; the tables retain all
artifacts and check outcomes.
