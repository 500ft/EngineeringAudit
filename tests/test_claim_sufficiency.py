"""M1.1: decision boundaries and identifiability under the applicable loading."""
import copy
import json
import math
from pathlib import Path

import pytest
from pydantic import ValidationError

from studies.evidence_sufficiency.claims.schema import Claim, Observation, Study
from studies.evidence_sufficiency.claims.evaluate import assess, build, within
from studies.evidence_sufficiency.claims.run import generate, table
# Reuse the separately assembled numerical oracle already checking this foundation.
from test_evidence_sufficiency import stiffness_solution

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "studies/evidence_sufficiency"
STUDY = Study.model_validate_json((HERE / "claims/spec.json").read_text())
FOUNDATION = json.loads((HERE / "spec.json").read_text())
RETAINED = json.loads((ROOT / "reports/evidence-sufficiency/results.json").read_text())


def test_same_force_evidence_resolves_stress_but_not_deflection():
    case = build(STUDY, FOUNDATION, RETAINED)["cases"][0]
    stress, deflection = case["claims"]["stress"], case["claims"]["deflection"]
    assert stress["compatible_explanations"] == deflection["compatible_explanations"] == ["H1", "H2"]
    assert stress["sufficient"] and stress["decision"] == "accept"
    assert not deflection["sufficient"] and deflection["decision"] is None
    assert deflection["opposite_decision_witness"] == ["H1", "H2"]
    assert [a["claim_correctness"]["stress"] for a in case["artifacts"]] == [True, True]
    assert [a["claim_correctness"]["deflection"] for a in case["artifacts"]] == [True, False]
    assert case["artifacts"][0]["output"]["stress"] == case["artifacts"][1]["output"]["stress"]


@pytest.mark.parametrize("index", [0, 1])
def test_explanations_and_correctness_against_independent_stiffness(index):
    case = build(STUDY, FOUNDATION, RETAINED)["cases"][index]
    original = FOUNDATION["cases"][index]
    intended = stiffness_solution(original)
    for artifact in case["artifacts"]:
        effective = dict(original, modulus=artifact["implemented_modulus_MPa"])
        independent = stiffness_solution(effective)
        assert artifact["independent_prediction"] == pytest.approx(independent)
        assert artifact["output"] == pytest.approx(independent)
        for claim in STUDY.claims:
            correct = abs(independent[claim.observable] - intended[claim.observable]) <= claim.absolute_tolerance
            assert artifact["claim_correctness"][claim.id] == correct


def test_displacement_control_stress_evidence_excludes_half_modulus():
    case = build(STUDY, FOUNDATION, RETAINED)["cases"][1]
    for claim in case["claims"].values():
        assert claim["compatible_explanations"] == ["H1"]
        assert claim["sufficient"] and claim["decision"] == "accept"
    # H2 has a correct deflection even though the stress observation excludes it.
    assert case["artifacts"][1]["claim_correctness"] == {"stress": False, "deflection": True}


def test_switching_observed_quantity_reverses_displacement_control_ambiguity():
    study = STUDY.model_copy(update={"observations": [Observation(observable="displacement", unit="mm", absolute_tolerance=1e-8)]})
    force, displacement = build(study, FOUNDATION, RETAINED)["cases"]
    assert all(c["sufficient"] for c in force["claims"].values())
    assert displacement["claims"]["deflection"]["sufficient"]
    assert not displacement["claims"]["stress"]["sufficient"]
    assert displacement["claims"]["stress"]["opposite_decision_witness"] == ["H1", "H2"]


def test_boundary_is_closed_with_no_hidden_relative_slack():
    assert within(1.125, 1, .125)
    assert within(.875, 1, .125)
    assert not within(math.nextafter(1.125, math.inf), 1, .125)
    assert not within(math.nextafter(.875, -math.inf), 1, .125)
    assert within(1, 1, 0)
    assert not within(math.nextafter(1, math.inf), 1, 0)


def test_compatibility_boundary_and_claim_boundary_have_distinct_tolerances():
    claim = Claim(id="test", observable="stress", unit="MPa", decision_rule="within_reference_tolerance", absolute_tolerance=0)
    predictions = {"a": {"stress": 1}, "b": {"stress": 1.125}}
    obs = Observation(observable="stress", unit="MPa", absolute_tolerance=.125)
    result = assess(claim, 1, predictions, {"stress": 1}, [obs])
    assert not result["sufficient"] and result["compatible_explanations"] == ["a", "b"]
    obs = obs.model_copy(update={"absolute_tolerance": math.nextafter(.125, 0)})
    assert assess(claim, 1, predictions, {"stress": 1}, [obs])["decision"] == "accept"
    claim = claim.model_copy(update={"absolute_tolerance": .125})
    assert assess(claim, 1, predictions, {"stress": 1}, [Observation(observable="stress", unit="MPa", absolute_tolerance=.125)])["decision"] == "accept"


def test_inconsistent_evidence_is_not_vacuously_sufficient_and_rejection_can_be_resolved():
    claim = STUDY.claims[0]
    predictions = {"x": {"stress": 25}}
    bad = assess(claim, 50, predictions, {"stress": 50}, STUDY.observations)
    assert bad["status"] == "inconsistent_evidence" and not bad["sufficient"]
    assert bad["decision"] is None and bad["opposite_decision_witness"] is None
    known_bad = assess(claim, 50, predictions, {"stress": 25}, STUDY.observations)
    assert known_bad["sufficient"] and known_bad["decision"] == "reject"


def test_labels_do_not_depend_on_mutation_names_ids_or_order():
    foundation, retained = copy.deepcopy(FOUNDATION), copy.deepcopy(RETAINED)
    mapping = {v["name"]: f"opaque{i}" for i, v in enumerate(foundation["variants"])}
    for v in foundation["variants"]:
        v["name"] = mapping[v["name"]]
    for row in retained["rows"]:
        row["variant"] = mapping[row["variant"]]
    data = STUDY.model_dump()
    data["evidence_source_variant"] = mapping[data["evidence_source_variant"]]
    for e in data["allowed_explanations"]:
        e["source_variant"] = mapping[e["source_variant"]]
        e["id"] = {"H1": "renamed_good", "H2": "renamed_other"}[e["id"]]
    data["allowed_explanations"].reverse()
    before = build(STUDY, FOUNDATION, RETAINED)
    after = build(Study.model_validate(data), foundation, retained)
    for old, new in zip(before["cases"], after["cases"]):
        for c in old["claims"]:
            assert old["claims"][c]["sufficient"] == new["claims"][c]["sufficient"]
            assert old["claims"][c]["decision"] == new["claims"][c]["decision"]


def test_legacy_labels_and_selector_scores_are_not_truth_inputs():
    retained = copy.deepcopy(RETAINED)
    for row in retained["rows"]:
        row.pop("correct")
        row.pop("checks")
    retained = {"rows": retained["rows"]}
    assert build(STUDY, FOUNDATION, retained) == build(STUDY, FOUNDATION, RETAINED)


@pytest.mark.parametrize("change", [{"unit": "mm"}, {"absolute_tolerance": -1}, {"absolute_tolerance": float("nan")}, {"decision_rule": "trust_selector"}])
def test_schema_rejects_invalid_claim_contract(change):
    with pytest.raises(ValidationError):
        Claim.model_validate({**STUDY.claims[0].model_dump(), **change})


def test_wrong_or_unsupported_load_convention_is_rejected():
    data = STUDY.model_dump()
    data["cases"][0]["loading_convention"] = "displacement"
    with pytest.raises(ValueError, match="loading convention"):
        build(Study.model_validate(data), FOUNDATION, RETAINED)
    data["cases"][0]["loading_convention"] = "pressure"
    with pytest.raises(ValidationError):
        Study.model_validate(data)


def test_geometry_fault_is_outside_modulus_only_explanation_set():
    data = STUDY.model_dump()
    data["allowed_explanations"][1]["source_variant"] = "area_fault"
    with pytest.raises(ValueError, match="more than the allowed modulus"):
        build(Study.model_validate(data), FOUNDATION, RETAINED)


@pytest.mark.parametrize("value", [0, -1, float("inf")])
def test_invalid_physical_modulus_is_rejected(value):
    foundation = copy.deepcopy(FOUNDATION)
    foundation["cases"][0]["modulus"] = value
    with pytest.raises(ValueError, match="positive finite modulus"):
        build(STUDY, foundation, RETAINED)


def test_committed_claim_result_and_table_reproduce():
    result = generate()
    assert result == json.loads((ROOT / "reports/claim-sufficiency/results.json").read_text())
    assert table(result) == (ROOT / "reports/claim-sufficiency/matrix.md").read_text()
