import json
from pathlib import Path

import pytest

from cadloop.fea.interpret import interpret

RUNS = Path(__file__).resolve().parents[1] / "cadloop/fea/runs"


def test_completed_and_reference_matching_global_sweep_is_not_converged():
    record = json.loads((RUNS / "mounting_plate_fea_result.json").read_text())
    result = interpret(record)
    assert record["status"] == "ok"
    assert result["solver_completed"] is True
    assert result["reference_agrees"] is True
    assert result["converged"] is False
    peaks = [m["max_von_mises_mpa_at_hole"] for m in record["meshes"]]
    assert result["last_peak_change_abs_rel"] == pytest.approx(abs(peaks[-1] - peaks[-2]) / peaks[-2])
    assert result["last_peak_change_abs_rel"] > result["change_limit_rel"]


@pytest.mark.parametrize("name", ["holeref", "holeref48"])
def test_single_mesh_reference_match_leaves_convergence_unknown(name):
    result = interpret(json.loads((RUNS / f"mounting_plate_{name}_fea_result.json").read_text()))
    assert result["solver_completed"] and result["reference_agrees"]
    assert result["converged"] is None


def test_no_solution_is_not_completion():
    result = interpret({"status": "ok", "oracle": {"agrees": True}})
    assert not result["solver_completed"]
    assert result["reference_agrees"] is None
    assert result["converged"] is None


@pytest.mark.parametrize('peaks, expected', [([1, 1.005, 1.008], True),
                                           ([1, 1.005, 0.9], False),
                                           ([1, 1.1, 1.105], False)])
def test_stability_requires_two_small_changes_and_uses_absolute_change(peaks, expected):
    record = {"meshes": [{"element_size_mm": size,
                           "max_von_mises_mpa_at_hole": peak,
                           "max_displacement_mm": 1}
                          for size, peak in zip([3, 2, 1], peaks)]}
    assert interpret(record)["converged"] is expected
    record["meshes"][-1]["hole_divisions_per_line"] = 48
    assert interpret(record)["converged"] is None


def test_committed_interpretation_is_bound_to_original_bytes():
    import hashlib
    derived = json.loads((RUNS.parents[2] / "reports/fea-interpretation.json").read_text())
    for row in derived["records"]:
        source = RUNS.parents[2] / row["source"]
        assert row["sha256"] == hashlib.sha256(source.read_bytes()).hexdigest()
        assert {k: row[k] for k in interpret(json.loads(source.read_text()))} == interpret(json.loads(source.read_text()))
