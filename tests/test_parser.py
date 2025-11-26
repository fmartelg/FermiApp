"""Tests for fermi_parser module"""
import pytest
from fermi_parser import parse_line, tokenize, ParseError


class TestParseLine:
    """Tests for parse_line function"""
    
    def test_parse_comment(self):
        result = parse_line("# this is a comment")
        assert result["type"] == "comment"
        assert result["text"] == " this is a comment"
    
    def test_parse_empty_line(self):
        result = parse_line("")
        assert result["type"] == "empty"
    
    def test_parse_whitespace_line(self):
        result = parse_line("   ")
        assert result["type"] == "empty"
    
    def test_parse_simple_assignment(self):
        result = parse_line("x = 10")
        assert result["type"] == "assignment"
        assert result["var"] == "x"
        assert result["expr"] == "10"
    
    def test_parse_assignment_with_expression(self):
        result = parse_line("y = x * 2")
        assert result["type"] == "assignment"
        assert result["var"] == "y"
        assert result["expr"] == "x * 2"
    
    def test_parse_assignment_with_suffix(self):
        result = parse_line("population = 2.7M")
        assert result["type"] == "assignment"
        assert result["var"] == "population"
        assert result["expr"] == "2.7M"
    
    def test_parse_assignment_with_inline_comment(self):
        result = parse_line("x = 10  # this is ten")
        assert result["type"] == "assignment"
        assert result["var"] == "x"
        assert result["expr"] == "10"
        assert result["comment"] == "this is ten"
    
    def test_parse_assignment_with_spaces(self):
        result = parse_line("  my_var  =  100  ")
        assert result["type"] == "assignment"
        assert result["var"] == "my_var"
        assert result["expr"] == "100"
    
    def test_parse_invalid_variable_name(self):
        with pytest.raises(ParseError):
            parse_line("123abc = 10")
    
    def test_parse_missing_variable_name(self):
        with pytest.raises(ParseError):
            parse_line("= 10")
    
    def test_parse_missing_expression(self):
        with pytest.raises(ParseError):
            parse_line("x =")
    
    def test_parse_no_equals(self):
        with pytest.raises(ParseError):
            parse_line("just some text")

    def test_parse_double_equals_raises_error(self):
        with pytest.raises(ParseError):
            parse_line("y == 2x")
    
    def test_parse_comparison_raises_error(self):
        with pytest.raises(ParseError):
            parse_line("x = y == 10")


class TestTokenize:
    """Tests for tokenize function"""
    
    def test_tokenize_simple_number(self):
        tokens = tokenize("10")
        assert tokens == [("NUMBER", 10.0)]
    
    def test_tokenize_number_with_suffix(self):
        tokens = tokenize("2.7M")
        assert tokens == [("NUMBER", 2700000.0)]
    
    def test_tokenize_simple_operation(self):
        tokens = tokenize("10 * 2")
        assert tokens == [
            ("NUMBER", 10.0),
            ("OPERATOR", "*"),
            ("NUMBER", 2.0)
        ]
    
    def test_tokenize_variable(self):
        tokens = tokenize("x")
        assert tokens == [("VARIABLE", "x")]
    
    def test_tokenize_variable_with_operation(self):
        tokens = tokenize("x * 2")
        assert tokens == [
            ("VARIABLE", "x"),
            ("OPERATOR", "*"),
            ("NUMBER", 2.0)
        ]
    
    def test_tokenize_complex_expression(self):
        tokens = tokenize("x + 2.5K")
        assert tokens == [
            ("VARIABLE", "x"),
            ("OPERATOR", "+"),
            ("NUMBER", 2500.0)
        ]
    
    def test_tokenize_all_operators(self):
        tokens = tokenize("a + b - c * d / e")
        assert len(tokens) == 9
        assert tokens[1] == ("OPERATOR", "+")
        assert tokens[3] == ("OPERATOR", "-")
        assert tokens[5] == ("OPERATOR", "*")
        assert tokens[7] == ("OPERATOR", "/")
    
    def test_tokenize_parentheses(self):
        tokens = tokenize("(x + 2) * 3")
        assert tokens[0] == ("LPAREN", "(")
        assert tokens[4] == ("RPAREN", ")")
    
    def test_tokenize_no_spaces(self):
        tokens = tokenize("10*2")
        assert tokens == [
            ("NUMBER", 10.0),
            ("OPERATOR", "*"),
            ("NUMBER", 2.0)
        ]
    
    def test_tokenize_with_underscores(self):
        tokens = tokenize("my_var_name")
        assert tokens == [("VARIABLE", "my_var_name")]
    
    def test_tokenize_invalid_token(self):
        with pytest.raises(ParseError):
            tokenize("x @ y")  # @ is not a valid operator