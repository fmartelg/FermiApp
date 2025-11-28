# Fermi Calculator

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

### Uncertainty Example: Piano Tuners in Chicago

```
# Classic Fermi estimation with uncertainty
population = 2.7M
households = population / 2.5
pianos_per_household = 0.03 0.07
pianos_per_tuner = 200 400
tunings_per_year = 1 2

total_pianos = households * pianos_per_household
total_tunings = total_pianos * tunings_per_year
piano_tuners = total_tunings / pianos_per_tuner
```

**Result:**
```
# Classic Fermi estimation with uncertainty
population = 2.7M
=> 2.70M
households = population / 2.5
=> 1.08M
pianos_per_household = 0.03 0.07
=> 0.03 0.05 0.07 (P10, P50, P90)
pianos_per_tuner = 200 400
=> 220 300 380 (P10, P50, P90)
tunings_per_year = 1 2
=> 1.10 1.50 1.90 (P10, P50, P90)

total_pianos = households * pianos_per_household
=> 36.66K 53.98K 71.24K (P10, P50, P90)
total_tunings = total_pianos * tunings_per_year
=> 50.43K 77.79K 116.36K (P10, P50, P90)
piano_tuners = total_tunings / pianos_per_tuner
=> 127.61 216.84 305.07 (P10, P50, P90)
```

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