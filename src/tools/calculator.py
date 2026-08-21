async def calculator(expression: str = None, query: str = None) -> str:
    expr = expression or query
    if not expr:
        return "No expression provided"

    try:
        allowed_chars = set("0123456789+-*/.() ")
        if not all(c in allowed_chars for c in expr):
            return "Error: Expression contains invalid characters"

        result = eval(expr)
        return f"Calculation: {expr} = {result}"
    except Exception as e:
        return f"Error calculating expression: {str(e)}"
