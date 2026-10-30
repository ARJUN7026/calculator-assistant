import ast
import operator
import re
import math

# Only allow these arithmetic operations
OPERATIONS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}

FUNCTIONS = {
    "sqrt": math.sqrt,
    "abs": abs,
    "round": round,
}

def evaluate(node):
    if isinstance(node, ast.Expression):
        return evaluate(node.body)

    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in OPERATIONS:
        left = evaluate(node.left)
        right = evaluate(node.right)
        return OPERATIONS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        number = evaluate(node.operand)
        return number if isinstance(node.op, ast.UAdd) else -number

    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        name = node.func.id
        if name in FUNCTIONS and not node.keywords:
            arguments = [evaluate(arg) for arg in node.args]
            return FUNCTIONS[name](*arguments)

    raise ValueError("I can only calculate basic arithmetic, sqrt, abs, and round.")

def calculate(question):
    text = question.lower().strip()
    text = re.sub(r"^(what is|calculate|compute|please calculate)\s+", "", text)
    text = text.rstrip("?.")

    # Convert common words into math symbols
    replacements = [
        ("to the power of", "**"),
        ("raised to", "**"),
        ("multiplied by", "*"),
        ("divided by", "/"),
        ("plus", "+"),
        ("minus", "-"),
        ("times", "*"),
        ("over", "/"),
    ]

    for word, symbol in replacements:
        text = text.replace(word, symbol)

    text = text.replace("×", "*").replace("÷", "/").replace("^", "**")

    # Handle square root phrases
    if text.startswith("square root of "):
        text = "sqrt(" + text[len("square root of "):] + ")"
    elif text.startswith("sqrt of "):
        text = "sqrt(" + text[len("sqrt of "):] + ")"

    tree = ast.parse(text, mode="eval")
    return evaluate(tree)

print("Calculator assistant. Type 'quit' to stop.")
print("Examples: 5 plus 8, 12 divided by 3, square root of 25")

while True:
    question = input("\nYour calculation: ")

    if question.lower().strip() in ("quit", "exit"):
        print("Goodbye!")
        break

    try:
        print("Answer:", calculate(question))
    except Exception as error:
        print("Sorry, I couldn't calculate that:", error)