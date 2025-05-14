import numpy as np
import pytest

from mpqp.core.instruction.gates.controlled_custom_gate import CustomControlledGate
from mpqp.gates import *


@pytest.mark.parametrize(
    "gate, expected_repr",
    [
        (
            CustomControlledGate([0, 1], 2, np.array([[1, 0], [0, -1]])),
            "MCU(array([[ 1, 0], [ 0, -1]]), [0, 1], 2)",
        ),
        (
            CustomControlledGate(0, 2, np.array([[1, 0], [0, -1]])),
            "CU(array([[ 1, 0], [ 0, -1]]), 0, 2)",
        ),
        (CustomControlledGate(0, 2, Z), "CZ(0, 2)"),
        (CustomControlledGate(1, 2, Rz, np.pi), "CRz(3.141592653589793, 1, 2)"),
        (CustomControlledGate(1, [0, 2], SWAP), "CSWAP(1, [0, 2])"),
        (CustomControlledGate([0, 2], 1, TOF), "MCX([0, 2], 1)"),
    ],
)
def test_gate_repr(gate: CustomControlledGate, expected_repr: str) -> None:
    assert repr(gate) == expected_repr
