"""Seeded artifact producer using series spring compliance, without references."""
import math


def parameters(spec: dict, variant: dict) -> dict:
    effective = dict(spec)
    for key, factor in variant["factors"].items():
        if key == "applied_load":
            key = "force" if spec["loading"] == "force" else "displacement"
        effective[key] *= factor
    return effective


def solve(spec: dict, segments: int) -> dict:
    # Nonuniform partition. Density has no role because gravity/inertia are absent.
    weights = list(range(1, segments + 1))
    lengths = [spec["length"] * w / sum(weights) for w in weights]
    springs = [spec["modulus"] * spec["area"] / length for length in lengths]
    compliance = math.fsum(1 / spring for spring in springs)
    if spec["loading"] == "force":
        force = spec["force"]
    elif spec["loading"] == "displacement":
        force = spec["displacement"] / compliance
    else:
        raise ValueError("unsupported boundary condition")
    extensions = [force / spring for spring in springs]
    return {"force": force, "stress": force / spec["area"],
            "displacement": math.fsum(extensions)}
