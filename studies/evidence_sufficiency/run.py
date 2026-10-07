"""Execute the full development matrix and small deterministic comparator pilot."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

from .artifact import parameters, solve
from .reference import answer
from .policies import decide, selections

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
POLICIES = ("fixed_stress", "random", "sensitivity", "all_checks", "cautious_stress", "abstain")


def matches(got: float, expected: float, spec: dict) -> bool:
    return math.isclose(got, expected, rel_tol=spec["relative_tolerance"],
                        abs_tol=spec["absolute_tolerance"])


def matrix(spec: dict) -> list[dict]:
    rows = []
    for case in spec["cases"]:
        reference = answer(case)
        for variant in spec["variants"]:
            output = solve(parameters(case, variant), variant["segments"])
            # Truth is the entire required response tuple against the original spec.
            # It neither reads a variant name nor calls a policy/check selector.
            correct = all(matches(output[k], reference[k], spec) for k in reference)
            checks = {}
            for check in spec["menu"]:
                key = check["observable"]
                checks[check["id"]] = (all(math.isfinite(v) for v in output.values())
                                       if key is None else matches(output[key], reference[key], spec))
            identity = hashlib.sha256((case["id"] + variant["name"]).encode()).hexdigest()[:12]
            rows.append({"id": identity, "base": case["id"], "loading": case["loading"],
                         "provenance": "seeded_development", "variant": variant["name"],
                         "reference": reference, "output": output, "correct": correct,
                         "checks": checks})
    return rows


def score(policy: str, rows: list[dict], menu: list[dict]) -> dict:
    totals = {k: 0.0 for k in ("wrong_accepts", "wrong_rejects", "abstentions", "cost")}
    cost = {c["id"]: c["cost"] for c in menu}
    for row in rows:
        for weight, selected in selections(policy, row["loading"], menu):
            # Capability boundary: only paid check results reach the decision rule.
            decision = decide(policy, {key: row["checks"][key] for key in selected})
            totals["wrong_accepts"] += weight * (decision == "accept" and not row["correct"])
            totals["wrong_rejects"] += weight * (decision == "reject" and row["correct"])
            totals["abstentions"] += weight * (decision == "abstain")
            totals["cost"] += weight * sum(cost[key] for key in selected)
    decided = len(rows) - totals["abstentions"]
    return {"policy": policy, "artifacts": len(rows), **totals,
            "coverage": decided / len(rows), "mean_cost": totals["cost"] / len(rows),
            "error_among_decisions": ((totals["wrong_accepts"] + totals["wrong_rejects"]) / decided
                                      if decided else None)}


def build(spec: dict) -> dict:
    rows = matrix(spec)
    scores = [score(policy, rows, spec["menu"]) for policy in POLICIES]
    groups = {}
    for result in scores:
        key = f'coverage={result["coverage"]:g},mean_cost={result["mean_cost"]:g}'
        groups.setdefault(key, []).append(result["policy"])
    return {"scope": spec["scope"], "rows": rows, "scores": scores,
            "matched_coverage_and_cost_groups": groups,
            "by_base": {case["id"]: [score(p, [r for r in rows if r["base"] == case["id"]], spec["menu"])
                                     for p in POLICIES] for case in spec["cases"]}}


def table(result: dict) -> str:
    lines = ["# Executed development outcome matrix", "",
             "Verification example, not physical validation. Generated from `spec.json` by",
             "`python -m studies.evidence_sufficiency.run`. Numeric source: [results.json](results.json).", "",
             "Stress and displacement compare with the independent original specification.",
             "Reaction is a positive tensile force magnitude. PASS/FAIL describes the purchased check.", "",
             "| Loading | Artifact | Correct tuple | Stress (MPa) | Extension (mm) | Reaction (N) | Complete | Stress | Extension | Reaction |",
             "| --- | --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |"]
    for row in result["rows"]:
        o, c = row["output"], row["checks"]
        cells = ["PASS" if c[k] else "FAIL" for k in ("completed", "stress", "displacement", "reaction")]
        lines.append(f'| {row["loading"]} | {row["variant"]} | {row["correct"]} | {o["stress"]:.5g} | {o["displacement"]:.5g} | {o["force"]:.5g} | ' + ' | '.join(cells) + ' |')
    lines += ["", "## Comparator smoke test", "", "Random scores are exact expectations over the equal-cost menu, not sampled trials.",
              "Only compare policies within matched coverage and cost groups in the JSON.",
              "These are seeded development cases selected to illustrate modulus sensitivity;",
              "they establish no general policy ranking. All-abstain has undefined decision error.", "",
              "| Policy | Wrong accepts | Wrong rejects | Abstentions | Coverage | Mean cost (tokens) | Error / decided |",
              "| --- | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for s in result["scores"]:
        error = "undefined" if s["error_among_decisions"] is None else f'{s["error_among_decisions"]:.3f}'
        lines.append(f'| {s["policy"]} | {s["wrong_accepts"]:g} | {s["wrong_rejects"]:g} | {s["abstentions"]:g} | {s["coverage"]:.3f} | {s["mean_cost"]:g} | {error} |')
    return '\n'.join(lines) + '\n'


def main() -> None:
    spec = json.loads((HERE / "spec.json").read_text())
    result = build(spec)
    result["provenance"] = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                            for path in [HERE / "spec.json", *sorted(HERE.glob("*.py"))]}
    out = ROOT / "reports/evidence-sufficiency"
    out.mkdir(parents=True, exist_ok=True)
    (out / "results.json").write_text(json.dumps(result, indent=2) + '\n')
    (out / "matrix.md").write_text(table(result))


if __name__ == "__main__":
    main()
