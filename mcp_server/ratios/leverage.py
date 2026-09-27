"""Leverage (solvency) ratios: how a company is financed - debt vs equity."""

from .common import net_worth, require, safe_divide


def debt_to_equity(
    borrowings: float | None, equity_capital: float | None, reserves: float | None
) -> float:
    """Debt-to-Equity = Borrowings / (Equity Capital + Reserves).

    Measures financial leverage from interest-bearing debt only.
    """
    debt = require(borrowings, "borrowings")
    equity = net_worth(equity_capital, reserves)
    return safe_divide(debt, equity, "debt_to_equity")


def total_liabilities_to_equity(
    total_liabilities: float | None,
    equity_capital: float | None,
    reserves: float | None,
) -> float:
    """Total-Liabilities-to-Equity = Total Liabilities / (Equity Capital + Reserves).

    Broader leverage measure: all liabilities, not just borrowings.
    """
    liabilities = require(total_liabilities, "total_liabilities")
    equity = net_worth(equity_capital, reserves)
    return safe_divide(liabilities, equity, "total_liabilities_to_equity")


def equity_ratio(
    equity_capital: float | None, reserves: float | None, total_assets: float | None
) -> float:
    """Equity Ratio = (Equity Capital + Reserves) / Total Assets.

    Share of the balance sheet funded by shareholders rather than
    liabilities; higher means lower reliance on debt.
    """
    equity = net_worth(equity_capital, reserves)
    assets = require(total_assets, "total_assets")
    return safe_divide(equity, assets, "equity_ratio")


def debt_ratio(total_liabilities: float | None, total_assets: float | None) -> float:
    """Debt Ratio = Total Liabilities / Total Assets.

    Share of the balance sheet funded by liabilities rather than equity.
    """
    liabilities = require(total_liabilities, "total_liabilities")
    assets = require(total_assets, "total_assets")
    return safe_divide(liabilities, assets, "debt_ratio")
