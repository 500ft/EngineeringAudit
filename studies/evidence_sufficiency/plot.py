"""Render preserved development outcomes; no solve, model call or uncertainty fit."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator

from .. import figure_style as style

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "reports/evidence-sufficiency"
SERIES = ("correct_control", "modulus_fault")
# Output key, check id, axis label, check name used in row titles.
OBSERVABLES = (("stress", "stress", "Stress [MPa]", "stress"),
               ("displacement", "displacement", "Extension [mm]", "extension"),
               ("force", "reaction", "Reaction [N]", "reaction"))
LOADINGS = ("force", "displacement")

# Layout in inches: 183 mm wide, two rows of three panels.
WIDTH, HEIGHT = 7.2, 5.1
LEFT, RIGHT, GAP = 0.62, 0.08, 0.64
PANEL_H, TOP_A, TOP_B = 1.32, 1.08, 2.88


def detecting_checks(rows: dict) -> list[str]:
    """Names of the observable checks that fail for the half-modulus artifact."""
    return [name for _, check, _, name in OBSERVABLES if not rows["modulus_fault"]["checks"][check]]


def row_title(loading: str, load: str, detecting: list[str]) -> str:
    if not detecting:
        found = "no observable check detects the fault"
    elif len(detecting) == 1:
        found = f"only the {detecting[0]} check detects the fault"
    else:
        found = f'the {" and ".join(detecting)} checks detect the fault'
    return f"Prescribed {loading}, {load}: {found}"


def figure(result: dict, spec: dict):
    cases = {c["loading"]: c for c in spec["cases"]}
    subsets = {loading: {r["variant"]: r for r in result["rows"] if r["loading"] == loading}
                        for loading in LOADINGS}
    detecting = {loading: detecting_checks(subsets[loading]) for loading in LOADINGS}
    # The title and footer must hold for every plotted row.
    assert detecting["force"] != detecting["displacement"], detecting
    assert all(detecting.values()), detecting
    assert not any(subsets[l]["modulus_fault"]["correct"] for l in LOADINGS)
    assert all(subsets[l]["correct_control"]["correct"] for l in LOADINGS)
    geometry = {(c["length"], c["area"]) for c in spec["cases"]}
    assert len(geometry) == 1, geometry
    (length, area), = geometry

    style.apply()
    fig = plt.figure(figsize=(WIDTH, HEIGHT))
    x0 = LEFT / WIDTH
    fig.text(x0, 1 - .10 / HEIGHT, "A modulus fault changes which checks detect it",
             size=style.TITLE_SIZE, weight="bold", va="top")
    fig.text(x0, 1 - .33 / HEIGHT, "SEEDED DEVELOPMENT  |  Verification example, not physical validation",
             size=style.NOTE_SIZE, va="top")
    handles = [Line2D([], [], color=v["color"], marker=v["marker"], ls="none", markersize=6, label=v["label"])
               for v in (style.VARIANTS[key] for key in SERIES)]
    handles.append(Line2D([], [], color=style.REFERENCE_COLOR, ls="--", lw=1.1, label="Specification reference"))
    fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(x0 - .012, 1 - .50 / HEIGHT),
               ncol=3, columnspacing=1.6, handletextpad=.4, borderaxespad=0)

    panel_w = (WIDTH - LEFT - RIGHT - 2 * GAP) / 3
    for i, loading in enumerate(LOADINGS):
        subset = subsets[loading]
        case = cases[loading]
        load = f'{case["force"]:g} N' if loading == "force" else f'{case["displacement"]:g} mm'
        top = TOP_A if i == 0 else TOP_B
        header_y = 1 - (top - .17) / HEIGHT
        fig.text(.10 / WIDTH, header_y, "AB"[i], size=style.LETTER_SIZE, weight="bold", va="baseline")
        fig.text(x0, header_y, row_title(loading, load, detecting[loading]),
                 size=style.TITLE_SIZE, va="baseline")
        for j, (key, check, label, _) in enumerate(OBSERVABLES):
            ax = fig.add_axes([(LEFT + j * (panel_w + GAP)) / WIDTH, 1 - (top + PANEL_H) / HEIGHT,
                               panel_w / WIDTH, PANEL_H / HEIGHT])
            # The reference is the independent specification answer, shared by every row of a loading.
            references = {r["reference"][key] for r in subset.values()}
            assert len(references) == 1, references
            ax.axhline(references.pop(), color=style.REFERENCE_COLOR, lw=1.1, ls="--", zorder=2)
            # Equal limits within each observable, with zero visible; units are never mixed.
            top_value = max(r["output"][key] for r in result["rows"] if r["variant"] in SERIES)
            ax.set(xlim=(-.45, 1.45), ylim=(0, top_value * 1.32), ylabel=label)
            ax.set_xticks([0, 1], [style.VARIANTS[v]["label"] for v in SERIES])
            ax.tick_params(axis="x", labelbottom=i == len(LOADINGS) - 1, length=3)
            ax.tick_params(axis="y", length=3)
            ax.yaxis.set_major_locator(MaxNLocator(nbins=4))
            ax.set_axisbelow(True)
            ax.grid(axis="y", color=style.GRID_COLOR, lw=.6)
            for x, variant in enumerate(SERIES):
                v, value = style.VARIANTS[variant], subset[variant]["output"][key]
                ax.vlines(x, 0, value, colors=v["color"], alpha=.3, lw=1.4)
                ax.plot(x, value, marker=v["marker"], color=v["color"], ms=6, ls="none", zorder=3)
                passed = subset[variant]["checks"][check]
                ax.annotate("PASS" if passed else "FAIL", (x, value), xytext=(0, 6),
                            textcoords="offset points", ha="center", va="bottom",
                            size=style.NOTE_SIZE, weight="normal" if passed else "bold")
    notes = ("PASS / FAIL: the named check against the specification. "
             "Both half-modulus artifacts fail the full response tuple.",
             f"Uniform axial bar, {length:g} mm long, {area:g} mm² section. "
             "One deterministic artifact per point, so no error bars.",
             "Values: matrix.md. Sources: results.json and spec.json.")
    for k, note in enumerate(notes):
        fig.text(x0, (.46 - .17 * k) / HEIGHT, note, size=style.NOTE_SIZE, va="baseline")
    return fig


def main():
    result = json.loads((OUT / "results.json").read_text())
    spec = json.loads((ROOT / "studies/evidence_sufficiency/spec.json").read_text())
    fig = figure(result, spec)
    style.save(fig, OUT / "boundary-condition")
    plt.close(fig)


if __name__ == "__main__":
    main()
