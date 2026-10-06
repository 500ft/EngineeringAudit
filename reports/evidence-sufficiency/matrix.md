# Executed development outcome matrix

Verification example, not physical validation. Generated from `spec.json` by
`python -m studies.evidence_sufficiency.run`. Numeric source: [results.json](results.json).

Stress and displacement compare with the independent original specification.
Reaction is a positive tensile force magnitude. PASS/FAIL describes the purchased check.

| Loading | Artifact | Correct tuple | Stress (MPa) | Extension (mm) | Reaction (N) | Complete | Stress | Extension | Reaction |
| --- | --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| force | correct_control | True | 50 | 0.025 | 1000 | PASS | PASS | PASS | PASS |
| force | benign_partition | True | 50 | 0.025 | 1000 | PASS | PASS | PASS | PASS |
| force | nuisance_density | True | 50 | 0.025 | 1000 | PASS | PASS | PASS | PASS |
| force | modulus_fault | False | 50 | 0.05 | 1000 | PASS | PASS | FAIL | PASS |
| force | area_fault | False | 100 | 0.05 | 1000 | PASS | FAIL | FAIL | PASS |
| force | load_fault | False | 25 | 0.0125 | 500 | PASS | FAIL | FAIL | FAIL |
| displacement | correct_control | True | 50 | 0.025 | 1000 | PASS | PASS | PASS | PASS |
| displacement | benign_partition | True | 50 | 0.025 | 1000 | PASS | PASS | PASS | PASS |
| displacement | nuisance_density | True | 50 | 0.025 | 1000 | PASS | PASS | PASS | PASS |
| displacement | modulus_fault | False | 25 | 0.025 | 500 | PASS | FAIL | PASS | FAIL |
| displacement | area_fault | False | 50 | 0.025 | 500 | PASS | PASS | PASS | FAIL |
| displacement | load_fault | False | 25 | 0.0125 | 500 | PASS | FAIL | FAIL | FAIL |

## Comparator smoke test

Random scores are exact expectations over the equal-cost menu, not sampled trials.
Only compare policies within matched coverage and cost groups in the JSON.
These are seeded development cases selected to illustrate modulus sensitivity;
they establish no general policy ranking. All-abstain has undefined decision error.

| Policy | Wrong accepts | Wrong rejects | Abstentions | Coverage | Mean cost (tokens) | Error / decided |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fixed_stress | 2 | 0 | 0 | 1.000 | 1 | 0.167 |
| random | 3 | 0 | 0 | 1.000 | 1 | 0.250 |
| sensitivity | 1 | 0 | 0 | 1.000 | 1 | 0.083 |
| all_checks | 0 | 0 | 0 | 1.000 | 4 | 0.000 |
| cautious_stress | 0 | 0 | 8 | 0.333 | 1 | 0.000 |
| abstain | 0 | 0 | 12 | 0.000 | 0 | undefined |
