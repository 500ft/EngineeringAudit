"""Independent claim truth and evidence compatibility, without any selector."""
import math

from ..artifact import parameters, solve
from ..reference import answer
from .schema import Claim, Observation, Study


def within(value: float, reference: float, tolerance: float) -> bool:
    """Closed absolute-error interval in the declared canonical unit.

    No relative tolerance or hidden numerical slack is added at a boundary.
    """
    if not all(math.isfinite(v) for v in (value, reference, tolerance)) or tolerance < 0:
        raise ValueError("comparison needs finite values and a nonnegative tolerance")
    return abs(value - reference) <= tolerance


def assess(claim: Claim, reference: float, explanations: dict[str, dict],
           evidence: dict[str, float], observations: list[Observation]) -> dict:
    """Sufficiency means unanimous claim correctness among compatible explanations.

    Empty support is inconsistent evidence, not a vacuously resolved claim.
    IDs are used only to report witnesses; their names never determine a label.
    """
    compatible = {
        key: output for key, output in explanations.items()
        if all(within(output[o.observable], evidence[o.observable], o.absolute_tolerance)
               for o in observations)
    }
    decisions = {key: within(output[claim.observable], reference, claim.absolute_tolerance)
                 for key, output in compatible.items()}
    accepts = [key for key, correct in decisions.items() if correct]
    rejects = [key for key, correct in decisions.items() if not correct]
    sufficient = bool(decisions) and len(set(decisions.values())) == 1
    return {"compatible_explanations": list(compatible),
            "explanation_decisions": decisions,
            "sufficient": sufficient,
            "decision": ("accept" if accepts else "reject") if sufficient else None,
            "status": ("resolved" if sufficient else "ambiguous" if decisions else "inconsistent_evidence"),
            "opposite_decision_witness": [accepts[0], rejects[0]] if accepts and rejects else None}


def validate_bar(case: dict) -> None:
    if case["loading"] not in {"force", "displacement"}:
        raise ValueError("unsupported loading convention")
    for key in ("length", "area", "modulus", case["loading"]):
        if not math.isfinite(case[key]) or case[key] <= 0:
            raise ValueError(f"this tensile-bar example requires positive finite {key}")


def build(study: Study, foundation: dict, retained: dict) -> dict:
    cases = {c["id"]: c for c in foundation["cases"]}
    variants = {v["name"]: v for v in foundation["variants"]}
    results = []
    for entry in study.cases:
        case = cases[entry.source_case]
        if case["loading"] != entry.loading_convention:
            raise ValueError("declared loading convention differs from source specification")
        validate_bar(case)
        intended = answer(case)
        # Observation values come from the retained executed artifact, not a selector.
        observed = next(r for r in retained["rows"] if r["base"] == entry.source_case
                        and r["variant"] == study.evidence_source_variant)
        evidence = {o.observable: observed["output"][o.observable] for o in study.observations}
        predictions, artifacts = {}, []
        for explanation in study.allowed_explanations:
            variant = variants[explanation.source_variant]
            effective = parameters(case, variant)
            # This demonstration admits only modulus uncertainty. Do not silently
            # treat new geometry/load faults as covered by its stated assumptions.
            if any(effective[k] != case[k] for k in case if k != "modulus"):
                raise ValueError("explanation changes more than the allowed modulus")
            validate_bar(effective)
            prediction = answer(effective)  # equilibrium/constitutive reference
            output = solve(effective, variant["segments"])  # separate compliance artifact
            predictions[explanation.id] = prediction
            artifacts.append({"id": explanation.id, "implemented_modulus_MPa": effective["modulus"],
                              "output": output, "independent_prediction": prediction,
                              "claim_correctness": {c.id: within(output[c.observable], intended[c.observable], c.absolute_tolerance)
                                                    for c in study.claims}})
        results.append({"source_case": entry.source_case, "loading_convention": entry.loading_convention,
                        "evidence_source_artifact": observed["id"], "evidence": evidence,
                        "reference": intended, "artifacts": artifacts,
                        "claims": {c.id: assess(c, intended[c.observable], predictions, evidence, study.observations)
                                   for c in study.claims}})
    return {"scope": study.scope, "assumptions": study.assumptions,
            "claim_definitions": [c.model_dump() for c in study.claims],
            "observation_definitions": [o.model_dump() for o in study.observations],
            "cases": results}
