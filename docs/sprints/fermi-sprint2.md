# Sprint Plan

## Sprint 2 - Uniform Distributions & Monte Carlo

### Goal

Add uniform distribution support with Monte Carlo simulation, transforming the calculator from scalar-only to probabilistic modeling with uncertainty quantification.

### Scope

**IN SCOPE:**

- Parse `min max` syntax for uniform distributions
- Generate 100K Monte Carlo samples using numpy
- Store and propagate arrays through calculations
- Element-wise arithmetic operations (scalar * array, array * array)
- Calculate P10, P50, P90 percentiles
- Format output with three percentile values
- Mix scalars and distributions in same model
- Update all modules to handle both scalar and array types

**OUT OF SCOPE (Future sprints):**

- Named distributions (normal, lognormal, beta) - Sprint 3
- Explicit distribution parameters: `normal(mean, std)` - Sprint 3
- Distribution fitting for 90% CI - Sprint 3
- Percentage notation (5% = 0.05) - Sprint 3
- Parentheses/grouping - Sprint 3
- Power operator (^) - Sprint 3
- Final result summary box - Sprint 4
- File operations - Sprint 4
- Auto-calculate mode - Sprint 4

### Architecture Changes

```
my_proj/
├── fermi_engine.py      # MODIFY: Handle arrays, numpy operations
├── fermi_parser.py      # MODIFY: Detect min max patterns
├── fermi_formatter.py   # MODIFY: Format distributions (P10/P50/P90)
├── fermi.py             # MODIFY: Display distribution results
├── fermi.tcss           # No changes needed
├── tests/
│   ├── test_parser.py   # ADD: Tests for min max parsing
│   ├── test_engine.py   # ADD: Tests for array operations
│   └── test_formatter.py # ADD: Tests for distribution formatting
└── requirements.txt     # MODIFY: Add numpy
```

### Steps

#### 1. Update Dependencies

**Tasks:**
- Add numpy to `requirements.txt`:
  ```
  textual>=0.47.0
  pytest>=7.4.0
  numpy>=1.24.0
  ```
- Install: `pip install numpy`

#### 2. Extend Parser (`fermi_parser.py`)

**Modify `tokenize()` to detect uniform distributions:**

```python
# Current: tokenize("2M 3M") → [("NUMBER", 2e6), ("NUMBER", 3e6)]
# New:     tokenize("2M 3M") → [("UNIFORM", 2e6, 3e6)]
```

**Implementation approach:**
- After tokenizing, check if we have exactly 2 consecutive NUMBER tokens
- If yes, combine them into a UNIFORM token
- Return `("UNIFORM", min_value, max_value)`

**Test cases:**
```python
assert tokenize("2M 3M") == [("UNIFORM", 2e6, 3e6)]
assert tokenize("10 20") == [("UNIFORM", 10.0, 20.0)]
assert tokenize("x + 5 10") == [("VARIABLE", "x"), ("OPERATOR", "+"), ("UNIFORM", 5.0, 10.0)]
assert tokenize("10") == [("NUMBER", 10.0)]  # Single number stays NUMBER
```

#### 3. Update Formatter (`fermi_formatter.py`)

**Add new function to format distributions:**

```python
import numpy as np

def format_distribution(arr: np.ndarray) -> str:
    """
    Format distribution as P10, P50, P90 percentiles.
    
    Args:
        arr: numpy array of samples (e.g., 100K samples)
    
    Returns:
        Formatted string like "2.00M 2.50M 3.00M (P10, P50, P90)"
    
    Examples:
        >>> samples = np.random.uniform(2e6, 3e6, 100000)
        >>> format_distribution(samples)
        "2.00M 2.50M 3.00M (P10, P50, P90)"
    """
    p10, p50, p90 = np.percentile(arr, [10, 50, 90])
    return f"{format_number(p10)} {format_number(p50)} {format_number(p90)} (P10, P50, P90)"
```

**Test cases:**
```python
def test_format_distribution_uniform():
    samples = np.random.uniform(2e6, 3e6, 100000)
    result = format_distribution(samples)
    # Should show values around 2M-3M with P10/P50/P90 labels
    assert "P10" in result
    assert "P50" in result
    assert "P90" in result
    assert "M" in result  # Should use M suffix
```

#### 4. Update Engine (`fermi_engine.py`)

**Major changes to handle arrays:**

**4a. Import numpy:**
```python
import numpy as np
from typing import Dict, List, Any, Union
```

**4b. Change variable storage type:**
```python
class FermiEngine:
    def __init__(self):
        # Variables can now be float OR numpy array
        self.variables: Dict[str, Union[float, np.ndarray]] = {}
        self.num_samples = 100000  # Monte Carlo sample size
```

**4c. Add sampling method:**
```python
def _sample_uniform(self, min_val: float, max_val: float) -> np.ndarray:
    """Generate uniform samples between min and max"""
    return np.random.uniform(min_val, max_val, self.num_samples)
```

**4d. Update `evaluate_expression()` return type:**
```python
def evaluate_expression(self, expr: str) -> Union[float, np.ndarray]:
    """
    Evaluate expression - returns scalar or array.
    
    Returns:
        float: If expression is deterministic (no distributions)
        np.ndarray: If expression contains distributions (100K samples)
    """
    tokens = tokenize(expr)
    if not tokens:
        raise ParseError("Empty expression")
    return self._evaluate_tokens(tokens)
```

**4e. Update `_evaluate_tokens()` to handle UNIFORM and arrays:**
```python
def _evaluate_tokens(self, tokens: List[tuple]) -> Union[float, np.ndarray]:
    """
    Evaluate tokens, handling both scalars and distributions.
    
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
        
        elif token_type in ("LPAREN", "RPAREN"):
            expr_parts.append(token[1])
    
    expr_string = "".join(expr_parts)
    
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
```

**Test cases:**
```python
def test_evaluate_uniform_distribution():
    engine = FermiEngine()
    result = engine.evaluate_expression("2M 3M")
    assert isinstance(result, np.ndarray)
    assert len(result) == 100000
    assert result.min() >= 2e6
    assert result.max() <= 3e6

def test_scalar_times_distribution():
    engine = FermiEngine()
    engine.variables["x"] = 10.0
    result = engine.evaluate_expression("x * 5 10")
    assert isinstance(result, np.ndarray)
    # Result should be 50-100 range

def test_distribution_arithmetic():
    engine = FermiEngine()
    result = engine.evaluate_expression("10 20 + 5 10")
    assert isinstance(result, np.ndarray)
    # Result should be 15-30 range

def test_mixed_model():
    engine = FermiEngine()
    engine.execute_line("pop = 2M 3M")
    engine.execute_line("households = pop / 2.5")
    
    pop = engine.variables["pop"]
    households = engine.variables["households"]
    
    assert isinstance(pop, np.ndarray)
    assert isinstance(households, np.ndarray)
```

#### 5. Update UI (`fermi.py`)

**Modify `format_results()` to handle distributions:**

```python
from fermi_formatter import format_number, format_distribution
import numpy as np

def format_results(self, input_text: str, results: list) -> str:
    """
    Format results for display with => notation.
    Handles both scalars and distributions.
    """
    input_lines = input_text.split("\n")
    output_lines = []
    
    for line, result in zip(input_lines, results):
        # Add the input line
        output_lines.append(line)
        
        # Add the result on the next line with =>
        if result["type"] == "assignment":
            value = result["value"]
            
            # Check if value is array (distribution) or scalar
            if isinstance(value, np.ndarray):
                formatted_value = format_distribution(value)
            else:
                formatted_value = format_number(value)
            
            output_lines.append(f"=> {formatted_value}")
        
        elif result["type"] == "error":
            output_lines.append(f"=> ERROR: {result['message']}")
    
    return "\n".join(output_lines)
```

### Test Scenarios

**Test 1: Simple uniform distribution**
```
Input:
x = 2M 3M

Expected Output:
x = 2M 3M
=> 2.00M 2.50M 3.00M (P10, P50, P90)
```

**Test 2: Distribution arithmetic**
```
Input:
a = 10 20
b = 5 10
c = a + b

Expected Output:
a = 10 20
=> 10.50 15.00 19.50 (P10, P50, P90)
b = 5 10
=> 5.50 7.50 9.50 (P10, P50, P90)
c = a + b
=> 16.00 22.50 29.00 (P10, P50, P90)
```

**Test 3: Mixed scalar and distribution**
```
Input:
population = 2M 3M
households = population / 2.5

Expected Output:
population = 2M 3M
=> 2.00M 2.50M 3.00M (P10, P50, P90)
households = population / 2.5
=> 800.00K 1.00M 1.20M (P10, P50, P90)
```

**Test 4: Piano tuners (simplified)**
```
Input:
population = 2.7M
pianos_per_household = 0.03 0.07
households = population / 2.5
total_pianos = households * pianos_per_household

Expected Output:
population = 2.7M
=> 2.70M
pianos_per_household = 0.03 0.07
=> 0.032 0.050 0.068 (P10, P50, P90)
households = population / 2.5
=> 1.08M
total_pianos = households * pianos_per_household
=> 34.56K 54.00K 73.44K (P10, P50, P90)
```

### Definition of Done

- [x] numpy added to dependencies and installed
- [x] Parser detects `min max` pattern and creates UNIFORM tokens
- [x] Engine generates 100K samples for uniform distributions
- [x] Engine stores arrays in variables dictionary
- [x] Scalar * scalar operations return scalars
- [x] Scalar * array operations return arrays (broadcasting)
- [x] Array * array operations return arrays (element-wise)
- [x] `format_distribution()` calculates and formats P10/P50/P90
- [x] UI displays distributions with three percentile values
- [x] All 4 test scenarios pass
- [x] Existing scalar tests still pass (backward compatibility)
- [x] Unit tests for uniform distribution functionality (15+ new tests)
- [x] Mixed scalar/distribution models work correctly

### Deliverable

A Fermi calculator that supports uniform distributions with Monte Carlo simulation, propagating uncertainty through calculations and displaying P10/P50/P90 percentiles.

### Notes

**Backward Compatibility:**
- All Sprint 1 functionality must still work
- Scalar-only models produce identical output as before
- Only difference: distributions now supported

**Random Seed (Optional):**
- Consider adding `np.random.seed(42)` for reproducible tests
- Can make tests deterministic for easier validation

**Performance:**
- 100K samples may be slow for complex models
- Can optimize later if needed (Sprint 4+)
- For Sprint 2, correctness > speed