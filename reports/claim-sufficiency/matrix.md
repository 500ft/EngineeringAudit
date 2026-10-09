# Claim correctness and evidence sufficiency

**Public axial-bar development. Finite implementation explanations; no physical validation.**

Source: [results.json](results.json). [Schema and derivation](../../studies/evidence_sufficiency/claims/README.md).

Correct means agreement with the original specification for the named observable.
Sufficient means every allowed explanation compatible with the observed evidence
gives the same correctness decision. It can resolve either acceptance or rejection.
No compatible explanation means inconsistent evidence, never sufficient evidence.

| Claim | Observable | Unit | Rule | Absolute tolerance |
| :--- | :--- | :--- | :--- | ---: |
| stress | stress | MPa | Absolute error ≤ tolerance | 1e-08 |
| deflection | displacement | mm | Absolute error ≤ tolerance | 1e-08 |

## Prescribed force

Observed evidence:

- stress: 50 MPa; compatibility tolerance 1e-08 MPa.

Both explanations keep geometry, loading and all stated assumptions fixed.
Only the implemented elastic modulus differs. Correctness is checked independently
against the original specification, not the explanation identifier.

| Explanation | Implemented modulus E [MPa] | Stress [MPa] | Deflection [mm] | Stress correct | Deflection correct |
| :--- | ---: | ---: | ---: | :---: | :---: |
| H1 | 200000 | 50.0 | 0.0250 | Yes | Yes |
| H2 | 100000 | 50.0 | 0.0500 | Yes | No |

| Claim | Compatible explanations | Evidence sufficient | Resolved decision | Opposite-decision witness |
| :--- | :--- | :---: | :--- | :--- |
| stress | H1, H2 | Yes | accept | None |
| deflection | H1, H2 | No | ambiguous | H1 / H2 |

## Prescribed displacement

Observed evidence:

- stress: 50 MPa; compatibility tolerance 1e-08 MPa.

Both explanations keep geometry, loading and all stated assumptions fixed.
Only the implemented elastic modulus differs. Correctness is checked independently
against the original specification, not the explanation identifier.

| Explanation | Implemented modulus E [MPa] | Stress [MPa] | Deflection [mm] | Stress correct | Deflection correct |
| :--- | ---: | ---: | ---: | :---: | :---: |
| H1 | 200000 | 50.0 | 0.0250 | Yes | Yes |
| H2 | 100000 | 25.0 | 0.0250 | No | Yes |

| Claim | Compatible explanations | Evidence sufficient | Resolved decision | Opposite-decision witness |
| :--- | :--- | :---: | :--- | :--- |
| stress | H1 | Yes | accept | None |
| deflection | H1 | Yes | accept | None |

Sufficiency is conditional on this declared finite explanation set and the evidence tolerances.
It does not certify an arbitrary implementation. All comparisons use unrounded values.
The tolerances are numerical agreement rules, not physical design allowables.
The two loading conventions are configurations of one family, not independent samples.

Reproduce: `python -m studies.evidence_sufficiency.claims.run`.
