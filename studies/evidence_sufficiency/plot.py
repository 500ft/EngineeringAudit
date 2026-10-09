"""Render preserved development outcomes; no solve, model call or uncertainty fit."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "reports/evidence-sufficiency"
# Coordinated scientific colors from the pinned enclosure reference.
SERIES = (("correct_control", "Control", "#2980b9", "o"),
          ("modulus_fault", "Half modulus", "#c0392b", "s"))
OBSERVABLES = (("stress", "stress", "Stress [MPa]"),
               ("displacement", "displacement", "Extension [mm]"),
               ("force", "reaction", "Reaction [N]"))


def main():
    result = json.loads((OUT / "results.json").read_text())
    spec = json.loads((ROOT / "studies/evidence_sufficiency/spec.json").read_text())
    cases = {c["loading"]: c for c in spec["cases"]}
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                         "axes.titlesize": 12, "axes.labelsize": 11,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "svg.fonttype": "none", "svg.hashsalt": "engineering-audit",
                         "figure.facecolor": "white", "axes.facecolor": "white"})
    fig, axes = plt.subplots(2, 3, figsize=(10.5, 7.2), sharey="col")
    fig.subplots_adjust(left=.085, right=.98, top=.76, bottom=.16,
                        wspace=.36, hspace=.92)
    fig.text(.085, .965, "A modulus fault changes which checks detect it", fontsize=16, weight="bold")
    fig.text(.085, .924, "SEEDED DEVELOPMENT  |  Uniform axial bar  |  Full response tuple", fontsize=11)
    handles = [Line2D([], [], color=color, marker=marker, ls="none", markersize=7, label=label)
               for _, label, color, marker in SERIES]
    handles.append(Line2D([], [], color="#6b7280", ls="--", lw=1.2, label="Specification reference"))
    fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(.075, .90),
               ncol=3, frameon=False, columnspacing=1.6)
    for i, loading in enumerate(("force", "displacement")):
        subset = {r["variant"]: r for r in result["rows"] if r["loading"] == loading}
        case = cases[loading]
        load = f'{case["force"]:g} N' if loading == "force" else f'{case["displacement"]:g} mm'
        fig.text(.085, .802 if i == 0 else .467,
                 f'{"A" if i == 0 else "B"}  Prescribed {loading}: {load}',
                 fontsize=12, weight="bold")
        for j, (key, check, label) in enumerate(OBSERVABLES):
            ax = axes[i, j]
            reference = subset["correct_control"]["reference"][key]
            ax.axhline(reference, color="#6b7280", lw=1.2, ls="--", zorder=2)
            values = [subset[v]["output"][key] for v, *_ in SERIES]
            # Equal limits within each observable, with zero visible; units are never mixed.
            all_values = [r["output"][key] for r in result["rows"]
                          if r["variant"] in {v for v, *_ in SERIES}]
            ax.set(xlim=(-.45, 1.45), ylim=(0, max(all_values)*1.45), ylabel=label)
            ax.set_xticks([0, 1], ["Control", "Half modulus"])
            ax.yaxis.set_major_locator(MaxNLocator(nbins=4))
            ax.set_axisbelow(True)
            ax.grid(axis="y", color="#e5e7eb", lw=.7)
            for x, ((variant, _, color, marker), value) in enumerate(zip(SERIES, values)):
                ax.vlines(x, 0, value, colors=color, alpha=.25, lw=1.5)
                ax.plot(x, value, marker=marker, color=color, ms=7, ls="none", zorder=3)
                outcome = "PASS" if subset[variant]["checks"][check] else "FAIL"
                ax.annotate(f'{value:.4g}\n{outcome}', (x, value), xytext=(0, 9),
                            textcoords="offset points", ha="center", va="bottom", fontsize=10)
            ax.tick_params(axis="both", labelsize=10)
    fig.text(.085, .075, "PASS / FAIL applies to the named observable check. Both half-modulus artifacts fail the full tuple.", fontsize=10)
    fig.text(.085, .038, "Verification example, not physical validation. No error bars. Sources: results.json and spec.json.", fontsize=10)
    for ext in ("png", "svg"):
        fig.savefig(OUT / f"boundary-condition.{ext}", dpi=180,
                    metadata={"Date": None} if ext == "svg" else {})
    # Matplotlib path lines carry trailing spaces; normalize the text export.
    svg = OUT / "boundary-condition.svg"
    svg.write_text("\n".join(line.rstrip() for line in svg.read_text().splitlines()) + "\n")
    plt.close(fig)


if __name__ == "__main__":
    main()
