"""Selectors see loading convention/menu, then only purchased check observations.

No artifact name, mutation, reference values or truth labels enter this module.
"""


def selections(policy: str, loading: str, menu: list[dict]) -> list[tuple[float, list[str]]]:
    ids = [check["id"] for check in menu]
    if policy == "random":
        if len({c["cost"] for c in menu}) != 1:
            raise ValueError("random comparator requires equal-cost checks")
        return [(1 / len(ids), [check]) for check in ids]
    if policy == "all_checks":
        return [(1.0, ids)]
    if policy == "abstain":
        return [(1.0, [])]
    if policy == "sensitivity":
        # Dimensionless derivatives d(log observable)/d(log E), from the model.
        sensitivities = {"force": {"stress": 0, "displacement": -1, "reaction": 0},
                         "displacement": {"stress": 1, "displacement": 0, "reaction": 1}}
        chosen = max(sensitivities[loading], key=lambda c: abs(sensitivities[loading][c]))
        return [(1.0, [chosen])]
    if policy in {"fixed_stress", "cautious_stress"}:
        return [(1.0, ["stress"])]
    raise ValueError(policy)


def decide(policy: str, purchased: dict[str, bool]) -> str:
    if not purchased:
        return "abstain"
    if not all(purchased.values()):
        return "reject"
    return "abstain" if policy == "cautious_stress" else "accept"
