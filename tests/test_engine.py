"""Tests for fermi_engine module"""
import pytest
import numpy as np
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


class TestEvaluateDistributions:
    """Tests for evaluating uniform distributions"""
    
    def test_evaluate_uniform_distribution(self):
        np.random.seed(42)
        engine = FermiEngine()
        result = engine.evaluate_expression("2M 3M")
        
        assert isinstance(result, np.ndarray)
        assert len(result) == 100000
        assert result.min() >= 2e6
        assert result.max() <= 3e6
    
    def test_evaluate_uniform_simple(self):
        np.random.seed(42)
        engine = FermiEngine()
        result = engine.evaluate_expression("10 20")
        
        assert isinstance(result, np.ndarray)
        assert len(result) == 100000
        assert result.min() >= 10
        assert result.max() <= 20
    
    def test_scalar_times_distribution(self):
        np.random.seed(42)
        engine = FermiEngine()
        engine.variables["x"] = 10.0
        result = engine.evaluate_expression("x * 5 10")
        
        assert isinstance(result, np.ndarray)
        assert len(result) == 100000
        # Result should be in range 50-100 (10 * 5 to 10 * 10)
        assert result.min() >= 50
        assert result.max() <= 100
    
    def test_distribution_times_scalar(self):
        np.random.seed(42)
        engine = FermiEngine()
        result = engine.evaluate_expression("5 10 * 2")
        
        assert isinstance(result, np.ndarray)
        # Result should be in range 10-20
        assert result.min() >= 10
        assert result.max() <= 20
    
    def test_distribution_arithmetic(self):
        np.random.seed(42)
        engine = FermiEngine()
        result = engine.evaluate_expression("10 20 + 5 10")
        
        assert isinstance(result, np.ndarray)
        # Result should be in range 15-30
        assert result.min() >= 15
        assert result.max() <= 30
    
    def test_distribution_subtraction(self):
        np.random.seed(42)
        engine = FermiEngine()
        result = engine.evaluate_expression("20 30 - 5 10")
        
        assert isinstance(result, np.ndarray)
        # Result should be in range 10-25
        assert result.min() >= 10
        assert result.max() <= 25
    
    def test_distribution_multiplication(self):
        np.random.seed(42)
        engine = FermiEngine()
        result = engine.evaluate_expression("2 3 * 4 5")
        
        assert isinstance(result, np.ndarray)
        # Result should be in range 8-15
        assert result.min() >= 8
        assert result.max() <= 15
    
    def test_distribution_division(self):
        np.random.seed(42)
        engine = FermiEngine()
        result = engine.evaluate_expression("20 30 / 2 5")
        
        assert isinstance(result, np.ndarray)
        # Result should be in range 4-15 (20/5 to 30/2)
        assert result.min() >= 4
        assert result.max() <= 15


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
    
    def test_execute_distribution_assignment(self):
        np.random.seed(42)
        engine = FermiEngine()
        result = engine.execute_line("x = 2M 3M")
        
        assert result["type"] == "assignment"
        assert result["var"] == "x"
        assert isinstance(result["value"], np.ndarray)
        assert len(result["value"]) == 100000


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
    
    def test_execute_model_with_distributions(self):
        np.random.seed(42)
        engine = FermiEngine()
        text = "a = 10 20\nb = 5 10\nc = a + b"
        results = engine.execute_model(text)
        
        assert len(results) == 3
        assert isinstance(results[0]["value"], np.ndarray)
        assert isinstance(results[1]["value"], np.ndarray)
        assert isinstance(results[2]["value"], np.ndarray)
    
    def test_execute_model_mixed_scalar_distribution(self):
        np.random.seed(42)
        engine = FermiEngine()
        text = """
population = 2M 3M
households = population / 2.5
        """.strip()
        
        results = engine.execute_model(text)
        
        assert len(results) == 2
        assert isinstance(results[0]["value"], np.ndarray)
        assert isinstance(results[1]["value"], np.ndarray)
        
        # Check that households is in expected range (0.8M - 1.2M)
        households = results[1]["value"]
        assert households.min() >= 800000
        assert households.max() <= 1200000


class TestClear:
    """Tests for clear method"""
    
    def test_clear_removes_all_variables(self):
        engine = FermiEngine()
        engine.variables["x"] = 10
        engine.variables["y"] = 20
        
        engine.clear()
        
        assert len(engine.variables) == 0