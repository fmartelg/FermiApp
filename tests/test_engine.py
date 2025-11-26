"""Tests for fermi_engine module"""
import pytest
from fermi_engine import FermiEngine
from fermi_parser import ParseError


class TestEvaluateExpression:
    """Tests for evaluate_expression method"""
    
    def test_evaluate_simple_number(self):
        engine = FermiEngine()
        assert engine.evaluate_expression("10") == 10.0
    
    def test_evaluate_addition(self):
        engine = FermiEngine()
        assert engine.evaluate_expression("10 + 20") == 30.0
    
    def test_evaluate_subtraction(self):
        engine = FermiEngine()
        assert engine.evaluate_expression("20 - 5") == 15.0
    
    def test_evaluate_multiplication(self):
        engine = FermiEngine()
        assert engine.evaluate_expression("10 * 2") == 20.0
    
    def test_evaluate_division(self):
        engine = FermiEngine()
        assert engine.evaluate_expression("20 / 4") == 5.0
    
    def test_evaluate_with_variable(self):
        engine = FermiEngine()
        engine.variables["x"] = 10
        assert engine.evaluate_expression("x * 2") == 20.0
    
    def test_evaluate_multiple_variables(self):
        engine = FermiEngine()
        engine.variables["x"] = 10
        engine.variables["y"] = 5
        assert engine.evaluate_expression("x + y") == 15.0
    
    def test_evaluate_complex_expression(self):
        engine = FermiEngine()
        assert engine.evaluate_expression("10 + 20 * 2") == 50.0
    
    def test_evaluate_with_parentheses(self):
        engine = FermiEngine()
        assert engine.evaluate_expression("(10 + 20) * 2") == 60.0
    
    def test_evaluate_undefined_variable_raises_error(self):
        engine = FermiEngine()
        with pytest.raises(NameError):
            engine.evaluate_expression("x * 2")
    
    def test_evaluate_with_suffix(self):
        engine = FermiEngine()
        assert engine.evaluate_expression("2.5K") == 2500.0


class TestExecuteLine:
    """Tests for execute_line method"""
    
    def test_execute_comment(self):
        engine = FermiEngine()
        result = engine.execute_line("# this is a comment")
        assert result["type"] == "comment"
        assert result["text"] == " this is a comment"
    
    def test_execute_empty_line(self):
        engine = FermiEngine()
        result = engine.execute_line("")
        assert result["type"] == "empty"
    
    def test_execute_simple_assignment(self):
        engine = FermiEngine()
        result = engine.execute_line("x = 10")
        assert result["type"] == "assignment"
        assert result["var"] == "x"
        assert result["value"] == 10.0
        assert engine.variables["x"] == 10.0
    
    def test_execute_assignment_with_expression(self):
        engine = FermiEngine()
        engine.execute_line("x = 10")
        result = engine.execute_line("y = x * 2")
        assert result["type"] == "assignment"
        assert result["var"] == "y"
        assert result["value"] == 20.0
    
    def test_execute_assignment_with_suffix(self):
        engine = FermiEngine()
        result = engine.execute_line("population = 2.7M")
        assert result["value"] == 2700000.0
    
    def test_execute_assignment_with_comment(self):
        engine = FermiEngine()
        result = engine.execute_line("x = 10  # ten")
        assert result["type"] == "assignment"
        assert result["value"] == 10.0
        assert result["comment"] == "ten"
    
    def test_execute_undefined_variable_returns_error(self):
        engine = FermiEngine()
        result = engine.execute_line("y = x * 2")
        assert result["type"] == "error"
        assert "Undefined variable" in result["message"]
    
    def test_execute_invalid_syntax_returns_error(self):
        engine = FermiEngine()
        result = engine.execute_line("invalid syntax")
        assert result["type"] == "error"


class TestExecuteModel:
    """Tests for execute_model method"""
    
    def test_execute_simple_model(self):
        engine = FermiEngine()
        text = "x = 10\ny = x * 2"
        results = engine.execute_model(text)
        
        assert len(results) == 2
        assert results[0]["value"] == 10.0
        assert results[1]["value"] == 20.0
    
    def test_execute_model_with_comments(self):
        engine = FermiEngine()
        text = "# comment\nx = 10\ny = 20"
        results = engine.execute_model(text)
        
        assert len(results) == 3
        assert results[0]["type"] == "comment"
        assert results[1]["value"] == 10.0
        assert results[2]["value"] == 20.0
    
    def test_execute_model_piano_tuners(self):
        engine = FermiEngine()
        text = """
population = 2.7M
people_per_household = 2.5
households = population / people_per_household
        """.strip()
        
        results = engine.execute_model(text)
        
        assert len(results) == 3
        assert results[2]["value"] == 1080000.0  # 2.7M / 2.5
    
    def test_execute_model_preserves_variables(self):
        engine = FermiEngine()
        text = "x = 10\ny = 20\nz = x + y"
        results = engine.execute_model(text)
        
        assert engine.variables["x"] == 10.0
        assert engine.variables["y"] == 20.0
        assert engine.variables["z"] == 30.0


class TestClear:
    """Tests for clear method"""
    
    def test_clear_removes_all_variables(self):
        engine = FermiEngine()
        engine.variables["x"] = 10
        engine.variables["y"] = 20
        
        engine.clear()
        
        assert len(engine.variables) == 0