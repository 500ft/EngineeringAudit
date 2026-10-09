"""Reproduce M1.1 from the public bar foundation; no selector or reserved cases."""
import hashlib
import json
from pathlib import Path

from .evaluate import build
from .schema import Study

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = ROOT / "reports/claim-sufficiency"


def digest_json(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def generate() -> dict:
    foundation = json.loads((HERE.parent / "spec.json").read_text())
    retained = json.loads((ROOT / "reports/evidence-sufficiency/results.json").read_text())
    study = Study.model_validate_json((HERE / "spec.json").read_text())
    result = build(study, foundation, retained)
    sources = [HERE / "spec.json", *sorted(HERE.glob("*.py")),
               HERE.parent / "spec.json", HERE.parent / "reference.py", HERE.parent / "artifact.py"]
    result["provenance"] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    # Only executed rows are consumed; presentation/scorer metadata is not input.
    result["provenance"]["reports/evidence-sufficiency/results.json#rows"] = digest_json(retained["rows"])
    return result


def table(result: dict) -> str:
    lines = ["# Claim correctness and evidence sufficiency", "",
             "**Public axial-bar development. Finite implementation explanations; no physical validation.**", "",
             "Source: [results.json](results.json). [Schema and derivation](../../studies/evidence_sufficiency/claims/README.md).", "",
             "Correct means agreement with the original specification for the named observable.",
             "Sufficient means every allowed explanation compatible with the observed evidence",
             "gives the same correctness decision. It can resolve either acceptance or rejection.",
             "No compatible explanation means inconsistent evidence, never sufficient evidence.", "",
             "| Claim | Observable | Unit | Rule | Absolute tolerance |",
             "| :--- | :--- | :--- | :--- | ---: |"]
    for claim in result["claim_definitions"]:
        lines.append(f'| {claim["id"]} | {claim["observable"]} | {claim["unit"]} | Absolute error ≤ tolerance | {claim["absolute_tolerance"]:g} |')
    for case in result["cases"]:
        lines += ["", f'## Prescribed {case["loading_convention"]}', "", "Observed evidence:", ""]
        for obs in result["observation_definitions"]:
            lines.append(f'- {obs["observable"]}: {case["evidence"][obs["observable"]]:g} {obs["unit"]}; compatibility tolerance {obs["absolute_tolerance"]:g} {obs["unit"]}.')
        lines += ["", "Both explanations keep geometry, loading and all stated assumptions fixed.",
                  "Only the implemented elastic modulus differs. Correctness is checked independently",
                  "against the original specification, not the explanation identifier.", "",
                  "| Explanation | Implemented E [MPa] | Stress [MPa] | Deflection [mm] | Stress correct | Deflection correct |",
                  "| :--- | ---: | ---: | ---: | :---: | :---: |"]
        for artifact in case["artifacts"]:
            o, correct = artifact["output"], artifact["claim_correctness"]
            lines.append(f'| {artifact["id"]} | {artifact["implemented_modulus_MPa"]:g} | {o["stress"]:g} | {o["displacement"]:.4f} | {"Yes" if correct["stress"] else "No"} | {"Yes" if correct["deflection"] else "No"} |')
        lines += ["", "| Claim | Compatible explanations | Evidence sufficient | Resolved decision | Opposite-decision witness |",
                  "| :--- | :--- | :---: | :--- | :--- |"]
        for name, assessment in case["claims"].items():
            witness = assessment["opposite_decision_witness"]
            lines.append(f'| {name} | {", ".join(assessment["compatible_explanations"]) or "None"} | {"Yes" if assessment["sufficient"] else "No"} | {assessment["decision"] or assessment["status"]} | {" / ".join(witness) if witness else "None"} |')
    lines += ["", "Sufficiency is conditional on this declared finite explanation set and the evidence tolerances.",
              "It does not certify an arbitrary implementation. All comparisons use unrounded values.",
              "The tolerances are numerical agreement rules, not physical design allowables.",
              "The two loading conventions are configurations of one family, not independent samples.", "",
              "Reproduce: `python -m studies.evidence_sufficiency.claims.run`."]
    return "\n".join(lines) + "\n"


def main():
    result = generate()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "results.json").write_text(json.dumps(result, indent=2) + "\n")
    (OUT / "matrix.md").write_text(table(result))


if __name__ == "__main__":
    main()
