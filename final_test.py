import numpy as np
import pytest


def test_constraint_matrix():
    from final import matrix_from_constraints

    shafts = {"input": {}, "fixed": {}, "output": {}}
    constraints = [
        {
            "type": "chain",
            "a": {"shaft": "input", "teeth": 10},
            "b": {"shaft": "output", "teeth": 20},
        }
    ]
    matrix, shaft_mapping = matrix_from_constraints(shafts, constraints)
    assert matrix.shape == (3, 3)
    shaft_speeds = {"input": 1, "fixed": 0, "output": 0.5}
    speed_vector = np.zeros(len(shaft_mapping), dtype=float)
    for shaft, speed in shaft_speeds.items():
        speed_vector[shaft_mapping[shaft]] = speed
    result = np.dot(matrix, speed_vector)
    assert np.allclose(result[:-1], 0)
    assert np.isclose(result[-1], 1)


def test_mesh_constraint_vector():
    from final import mesh_constraint_vector

    shaft_mapping = {"input": 0, "output": 1}
    a = {"shaft": "input", "teeth": 10}
    b = {"shaft": "output", "teeth": 20}
    vector = mesh_constraint_vector(a, b, shaft_mapping)
    expected_vector = np.array([10, 20])
    assert np.array_equal(vector, expected_vector)


def test_chain_constraint_vector():
    from final import chain_constraint_vector

    shaft_mapping = {"input": 0, "output": 1}
    a = {"shaft": "input", "teeth": 10}
    b = {"shaft": "output", "teeth": 20}
    vector = chain_constraint_vector(a, b, shaft_mapping)
    expected_vector = np.array([10, -20])
    assert np.array_equal(vector, expected_vector)


def test_planetary_constraint_vector():
    from final import planetary_constraint_vector

    shaft_mapping = {"input": 0, "fixed": 1, "output": 2}
    sun = {"shaft": "input", "teeth": 10}
    ring = {"shaft": "fixed", "teeth": 30}
    carrier = {"shaft": "output"}
    vector = planetary_constraint_vector(sun, ring, carrier, shaft_mapping)
    expected_vector = np.array([10, 30, -40])
    assert np.array_equal(vector, expected_vector)


pytest.main(["-v", "--tb=line", "-rN", __file__])
