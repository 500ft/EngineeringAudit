# cadloop/fea

Takes a part the CAD stage built and exported, solves it on the licensed MAPDL
on the host, renders contour images, and checks the answer against a closed-form
result. One command:

```bash
.venv/bin/python cadloop/fea/run_fea.py
```

That launches MAPDL on the host, tunnels its gRPC port, imports the IGES, builds
the volume, meshes at several element sizes, solves, writes PNGs, and gates the
peak stress. Everything lands in `cadloop/fea/runs/`.

## Why there is an oracle and not just pictures

A contour plot is the weakest evidence this pipeline produces. A solve that ran
with the wrong boundary conditions, the wrong units, or a mesh too coarse to
resolve the feature produces a plausible, colourful, wrong image every time — and
it looks exactly like a right one.

This is not hypothetical here. The first version of this gate **rejected a correct
solve at 22% error**, because the Heywood/Howland stress-concentration series was
taken as gross-section referenced when it is net-section referenced; the
prediction was low by `W/(W-d)`, 32% for this plate. The images before and after
that fix are identical. Only the number moved.

So the run produces both, and the acceptance is the number:

- peak stress at the hole vs. Heywood/Howland for a finite-width plate,
- within 12% relative,
- on a model whose bounding box has been **measured** to match the geometry file.

## What the last runs measured

`mounting_plate`, 80x50x8 mm with a 12 mm central hole, aluminium 6061-T6
(E = 68.9 GPa, nu = 0.33, yield 276 MPa), read from `geometry.json`.

**Load case**, stated in the result JSON as data rather than left implicit:

| | |
| --- | --- |
| Held | entire X=0 end face, 50x8 mm, all DOF (`D,ALL,ALL,0`) |
| Loaded | entire X=80 end face, 50x8 mm = 400 mm2 |
| Traction | 1 MPa, `SFA ... PRES, -1` (negative pressure is tension) |
| Total force | **400 N**, +X |

Why this load: because a closed-form answer exists for it, so the pipeline can be
checked rather than believed. 1 MPa is arbitrary -- the problem is linear elastic,
so stress scales exactly with the traction, and 1 MPa makes the peak read off
directly as the stress-concentration factor. **It is not a service load.** No duty
cycle or mounting arrangement has been established for this plate, so the factor
of safety below is against an arbitrary 400 N and says nothing about whether the
part survives anything real.

**Global refinement** runs out of licence before it runs out of error:

| element size | nodes | peak at hole | change |
| --- | --- | --- | --- |
| 5 mm | 3 409 | 2.797 MPa | |
| 3 mm | 16 207 | 2.991 MPa | +6.9% |
| 2 mm | 39 475 | 2.954 MPa | -1.2% |
| 1.5 mm | 108 905 | 3.170 MPa | +7.3% |

Non-monotonic, still moving 7% at 85% of the 128k node ceiling. That is free-tet
node placement, not convergence: the peak is sampled at whatever node lands
nearest the true maximum.

**Refining the hole instead** converges, and on fewer nodes:

| hole divisions | global size | nodes | peak at hole |
| --- | --- | --- | --- |
| 24 | 3 mm | 72 097 | 3.2991 MPa |
| 48 | 5 mm | 121 301 | 3.3013 MPa |

Doubling hole resolution moved the peak **0.07%**, while the global mesh was made
*coarser*. The peak is controlled entirely by resolution at the hole; the far
field was never the issue.

```
converged peak 3.301 MPa   Howland (2D) 3.209 MPa   +2.9%
displacement 0.001273 mm   FoS vs 276 MPa yield: 87 (against the arbitrary load)
bbox [80.0, 50.0, 8.0] at origin [0, 0, 0]
```

The images corroborate the number independently: peak at the hole edge
*perpendicular* to the load, minimum at the poles 90 degrees away, far field at
the applied 1 MPa. That is Kirsch's four-lobe pattern, with the hole edge in
compression along the load axis. A wrong load direction or a unit error cannot
produce it.

## The residual 2.9%, and what it is not

An earlier version of this file attributed a 7.3% gap to the clamped end face and
the plate's short length. **That was wrong**, and the convergence study is what
disproved it: coarsening the far-field mesh while refining the hole left the
answer unchanged, so the far field and its restraint are not what set the peak.
The gap was an under-resolved hole.

What remains is +2.9% above the closed form, stable under refinement. Howland's
solution is two-dimensional plane stress; this is a 3D solid with t/d = 0.67,
where the peak at mid-thickness genuinely exceeds the plane-stress value. Right
direction, plausible magnitude. Not independently confirmed here, so it is a
consistent explanation rather than a demonstrated one.

## Animating the deformation

```bash
.venv/bin/python cadloop/fea/animate.py
```

Writes `runs/<part>_deformation.gif`: the mesh warped by the nodal displacement
vector, swept from undeformed to deformed and back, against a thin outline of the
original shape.

**The exaggeration factor is burned into every frame, and that is not decoration.**
The real peak deflection here is 0.001273 mm on an 80 mm span -- about a
ten-thousandth of the part. Nothing is visible at true scale, so the animation is
scaled 6284x. A deformation animation without its scale factor reads as a part
that is visibly bending when it is not, and that is the one way this picture can
mislead. Two mistakes were made and fixed while producing it: white caption text
on a white background made the factor invisible, and a caption saying "the right
face" was wrong because the iso view puts +X at the lower left. Faces are named by
coordinate and by colour, never by where they appear on screen.

What it shows: pure axial extension along +X, zero at the fixed X=0 face, maximum
at the pulled X=80 face, with no bending or twist -- which is what a centred
uniaxial load on a symmetric part should produce, and a check in its own right.
The hole goes elliptical, stretched along the load axis and pinched across it by
Poisson contraction, which is why the stress peaks on the flanks of the hole
rather than at its poles.

## Host notes

MAPDL v261 at
`C:\Program Files\ANSYS Inc\ANSYS Student\v261\ansys\bin\winx64\ANSYS261.exe`.
Traps are catalogued in `docs/solidworks_api_findings.md` under *MAPDL / ANSYS on
this host*; the ones that cost the most time:

- A stale `<jobname>.lock` stops MAPDL starting **and it exits before opening a
  log** — no process, no port, no new file, nothing to read. `run_fea.py` deletes
  the lock before launching.
- `start /b` over SSH did not keep the server alive. It is launched over an SSH
  channel held open for the life of the run, and readiness is the listening port.
- `-smp` is required; the default distributed mode left a wrapper that never
  bound the port.
- Images need `pip install "ansys-mapdl-core[graphics]"`. Rendering is
  client-side, so nothing is installed on the host for it.
- ANSYS Student stops at 128k nodes. That is a licence ceiling: a sweep that hits
  it has run out of licence, not converged.

## Configuration

Same `CADLOOP_HOST_CONFIG` file as the CAD stage (`ssh_host`, `ssh_user`,
`ssh_key`). It holds a password, so it lives outside version control. See
`docs/host_setup.md`.

## What this does not yet do

- **One fixture, one load case.** The boundary conditions are written for a
  plate loaded along X. `run_fea.py` now refuses a part whose bounding box does
  not match the geometry file rather than silently solving a rotated model, but
  a different part still needs different boundary conditions, not a parameter.
- **No modal or nonlinear analysis.** Linear static only.
- **The restraint is cruder than the correlation assumes**, which is most of the
  7.3%. See above.
- **Not gated in CI.** `tests/test_fea_oracle.py` checks the closed-form
  prediction, which is what the gate rests on. The solve itself needs the host
  and a licence, so CI cannot run it.

## The older scripts

`inspect_geometry.py` and `run_static_plate.py` are the earlier two-step manual
route, kept because the 150x80x6 measurement above came from them. `run_fea.py`
supersedes both.
