from pydantic import BaseModel, Field, field_validator


class FinancialPeriod(BaseModel):
    """One period's raw financial figures. All figures optional except
    the period label - callers supply whatever line items they have."""

    period: str  # e.g. "FY2023", "2023-24", "Q1 2025"

    # --- Balance sheet: liabilities ---
    equity_capital: float | None = Field(default=None, ge=0)
    reserves: float | None = Field(default=None, ge=0)
    borrowings: float | None = Field(default=None, ge=0)
    other_liabilities: float | None = Field(default=None, ge=0)
    total_liabilities: float | None = Field(default=None, ge=0)

    # --- Balance sheet: assets ---
    fixed_assets: float | None = Field(default=None, ge=0)
    cwip: float | None = Field(default=None, ge=0)
    investments: float | None = Field(default=None, ge=0)
    other_assets: float | None = Field(default=None, ge=0)
    total_assets: float | None = Field(default=None, ge=0)

    # Future line items (revenue, net_profit, current_assets, inventory,
    # number_of_shares, market_price, ...) are added here later, each as
    # its own `float | None = None` field - no structural change needed.


class FinancialData(BaseModel):
    """A company's financial figures across one or more periods."""

    company_name: str | None = None
    periods: list[FinancialPeriod]

    @field_validator("periods")
    @classmethod
    def unique_periods(cls, v: list[FinancialPeriod]) -> list[FinancialPeriod]:
        labels = [p.period for p in v]
        if len(labels) != len(set(labels)):
            raise ValueError("Duplicate period labels are not allowed.")
        if not v:
            raise ValueError("At least one period is required.")
        return v
