from pathlib import Path
import sys

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.sat import SatSolver


@pytest.fixture
def solver():
    """
    Instantiate SatSolver without triggering the heavy __init__ logic while
    still allowing us to call the instance methods directly.
    """
    return SatSolver.__new__(SatSolver)


def test_bestcase_satisfies_positive_unit_clauses(solver):
    sat, assignment = solver.sat_bestcase(3, [[1], [2], [3]])

    assert sat is True
    assert assignment == {1: True, 2: True, 3: True}


def test_bestcase_handles_mixed_unit_and_binary_clauses(solver):
    clauses = [[-1], [1, 2], [-2, 3], [3]]

    sat, assignment = solver.sat_bestcase(3, clauses)

    assert sat is True
    assert assignment == {1: False, 2: True, 3: True}


def test_bestcase_returns_best_assignment_for_unsat_instance(solver):
    sat, assignment = solver.sat_bestcase(1, [[1], [-1]])

    assert sat is False
    assert assignment == {1: True}


def test_bestcase_empty_clause_list_is_satisfiable(solver):
    sat, assignment = solver.sat_bestcase(2, [])

    assert sat is True
    assert assignment == {1: False, 2: False}
