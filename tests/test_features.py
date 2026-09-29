"""
Unit tests for features.py — the parsing/classification core of the pipeline.

Run with: pytest tests/
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from features import extract_features


def test_linear_increasing():
    f = extract_features("2*x + 3")
    assert f['family'] == 'linear'
    assert f['direction'] == 'increasing'
    assert f['roots'] == [-1.5]


def test_linear_decreasing():
    f = extract_features("-x + 5")
    assert f['family'] == 'linear'
    assert f['direction'] == 'decreasing'
    assert f['roots'] == [5.0]


def test_quadratic_valley_has_two_roots():
    f = extract_features("x**2 - 3*x + 2")
    assert f['family'] == 'quadratic'
    assert f['direction'] == 'upward'
    assert f['roots'] == [1.0, 2.0]


def test_quadratic_hill_direction():
    f = extract_features("-x**2 + 9")
    assert f['family'] == 'quadratic'
    assert f['direction'] == 'downward'
    assert f['roots'] == [-3.0, 3.0]


def test_quadratic_even_symmetry():
    f = extract_features("x**2 - 4")
    assert f['symmetric'] == 'even'
    assert f['roots'] == [-2.0, 2.0]


def test_periodic_family_detected():
    f = extract_features("sin(x)")
    assert f['family'] == 'periodic'
    assert f['symmetric'] == 'odd'


def test_periodic_roots_include_zero():
    f = extract_features("sin(x)")
    assert 0.0 in f['roots']


def test_no_real_roots_in_range_returns_empty():
    f = extract_features("x**2 + 1")
    assert f['roots'] == []


def test_constant_function():
    f = extract_features("7")
    assert f['family'] == 'constant'
