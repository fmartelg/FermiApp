# Fermi Calculator App Specification

## Overview

A Textual TUI app for performing Fermi estimations with uncertainty quantification using Monte Carlo simulation.

## Input Format

### Basic Operations

```
# Simple ranges (uniform distribution)
population = 2M 3M
=> 2.00M 2.50M 3.00M (P10, P50, P90)

# Fixed values
kg_per_tonne = 1000
=> 1000

# Arithmetic operations
600K 700K * 1K
=> 600.05M 650.12M 699.87M

# Chained calculations
2M 3M / 365
=> 5482.19 6849.32 8219.18
```

### Distribution Syntax

```
# Uniform: min max (default)
pianos = 50K 60K
=> 50.50K 55.00K 59.50K (P10, P50, P90)

# Normal: min max normal (90% CI)
tunings_per_year = 1.2 1.8 normal
=> 1.31 1.50 1.69 (fitted normal distribution)

# Lognormal: min max lognormal (90% CI)
income = 30K 80K lognormal
=> 34.2K 50.5K 73.8K (fitted lognormal)

# Beta: min max beta (90% CI, bounds in [0,1])
proportion = 0.3 0.5 beta
=> 0.32 0.40 0.48 (fitted beta)

# Advanced: explicit parameters
tunings = normal(1.5, 0.234)  # mean, std
income = lognormal(50K, 1.5)   # median, shape
proportion = beta(40, 60)      # alpha, beta

# Percentage shorthand (uniform)
adoption_rate = 5% 10%
=> 5.50% 7.50% 9.50%
```

### Comments and Grouping

```
# Comments start with #
population = 25M 28M  # North Korea population

# Parentheses for sub-calculations
/ (
    125M 155M  # Population of Russia
    * 0.5      # Excluding women
    * 0.3 0.5 beta  # Share of men "of fighting age"
)
=> result with P10, P50, P90
```

## Output Format

### Display Pattern

```
[input expression]
=> [P10 P50 P90] or [single_value]
```

### Monte Carlo Simulation

- **Default samples**: 100,000 per distribution
- **Output percentiles**: P10 (10th percentile), P50 (median), P90 (90th percentile)
- Ranges created with `min max` syntax use **uniform distribution**
- Ranges with distribution family `min max normal` fit parameters to 90% CI (P5, P95)
- All operations performed element-wise across samples
- Final results show distribution of outcomes

### Number Formatting

- Use K, M, B suffixes for readability (1K = 1,000, 1M = 1,000,000, 1B = 1,000,000,000)
- Show 2 decimal places by default
- For distributions, show P10, P50, P90 values
- Show sample count for clarity: `(100.00K samples)`

## Example 1: Piano Tuners in Chicago

```
# Piano tuners needed in Chicago
2.7M              # population
=> 2.70M
/ 2.5             # people per household
=> 1.08M
* 0.03 0.07       # pianos per household (uniform)
=> 32.94K 54.21K 75.42K (P10, P50, P90, 100K samples)
* 1 2             # tunings per year (uniform)
=> 33.12K 81.32K 150.84K (100K samples)
* 2               # hours per tuning
=> 66.24K 162.64K 301.68K
/ (
    40 * 50 * 0.8  # tuner working hours per year
    => 1600
)
=> 41.40 101.65 188.55   # tuners needed (P10, P50, P90)
```

## Example 2: North Korea Food Supply

```
600K 700K         # tonnes of rice (uniform)
=> 610.00K 650.00K 690.00K (P10, P50, P90)
* 1K              # kg in a tonne
=> 610.00M 650.00M 690.00M
* 1.2K 1.4K       # calories per kg of rice (uniform)
=> 732.24B 845.00B 965.88B
/ 1.9K 2.5K       # daily caloric intake (uniform)
=> 292.90M 444.74M 508.36M
/ 25M 28M         # population of NK (uniform)
=> 10.46 17.79 20.33
/ 365             # years of food this buys
=> 0.029 0.049 0.056
```

## Example 3: Russian Casualties (with Beta)

```
200K 650K         # Russian casualties (uniform)
=> 245.00K 425.00K 605.00K (P10, P50, P90)
/ (
    125M 155M      # Population of Russia (uniform)
    => 128.00M 140.00M 152.00M
    * 0.5          # Excluding women
    => 64.00M 70.00M 76.00M
    * 0.3 0.5 beta # Share of men "of fighting age" (90% CI)
    => 20.48M 28.00M 36.48M (100.00K samples)
)
=> 0.0067 0.0152 0.0295 (100.00K samples)
* 100
=> 0.67% 1.52% 2.95% (100.00K samples)
# ^ percentage chance fighting age male drafted & dies
```

## UI Layout

```
┌─ Fermi Calculator ─────────────────────────────────┐
│                                                     │
│  Input                    │  Results                │
│  ──────────────────────   │  ─────────────────────  │
│  [TextArea for           │  [Display area showing │
│   multi-line input]      │   step-by-step calc    │
│                          │   with => P10/P50/P90] │
│                          │                        │
│                          │                        │
│  [Calculate Button]      │  [Final Result:]       │
│                          │  [P10, P50, P90]       │
└─────────────────────────────────────────────────────┘
```

## Technical Requirements

1. **Parser**: Parse expressions line-by-line, identify operators and distributions
2. **Evaluator**: Support basic math (+, -, *, /, ^, %)
3. **Sampling**: Run Monte Carlo with 100K samples default for all distributions
4. **Distribution Fitting**: For `min max distname` syntax, fit parameters so P5=min, P95=max
5. **Statistics**: Calculate P10, P50 (median), P90 percentiles from sample arrays
6. **Display**: Format numbers with K/M/B suffixes, show three percentile values
7. **Error Handling**: Show parse errors inline, highlight problematic lines

## Distribution Details

### Uniform Distribution (default for ranges)

- **Syntax**: `min max`
- Generates uniform random samples between min and max
- Example: `2M 3M` → uniform(2M, 3M)

### Normal Distribution

- **Syntax (CI)**: `min max normal` - fits normal so P5=min, P95=max
- **Syntax (explicit)**: `normal(mean, std_dev)`
- Generates samples from normal distribution
- Example: `1.2 1.8 normal` → fitted to 90% CI
- Example: `normal(100, 15)` → mean=100, std=15

### Lognormal Distribution

- **Syntax (CI)**: `min max lognormal` - fits lognormal so P5=min, P95=max
- **Syntax (explicit)**: `lognormal(median, shape)`
- For positive-only values with right skew
- Example: `30K 80K lognormal` → fitted to 90% CI
- Example: `lognormal(50K, 1.5)` → median=50K, shape=1.5

### Beta Distribution

- **Syntax (CI)**: `min max beta` - fits beta so P5=min, P95=max (values in [0,1])
- **Syntax (explicit)**: `beta(alpha, beta)`
- Bounded between 0 and 1, for proportions
- Example: `0.3 0.5 beta` → fitted to 90% CI
- Example: `beta(40, 60)` → alpha=40, beta=60, mean≈0.4

## Key Features

- Real-time evaluation as user types (debounced)
- Support for comments (#)
- Parentheses for grouping calculations
- Four distributions: uniform (default), normal, lognormal, beta
- Two syntax styles: `min max distname` (90% CI) or `distname(params)` (explicit)
- Number suffixes: K (thousand), M (million), B (billion)
- Percentage notation: 5% = 0.05
- Monte Carlo simulation with 100K samples
- Output shows P10, P50, P90 percentiles for uncertainty quantification
