"""Pure financial-ratio calculation layer.

Organized by domain (growth, profitability, liquidity, leverage,
efficiency, valuation). Nothing in this package imports or depends on
MCP, an LLM, or any transport - it is plain, independently testable
Python functions over typed numeric inputs.

Only domains whose required inputs already exist on `FinancialPeriod`
(see mcp_server/models.py) have functions implemented so far:
growth and leverage. The other domain modules exist as placeholders
documenting what input data they are waiting on.
"""

from .exceptions import RatioInputError
from .growth import growth_rate
from .leverage import (
    debt_ratio,
    debt_to_equity,
    equity_ratio,
    total_liabilities_to_equity,
)
from .report import calculate_all_ratios

__all__ = [
    "RatioInputError",
    "growth_rate",
    "debt_to_equity",
    "total_liabilities_to_equity",
    "equity_ratio",
    "debt_ratio",
    "calculate_all_ratios",
]
