# Results, data and figure index

## Current evidence-sufficiency result

| Artifact | Meaning | Reproduction |
| --- | --- | --- |
| [Specification](../studies/evidence_sufficiency/spec.json) | Single home for dimensions, loading, perturbations, comparison tolerances and acquisition costs | Inputs to the runner |
| [Numeric result](../reports/evidence-sufficiency/results.json) | Full development outcome matrix, truth, source hashes, policy and per-configuration scores | `python -m studies.evidence_sufficiency.run` |
| [Table](../reports/evidence-sufficiency/matrix.md) | Generated human-readable outcomes and scores | Same command |
| [Figure](../reports/evidence-sufficiency/boundary-condition.png) | Computed stress in MPa for correct and half-modulus cases under both loading conventions | `python -m studies.evidence_sufficiency.plot` with matplotlib installed |
| [FEA interpretation](../reports/fea-interpretation.json) | Completion, correlation agreement and convergence separated, with original record hashes | `python -m cadloop.fea.interpret` |

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
old figures and the superseded research schedule at their stable paths.
The previous pipeline diagram was removed from the current README because it
described the earlier evaluator question; its source remains in Git history.
[Figure manifest](figure-manifest.json) records the active figure and historical
visualizations. There is no manuscript in this repository; current claims are
in README, ROADMAP, LIMITATIONS and the linked result documentation.
