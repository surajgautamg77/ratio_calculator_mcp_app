"""Growth ratios: how a metric changed between two periods.

A single generic function covers this domain, since the growth formula
is identical regardless of which line item it is applied to (total
assets, reserves, borrowings, and - once available - revenue or net
profit). Callers pass the same metric's value from two periods, e.g.:

    growth_rate(current.total_assets, previous.total_assets)
"""

from .common import require, safe_divide


def growth_rate(current: float | None, previous: float | None) -> float:
    """Growth rate = (Current - Previous) / Previous.

    Returned as a decimal fraction (0.25 == 25% growth), not a
    percentage. `previous` must be non-zero.
    """
    current_value = require(current, "current")
    previous_value = require(previous, "previous")
    return safe_divide(current_value - previous_value, previous_value, "growth_rate")
