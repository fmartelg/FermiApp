# Fermi Calculator App Specification

## Overview

A Textual TUI app for performing Fermi estimations with uncertainty quantification using Monte Carlo simulation. The app separates model definition from execution, allowing users to define variables and equations first, then execute the entire model to see results.

## Interaction Model

1. **User defines model** in left TextArea using variable assignments and equations
2. **Syntax highlighting** provides real-time feedback on variables, operators, distributions
3. **User executes model** by pressing "Calculate" button (or Ctrl+Enter)
4. **System evaluates** all expressions in order, propagating uncertainty through calculations
5. **Results display** in right panel, aligned with input expressions
6. **User can edit** any parameter and re-execute to see updated results

## Input Format

### Variable Assignment

```
# Define variables with names
population = 2.7M
people_per_household = 2.5
pianos_per_household = 0.03 0.07  # uniform distribution
tunings_per_year = 1 2 normal      # normal distribution
```

### Basic Operations

```
# Scalar operations
kg_per_tonne = 1000
=> 1000

# Range operations (uniform distribution by default)
population = 2M 3M
=> 2.00M 2.50M 3.00M (P10, P50, P90)

# Arithmetic with variables
households = population / people_per_household
total_pianos = households * pianos_per_household
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
population = 25M 28M lognormal  # North Korea population

# Parentheses for grouping sub-calculations
men_fighting_age = (
    population * 0.5 * 0.3 0.5 beta
)
```

## Output Format

### Display Pattern

```
[variable_name] = [expression]
=> [P10 P50 P90] or [single_value]
```

### Monte Carlo Simulation

- **Default samples**: 100,000 per distribution
- **Output percentiles**: P10 (10th percentile), P50 (median), P90 (90th percentile)
- Ranges created with `min max` syntax use **uniform distribution**
- Ranges with distribution family `min max distname` fit parameters to 90% CI (P5, P95)
- All operations performed element-wise across samples
- Final results show distribution of outcomes
- Variables can be referenced in later expressions

### Number Formatting

- Use K, M, B suffixes for readability (1K = 1,000, 1M = 1,000,000, 1B = 1,000,000,000)
- Show 2 decimal places by default
- For distributions, show P10, P50, P90 values
- Optional: Show sample count for clarity: `(100K samples)`

## Example 1: Piano Tuners in Chicago

### Input (Left Panel)
```
# Piano tuners needed in Chicago

# Define base parameters
population = 2.7M
people_per_household = 2.5
pianos_per_household = 0.03 0.07  # uniform
tunings_per_year = 1 2  # uniform
hours_per_tuning = 2
work_weeks_per_year = 50
hours_per_week = 40
utilization = 0.8

# Calculate intermediate values
households = population / people_per_household
total_pianos = households * pianos_per_household
annual_tunings = total_pianos * tunings_per_year
total_tuning_hours = annual_tunings * hours_per_tuning

# Calculate tuner capacity
tuner_hours_per_year = hours_per_week * work_weeks_per_year * utilization

# Final result
tuners_needed = total_tuning_hours / tuner_hours_per_year
```

### Output (Right Panel)
```
# Piano tuners needed in Chicago

# Define base parameters
population = 2.7M
=> 2.70M

people_per_household = 2.5
=> 2.50

pianos_per_household = 0.03 0.07  # uniform
=> 0.031 0.050 0.069 (P10, P50, P90)

tunings_per_year = 1 2  # uniform
=> 1.10 1.50 1.90 (P10, P50, P90)

hours_per_tuning = 2
=> 2.00

work_weeks_per_year = 50
=> 50

hours_per_week = 40
=> 40

utilization = 0.8
=> 0.80

# Calculate intermediate values
households = population / people_per_household
=> 1.08M

total_pianos = households * pianos_per_household
=> 33.48K 54.00K 74.52K (P10, P50, P90)

annual_tunings = total_pianos * tunings_per_year
=> 36.83K 81.00K 141.59K (P10, P50, P90)

total_tuning_hours = annual_tunings * hours_per_tuning
=> 73.66K 162.00K 283.18K (P10, P50, P90)

# Calculate tuner capacity
tuner_hours_per_year = hours_per_week * work_weeks_per_year * utilization
=> 1600.00

# Final result
tuners_needed = total_tuning_hours / tuner_hours_per_year
=> 46.04 101.25 176.99 (P10, P50, P90)

────────────────────────────────────────
FINAL RESULT: tuners_needed
  P10:  46.04 tuners
  P50: 101.25 tuners  
  P90: 176.99 tuners
  
90% confidence interval: [46.04, 176.99]
────────────────────────────────────────
```

## Example 2: North Korea Food Supply

### Input (Left Panel)

```
# North Korea Food Supply Analysis

# Rice supply (uncertain, lognormal distribution)
rice_tonnes = 600K 700K lognormal

# Conversion factors
kg_per_tonne = 1000
calories_per_kg = 1.2K 1.4K normal

# Population needs
daily_calories = 1.9K 2.5K  # uniform
population = 25M 28M lognormal
days_per_year = 365

# Calculate total calories from rice
rice_kg = rice_tonnes * kg_per_tonne
total_calories = rice_kg * calories_per_kg

# Calculate daily consumption
daily_consumption = population * daily_calories
annual_consumption = daily_consumption * days_per_year

# How long does this last?
years_of_food = total_calories / annual_consumption
```

### Output (Right Panel)
```
# North Korea Food Supply Analysis

# Rice supply (uncertain, lognormal distribution)
rice_tonnes = 600K 700K lognormal
=> 612.34K 648.56K 688.23K (P10, P50, P90)

# Conversion factors
kg_per_tonne = 1000
=> 1000

calories_per_kg = 1.2K 1.4K normal
=> 1.22K 1.30K 1.38K (P10, P50, P90)

# Population needs
daily_calories = 1.9K 2.5K  # uniform
=> 1.96K 2.20K 2.44K (P10, P50, P90)

population = 25M 28M lognormal
=> 25.48M 26.42M 27.58M (P10, P50, P90)

days_per_year = 365
=> 365

# Calculate total calories from rice
rice_kg = rice_tonnes * kg_per_tonne
=> 612.34M 648.56M 688.23M (P10, P50, P90)

total_calories = rice_kg * calories_per_kg
=> 747.25B 843.13B 950.15B (P10, P50, P90)

# Calculate daily consumption
daily_consumption = population * daily_calories
=> 49.94M 58.12M 67.29M (P10, P50, P90)

annual_consumption = daily_consumption * days_per_year
=> 18.23B 21.21B 24.56B (P10, P50, P90)

# How long does this last?
years_of_food = total_calories / annual_consumption
=> 0.030 0.040 0.052 (P10, P50, P90)

────────────────────────────────────────
FINAL RESULT: years_of_food
  P10: 0.030 years (11.0 days)
  P50: 0.040 years (14.6 days)
  P90: 0.052 years (19.0 days)
  
90% confidence interval: [11.0 days, 19.0 days]
────────────────────────────────────────
```

## Example 3: Russian Casualties (with Beta)

### Input (Left Panel)
```
# Russian casualties analysis

# Estimates
casualties = 200K 650K  # uniform

# Population breakdown
russia_population = 125M 155M  # uniform
gender_factor = 0.5  # excluding women
fighting_age_share = 0.3 0.5 beta  # 90% CI

# Calculate
men_total = russia_population * gender_factor
men_fighting_age = men_total * fighting_age_share
casualty_rate = casualties / men_fighting_age
percentage = casualty_rate * 100
```

### Output (Right Panel)
```
# Russian casualties analysis

# Estimates
casualties = 200K 650K  # uniform
=> 245.00K 425.00K 605.00K (P10, P50, P90)

# Population breakdown
russia_population = 125M 155M  # uniform
=> 128.00M 140.00M 152.00M (P10, P50, P90)

gender_factor = 0.5  # excluding women
=> 0.50

fighting_age_share = 0.3 0.5 beta  # 90% CI
=> 0.32 0.40 0.48 (P10, P50, P90)

# Calculate
men_total = russia_population * gender_factor
=> 64.00M 70.00M 76.00M (P10, P50, P90)

men_fighting_age = men_total * fighting_age_share
=> 20.48M 28.00M 36.48M (P10, P50, P90)

casualty_rate = casualties / men_fighting_age
=> 0.0067 0.0152 0.0295 (P10, P50, P90)

percentage = casualty_rate * 100
=> 0.67% 1.52% 2.95% (P10, P50, P90)

────────────────────────────────────────
FINAL RESULT: percentage
  P10: 0.67%
  P50: 1.52%
  P90: 2.95%
  
90% confidence interval: [0.67%, 2.95%]
% chance fighting age male drafted & dies
────────────────────────────────────────
```

## UI Layout

```
┌─ Fermi Calculator ─────────────────────────────────────────────┐
│                                                                │
│  Model Definition (Input)    │  Results (Output)               │
│  ─────────────────────────   │  ────────────────────────────── │
│                              │                                 │
│  [TextArea for model]        │  [Display showing results]      │
│                              │  [Aligned with input lines]     │
│  population = 2.7M           │  population = 2.7M              │
│  households = population/2.5 │  households = 1.08M             │
│  ...                         │  ...                            │
│                              │                                 │
│                              │                                 │
│                              │                                 │
│  ─────────────────────────   │  ────────────────────────────── │
│  [Calculate] [Clear] [Auto]  │  FINAL: result_variable         │
│                              │  P10: ... P50: ... P90: ...     │
└────────────────────────────────────────────────────────────────┘
```

## Technical Requirements

1. **Parser**: Parse variable assignments and expressions, build dependency graph
2. **Evaluator**: Evaluate expressions in correct order, support operators (+, -, *, /, ^, %)
3. **Variable Storage**: Maintain symbol table mapping variable names to values/distributions
4. **Sampling**: Run Monte Carlo with 100K samples for all distributions
5. **Distribution Fitting**: For `min max distname` syntax, fit parameters so P5=min, P95=max
6. **Statistics**: Calculate P10, P50 (median), P90 percentiles from sample arrays
7. **Display**: Format numbers with K/M/B suffixes, show aligned results
8. **Error Handling**: Show parse/evaluation errors inline, highlight problematic lines

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

- **Model-based approach**: Define variables and equations, then execute
- **Named variables**: Reference any variable in later calculations
- **Multiple execution modes**:
  - Manual: Press Calculate button or Ctrl+Enter
  - Auto (optional): Debounced automatic recalculation on changes
- **Clear separation**: Input (model definition) vs Output (results)
- Support for comments (#)
- Parentheses for grouping calculations
- Four distributions: uniform (default), normal, lognormal, beta
- Two syntax styles: `min max distname` (90% CI) or `distname(params)` (explicit)
- Number suffixes: K (thousand), M (million), B (billion)
- Percentage notation: 5% = 0.05
- Monte Carlo simulation with 100K samples
- Output shows P10, P50, P90 percentiles for uncertainty quantification
- Aligned display of inputs and results
- Final result summary section

## Keybindings

- `Ctrl+Enter`: Execute model (calculate all results)
- `Ctrl+L`: Clear all input and results
- `Ctrl+S`: Save current model to file
- `Ctrl+O`: Load model from file
- `Ctrl+M`: Toggle manual/auto calculation mode
- `Ctrl+Q`: Quit application