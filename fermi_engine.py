"""Core evaluation engine for Fermi Calculator"""
from typing import Dict, List, Any, Union
import numpy as np
from fermi_parser import parse_line, tokenize, ParseError
from fermi_formatter import format_number


class FermiEngine:
    """Engine for evaluating Fermi calculator expressions"""
    
    def __init__(self):
        """Initialize the engine with empty variable storage"""
        self.variables: Dict[str, Union[float, np.ndarray]] = {}
        self.num_samples = 100000  # Monte Carlo sample size
    
    def _sample_uniform(self, min_val: float, max_val: float) -> np.ndarray:
        """Generate uniform samples between min and max"""
        return np.random.uniform(min_val, max_val, self.num_samples)
    
    def evaluate_expression(self, expr: str) -> Union[float, np.ndarray]:
        """
        Evaluate an expression with variables.
        
        Args:
            expr: Expression string (e.g., "x * 2", "10 + 20", "2M 3M")
        
        Returns:
            float: If expression is deterministic (no distributions)
            np.ndarray: If expression contains distributions (100K samples)
        
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
            >>> result = engine.evaluate_expression("2M 3M")
            >>> isinstance(result, np.ndarray)
            True
        """
        # Tokenize the expression
        tokens = tokenize(expr)
        
        if not tokens:
            raise ParseError("Empty expression")
        
        # Convert tokens to evaluable form
        return self._evaluate_tokens(tokens)
    
    def _evaluate_tokens(self, tokens: List[tuple]) -> Union[float, np.ndarray]:
        """
        Evaluate a list of tokens using operator precedence.
        
        Handles: +, -, *, /, parentheses, and UNIFORM distributions
        Strategy:
        - UNIFORM tokens → generate numpy arrays
        - NUMBER tokens → stay as floats
        - VARIABLE tokens → look up (can be float or array)
        - Operations work element-wise when arrays involved
        """
        expr_parts = []
        
        for token in tokens:
            token_type = token[0]
            
            if token_type == "NUMBER":
                value = token[1]
                expr_parts.append(str(value))
            
            elif token_type == "UNIFORM":
                min_val, max_val = token[1], token[2]
                samples = self._sample_uniform(min_val, max_val)
                # Store array in a temp variable for eval
                var_name = f"_dist_{len(expr_parts)}"
                self.variables[var_name] = samples
                expr_parts.append(var_name)
            
            elif token_type == "VARIABLE":
                var_name = token[1]
                if var_name not in self.variables:
                    raise NameError(f"Undefined variable: {var_name}")
                expr_parts.append(var_name)
            
            elif token_type == "OPERATOR":
                expr_parts.append(token[1])
            
            elif token_type == "LPAREN":
                expr_parts.append("(")
            
            elif token_type == "RPAREN":
                expr_parts.append(")")
        
        expr_string = "".join(expr_parts)
        
        # Evaluate using Python's eval (safe because we control the tokens)
        try:
            # Eval with access to variables (including temp distribution arrays)
            result = eval(expr_string, {"__builtins__": {}}, self.variables)
            
            # Clean up temporary distribution variables
            temp_vars = [k for k in self.variables.keys() if k.startswith("_dist_")]
            for k in temp_vars:
                del self.variables[k]
            
            if isinstance(result, np.ndarray):
                return result
            else:
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
            - {"type": "assignment", "var": "x", "value": np.ndarray} for distributions
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
                
                # Evaluate the expression (returns float or np.ndarray)
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