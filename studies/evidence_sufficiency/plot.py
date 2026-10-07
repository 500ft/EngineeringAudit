"""Optional figure renderer; reads executed results, does not recompute answers."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "reports/evidence-sufficiency"
rows = json.loads((OUT / "results.json").read_text())["rows"]
fig, axes = plt.subplots(1, 2, figsize=(9, 3.7), layout="constrained")
for ax, loading in zip(axes, ("force", "displacement")):
    subset = {r["variant"]: r for r in rows if r["loading"] == loading}
    values = [subset[k]["output"]["stress"] for k in ("correct_control", "modulus_fault")]
    bars = ax.bar(["Correct control", "Half modulus"], values, color=["#31688e", "#d97732"], width=.55)
    ax.bar_label(bars, fmt="%g MPa", padding=4)
    ax.set(title=f"Prescribed {loading}", ylabel="Axial stress (MPa)", ylim=(0, max(values)*1.3))
    ax.spines[["top", "right"]].set_visible(False)
    ax.text(.5, .90, "Stress check: " + ("blind" if loading == "force" else "sensitive"),
            ha="center", transform=ax.transAxes)
fig.suptitle("Modulus fault: the loading convention changes what stress can reveal", fontsize=12)
fig.supxlabel("Verification example, not physical validation. Source: results.json; configuration: spec.json.", fontsize=9)
fig.savefig(OUT / "boundary-condition.png", dpi=160)
