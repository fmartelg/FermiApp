"""Core evaluation engine for Fermi Calculator"""
from typing import Dict, List, Any
from fermi_parser import parse_line, tokenize, ParseError
from fermi_formatter import format_number


class FermiEngine:
    """Engine for evaluating Fermi calculator expressions"""
    
    def __init__(self):
        """Initialize the engine with empty variable storage"""
        self.variables: Dict[str, float] = {}
    
    def evaluate_expression(self, expr: str) -> float:
        """
        Evaluate an expression with variables.
        
        Args:
            expr: Expression string (e.g., "x * 2", "10 + 20")
        
        Returns:
            Computed float value
        
        Raises:
            ParseError: If expression is invalid
            NameError: If variable is undefined
        
        Examples:
            >>> engine = FermiEngine()
            >>> engine.evaluate_expression("10 + 20")
            30.0
            >>> engine.variables["x"] = 10
            >>> engine.evaluate_expression("x * 2")
            20.0
        """
        # Tokenize the expression
        tokens = tokenize(expr)
        
        if not tokens:
            raise ParseError("Empty expression")
        
        # Convert tokens to evaluable form
        # Build a simple expression evaluator
        return self._evaluate_tokens(tokens)
    
    def _evaluate_tokens(self, tokens: List[tuple]) -> float:
        """
        Evaluate a list of tokens using operator precedence.
        
        Handles: +, -, *, /, parentheses
        Uses standard math precedence: () > * / > + -
        """
        # Convert tokens to postfix notation (Shunting Yard algorithm)
        # Then evaluate postfix
        
        # For now, use a simpler approach: convert to Python expression
        # and use eval with restricted namespace
        
        expr_parts = []
        for token_type, value in tokens:
            if token_type == "NUMBER":
                expr_parts.append(str(value))
            elif token_type == "VARIABLE":
                if value not in self.variables:
                    raise NameError(f"Undefined variable: {value}")
                expr_parts.append(str(self.variables[value]))
            elif token_type == "OPERATOR":
                expr_parts.append(value)
            elif token_type == "LPAREN":
                expr_parts.append("(")
            elif token_type == "RPAREN":
                expr_parts.append(")")
        
        expr_string = "".join(expr_parts)
        
        # Evaluate using Python's eval (safe because we control the tokens)
        try:
            result = eval(expr_string, {"__builtins__": {}}, {})
            return float(result)
        except Exception as e:
            raise ParseError(f"Evaluation error: {e}")
    
    def execute_line(self, line: str) -> Dict[str, Any]:
        """
        Execute one line, return result.
        
        Args:
            line: A single line of input
        
        Returns:
            Dictionary with:
            - {"type": "comment"} for comments
            - {"type": "assignment", "var": "x", "value": 10.0} for assignments
            - {"type": "empty"} for blank lines
            - {"type": "error", "message": "..."} for errors
        
        Examples:
            >>> engine = FermiEngine()
            >>> engine.execute_line("x = 10")
            {'type': 'assignment', 'var': 'x', 'value': 10.0}
            >>> engine.variables["x"]
            10.0
        """
        try:
            parsed = parse_line(line)
            
            if parsed["type"] == "comment":
                return {"type": "comment", "text": parsed["text"]}
            
            elif parsed["type"] == "empty":
                return {"type": "empty"}
            
            elif parsed["type"] == "assignment":
                var_name = parsed["var"]
                expr = parsed["expr"]
                
                # Evaluate the expression
                value = self.evaluate_expression(expr)
                
                # Store in variables
                self.variables[var_name] = value
                
                result = {
                    "type": "assignment",
                    "var": var_name,
                    "value": value
                }
                
                # Include comment if present
                if "comment" in parsed:
                    result["comment"] = parsed["comment"]
                
                return result
            
            else:
                return {"type": "error", "message": f"Unknown line type: {parsed['type']}"}
        
        except (ParseError, NameError) as e:
            return {"type": "error", "message": str(e)}
        except Exception as e:
            return {"type": "error", "message": f"Unexpected error: {e}"}
    
    def execute_model(self, text: str) -> List[Dict[str, Any]]:
        """
        Execute entire model, return list of results.
        
        Args:
            text: Multi-line model text
        
        Returns:
            List of result dictionaries (one per line)
        
        Examples:
            >>> engine = FermiEngine()
            >>> results = engine.execute_model("x = 10\\ny = x * 2")
            >>> len(results)
            2
            >>> results[0]["value"]
            10.0
            >>> results[1]["value"]
            20.0
        """
        lines = text.split("\n")
        results = []
        
        for line in lines:
            result = self.execute_line(line)
            results.append(result)
        
        return results
    
    def clear(self):
        """Clear all stored variables"""
        self.variables.clear()