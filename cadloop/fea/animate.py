#!/usr/bin/env python3
"""Animate which way the part deforms, at a stated exaggeration. Workstation side.

Reuses run_fea's host launch, import and solve, then warps the mesh by the nodal
displacement vector across a sweep of scale factors and writes a GIF.

**The exaggeration is the point of the caption.** This plate's real peak
deflection under the 400 N load case is 0.001273 mm across an 80 mm span -- about
a micron, roughly a ten-thousandth of the part. Nothing is visible at true scale.
Every frame here is scaled by a factor in the thousands, and that factor is
burned into the image rather than left in a README, because a deformation
animation without its scale factor reads as a part that is visibly bending when
it is not. That is the one way this picture could mislead.

The undeformed edges stay on screen as a grey reference so the direction of
motion can be read against something fixed.

usage: python animate.py [--hole-divisions 24] [--element-sizes 3] [--frames 24]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_fea as rf  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--part", default="mounting_plate")
    parser.add_argument("--geometry", type=Path,
                        default=rf.HERE.parent / "scaffold" / "geometry.json")
    parser.add_argument("--pressure-mpa", type=float, default=1.0)
    parser.add_argument("--element-sizes", type=float, default=3.0)
    parser.add_argument("--hole-divisions", type=int, default=24)
    parser.add_argument("--frames", type=int, default=24)
    parser.add_argument("--visible-fraction", type=float, default=0.10,
                        help="peak deflection as a fraction of the longest span")
    parser.add_argument("--out-dir", type=Path, default=rf.HERE / "runs")
    args = parser.parse_args()

    import numpy as np
    import pyvista as pv

    doc = json.loads(args.geometry.read_text())
    g = doc[args.part]
    geometry = {k: g[k]["value"] for k in ("length", "width", "thickness", "hole_diameter")}
    m = doc["material"]
    material = {"name": m.get("name", "unnamed"),
                "youngs_modulus": m["youngs_modulus"]["value"],
                "poissons_ratio": m["poissons_ratio"]["value"],
                "yield_strength": m["yield_strength"]["value"],
                "density": m["density"]["value"]}

    report = {"iges_name": "%s.igs" % args.part}
    c = rf.config()
    tunnel = None
    mapdl = None
    try:
        if not rf.start_mapdl(c, report):
            print(report["mapdl_launch"])
            return 1
        tunnel = rf.open_tunnel(c)

        from ansys.mapdl.core import Mapdl
        mapdl = Mapdl(ip="127.0.0.1", port=rf.PORT, start_instance=False,
                      cleanup_on_exit=False)
        rf.import_geometry(mapdl, report["iges_name"], report)
        solved = rf.mesh_and_solve(mapdl, args.element_sizes, geometry, material,
                                   args.pressure_mpa, hole_divisions=args.hole_divisions)
        if "error" in solved:
            print(solved["error"])
            return 1

        grid = mapdl.mesh.grid
        displacement = np.column_stack([
            np.asarray(mapdl.post_processing.nodal_displacement(axis))
            for axis in ("X", "Y", "Z")])
        if displacement.shape[0] != grid.n_points:
            print("displacement rows %d != grid points %d"
                  % (displacement.shape[0], grid.n_points))
            return 1

        grid["displacement"] = displacement
        magnitude = np.linalg.norm(displacement, axis=1)
        grid["magnitude_mm"] = magnitude
        peak = float(magnitude.max())

        span = max(geometry["length"], geometry["width"])
        scale = args.visible_fraction * span / peak

        # Named by coordinate and by colour, never "left" or "right": which face
        # looks left depends on the camera, and this iso view puts +X at the lower
        # left. A view-relative caption on a rotatable render is a wrong caption.
        caption = (
            "deformation exaggerated %.0fx -- peak is %.6f mm on an %g mm span\n"
            "X=0 face fully fixed (blue, zero displacement)\n"
            "X=%g face pulled along +X by %g MPa = %g N (red, maximum)\n"
            "%s, E=%g MPa   thin outline is the undeformed shape"
            % (scale, peak, geometry["length"],
               geometry["length"], args.pressure_mpa,
               args.pressure_mpa * geometry["width"] * geometry["thickness"],
               material["name"], material["youngs_modulus"]))

        out = args.out_dir / ("%s_deformation.gif" % args.part)
        out.parent.mkdir(parents=True, exist_ok=True)

        plotter = pv.Plotter(off_screen=True, window_size=[1200, 900])
        # Explicit background: the caption below is drawn against it, and white
        # text on a white default made the exaggeration factor invisible -- the one
        # thing this image must not lose.
        plotter.set_background("white")
        # Undeformed reference, so the motion is read against something fixed.
        plotter.add_mesh(grid.extract_feature_edges(), color="#444444", opacity=0.9,
                         line_width=2)
        warped = grid.warp_by_vector("displacement", factor=0.0)
        plotter.add_mesh(warped, scalars="magnitude_mm", cmap="jet", show_edges=False,
                         scalar_bar_args={"title": "displacement (mm)"})
        plotter.add_text(caption, position="upper_left", font_size=11, color="black")
        plotter.camera_position = "iso"
        plotter.open_gif(str(out), fps=12)

        # Zero to full and back, so the direction of travel is unambiguous.
        sweep = np.concatenate([np.linspace(0.0, 1.0, args.frames // 2),
                                np.linspace(1.0, 0.0, args.frames - args.frames // 2)])
        for fraction in sweep:
            warped.points = grid.warp_by_vector("displacement",
                                                factor=scale * float(fraction)).points
            plotter.write_frame()
        plotter.close()

        print(json.dumps({
            "gif": str(out),
            "exaggeration": scale,
            "peak_displacement_mm": peak,
            "nodes": solved["n_nodes"],
            "peak_von_mises_mpa": solved.get("max_von_mises_mpa_at_hole"),
            "load_n": args.pressure_mpa * geometry["width"] * geometry["thickness"],
        }, indent=2))
        return 0

    finally:
        try:
            if mapdl is not None:
                mapdl.exit()
        except Exception:
            pass
        if tunnel is not None:
            tunnel.terminate()
        for held in rf._HELD:
            held.terminate()


if __name__ == "__main__":
    sys.exit(main())
