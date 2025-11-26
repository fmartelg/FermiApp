"""Tests for fermi_formatter module"""
import pytest
from fermi_formatter import parse_number, format_number


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