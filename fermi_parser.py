"""Parser for Fermi Calculator expressions"""
import re
from typing import Dict, List, Tuple, Any


class ParseError(Exception):
    """Exception raised for parsing errors"""
    pass


def parse_line(line: str) -> Dict[str, Any]:
    """
    Parse a single line into structured data.
    
    Args:
        line: A single line of input text
    
    Returns:
        Dictionary with:
        - {"type": "comment", "text": "..."} for comments
        - {"type": "assignment", "var": "x", "expr": "10 * 2"} for assignments
        - {"type": "empty"} for blank lines
    
    Raises:
        ParseError: If line has invalid syntax
    
    Examples:
        >>> parse_line("# comment")
        {'type': 'comment', 'text': ' comment'}
        
        >>> parse_line("x = 10")
        {'type': 'assignment', 'var': 'x', 'expr': '10'}
        
        >>> parse_line("")
        {'type': 'empty'}
    """
    line = line.rstrip()  # Remove trailing whitespace
    
    # Empty line
    if not line or line.isspace():
        return {"type": "empty"}
    
    # Comment line
    if line.strip().startswith("#"):
        return {"type": "comment", "text": line.strip()[1:]}
    
    # Assignment: variable = expression
    if "=" in line:
        # Split on first = only (in case expression contains =)
        parts = line.split("=", 1)
        if len(parts) != 2:
            raise ParseError(f"Invalid assignment syntax: {line}")
        
        var_name = parts[0].strip()
        expr = parts[1].strip()
        
        # Validate variable name (must be valid Python identifier)
        if not var_name:
            raise ParseError(f"Missing variable name: {line}")
        
        if not var_name.isidentifier():
            raise ParseError(f"Invalid variable name '{var_name}': {line}")
        
        if not expr:
            raise ParseError(f"Missing expression after '=': {line}")
        
        # Reject any '=' in the expression
        if "=" in expr:
            raise ParseError(f"Invalid syntax: '=' not allowed in expression: {line}")
        
        # Check for inline comment
        comment = None
        if "#" in expr:
            expr_parts = expr.split("#", 1)
            expr = expr_parts[0].strip()
            comment = expr_parts[1].strip()
        
        result = {"type": "assignment", "var": var_name, "expr": expr}
        if comment:
            result["comment"] = comment
        
        return result
    
    # If we get here, it's an invalid line
    raise ParseError(f"Invalid syntax: {line}")


def tokenize(expr: str) -> List[Tuple[str, Any]]:
    """
    Tokenize an expression into numbers, operators, and variables.
    
    Args:
        expr: Expression string (e.g., "10 * x + 2.5K")
    
    Returns:
        List of (token_type, value) tuples:
        - ("NUMBER", float_value) for numbers
        - ("OPERATOR", op_string) for operators (+, -, *, /)
        - ("VARIABLE", var_name) for variable references
        - ("LPAREN", "(") for left parenthesis
        - ("RPAREN", ")") for right parenthesis
    
    Examples:
        >>> tokenize("10 * 2")
        [('NUMBER', 10.0), ('OPERATOR', '*'), ('NUMBER', 2.0)]
        
        >>> tokenize("x + 2.5K")
        [('VARIABLE', 'x'), ('OPERATOR', '+'), ('NUMBER', 2500.0)]
    """
    from fermi_formatter import parse_number
    
    tokens = []
    expr = expr.replace(" ", "")  # Remove all spaces
    i = 0
    
    while i < len(expr):
        # Try to match a number (with optional K/M/B suffix)
        match = re.match(r'^\d+\.?\d*[KMB]?', expr[i:])
        if match:
            num_str = match.group()
            try:
                value = parse_number(num_str)
                tokens.append(("NUMBER", value))
                i += len(num_str)
                continue
            except ValueError:
                raise ParseError(f"Invalid number format: {num_str}")
        
        # Try to match a variable
        match = re.match(r'^[a-zA-Z_]\w*', expr[i:])
        if match:
            var_name = match.group()
            tokens.append(("VARIABLE", var_name))
            i += len(var_name)
            continue
        
        # Check for single-character tokens
        char = expr[i]
        
        if char in ['+', '-', '*', '/']:
            tokens.append(("OPERATOR", char))
            i += 1
            continue
        
        if char == '(':
            tokens.append(("LPAREN", "("))
            i += 1
            continue
        
        if char == ')':
            tokens.append(("RPAREN", ")"))
            i += 1
            continue
        
        # If we get here, it's an invalid character
        raise ParseError(f"Invalid character in expression: '{char}'")
    
    return tokens