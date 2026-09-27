"""Liquidity ratios: pending required inputs.

Current ratio and quick ratio both need `current_assets` /
`current_liabilities` (and quick ratio also `inventory`), none of
which exist on `FinancialPeriod` yet. Add functions here once those
fields exist.
"""
