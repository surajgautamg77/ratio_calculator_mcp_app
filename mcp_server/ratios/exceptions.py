class RatioInputError(ValueError):
    """Raised when a ratio cannot be calculated: a required input is
    missing (None) or a denominator is zero. Callers should catch this
    rather than let a bare TypeError/ZeroDivisionError surface."""
