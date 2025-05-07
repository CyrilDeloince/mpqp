from typing import TYPE_CHECKING, Any, Optional, Union
from qiskit.circuit import Parameter

from mpqp.core.instruction.gates.controlled_gate import ControlledGate
from mpqp.core.instruction.gates.custom_gate import CustomGate
from mpqp.core.instruction.gates.gate_definition import UnitaryMatrix
from mpqp.core.languages import Language
from mpqp.tools.generics import Matrix

from .gate import Gate


class CustomControlledGate(ControlledGate):
    def __init__(
        self,
        controls: list[int] | int,
        targets: list[int] | int,
        gate: Union[type[Gate], Matrix],
        label: Optional[str] = None,
    ):
        from mpqp.tools.generics import SimpleClassReprABCMeta

        if isinstance(gate, SimpleClassReprABCMeta):
            ControlledGate.__init__(self, controls, targets, gate(targets), label)
        else:
            if isinstance(targets, int):
                targets = [targets]
            ControlledGate.__init__(
                self, controls, targets, CustomGate(UnitaryMatrix(gate), targets), label
            )

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.controls},{self.targets})"

    def to_canonical_matrix(self):
        import numpy as np

        l = 2 ** len(self.targets)
        m = np.identity(2 ** (len(self.controls) + len(self.targets)), dtype=complex)
        m[-l:, -l:] = self.non_controlled_gate.to_matrix()
        return m

    def to_other_language(
        self,
        language: Language = Language.QISKIT,
        qiskit_parameters: set[Parameter] | None = None,
    ) -> Any:
        if language == Language.QISKIT:
            from qiskit.quantum_info import Operator

            gate = self.non_controlled_gate.to_other_language()
            if isinstance(gate, Operator):
                gate = gate.to_instruction()
            gate = gate.control(len(self.controls))
            return gate
        elif language == Language.QASM2:
            from qiskit import QuantumCircuit, qasm2

            nb_qubits = max(max(self.targets), max(self.controls)) + 1

            qiskit_circ = QuantumCircuit(nb_qubits)

            if isinstance(self.non_controlled_gate, CustomGate):
                targets = self.targets + self.controls
                targets.sort()
                gate = CustomGate(UnitaryMatrix(self.to_matrix()), targets)

                return gate.to_other_language(Language.QASM2)

            else:
                qiskit_circ.append(
                    self.to_other_language(Language.QISKIT),
                    self.controls + self.targets,
                )
            qasm_str = qasm2.dumps(qiskit_circ)
            qasm_lines = qasm_str.splitlines()
            if isinstance(self.non_controlled_gate, CustomGate):
                return qasm_str, 0
            instructions_only = [
                line
                for line in qasm_lines
                if not (
                    line.startswith("qreg")
                    or line.startswith("include")
                    or line.startswith("creg")
                    or line.startswith("OPENQASM")
                )
            ]

            return "\n".join(instructions_only), 0
        else:
            raise NotImplementedError(f"Error: {language} is not supported")
