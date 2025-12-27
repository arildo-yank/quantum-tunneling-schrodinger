import sys
import numpy as np

# =========================================================
# Compatibilidade NumPy 2.x
# =========================================================
if not hasattr(np, "trapz"):
    np.trapz = np.trapezoid

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QColor

import pyqtgraph.opengl as gl
import Schrödinger_engine as eng


class Quantum3DApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simulação Quântica 3D - Superfície Colorida")
        self.resize(1280, 720)

        # -------------------------------------------------
        # 1. Configurar Câmera e Mundo
        # -------------------------------------------------
        self.view = gl.GLViewWidget()
        self.setCentralWidget(self.view)

        # Câmera posicionada para ver o "rio" de frente/cima
        self.view.setCameraPosition(distance=150, elevation=50, azimuth=-90)

        # Grade no chão
        grid = gl.GLGridItem()
        grid.scale(5, 5, 1)
        self.view.addItem(grid)

        # -------------------------------------------------
        # 2. Configurações da Malha
        # -------------------------------------------------
        self.y_width = 30
        self.y_steps = 40
        self.Z_SCALE = 300.0  # Fator montanha

        self.x_vals = eng.x
        self.y_vals = np.linspace(-self.y_width / 2, self.y_width / 2, self.y_steps)

        # Estado inicial
        self.psi = eng.psi0.copy()

        # -------------------------------------------------
        # 3. Preparar Cores por Região (O SEGREDO DAS CORES)
        # -------------------------------------------------
        # Em vez de shader, criamos uma matriz de cores (R, G, B, A)
        # Dimensões: (Pontos em X, Pontos em Y, 4 canais de cor)
        self.colors = np.zeros((len(self.x_vals), self.y_steps, 4))

        # Definir onde fica a barreira
        mask = eng.V > 0
        x_bar = eng.x[mask]

        if x_bar.size > 0:
            left_edge = x_bar.min()
            right_edge = x_bar.max()
        else:
            left_edge = 1000  # Fora da tela
            right_edge = 1000

        # Cores (R, G, B, Alpha) - Normalizado 0.0 a 1.0
        # Azul Neon (Esquerda)
        c_blue = np.array([0.1, 0.8, 1.0, 1.0])
        # Amarelo Ouro (Dentro da Barreira)
        c_yellow = np.array([1.0, 0.8, 0.0, 1.0])
        # Verde Matrix (Direita - Transmitido)
        c_green = np.array([0.1, 1.0, 0.2, 1.0])

        # Preencher a matriz de cores baseada no Eixo X
        for i, x in enumerate(self.x_vals):
            if x < left_edge:
                self.colors[i, :] = c_blue
            elif x > right_edge:
                self.colors[i, :] = c_green
            else:
                self.colors[i, :] = c_yellow

        # -------------------------------------------------
        # 4. Criar a Superfície
        # -------------------------------------------------
        initial_z = np.zeros((len(self.x_vals), self.y_steps))

        self.wave_surface = gl.GLSurfacePlotItem(
            x=self.x_vals,
            y=self.y_vals,
            z=initial_z,
            colors=self.colors,  # <--- USAMOS CORES MANUAIS AQUI
            shader='shaded',  # 'shaded' usa luz, mas respeita nossas cores
            computeNormals=False,
            smooth=False
        )
        self.view.addItem(self.wave_surface)

        # -------------------------------------------------
        # 5. Barreira Visual
        # -------------------------------------------------
        self.create_barrier_visual()

        # -------------------------------------------------
        # 6. Timer
        # -------------------------------------------------
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(30)

    def create_barrier_visual(self):
        mask = eng.V > 0
        if not np.any(mask): return

        x_bar = eng.x[mask]
        x_min, x_max = x_bar.min(), x_bar.max()
        width = x_max - x_min
        center_x = (x_max + x_min) / 2

        # Altura aumentada para cobrir a "montanha" (Ex: 60)
        z_height = 60

        box = gl.GLBoxItem()
        box.setSize(x=width, y=self.y_width, z=z_height)
        # Centraliza
        box.translate(center_x - width / 2, -self.y_width / 2, 0)

        # COR DA BARREIRA: Laranja com Alpha mais alto (100/255) para ser visível
        box.setColor(QColor(255, 140, 0, 100))

        self.view.addItem(box)

    def update_simulation(self):
        # Evoluir física
        self.psi = eng.evolve_step(self.psi, mode="1D")
        self.psi = eng.normalize(self.psi, mode="1D")

        # Probabilidade
        prob = np.abs(self.psi) ** 2

        # Amplificar altura (Montanha)
        z_amplified = prob * self.Z_SCALE

        # Criar malha Z (repetir Y vezes)
        z_data = np.tile(z_amplified, (self.y_steps, 1)).T

        # Atualizar APENAS a altura (Z). As cores (X) já estão fixas.
        self.wave_surface.setData(z=z_data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Quantum3DApp()
    window.show()
    sys.exit(app.exec())