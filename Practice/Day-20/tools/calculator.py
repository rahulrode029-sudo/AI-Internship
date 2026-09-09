import ast
import operator


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def calculator(expression: str) -> str:
    """
    Safely evaluate a mathematical expression.

    Args:
        expression: Mathematical expression such as 10 + 20 or 5 * 8.

    Returns:
        Calculation result or error message.
    """

    try:
        tree = ast.parse(expression, mode="eval")

        def evaluate(node):
            if isinstance(node, ast.Constant):
                if isinstance(node.value, (int, float)):
                    return node.value
                raise ValueError("Only numbers are allowed.")

            if isinstance(node, ast.BinOp):
                left = evaluate(node.left)
                right = evaluate(node.right)

                operation = OPERATORS.get(type(node.op))

                if operation is None:
                    raise ValueError("Unsupported mathematical operation.")

                if isinstance(node.op, ast.Div) and right == 0:
                    raise ZeroDivisionError("Cannot divide by zero.")

                return operation(left, right)

            if isinstance(node, ast.UnaryOp):
                operation = OPERATORS.get(type(node.op))

                if operation is None:
                    raise ValueError("Unsupported unary operation.")

                return operation(evaluate(node.operand))

            raise ValueError("Invalid mathematical expression.")

        result = evaluate(tree.body)

        return f"Calculation result: {result}"

    except ZeroDivisionError as e:
        return f"Calculator error: {e}"

    except Exception as e:
        return f"Calculator error: {e}"