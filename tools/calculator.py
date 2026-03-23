from langchain.tools import tool

@tool
def calculator(expression: str) -> str:
    """
    Evaluates a mathematical expression and returns the result.
    Input should be a valid Python math expression as a string.
    Examples: '2 + 2', '10 * 5', '100 / 4', '2 ** 8'
    """
    try:
        allowed = {
            "__builtins__": {},
            "abs": abs, "round": round,
            "min": min, "max": max, "pow": pow
        }
        result = eval(str(expression), allowed)
        return f"Result: {result}"
    except ZeroDivisionError:
        return "Error: Division by zero is not allowed."
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"