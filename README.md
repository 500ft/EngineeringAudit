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

![Computed stress comparison](reports/evidence-sufficiency/boundary-condition.png)

Verification example, not physical validation. The figure reads the executed
[results](reports/evidence-sufficiency/results.json); dimensions, units, loads,
perturbations and check costs live in the [specification](studies/evidence_sufficiency/spec.json).
See the [computed outcome matrix and comparator table](reports/evidence-sufficiency/matrix.md)
and [derivation and evidence boundary](studies/evidence_sufficiency/README.md).
This is one mechanics family with two loading configurations, not a completed
multi-problem benchmark or evidence of general reviewer performance.

The [active roadmap](ROADMAP.md) gives prerequisites and completion evidence.
Its next step is a claim-specific schema and independently qualified references.
The public example still uses full-tuple correctness and abstract check tokens;
claim-relative sufficiency, setup/execution costs and reserved-family evaluation
remain future work. The wild-capture campaign and its CLI entry point are retired.

## Reproduce

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test]'
python -m studies.evidence_sufficiency.run
python -m cadloop.fea.interpret
pytest
engineering-audit eval benchmark/
```

The first two module commands are local calculations and record interpretation;
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
and [FEA scope](cadloop/fea/README.md). No new host run was made for this pivot.

## Navigation

- [Roadmap and finish line](ROADMAP.md)
- [Decision and open questions](docs/OPEN_QUESTIONS.md)
- [Result index and reproduction](docs/data-and-figures.md)
- [Limitations](LIMITATIONS.md)
- [Preserved research and CAD history](docs/history/README.md)
- [Legacy benchmark schema](docs/schema_contract.md), [taxonomy](docs/failure_taxonomy.md), [provenance](docs/capture_provenance.md)
- [CAD agent briefing](docs/cad_agent_briefing.md), [host setup](docs/host_setup.md)

See [CONTRIBUTING.md](CONTRIBUTING.md). License: [LICENSE](LICENSE).
