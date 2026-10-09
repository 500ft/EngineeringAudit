# Evidence Sufficiency Benchmark

Formerly `engineering-audit`. The Python package and command-line tool keep that name.

[![CI](https://github.com/500ft/evidence-sufficiency-benchmark/actions/workflows/ci.yml/badge.svg)](https://github.com/500ft/evidence-sufficiency-benchmark/actions/workflows/ci.yml)

Can an automated reviewer recognize when passing evidence cannot verify a
specific claim, and select the least-cost applicable checks that resolve it?

The first executed evidence-sufficiency example covers a linear elastic axial
bar under prescribed force and prescribed displacement. Stress is blind to an
incorrect elastic modulus under force loading and sensitive under displacement
loading. Correct controls, benign mesh partitions, a nuisance density change,
and seeded parameter faults are checked against an independent analytic answer
and a separately assembled stiffness model.

![Seeded axial-bar development example: stress, extension and reaction checks for control and half-modulus artifacts under force and displacement loading](reports/evidence-sufficiency/boundary-condition.png)

Verification example, not physical validation. Circles mark controls and squares
mark half-modulus artifacts; dashed lines show specification references. Each
point labels its observable check result, and each row title names the checks
that detect the fault under that loading. Both half-modulus artifacts fail the
full response tuple. [SVG](reports/evidence-sufficiency/boundary-condition.svg).
The figure reads the executed
[results](reports/evidence-sufficiency/results.json); dimensions, units, loads,
perturbations and check costs live in the [specification](studies/evidence_sufficiency/spec.json).
See the [computed outcome matrix and comparator table](reports/evidence-sufficiency/matrix.md)
and [derivation and evidence boundary](studies/evidence_sufficiency/README.md).
This is one mechanics family with two loading configurations, not a completed
multi-problem benchmark or evidence of general reviewer performance.

The [active roadmap](ROADMAP.md) gives prerequisites and completion evidence.
M1.1 now separates claim correctness from evidence sufficiency in a
[claim-specific result](reports/claim-sufficiency/matrix.md). Under force control,
the same observed stress resolves stress agreement but leaves deflection
agreement ambiguous across the declared implementation explanations. See the
[claim contract and independent derivation](studies/evidence_sufficiency/claims/README.md).
The next step is independently qualified problems and review. The historical
full-tuple example retains abstract check tokens; setup/execution costs and
reserved-family evaluation remain future work. The wild-capture campaign and
its CLI entry point are retired.

## Prior work and positioning (2026-10-09)

Entries are in [docs/references.bib](docs/references.bib).

- The formal core, choosing checks to decide which of several explanations
  holds, is known as equivalence class determination or group identification:
  Golovin, Krause and Ray 2010 (EC2), Chen, Hassani and Krause 2017 (correlated
  and noisy tests), Bellala, Bhavnani and Scott 2012 (group-based active query
  selection for rapid diagnosis). The formulation is cited, not claimed as new.
- The blind-check design (seeded faults the reviewer must detect) follows
  Salari and Knupp 2000, who seeded coding mistakes into a code-verification
  exercise and ran a blind test. Cite it as the design precedent.
- The claim here is the counting result only: whether a reviewer recognises
  that the engineering evidence for a specific claim is insufficient and buys
  the checks that settle it. A benchmark of that kind was not found in the
  2026-10-09 review (abstract-level, web search only, forward citations not
  searched).
- Name collision: Zhang and Wu 2026 (Computers, Materials and Continua) use
  the title "Evidence Sufficiency Benchmark" for an LLM answer-abstention
  benchmark in retrieval-augmented generation, a different field and not prior
  art for this question. Any paper or external write-up from this repo must
  use a distinguishing title, for example "engineering evidence sufficiency".
  The repository name is unchanged; the owner has not decided on renaming.

## Reproduce

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test]'
python -m studies.evidence_sufficiency.run
python -m studies.evidence_sufficiency.claims.run
python -m cadloop.fea.interpret
pytest
engineering-audit eval benchmark/
```

These module commands are local calculations and record interpretation;
they do not contact a model or a CAD host. To regenerate the figure, install
`matplotlib` and run `python -m studies.evidence_sufficiency.plot`.

## Existing tools and evidence

The calculation verifier and its capture store remain useful regression assets.
It checks formulas, units and supported assumptions in structured engineering
answers. The [legacy evaluator report](reports/benchmark-results.md) measures
agreement with case annotations; a passing failure case means its error was
detected. It is separate from the new evidence-sufficiency matrix.

```bash
engineering-audit audit benchmark/synthetic/syn-fm01-0001.md --output /tmp/audit.md
engineering-audit eval benchmark/ --report /tmp/benchmark-results.md
```

The [CAD/FEA machinery](cadloop/README.md) includes parametric re-drive, IGES
import, MAPDL static solves and a stress-reference comparison. Solver completion,
reference agreement and mesh convergence are separate facts. The preserved
global sweep is not converged under the declared stability criterion. Later
hole-refined records show close peaks but do not establish systematic refinement
convergence. See the [offline interpretation](reports/fea-interpretation.json)
and [FEA evidence table](reports/fea-interpretation.md). See
[FEA scope](cadloop/fea/README.md) for the criterion and limitations. No new host run was made for this pivot.

## Navigation

- [Roadmap and finish line](ROADMAP.md)
- [Decision and open questions](docs/OPEN_QUESTIONS.md)
- [Result index and reproduction](docs/data-and-figures.md)
- [Limitations](LIMITATIONS.md)
- [Preserved research and CAD history](docs/history/README.md)
- [Legacy benchmark schema](docs/schema_contract.md), [taxonomy](docs/failure_taxonomy.md), [provenance](docs/capture_provenance.md)
- [CAD agent briefing](docs/cad_agent_briefing.md), [host setup](docs/host_setup.md)

See [CONTRIBUTING.md](CONTRIBUTING.md). License: [LICENSE](LICENSE).
