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


VARIANT_LABELS = {"correct_control": "Correct control", "benign_partition": "Benign partition",
                  "nuisance_density": "Nuisance density", "modulus_fault": "Modulus fault",
                  "area_fault": "Area fault", "load_fault": "Load fault"}
POLICY_LABELS = {"fixed_stress": "Fixed stress", "random": "Random (exact)",
                 "sensitivity": "Modulus sensitivity", "all_checks": "All checks",
                 "cautious_stress": "Cautious stress", "abstain": "Always abstain"}


def table(result: dict) -> str:
    lines = ["# Evidence-sufficiency development results", "",
             "**Seeded development. Verification example, not physical validation.**", "",
             "One axial-bar family, two loading conventions. Correctness means the full",
             "stress, extension and reaction tuple agrees with the original specification.",
             "A PASS in one check does not certify that tuple. Completion checks finite outputs only.", "",
             "Source: [results.json](results.json). Configuration: [spec.json](../../studies/evidence_sufficiency/spec.json).",
             "Downloads: [outcomes.csv](outcomes.csv), [policies.csv](policies.csv).",
             "Values below are rounded for display; downloads retain stored precision.", "",
             "![Six panels compare control and half-modulus stress, extension and reaction under force and displacement loading; each point names its check outcome.](boundary-condition.png)", "",
             "[Vector figure](boundary-condition.svg). Both half-modulus artifacts fail the full tuple,",
             "but different observable checks detect the fault under each loading convention.", ""]
    for loading in ("force", "displacement"):
        rows = [r for r in result["rows"] if r["loading"] == loading]
        ref = rows[0]["reference"]
        lines += [f'## Prescribed {loading}', "",
                  f'Original reference: stress **{ref["stress"]:.1f} MPa**, extension **{ref["displacement"]:.4f} mm**, reaction **{ref["force"]:.1f} N**.',
                  "Reaction is the positive tensile force magnitude.", "",
                  "### Artifact outputs", "",
                  "| Artifact | Stress [MPa] | Extension [mm] | Reaction [N] | Full tuple |",
                  "| :--- | ---: | ---: | ---: | :--- |"]
        for row in rows:
            o = row["output"]
            lines.append(f'| {VARIANT_LABELS[row["variant"]]} | {o["stress"]:.1f} | {o["displacement"]:.4f} | {o["force"]:.1f} | {"Correct" if row["correct"] else "Incorrect"} |')
        lines += ["", "### Executed checks", "",
                  "| Artifact | Completion | Stress | Extension | Reaction |",
                  "| :--- | :---: | :---: | :---: | :---: |"]
        for row in rows:
            cells = ["PASS" if row["checks"][k] else "**FAIL**" for k in ("completed", "stress", "displacement", "reaction")]
            lines.append(f'| {VARIANT_LABELS[row["variant"]]} | ' + ' | '.join(cells) + ' |')
        lines += [""]
    n = result["scores"][0]["artifacts"]
    lines += ["## Comparator smoke test", "",
              f'Each comparator is scored on the same **{n} development artifacts**.',
              "Random counts are exact expectations over equal-cost choices, not sampled trials.",
              "No LLM reviewers were run. These selected seeded faults establish no general policy ranking.", "",
              "### Decision counts", "",
              "| Policy | Wrong accepts [count] | Wrong rejects [count] | Abstentions [count] |",
              "| :--- | ---: | ---: | ---: |"]
    for s in result["scores"]:
        lines.append(f'| {POLICY_LABELS[s["policy"]]} | {s["wrong_accepts"]:g} | {s["wrong_rejects"]:g} | {s["abstentions"]:g} |')
    lines += ["", "### Coverage and cost", "",
              "Coverage is the fraction accepted or rejected. Error is wrong decisions / all decisions.",
              "Costs are abstract acquisition tokens; setup and runtime are not measured.", "",
              "| Policy | Coverage [%] | Mean cost [tokens/artifact] | Decision error [%] |",
              "| :--- | ---: | ---: | ---: |"]
    for s in result["scores"]:
        error = "N/A (no decisions)" if s["error_among_decisions"] is None else f'{100*s["error_among_decisions"]:.1f}'
        lines.append(f'| {POLICY_LABELS[s["policy"]]} | {100*s["coverage"]:.1f} | {s["mean_cost"]:g} | {error} |')
    lines += ["", "**Matched coverage and cost:**"]
    for key, policies in result["matched_coverage_and_cost_groups"].items():
        if len(policies) > 1:
            lines += ["", ', '.join(POLICY_LABELS[p] for p in policies) + f' (`{key}`).']
    lines += ["", "The other policies use different coverage or cost and are separate controls.",
              "Always abstaining has undefined decision error and cannot win on accuracy.", "",
              "Generated by `python -m studies.evidence_sufficiency.run`.",
              "[Derivation and limits](../../studies/evidence_sufficiency/README.md)."]
    return '\n'.join(lines) + '\n'


def write_csv(result: dict, out: Path) -> None:
    """Downloadable views of the stored outcomes; no additional numerical source."""
    import csv
    with (out / "outcomes.csv").open("w", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["artifact_id", "loading", "variant", "full_tuple_correct", "stress_MPa",
                         "extension_mm", "reaction_N", "completion_pass", "stress_pass",
                         "extension_pass", "reaction_pass"])
        for r in result["rows"]:
            writer.writerow([r["id"], r["loading"], r["variant"], r["correct"],
                             r["output"]["stress"], r["output"]["displacement"], r["output"]["force"],
                             *[r["checks"][k] for k in ("completed", "stress", "displacement", "reaction")]])
    with (out / "policies.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(result["scores"][0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(result["scores"])


def main() -> None:
    spec = json.loads((HERE / "spec.json").read_text())
    result = build(spec)
    result["provenance"] = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                            for path in [HERE / "spec.json", *sorted(HERE.glob("*.py"))]}
    out = ROOT / "reports/evidence-sufficiency"
    out.mkdir(parents=True, exist_ok=True)
    (out / "results.json").write_text(json.dumps(result, indent=2) + '\n')
    (out / "matrix.md").write_text(table(result))
    write_csv(result, out)


if __name__ == "__main__":
    main()
