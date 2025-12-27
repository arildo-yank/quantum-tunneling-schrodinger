import sys
import numpy as np

# =========================================================
# Compatibilidade NumPy 2.x
# =========================================================
if not hasattr(np, "trapz"):
    np.trapz = np.trapezoid

from PyQt6.QtWidgets import QApplication, QMainWindow
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore

import Schrödinger_engine as eng


# =========================================================
# QUANTUM VIEWER — VISUALIZAÇÃO DIDÁTICA (SIMPLIFICADA)
# =========================================================
class QuantumViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Quantum Tunneling — Visualização Didática (1D)")
        self.resize(1100, 650)

        # =================================================
        # SETUP DO GRÁFICO
        # =================================================
        self.plot = pg.PlotWidget()
        self.setCentralWidget(self.plot)

        self.plot.setBackground('#0f172a')
        self.plot.setLabel('bottom', 'Posição (x)')
        self.plot.setLabel('left', 'Densidade de Probabilidade |ψ(x)|²')

        # Define os limites baseados no motor
        self.plot.setXRange(eng.x.min(), eng.x.max())
        self.plot.setYRange(0, 0.12)
        self.plot.showGrid(True, True, 0.15)

        # =================================================
        # FUNÇÃO DE ONDA INICIAL
        # =================================================
        self.psi = eng.psi0.copy()

        # =================================================
        # CURVAS — REGIÕES FÍSICAS
        # =================================================
        # Esquerda: Onda incidente + reflexão
        self.curve_left = self.plot.plot(
            pen=pg.mkPen('#22d3ee', width=2)  # Azul ciano
        )

        # Centro: Região da barreira (Tunelamento/Evanescente)
        self.curve_barrier = self.plot.plot(
            pen=pg.mkPen('#facc15', width=2)  # Amarelo
        )

        # Direita: Onda transmitida
        self.curve_right = self.plot.plot(
            pen=pg.mkPen('#22c55e', width=2)  # Verde
        )

        # =================================================
        # VISUALIZAÇÃO DA BARREIRA (Área Sombreada)
        # =================================================
        # Pegamos onde V > 0 no motor
        mask = eng.V > 0
        xb = eng.x[mask]

        if xb.size > 0:
            self.barrier_region = pg.LinearRegionItem(
                values=(xb.min(), xb.max()),
                orientation=pg.LinearRegionItem.Vertical,
                brush=pg.mkBrush(255, 165, 0, 90),  # Laranja translúcido
                movable=False
            )
            self.plot.addItem(self.barrier_region)

        # =================================================
        # TIMER — EVOLUÇÃO TEMPORAL
        # =================================================
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # ~33 FPS

    # =====================================================
    # ATUALIZAÇÃO DO FRAME
    # =====================================================
    def update_frame(self):
        # 1. Evolução Temporal (Usando o motor explicitamente em 1D)
        self.psi = eng.evolve_step(self.psi, mode="1D")

        # 2. Normalização (Essencial para manter a física correta)
        self.psi = eng.normalize(self.psi, mode="1D")

        # 3. Calcular probabilidade para plotagem
        prob = np.abs(self.psi) ** 2

        # -------------------------------------------------
        # SEPARAÇÃO POR REGIÕES (Para colorir diferente)
        # -------------------------------------------------
        x = eng.x
        left_edge = eng.barreira_center - eng.barreira_width / 2
        right_edge = eng.barreira_center + eng.barreira_width / 2

        # Usamos np.nan para deixar "buracos" onde a linha não deve aparecer
        left_region = np.where(x < left_edge, prob, np.nan)
        barrier_region = np.where(
            (x >= left_edge) & (x <= right_edge), prob, np.nan
        )
        right_region = np.where(x > right_edge, prob, np.nan)

        # -------------------------------------------------
        # ATUALIZAR CURVAS NA TELA
        # -------------------------------------------------
        self.curve_left.setData(x, left_region)
        self.curve_barrier.setData(x, barrier_region)
        self.curve_right.setData(x, right_region)


# =========================================================
# PONTO DE ENTRADA
# =========================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = QuantumViewer()
    win.show()
    sys.exit(app.exec())