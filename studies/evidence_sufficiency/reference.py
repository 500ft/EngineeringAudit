"""Closed-form answer derivation, independent of checks and policy selection."""

def answer(spec: dict) -> dict:
    """Uniform linear elastic axial bar, left end fixed, no body force.

    Equilibrium: N'=0. Hooke: u'=N/(EA). Integration: u(L)=NL/(EA).
    Force and displacement denote positive tensile magnitudes.
    """
    length, area, modulus = (spec[k] for k in ("length", "area", "modulus"))
    if spec["loading"] == "force":
        force = spec["force"]
        displacement = force * length / (modulus * area)
    elif spec["loading"] == "displacement":
        displacement = spec["displacement"]
        force = modulus * area * displacement / length
    else:
        raise ValueError("unsupported boundary condition")
    return {"force": force, "stress": force / area, "displacement": displacement}
