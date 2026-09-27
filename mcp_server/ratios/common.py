"""Small helpers shared across ratio domains. Not ratios themselves."""

from .exceptions import RatioInputError


def require(value: float | None, name: str) -> float:
    """Return `value` as a float, or raise if it is missing (None)."""
    if value is None:
        raise RatioInputError(f"Missing required input: {name}")
    return float(value)


def safe_divide(numerator: float, denominator: float, formula_name: str) -> float:
    """Divide, raising a clear error instead of a bare ZeroDivisionError."""
    if denominator == 0:
        raise RatioInputError(
            f"Cannot compute {formula_name}: denominator is zero."
        )
    return numerator / denominator


def net_worth(equity_capital: float | None, reserves: float | None) -> float:
    """Net worth (shareholders' equity) = Equity Capital + Reserves.

    Not a ratio on its own, but used as the equity base by several
    leverage (and later, profitability) ratios.
    """
    return require(equity_capital, "equity_capital") + require(reserves, "reserves")
