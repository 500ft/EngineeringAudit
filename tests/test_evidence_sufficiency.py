"""Independent stiffness assembly verifies labels without the selector/reference."""
import copy
import json
from pathlib import Path

import numpy as np
import pytest

from studies.evidence_sufficiency.artifact import parameters
from studies.evidence_sufficiency.run import build, matrix, score, table

ROOT = Path(__file__).resolve().parents[1]
SPEC = json.loads((ROOT / "studies/evidence_sufficiency/spec.json").read_text())


def stiffness_solution(case):
    # Assemble uniform two-node elements, solve constrained DOFs, recover reactions.
    n = 7
    stiffness = np.zeros((n + 1, n + 1))
    for i in range(n):
        stiffness[i:i+2, i:i+2] += case["modulus"] * case["area"] / (case["length"] / n) * np.array([[1, -1], [-1, 1]])
    u = np.zeros(n + 1)
    rhs = np.zeros(n + 1)
    if case["loading"] == "force":
        rhs[-1] = case["force"]
        u[1:] = np.linalg.solve(stiffness[1:, 1:], rhs[1:])
    else:
        u[-1] = case["displacement"]
        u[1:-1] = np.linalg.solve(stiffness[1:-1, 1:-1], -stiffness[1:-1, -1] * u[-1])
    force = -(stiffness @ u)[0]
    return {"force": force, "stress": case["modulus"] * (u[1] - u[0]) / (case["length"] / n), "displacement": u[-1]}


@pytest.mark.parametrize("case", SPEC["cases"], ids=lambda c: c["id"])
def test_all_labels_and_artifacts_against_independent_stiffness_system(case):
    expected = stiffness_solution(case)
    rows = {r["variant"]: r for r in matrix(SPEC) if r["base"] == case["id"]}
    for variant in SPEC["variants"]:
        row = rows[variant["name"]]
        independent_output = stiffness_solution(parameters(case, variant))
        assert row["reference"] == pytest.approx(expected)
        assert row["output"] == pytest.approx(independent_output)
        correct = all(np.isclose(independent_output[k], expected[k], rtol=SPEC["relative_tolerance"], atol=SPEC["absolute_tolerance"]) for k in expected)
        assert row["correct"] == correct


def test_stress_is_blind_to_modulus_only_under_force_control():
    rows = {r["loading"]: r for r in matrix(SPEC) if r["variant"] == "modulus_fault"}
    assert not any(r["correct"] for r in rows.values())
    assert rows["force"]["checks"]["stress"]
    assert not rows["force"]["checks"]["displacement"]
    assert not rows["displacement"]["checks"]["stress"]
    assert rows["displacement"]["checks"]["displacement"]


def test_truth_does_not_use_variant_name_or_selected_checks():
    renamed = copy.deepcopy(SPEC)
    for i, variant in enumerate(renamed["variants"]):
        variant["name"] = f"opaque_{i}"
    renamed["menu"] = []
    before, after = matrix(SPEC), matrix(renamed)
    assert [r["correct"] for r in before] == [r["correct"] for r in after]
    assert [r["output"] for r in before] == [r["output"] for r in after]


def test_cost_coverage_and_all_abstain_cannot_masquerade_as_zero_error():
    rows = matrix(SPEC)
    for policy in ("fixed_stress", "random", "sensitivity"):
        s = score(policy, rows, SPEC["menu"])
        assert s["coverage"] == 1
        assert s["mean_cost"] == 1
        assert s["wrong_rejects"] == 0
    full = score("all_checks", rows, SPEC["menu"])
    assert full["wrong_accepts"] == full["wrong_rejects"] == 0
    empty = score("abstain", rows, SPEC["menu"])
    assert empty["coverage"] == empty["cost"] == 0
    assert empty["error_among_decisions"] is None
    assert set(rows[0]["checks"]) == {c["id"] for c in SPEC["menu"]}


def test_failed_checks_reject_and_cautious_passes_abstain():
    # Independent decision test, including a wrong-rejection scoring path.
    row = {"loading": "force", "correct": True, "checks": {"stress": False}}
    assert score("fixed_stress", [row], SPEC["menu"])["wrong_rejects"] == 1
    row["checks"]["stress"] = True
    assert score("cautious_stress", [row], SPEC["menu"])["abstentions"] == 1


def test_committed_matrix_and_table_reproduce():
    generated = build(SPEC)
    committed = json.loads((ROOT / "reports/evidence-sufficiency/results.json").read_text())
    committed.pop("provenance")
    assert generated == committed
    assert table(generated) == (ROOT / "reports/evidence-sufficiency/matrix.md").read_text()
