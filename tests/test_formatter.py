"""Tests for fermi_formatter module"""
import pytest
import numpy as np
from fermi_formatter import parse_number, format_number, format_distribution


class TestParseNumber:
    """Tests for parse_number function"""
    
    def test_parse_millions(self):
        assert parse_number("2.7M") == 2700000.0
    
    def test_parse_thousands(self):
        assert parse_number("10K") == 10000.0
    
    def test_parse_billions(self):
        assert parse_number("1.5B") == 1500000000.0
    
    def test_parse_plain_number(self):
        assert parse_number("1000") == 1000.0
    
    def test_parse_decimal(self):
        assert parse_number("2.5K") == 2500.0
    
    def test_parse_lowercase_suffix(self):
        assert parse_number("5m") == 5000000.0
    
    def test_parse_with_whitespace(self):
        assert parse_number("  10K  ") == 10000.0
    
    def test_parse_invalid_raises_error(self):
        with pytest.raises(ValueError):
            parse_number("invalid")
    
    def test_parse_empty_raises_error(self):
        with pytest.raises(ValueError):
            parse_number("")


class TestFormatNumber:
    """Tests for format_number function"""
    
    def test_format_millions(self):
        assert format_number(2700000) == "2.70M"
    
    def test_format_thousands(self):
        assert format_number(10000) == "10.00K"
    
    def test_format_plain(self):
        assert format_number(100) == "100"
    
    def test_format_billions(self):
        assert format_number(1500000000) == "1.50B"
    
    def test_format_small_decimal(self):
        result = format_number(2.5)
        assert result == "2.50"
    
    def test_format_zero(self):
        assert format_number(0) == "0"
    
    def test_format_negative(self):
        assert format_number(-5000000) == "-5.00M"


class TestFormatDistribution:
    """Tests for format_distribution function"""
    
    def test_format_distribution_uniform_millions(self):
        np.random.seed(42)  # For reproducibility
        samples = np.random.uniform(2e6, 3e6, 100000)
        result = format_distribution(samples)
        
        assert "P10" in result
        assert "P50" in result
        assert "P90" in result
        assert "M" in result  # Should use M suffix
    
    def test_format_distribution_uniform_thousands(self):
        np.random.seed(42)
        samples = np.random.uniform(10000, 20000, 100000)
        result = format_distribution(samples)
        
        assert "P10" in result
        assert "K" in result  # Should use K suffix
    
    def test_format_distribution_percentile_values(self):
        # Create a known distribution
        np.random.seed(42)
        samples = np.random.uniform(100, 200, 100000)
        result = format_distribution(samples)
        
        # Result should contain all percentile labels
        assert "P10" in result
        assert "P50" in result
        assert "P90" in result
        
        # Extract the three numbers (first three parts before parenthesis)
        parts = result.split()
        # Format is: "110 150 190 (P10, P50, P90)"
        # Parts: ['110', '150', '190', '(P10,', 'P50,', 'P90)']
        
        # Check we have at least 3 numeric values
        assert len(parts) >= 3
        
        # First three should be numbers (can parse as float after stripping)
        p10_val = float(parts[0])
        p50_val = float(parts[1])
        p90_val = float(parts[2])
        
        # Values should be in ascending order: P10 < P50 < P90
        assert p10_val < p50_val < p90_val
        
        # Values should be in expected range (100-200)
        assert 100 <= p10_val <= 200
        assert 100 <= p50_val <= 200
        assert 100 <= p90_val <= 200
    
    def test_format_distribution_small_numbers(self):
        np.random.seed(42)
        samples = np.random.uniform(1, 10, 100000)
        result = format_distribution(samples)
        
        assert "P10" in result
        assert "P50" in result
        assert "P90" in result
    
    def test_format_distribution_large_numbers(self):
        np.random.seed(42)
        samples = np.random.uniform(1e9, 2e9, 100000)
        result = format_distribution(samples)
        
        assert "P10" in result
        assert "B" in result  # Should use B suffix
    
    def test_format_distribution_decimal_range(self):
        np.random.seed(42)
        samples = np.random.uniform(0.5, 1.5, 100000)
        result = format_distribution(samples)
        
        assert "P10" in result
        assert "P50" in result
        assert "P90" in result