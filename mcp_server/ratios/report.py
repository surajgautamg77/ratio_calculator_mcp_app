"""Aggregates the individual ratio functions into one structured report.

This is the only place that knows about `FinancialData`/`FinancialPeriod`
and about which fields each ratio needs. It contains no formulas itself -
it only decides, per period, whether a ratio's inputs are present and,
if so, delegates to the corresponding function in growth.py / leverage.py
/ etc.
"""

from typing import Any, Callable

from mcp_server.models import FinancialData, FinancialPeriod

from .exceptions import RatioInputError
from .growth import growth_rate
from .leverage import debt_ratio, debt_to_equity, equity_ratio, total_liabilities_to_equity

DOMAINS = (
    "growth",
    "profitability",
    "liquidity",
    "leverage",
    "efficiency",
    "valuation",
)

# --- Leverage: single-period ratios. Each spec names the FinancialPeriod
# fields it needs (in the order its function expects them). ---
_LEVERAGE_SPECS: list[dict[str, Any]] = [
    {"name": "debt_to_equity", "inputs": ("borrowings", "equity_capital", "reserves"), "func": debt_to_equity},
    {
        "name": "total_liabilities_to_equity",
        "inputs": ("total_liabilities", "equity_capital", "reserves"),
        "func": total_liabilities_to_equity,
    },
    {"name": "equity_ratio", "inputs": ("equity_capital", "reserves", "total_assets"), "func": equity_ratio},
    {"name": "debt_ratio", "inputs": ("total_liabilities", "total_assets"), "func": debt_ratio},
]

# --- Growth: same formula applied to every balance-sheet line item that
# exists on FinancialPeriod, computed between each period and the one
# before it. ---
_GROWTH_METRICS: tuple[str, ...] = (
    "equity_capital",
    "reserves",
    "borrowings",
    "other_liabilities",
    "total_liabilities",
    "fixed_assets",
    "cwip",
    "investments",
    "other_assets",
    "total_assets",
)

# Domains with no implemented ratios yet, and why - see the placeholder
# modules (profitability.py, liquidity.py, efficiency.py, valuation.py).
_UNIMPLEMENTED_DOMAINS: dict[str, str] = {
    "profitability": "No profitability ratios implemented yet; requires revenue, gross_profit, operating_profit, net_profit (not present on FinancialPeriod).",
    "liquidity": "No liquidity ratios implemented yet; requires current_assets, current_liabilities, inventory (not present on FinancialPeriod).",
    "efficiency": "No efficiency ratios implemented yet; requires revenue, inventory, receivables (not present on FinancialPeriod).",
    "valuation": "No valuation ratios implemented yet; requires market_price, number_of_shares, net_profit (not present on FinancialPeriod).",
}


def _compute_leverage_for_period(period: FinancialPeriod) -> tuple[dict[str, float], list[dict[str, Any]]]:
    results: dict[str, float] = {}
    unavailable: list[dict[str, Any]] = []

    for spec in _LEVERAGE_SPECS:
        values = [getattr(period, field) for field in spec["inputs"]]
        missing = [field for field, value in zip(spec["inputs"], values) if value is None]
        if missing:
            unavailable.append(
                {"ratio": spec["name"], "period": period.period, "missing_inputs": missing}
            )
            continue
        try:
            results[spec["name"]] = spec["func"](*values)
        except RatioInputError as e:
            unavailable.append({"ratio": spec["name"], "period": period.period, "reason": str(e)})

    return results, unavailable


def _compute_growth(periods: list[FinancialPeriod]) -> tuple[dict[str, dict[str, float]], list[dict[str, Any]]]:
    results: dict[str, dict[str, float]] = {}
    unavailable: list[dict[str, Any]] = []

    if periods:
        unavailable.append(
            {
                "ratio": "all growth metrics",
                "period": periods[0].period,
                "reason": "No prior period to compare against.",
            }
        )

    for previous, current in zip(periods, periods[1:]):
        period_results: dict[str, float] = {}
        for metric in _GROWTH_METRICS:
            current_value = getattr(current, metric)
            previous_value = getattr(previous, metric)
            ratio_name = f"{metric}_growth"

            missing = [
                label
                for label, value in (("current." + metric, current_value), ("previous." + metric, previous_value))
                if value is None
            ]
            if missing:
                unavailable.append({"ratio": ratio_name, "period": current.period, "missing_inputs": missing})
                continue
            try:
                period_results[ratio_name] = growth_rate(current_value, previous_value)
            except RatioInputError as e:
                unavailable.append({"ratio": ratio_name, "period": current.period, "reason": str(e)})

        results[current.period] = period_results

    return results, unavailable


def calculate_all_ratios(financial_data: FinancialData) -> dict[str, Any]:
    """Calculate every ratio that the given data has enough inputs for.

    Returns a dict with one key per domain (growth, profitability,
    liquidity, leverage, efficiency, valuation) - each mapping period
    label -> {ratio_name: value} - plus an "unavailable" key mapping
    domain -> a list of ratios that could not be calculated and why
    (missing inputs, no prior period, or a zero denominator).

    Nothing here invents or defaults missing figures; a ratio is only
    computed when every input it needs is present in `financial_data`.
    """
    periods = financial_data.periods

    growth_results, growth_unavailable = _compute_growth(periods)

    leverage_results: dict[str, dict[str, float]] = {}
    leverage_unavailable: list[dict[str, Any]] = []
    for period in periods:
        period_results, period_unavailable = _compute_leverage_for_period(period)
        leverage_results[period.period] = period_results
        leverage_unavailable.extend(period_unavailable)

    report: dict[str, Any] = {
        "growth": growth_results,
        "profitability": {},
        "liquidity": {},
        "leverage": leverage_results,
        "efficiency": {},
        "valuation": {},
        "unavailable": {
            "growth": growth_unavailable,
            "profitability": [{"reason": _UNIMPLEMENTED_DOMAINS["profitability"]}],
            "liquidity": [{"reason": _UNIMPLEMENTED_DOMAINS["liquidity"]}],
            "leverage": leverage_unavailable,
            "efficiency": [{"reason": _UNIMPLEMENTED_DOMAINS["efficiency"]}],
            "valuation": [{"reason": _UNIMPLEMENTED_DOMAINS["valuation"]}],
        },
    }
    return report
