# Fermi Sprint Plans

## Sprint 1 - Core Engine + Basic UI

### Goal

Build a minimal working Fermi calculator that can evaluate scalar variables with basic arithmetic, displayed in a two-panel Textual UI.

### Scope

**IN SCOPE:**

- Parse and evaluate scalar values with K/M/B suffixes
- Variable assignment and references
- Basic arithmetic operators: `+`, `-`, `*`, `/`
- Two-panel Textual UI (input TextArea, output display)
- Manual Calculate button
- Simple result display (no distributions yet)

**OUT OF SCOPE (Future sprints):**

- Distributions (uniform, normal, lognormal, beta)
- Monte Carlo sampling
- P10/P50/P90 percentiles
- Parentheses/grouping
- Percentage notation
- Auto-calculate mode
- File save/load
- Syntax highlighting
- Advanced error handling

### Architecture

```
my_proj/
├── fermi_engine.py      # Core calculation engine
├── fermi_parser.py      # Parser for expressions
├── fermi_formatter.py   # Number formatting utilities
├── fermi.py             # Textual app (main)
├── fermi.tcss           # Textual CSS
├── tests/
│   ├── test_parser.py
│   ├── test_engine.py
│   └── test_formatter.py
└── requirements.txt
```

### Steps

#### 1. Setup Project Structure

**Tasks:**

- Create `requirements.txt` with dependencies:

  ```
  textual>=0.47.0
  ```

- Create `tests/` directory
- Keep existing `fermi-spec.md` and `fermi-sprints.md`

#### 2. Build Number Formatter (`fermi_formatter.py`)

**Functions:**

```python
def parse_number(s: str) -> float:
    """Parse '2.7M' -> 2700000.0"""
    # Handle K (1e3), M (1e6), B (1e9)
    # Handle plain numbers: '1000' -> 1000.0
    # Raise ValueError for invalid input

def format_number(n: float) -> str:
    """Format 2700000.0 -> '2.70M'"""
    # Choose appropriate suffix (K/M/B)
    # Format to 2 decimal places
    # Handle edge cases (0, negative, very small)
```

**Test cases:**

```python
assert parse_number("2.7M") == 2700000.0
assert parse_number("10K") == 10000.0
assert parse_number("1.5B") == 1500000000.0
assert parse_number("1000") == 1000.0
assert format_number(2700000) == "2.70M"
assert format_number(10000) == "10.00K"
assert format_number(100) == "100"
```

#### 3. Build Parser (`fermi_parser.py`)

**Functions:**

```python
def parse_line(line: str) -> dict:
    """
    Parse a single line into structured data.
    
    Returns:
    - {"type": "comment", "text": "..."} for comments
    - {"type": "assignment", "var": "x", "expr": "10 * 2"} for assignments
    - {"type": "empty"} for blank lines
    - Raises ParseError for invalid syntax
    """

def tokenize(expr: str) -> list:
    """Tokenize expression into numbers, operators, variables"""
    # Return list of tokens: [("NUMBER", 10), ("OP", "*"), ("VAR", "x")]
```

**Test cases:**

```python
assert parse_line("# comment") == {"type": "comment", "text": " comment"}
assert parse_line("x = 10") == {"type": "assignment", "var": "x", "expr": "10"}
assert parse_line("y = x * 2") == {"type": "assignment", "var": "y", "expr": "x * 2"}
assert parse_line("") == {"type": "empty"}
```

#### 4. Build Evaluator (`fermi_engine.py`)

**Classes/Functions:**

```python
class FermiEngine:
    def __init__(self):
        self.variables = {}  # Symbol table: {"x": 10, "y": 20}
    
    def evaluate_expression(self, expr: str) -> float:
        """Evaluate expression with variables"""
        # Parse expr, substitute variables, compute result
        # Support: +, -, *, /
        # Use Python's eval with restricted namespace (safe)
        
    def execute_line(self, line: str) -> dict:
        """
        Execute one line, return result.
        
        Returns:
        - {"type": "comment"} for comments
        - {"type": "assignment", "var": "x", "value": 10} for assignments
        - {"type": "empty"} for blank lines
        - {"type": "error", "message": "..."} for errors
        """
    
    def execute_model(self, text: str) -> list:
        """Execute entire model, return list of results"""
        # Split into lines
        # Execute each line
        # Return list of results (one per line)
```

**Test cases:**

```python
engine = FermiEngine()
assert engine.evaluate_expression("10 + 20") == 30
engine.variables["x"] = 10
assert engine.evaluate_expression("x * 2") == 20
assert engine.evaluate_expression("x + x") == 20
```

#### 5. Build Textual UI (`fermi.py`)

**Components:**

```python
from textual.app import App, ComposeResult
from textual.widgets import TextArea, Static, Header, Footer, Button
from textual.containers import Horizontal, Vertical
from fermi_engine import FermiEngine

class FermiApp(App):
    CSS_PATH = "fermi.tcss"
    BINDINGS = [
        ("ctrl+enter", "calculate", "Calculate"),
        ("ctrl+q", "quit", "Quit"),
    ]
    
    def __init__(self):
        super().__init__()
        self.engine = FermiEngine()
    
    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="main"):
            with Vertical(id="input-panel"):
                yield Static("Model Definition", classes="panel-title")
                yield TextArea(id="input")
                yield Button("Calculate", id="calc-btn")
            with Vertical(id="output-panel"):
                yield Static("Results", classes="panel-title")
                yield Static("", id="output")
        yield Footer()
    
    def on_button_pressed(self, event):
        if event.button.id == "calc-btn":
            self.action_calculate()
    
    def action_calculate(self):
        # Get input text
        input_widget = self.query_one("#input", TextArea)
        text = input_widget.text
        
        # Execute model
        results = self.engine.execute_model(text)
        
        # Format output
        output_text = self.format_results(results)
        
        # Display
        output_widget = self.query_one("#output", Static)
        output_widget.update(output_text)
    
    def format_results(self, results: list) -> str:
        """Format results for display"""
        # Build output string with => notation
        pass

if __name__ == "__main__":
    app = FermiApp()
    app.run()
```

#### 6. Update CSS (`fermi.tcss`)

```css
#main {
    height: 100%;
}

#input-panel, #output-panel {
    width: 1fr;
    height: 100%;
}

#input {
    height: 1fr;
}

#output {
    height: 1fr;
    padding: 1;
    overflow-y: auto;
}

.panel-title {
    background: $primary;
    padding: 1;
    text-align: center;
}

#calc-btn {
    dock: bottom;
}
```

### Test Scenarios

**Test 1: Simple scalar**

```
Input:
x = 10

Expected Output:
x = 10
=> 10
```

**Test 2: Arithmetic**

```
Input:
x = 10
y = x * 2

Expected Output:
x = 10
=> 10
y = x * 2
=> 20
```

**Test 3: K/M/B suffixes**

```
Input:
population = 2.7M
households = population / 2.5

Expected Output:
population = 2.7M
=> 2.70M
households = population / 2.5
=> 1.08M
```

**Test 4: Comments**

```
Input:
# This is a comment
x = 100

Expected Output:
# This is a comment
x = 100
=> 100
```

### Definition of Done

- [ ] All unit tests passing (parser, formatter, engine)
- [ ] Textual app launches without errors
- [ ] Two-panel layout displays correctly
- [ ] Calculate button executes model
- [ ] Results display aligned with input
- [ ] All 4 test scenarios work correctly
- [ ] K/M/B suffixes parse and format correctly
- [ ] Variables can reference other variables
- [ ] Comments are preserved in output
- [ ] Basic error handling (undefined variable shows error message)

### Deliverable

A working Textual app that can evaluate scalar Fermi calculations like the Piano Tuners example (without distributions).
