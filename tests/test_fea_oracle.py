"""Checks the implemented correlation and its explicit net-section conversion.

These are formula regressions, not validation of a plate solve. Behavior outside
its stated ratio domain cannot establish the source convention.
"""
from __future__ import annotations

import pytest

from cadloop.fea import run_fea

kt = run_fea.kt_plate_central_hole
peak = run_fea.peak_stress_mpa


def test_small_hole_recovers_the_infinite_plate_result() -> None:
    """Kirsch's 3.0. A sanity check only: both conventions agree in this limit,
    so passing it says nothing about which one the series uses."""
    assert kt(0.01, 100.0) == pytest.approx(3.0, abs=0.01)


def test_declared_net_section_fit_decreases_within_its_domain() -> None:
    """Regression of the declared net-section fit within its domain."""
    values = [kt(ratio * 100.0, 100.0) for ratio in (0.05, 0.1, 0.2, 0.3, 0.4, 0.5)]
    assert values == sorted(values, reverse=True)
    assert values[-1] < values[0] < 3.0 + 1e-9


def test_the_net_section_conversion_is_applied() -> None:
    """The applied traction is gross stress; Kt multiplies net stress. Skipping
    the W/(W-d) factor is exactly the 32% underprediction the gate hit."""
    got = peak(12.0, 50.0, 1.0)
    assert got["net_over_gross"] == pytest.approx(50.0 / 38.0)
    assert got["expected_peak_mpa"] == pytest.approx(2.43846528 * 50.0 / 38.0, rel=1e-9)
    assert got["expected_peak_mpa"] > got["kt_net_section"], "conversion not applied"


def test_scales_linearly_with_the_applied_stress() -> None:
    """Linear elasticity. A prediction that did not scale would mean the applied
    stress had leaked into the factor."""
    one = peak(12.0, 50.0, 1.0)["expected_peak_mpa"]
    ten = peak(12.0, 50.0, 10.0)["expected_peak_mpa"]
    assert ten == pytest.approx(10.0 * one, rel=1e-12)


@pytest.mark.parametrize("hole, width", [(0.0, 50.0), (30.0, 50.0), (-5.0, 50.0)])
def test_refuses_ratios_outside_the_correlation(hole: float, width: float) -> None:
    """Extrapolating past d/W = 0.5 silently would be the dangerous behaviour."""
    with pytest.raises(ValueError):
        kt(hole, width)
