import ast
import operator
import re
from crewai.tools import tool


# Safe operators mapping
SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
}


class SafeEvaluator(ast.NodeVisitor):
    """Safely evaluate mathematical expressions using AST."""
    
    def __init__(self):
        self.result = None
    
    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_type = type(node.op)
        
        if op_type in SAFE_OPERATORS:
            self.result = SAFE_OPERATORS[op_type](left, right)
        else:
            raise ValueError(f"Unsupported operator: {op_type}")
        
        return self.result
    
    def visit_Num(self, node):
        return node.n
    
    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        if isinstance(node.op, ast.USub):
            return -operand
        elif isinstance(node.op, ast.UAdd):
            return operand
        return operand
    
    def visit_Constant(self, node):
        return node.value


cat > backend/app/tools/calculator_tool.py << 'EOF'
import ast
import operator
import re
from crewai.tools import tool


# Safe operators mapping
SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
}


class SafeEvaluator(ast.NodeVisitor):
    """Safely evaluate mathematical expressions using AST."""
    
    def __init__(self):
        self.result = None
    
    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_type = type(node.op)
        
        if op_type in SAFE_OPERATORS:
            self.result = SAFE_OPERATORS[op_type](left, right)
        else:
            raise ValueError(f"Unsupported operator: {op_type}")
        
        return self.result
    
    def visit_Num(self, node):
        return node.n
    
    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        if isinstance(node.op, ast.USub):
            return -operand
        elif isinstance(node.op, ast.UAdd):
            return operand
        return operand
    
    def visit_Constant(self, node):
        return node.value


@tool("CalculatorTool")
class CalculatorTool:
    """
    Safely evaluates mathematical expressions.
    Uses AST-based parsing instead of eval() for security.
    """
    
    def _run(self, expression: str) -> str:
        """Evaluate a mathematical expression safely."""
        sanitized = re.sub(r'[^0-9+\-*/().\s]', '', expression)
        
        if not sanitized or sanitized.count('(') != sanitized.count(')'):
            return "Error: Invalid expression"
        
        try:
            tree = ast.parse(sanitized, mode='eval')
            evaluator = SafeEvaluator()
            result = evaluator.visit(tree.body)
            return f"Result: {result}"
        except Exception as e:
            return f"Error: {str(e)}"
