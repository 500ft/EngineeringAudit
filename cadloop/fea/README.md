# CAD-to-FEA machinery and evidence

`run_fea.py` imports the exported IGES into MAPDL, meshes and solves the plate,
records stress and displacement, renders contours, and compares the hole-band
peak with a declared finite-width stress correlation. This is implemented.
It requires the licensed host; the offline interpretation below does not.

## Corrected interpretation, 2026-10-06

[Original runs](runs) remain unchanged. The [derived interpretation](../../reports/fea-interpretation.json)
binds them by hash and separates three facts. The generated
[evidence table](../../reports/fea-interpretation.md) keeps these fields in separate columns:

- `solver_completed`: meshes returned finite stress and displacement.
- `reference_agrees`: the final solved peak matches the recorded correlation
  within its declared tolerance, recomputed from values rather than copied
  from the old status flag.
- `converged`: a declared mesh-stability criterion, or null if evidence is
  insufficient. The criterion requires two successive small final changes on
  decreasing global mesh sizes with unchanged hole refinement. It is a
  retrospective reporting threshold, not a discretization error estimate.

The global sweep's last peak change is 7.3%, so it is not converged. Its
`status: ok` meant reference agreement. The later hole-refined records have
close peak stresses but each contains a single solve, and the pair changes
both global and local refinement. They support agreement between those
particular discretizations, not a controlled convergence study. Their derived
convergence fields remain null. No new host solve was performed here.

Reproduce the correction and regression:

```bash
python -m cadloop.fea.interpret
pytest tests/test_fea_interpretation.py tests/test_fea_oracle.py
```

Future runner output includes an `evidence` object using the same interpreter.
The legacy `status` and exit code still describe the stress-reference gate;
consumers needing mesh stability must inspect `evidence.converged` explicitly.

## Model and comparison boundary

The result JSON stores geometry in mm, elastic modulus, stress and traction
in MPa, loaded area in mm², and total force in N. The left X face is fixed in all
DOFs and the right X face receives tensile traction. This is an arbitrary
linear-static verification load with no established service-load meaning.

The net-section polynomial is converted to gross-section loading with W/(W-d).
Its stated domain is limited. Extrapolating it toward a vanished ligament cannot
prove its convention. Formula tests check implementation and limiting behavior;
they do not independently establish the empirical correlation's applicability
to a finite restrained solid. The former claim that the observed discrepancy
must have a particular sign due to restraint is withdrawn. Neither the original
nor refined results isolate that cause.

A stress-only comparison cannot validate modulus under force-controlled axial
loading. The [executed analytic example](../../reports/evidence-sufficiency/matrix.md)
shows why loading convention and claimed observable must be explicit. A contour
image is a view of the same numerical solve, not independent verification, and
its shape cannot rule out a unit error. The original contour PNGs and scaled
deformation GIF are retained as historical visualizations, not current proof.

## Use and retained host knowledge

For an independently authorized host task:

```bash
python cadloop/fea/run_fea.py
python cadloop/fea/animate.py
```

See [host setup](../../docs/host_setup.md),
[API findings](../../docs/solidworks_api_findings.md), and
[agent briefing](../../docs/cad_agent_briefing.md). Configuration lives outside
version control. The older `inspect_geometry.py` and `run_static_plate.py`
remain available to reproduce the earlier plate fixture workflow.

Coverage remains one plate fixture and linear static analysis. The node licence
ceiling is a resource constraint. Systematic local refinement, a qualified
reference for the exact solid and restraint, and physical validation remain
unestablished. The [previous narrative](../../docs/history/fea-before-correction-2026-10-06.md)
is preserved as correction history.
