"""Offline interpretation of preserved FEA records; never starts a solver."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

# Retrospective reporting criterion, not a certified discretization error bound.
DEFAULT_CHANGE_LIMIT = 0.01


def interpret(report: dict, change_limit: float = DEFAULT_CHANGE_LIMIT) -> dict:
    """Separate completion, reference agreement and mesh evidence.

    Require three ordered meshes and two small final changes for the declared
    stability criterion. Single-mesh records cannot establish convergence.
    """
    if not 0 < change_limit < 1:
        raise ValueError("change_limit must lie between zero and one")
    meshes = [m for m in report.get("meshes", []) if "error" not in m
              and m.get("max_von_mises_mpa_at_hole") is not None]
    completed = bool(meshes) and all(
        math.isfinite(m["max_von_mises_mpa_at_hole"])
        and math.isfinite(m.get("max_displacement_mm", math.nan)) for m in meshes)
    oracle = report.get("oracle", {})
    expected = oracle.get("expected_peak_mpa")
    agreement = None
    if completed and expected and "tolerance_rel" in oracle:
        agreement = abs(meshes[-1]["max_von_mises_mpa_at_hole"] / expected - 1) <= oracle["tolerance_rel"]
    changes = [abs(b["max_von_mises_mpa_at_hole"] / a["max_von_mises_mpa_at_hole"] - 1)
               for a, b in zip(meshes, meshes[1:])
               if a["max_von_mises_mpa_at_hole"] != 0]
    ordered = all(b["element_size_mm"] < a["element_size_mm"]
                  and b.get("hole_divisions_per_line") == a.get("hole_divisions_per_line")
                  for a, b in zip(meshes, meshes[1:]))
    converged = None
    if completed and ordered and changes:
        if changes[-1] > change_limit:
            converged = False
        elif len(changes) >= 2:
            converged = all(c <= change_limit for c in changes[-2:])
    return {
        "solver_completed": completed,
        "reference_agrees": agreement,
        "converged": converged,
        "convergence_status": ("insufficient_evidence" if converged is None else
                               "criterion_met" if converged else "not_converged"),
        "change_limit_rel": change_limit,
        "required_final_small_changes": 2,
        "last_peak_change_abs_rel": changes[-1] if changes else None,
        "scope": "mesh stability criterion only; no physical validation or error bound",
    }


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    records = []
    for path in sorted((root / "cadloop/fea/runs").glob("*fea_result.json")):
        records.append({"source": str(path.relative_to(root)),
                        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                        **interpret(json.loads(path.read_text()))})
    target = root / "reports/fea-interpretation.json"
    target.write_text(json.dumps({"records": records}, indent=2) + "\n")


if __name__ == "__main__":
    main()
