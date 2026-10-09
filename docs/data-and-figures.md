# Results, data and figure index

The sole active development plan is [ROADMAP.md](../ROADMAP.md). The result
below is completed development evidence; future claim-specific benchmark gates
are recorded in that roadmap.

## Current evidence-sufficiency result

| Artifact | Meaning | Reproduction |
| --- | --- | --- |
| [Specification](../studies/evidence_sufficiency/spec.json) | Single home for dimensions, loading, perturbations, comparison tolerances and acquisition costs | Inputs to the runner |
| [Numeric result](../reports/evidence-sufficiency/results.json) | Full development outcome matrix, truth, source hashes, policy and per-configuration scores | `python -m studies.evidence_sufficiency.run` |
| [Tables](../reports/evidence-sufficiency/matrix.md), [outcome CSV](../reports/evidence-sufficiency/outcomes.csv), [policy CSV](../reports/evidence-sufficiency/policies.csv) | Values and checks separated by loading, followed by counts and coverage/cost; CSVs retain full precision | Same command |
| [PNG](../reports/evidence-sufficiency/boundary-condition.png), [SVG](../reports/evidence-sufficiency/boundary-condition.svg) | Control and half-modulus stress [MPa], extension [mm] and reaction [N], with observable check outcomes | `python -m studies.evidence_sufficiency.plot` with matplotlib installed |
| [FEA table](../reports/fea-interpretation.md), [numeric interpretation](../reports/fea-interpretation.json) | Completion, correlation agreement and convergence separated, with original record hashes | `python -m cadloop.fea.interpret` |

The figure is a verification example, not physical validation. Configuration
and source provenance are linked above; no decorative or generated artwork is
used. The table and figure derive their numbers from the executed matrix.
[Protocol and derivation](../studies/evidence_sufficiency/README.md) explain the
independent reference and what selectors can observe.

## Preserved calculation-verifier benchmark

[benchmark-results.md](../reports/benchmark-results.md) is the numeric result
home for the earlier annotated-case evaluator. Reproduce without changing the
committed historical report:

```bash
engineering-audit eval benchmark/ --report /tmp/engineering-audit-benchmark.md
pytest
```

For a complete case, `passed` means detected failure modes match annotations.
A correctly detected faulty answer is therefore a benchmark PASS. It does not
mean the answer itself was correct. Pending capture cases remain excluded.
The challenge-protocol captures are elicited outputs; they do not establish
wild-usage performance. See [provenance](capture_provenance.md),
[schema](schema_contract.md), and [limitations](../LIMITATIONS.md).

[History](history/README.md) indexes original captures, dated CAD/FEA records,
old figures at their stable paths and removed schedules through Git history.
The previous pipeline diagram was removed from the current README because it
described the earlier evaluator question; its source remains in Git history.
[Figure manifest](figure-manifest.json) records the active figure and historical
visualizations. There is no manuscript in this repository; current claims are
in README, ROADMAP, LIMITATIONS and the linked result documentation.

## Visual design and retained views

The scientific reference is the enclosure repository at
[`bad572fc0902437445a5446bb5bc43098cc6211f`](https://github.com/500ft/sensor-enclosure-thermal-design/tree/bad572fc0902437445a5446bb5bc43098cc6211f):
[thermal bias](https://github.com/500ft/sensor-enclosure-thermal-design/blob/bad572fc0902437445a5446bb5bc43098cc6211f/analysis/figures/thermal_bias.png),
[transient prediction](https://github.com/500ft/sensor-enclosure-thermal-design/blob/bad572fc0902437445a5446bb5bc43098cc6211f/analysis/figures/thermal_transient_prediction.png)
and [generator](https://github.com/500ft/sensor-enclosure-thermal-design/blob/bad572fc0902437445a5446bb5bc43098cc6211f/analysis/thermal_bias.py).
The supplied files were hash-verified and inspected. The local design uses its
white background, coordinated panels, blue/red series, explicit units and
restrained grid. Circle/square markers and direct check labels provide color
redundancy. Zero and specification references remain visible. Each observable
has its own axis and a shared range across loading conventions; there are no
error bars or dual axes. SVG text remains editable.

The active matrix is split into compact Markdown tables rather than rasterized.
Numeric columns align right, controls precede faults, percentages have one
decimal and physical values retain enough decimals for the supplied cases.
Full-precision CSVs are generated views of the same numeric JSON. Blank policy
CSV decision error means no decisions; it is shown as N/A in Markdown.
The FEA table similarly distinguishes a missing within-run change from a failed
stability criterion. It preserves completion and reference agreement separately.

Historical CAD/FEA contours and the deformation animation are retained unchanged
because they are original run artifacts. The legacy evaluator report stays
unchanged as the reproducible historical result; its PASS/SKIP semantics are
explained above. Existing CAD workflow diagrams and navigation tables describe
retained machinery and do not encode new scientific results. No manuscript or
frozen release artifact was restyled. The roadmap and pending decisions are
unchanged; claim-specific benchmark development remains incomplete.
