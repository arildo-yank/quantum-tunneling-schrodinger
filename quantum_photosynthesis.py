"""
=========================================================
QUANTUM PHOTOSYNTHESIS ENGINE
---------------------------------------------------------
This module reinterprets the Schrödinger tunneling simulator
as a quantum-coherent energy transport model inspired by
natural photosynthesis (exciton transport).
=========================================================
"""

import numpy as np
import Schrödinger_engine as eng


class QuantumPhotosynthesis:
    """
    Quantum Photosynthesis Model
    Concept: Non-Hermitian system with an absorbing potential (Sink).
    """

    def __init__(self):
        # Copy base wavefunction
        self.psi = eng.psi0.copy()

        # Energy sink position (reaction center)
        # Posiciona o "coletor" logo após a barreira
        self.sink_center = eng.barreira_center + eng.barreira_width * 2
        self.sink_width = 15.0  # Aumentei um pouco para ficar visualmente claro

        # Sink strength (controls capture efficiency)
        self.sink_strength = 0.05

        # Tracking
        self.time = 0.0
        self.captured_energy = 0.0

    # --------------------------------------------------
    # Reaction Center (Quantum Sink)
    # --------------------------------------------------
    def _reaction_center_mask(self):
        x = eng.x
        return (
                (x > self.sink_center - self.sink_width / 2) &
                (x < self.sink_center + self.sink_width / 2)
        )

    def apply_reaction_center(self, psi):
        """
        Simulates irreversible energy capture (Absorption)
        """
        mask = self._reaction_center_mask()

        # Probabilidade na região do Sink
        prob = np.abs(psi[mask]) ** 2

        # Energy captured this step
        if prob.size > 0:
            captured = np.sum(prob) * eng.dx * self.sink_strength
            self.captured_energy += captured

            # Remove amplitude (energy absorbed)
            psi[mask] *= np.exp(-self.sink_strength)

        return psi

    # --------------------------------------------------
    # Time Evolution
    # --------------------------------------------------
    def evolve_step(self, dt_scale=1.0):
        # 1. Standard Evolution
        self.psi = eng.evolve_step(self.psi, mode="1D")

        # 2. Apply Sink (Photosynthesis)
        self.psi = self.apply_reaction_center(self.psi)

        # No modo Bio, NÃO normalizamos para 1.0,
        # porque a energia está sendo "gastada" (capturada).
        # A soma total deve diminuir.

        self.time += eng.dt * dt_scale

        return self.psi

    def get_efficiency_percent(self):
        # Retorna quanto % da energia inicial já foi capturada
        return min(100.0, self.captured_energy * 100.0)