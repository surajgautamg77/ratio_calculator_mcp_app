import sys
from pathlib import Path

# Allow `uv run python mcp_server/server.py` to resolve `mcp_server.*`
# imports below, since this file has no installed package context.
_PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from mcp.server.mcpserver import MCPServer

from mcp_server.models import FinancialData
from mcp_server.ratios import calculate_all_ratios as compute_all_ratios

mcp = MCPServer("Math MCP Server")


@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


@mcp.tool()
def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide a by b. Raises an error if b is zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


@mcp.tool()
def power(base: float, exponent: float) -> float:
    """Raise base to the given exponent."""
    return base ** exponent


@mcp.tool(name="calculate_all_ratios")
def calculate_all_ratios(financial_data: FinancialData) -> dict:
    """Calculate every financial ratio the given historical data supports.

    Accepts multi-period financial data and returns a structured report
    organized by domain (growth, profitability, liquidity, leverage,
    efficiency, valuation), plus an "unavailable" section listing any
    ratios that could not be calculated and why (missing inputs, no
    prior period, or a zero denominator). This tool does no financial
    math itself - it delegates to the calculation layer in
    mcp_server/ratios/.
    """
    return compute_all_ratios(financial_data)


if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8000)