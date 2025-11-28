# Fermi Calculator

![Version](https://img.shields.io/badge/version-0.1.0-blue)

A Textual TUI application for performing Fermi estimations with uncertainty quantification using Monte Carlo simulation.

![Screenshot](./Screenshot%202025-11-27%20222310.png)

Inspired by and based on Nuño Sempere's [fermi CLI calculator](https://git.nunosempere.com/NunoSempere/fermi).

## Features

- 🎲 **Monte Carlo Simulation**: 100,000 samples for robust uncertainty quantification
- 📊 **Uniform Distributions**: Use `min max` syntax for uncertain quantities
- 🔢 **Number Suffixes**: Support for K (thousand), M (million), B (billion) notation
- 📈 **Percentile Output**: Displays P10, P50 (median), and P90 values
- 🎨 **Modern TUI**: Two-panel Textual interface with real-time updates
- 🧮 **Mathematical Operations**: Standard arithmetic (+, -, *, /, ^)
- 💾 **Variable Storage**: Define and reference variables across calculations
- ⚡ **Instant Results**: Calculate with F5 or click the Calculate button

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/fermi_calc.git
cd fermi_calc

# Create and activate a virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Dependencies

- `textual` - Modern TUI framework
- `numpy` - Numerical computing for Monte Carlo simulation

## Usage

Run the calculator:

```bash
python fermi.py
```

### Basic Example

```
# Simple scalar calculation
population = 2.7M
households = population / 2.5
```

**Result:**
```
population = 2.7M
=> 2.70M

households = population / 2.5
=> 1.08M
```

### Uncertainty Example: MBA Enrollment Marketing Campaign

```
tam = 45M 55M                        # Total addressable market
aware_rate = 0.30 0.50               # See online ad
interest_rate = 0.10 0.20            # Click on ad
consideration_rate = 0.40 0.60       # Visit MBA program detail page
intent_rate = 0.15 0.30              # Visit enrollment page
conversion_rate = 0.50 0.70          # Complete enrollment

aware = tam * aware_rate
interest = aware * interest_rate
consideration = interest * consideration_rate
intent = consideration * intent_rate
enrollments = intent * conversion_rate
```

**Result:**
```
tam = 45M 55M                        # Total addressable market
=> 46.00M 50.02M 54.00M (P10, P50, P90)
aware_rate = 0.30 0.50               # See online ad
=> 0.32 0.40 0.48 (P10, P50, P90)
interest_rate = 0.10 0.20            # Click on ad
=> 0.11 0.15 0.19 (P10, P50, P90)
consideration_rate = 0.40 0.60       # Visit product detail page
=> 0.42 0.50 0.58 (P10, P50, P90)
intent_rate = 0.15 0.30              # Visit enrollment page
=> 0.17 0.22 0.28 (P10, P50, P90)
conversion_rate = 0.50 0.70          # Complete enrollment
=> 0.52 0.60 0.68 (P10, P50, P90)

aware = tam * aware_rate
=> 15.88M 19.93M 24.25M (P10, P50, P90)
interest = aware * interest_rate
=> 2.06M 2.93M 4.05M (P10, P50, P90)
consideration = interest * consideration_rate
=> 995.53K 1.45M 2.07M (P10, P50, P90)
intent = consideration * intent_rate
=> 203.18K 320.19K 495.88K (P10, P50, P90)
enrollments = intent * conversion_rate
=> 119.32K 191.48K 301.13K (P10, P50, P90)
```

**Interpreting Results:**

The output shows three key percentiles from the Monte Carlo simulation:
- **P10 (119.32K)**: 10% of simulated outcomes fall below this value
- **P50 (191.48K)**: The median - half the simulations are above, half below
- **P90 (301.13K)**: 90% of simulated outcomes fall above this value

The **P10-P90 range (119K-301K)** represents an 80% credible interval. You might say: "Given my current beliefs about conversion rates and market size, I estimate an 80% probability that enrollments will fall between 119K and 301K."

**Important caveat:** These results only reflect the uncertainties you've specified in your input ranges. If your input estimates are overconfident (ranges too narrow) or miss key factors, the output will be similarly flawed. Fermi calculations help you think systematically about uncertainty, but they're only as good as your assumptions and the beliefs they encode.

### Syntax Guide

| Feature              | Syntax                  | Example                   |
| -------------------- | ----------------------- | ------------------------- |
| Variable assignment  | `name = expression`     | `cost = 1000`             |
| Uniform distribution | `min max`               | `price = 10 20`           |
| Number suffixes      | `K`, `M`, `B`           | `population = 2.7M`       |
| Arithmetic           | `+`, `-`, `*`, `/`, `^` | `total = a * b + c`       |
| Comments             | `#`                     | `# This is a comment`     |
| Variable reference   | Use variable name       | `total = cost * quantity` |

## Documentation

- **[Complete Specification](docs/fermi-spec.md)** - Full feature documentation
- **[Sprint 1 Notes](docs/sprints/fermi-sprint1.md)** - Basic calculations
- **[Sprint 2 Notes](docs/sprints/fermi-sprint2.md)** - Uniform distributions

## Development

### Project Structure

```
fermi_calc/
├── docs/
│   ├── fermi-spec.md           # Complete specification
│   └── sprints/                # Development sprint notes
├── tests/
│   ├── test_engine.py          # Tests for evaluation engine
│   ├── test_formatter.py       # Tests for number formatting
│   └── test_parser.py          # Tests for expression parsing
├── .gitignore                  # Git ignore rules
├── fermi_engine.py             # Core evaluation engine with Monte Carlo
├── fermi_formatter.py          # Number parsing and formatting utilities
├── fermi_parser.py             # Expression parser and tokenizer
├── fermi.py                    # Main application entry point
├── fermi.tcss                  # Textual CSS styling
├── LICENSE                     # MIT License
├── README.md                   # This file
└── requirements.txt            # Python dependencies
```

### Running Tests

```bash
# Run test suite
pytest tests/

# Run with coverage
pytest --cov=. tests/
```

## Roadmap

- [x] **Sprint 1**: Basic scalar calculations and variable references
- [x] **Sprint 2**: Uniform distributions with Monte Carlo simulation
- [ ] **Sprint 3**: Additional distributions (normal, lognormal, beta)
- [ ] **Sprint 4**: File save/load functionality
- [ ] **Sprint 5**: Enhanced UI features and export options

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Credits

This project is inspired by and based on Nuño Sempere's [fermi CLI calculator](https://git.nunosempere.com/NunoSempere/fermi), which provides a command-line interface for similar Fermi estimation workflows.

## License

MIT License - See [license.md](license.md) for details.

## Contact

- **Issues**: [GitHub Issues](https://github.com/yourusername/fermi_calc/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/fermi_calc/discussions)

## Acknowledgments

- Nuño Sempere for the original fermi calculator concept
- The Textual framework team for the excellent TUI library
- The Python scientific computing community

---

*Made with **AI** for better Fermi estimations*