import numpy as np
import pytest

from mpqp.core.instruction.gates.custom_controlled__gate import CustomControlledGate
from mpqp.gates import *


@pytest.mark.parametrize(
    "gate, expected_repr",
    [
        (
            CustomControlledGate([0, 1], CustomGate(np.array([[1, 0], [0, -1]]), 2)),
            "MCU(array([[ 1, 0], [ 0, -1]]), [0, 1], 2)",
        ),
        (
            CustomControlledGate([0], CustomGate(np.array([[1, 0], [0, -1]]), 2)),
            "CU(array([[ 1, 0], [ 0, -1]]), 0, 2)",
        ),
        (CustomControlledGate(0, Z(2)), "CZ(0, 2)"),
        (CustomControlledGate(1, Rz(np.pi, 2)), "CRz(3.141592653589793, 1, 2)"),
        (CustomControlledGate(1, SWAP(0, 2)), "CSWAP(1, [0, 2])"),
        (CustomControlledGate(3, TOF([0, 1], 2)), "MCX([3, 0, 1], 2)"),
    ],
)
def test_gate_repr(gate: CustomControlledGate, expected_repr: str) -> None:
    assert repr(gate) == expected_repr
