from mcp.server.fastmcp import FastMCP

mcp = FastMCP("CreditDataService")#define mcp

#mock data set creating

MOCK_CUSTOMER_DB = {
    "CUST101": { "debt_to_income": 0.25, "missed_payments_30d": 0, "monthly_income": 8500},
    "CUST102": {"debt_to_income": 0.55, "missed_payments_30d": 3, "monthly_income": 3200}
}

@mcp.tool()
def get_customer_financial_ratios(customer_id: str) -> str:
    """Fetches internal bank ratios(debt-to-income and monthly income ) for a given cusotmer id """
    customer = MOCK_CUSTOMER_DB.get(customer_id.upper())
    if not customer:
        return f"Error: Customer ID {customer_id} not found "
    return f"Income: ${customer['monthly_income']}, debt_to_income ratio:{customer['debt_to_income']}"

@mcp.tool()
def check_credit_bureau_flags(customer_id: str) -> str:
    """Queries external credit bureau metrics for recent deliquencies or missed payments"""
    customer = MOCK_CUSTOMER_DB.get(customer_id.upper())
    if not customer:
        return f"Error: Customer ID {customer_id} not found "
    
    flags = customer['missed_payments_30d']
    if flags > 0:
        return f"WARNING: Bureau reports {flags} missed payments within last 30 days. High Risk"
    return "CLEARED: No derogatory flags or missed payments reported."

if __name__ == "__main__":
    mcp.run()


