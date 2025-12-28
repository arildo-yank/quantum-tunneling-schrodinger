import sys
import numpy as np

# =========================================================
# Compatibilidade NumPy 2.x
# =========================================================
if not hasattr(np, "trapz"):
    np.trapz = np.trapezoid

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QHBoxLayout, QVBoxLayout, QLabel,
    QPushButton, QSlider, QGroupBox, QStackedWidget
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPalette, QColor

import pyqtgraph as pg
import pyqtgraph.opengl as gl  # Módulo 3D
from pyqtgraph.Qt import QtCore

import Schrödinger_engine as eng


class QuantumApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YANKCO Quantum Tunneling Simulator (STABLE EDITION)")
        self.resize(1600, 900)

        # --- ESTADO INICIAL ---
        self.psi0 = eng.psi0.copy()
        self.psi = self.psi0.copy()
        self.time = 0.0
        self.is_paused = False

        # Configuração da Barreira
        self.V0 = 2.0
        eng.set_barrier_height(self.V0)

        # Modos: "1D", "3D_RADIAL", "3D_SURFACE"
        self.dimension_mode = "1D"

        # Parâmetros visuais 3D
        self.Z_SCALE = 300.0  # Fator de exagero da altura
        self.y_steps = 40  # Resolução lateral
        self.y_width = 30  # Largura visual

        self._setup_theme()
        self._setup_ui()

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_simulation)
        self.timer.start(30)

        # Inicializa visual 3D
        self._update_barrier_visuals()
        self._update_display()

    def _setup_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(12, 18, 28))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(230, 237, 243))
        palette.setColor(QPalette.ColorRole.Base, QColor(20, 27, 38))
        palette.setColor(QPalette.ColorRole.Text, QColor(230, 237, 243))
        palette.setColor(QPalette.ColorRole.Button, QColor(25, 32, 44))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(230, 237, 243))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(88, 166, 255))
        self.setPalette(palette)

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)

        layout.addWidget(self._left_panel(), 1)

        # Stacked Widget para alternar 2D/3D
        self.view_stack = QStackedWidget()
        self.plot_2d_widget = self._create_2d_plot()
        self.view_stack.addWidget(self.plot_2d_widget)
        self.plot_3d_widget = self._create_3d_view()
        self.view_stack.addWidget(self.plot_3d_widget)

        layout.addWidget(self.view_stack, 4)

    # =====================================================
    # CRIAÇÃO DOS WIDGETS
    # =====================================================
    def _create_2d_plot(self):
        container = QWidget()
        l = QVBoxLayout(container)
        l.setContentsMargins(0, 0, 0, 0)

        plot = pg.PlotWidget()
        plot.setBackground('#0d1117')
        plot.setLabel('left', '|ψ|²')
        plot.setLabel('bottom', 'Posição')
        plot.setXRange(eng.x.min(), eng.x.max())
        plot.setYRange(0, 0.12)
        plot.showGrid(True, True, 0.2)

        self.curve_L = plot.plot(pen=pg.mkPen('#22d3ee', width=2))  # Azul
        self.curve_B = plot.plot(pen=pg.mkPen('#facc15', width=2))  # Amarelo
        self.curve_R = plot.plot(pen=pg.mkPen('#22c55e', width=2))  # Verde

        self.barrier_region_2d = pg.LinearRegionItem(
            brush=pg.mkBrush(255, 140, 0, 80), movable=False
        )
        plot.addItem(self.barrier_region_2d)

        l.addWidget(plot)
        return container

    def _create_3d_view(self):
        view = gl.GLViewWidget()
        view.setCameraPosition(distance=150, elevation=45, azimuth=-90)

        grid = gl.GLGridItem()
        grid.scale(5, 5, 1)
        view.addItem(grid)

        # --- SUPERFÍCIE SEGURA (FLOAT32) ---
        z0 = np.zeros((len(eng.x), self.y_steps), dtype=np.float32)

        # MUDANÇA DE COR AQUI (R, G, B, Alpha)
        # 0.6 = Roxo, 0.1 = Verde, 1.0 = Azul
        WAVE_COLOR = (0.6, 0.3, 1.0, 0.9)  # ROXO NEON

        self.wave_surface = gl.GLSurfacePlotItem(
            z=z0,
            color=WAVE_COLOR,
            shader=None,
            computeNormals=False,
            smooth=False
        )

        # Ajustar Escala e Posição
        x_range = eng.x.max() - eng.x.min()
        dx = x_range / (len(eng.x) - 1)
        dy = self.y_width / (self.y_steps - 1)

        self.wave_surface.scale(dx, dy, 1)
        self.wave_surface.translate(eng.x.min(), -self.y_width / 2, 0)

        view.addItem(self.wave_surface)

        # Barreira 3D (Caixa)
        self.barrier_box_3d = gl.GLBoxItem()
        self.barrier_box_3d.setColor(QColor(255, 140, 0, 100))
        view.addItem(self.barrier_box_3d)

        return view

    def _left_panel(self):
        panel = QWidget()
        v = QVBoxLayout(panel)

        title = QLabel("Quantum Tunneling")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size:18px; font-weight:600; color:#58a6ff;")
        v.addWidget(title)

        status = QGroupBox("Status")
        s = QVBoxLayout()
        self.lbl_time = QLabel()
        self.lbl_energy = QLabel()
        self.lbl_trans = QLabel()
        self.lbl_refl = QLabel()
        self.lbl_norm = QLabel()
        self.lbl_V0 = QLabel()
        self.lbl_dimension = QLabel()

        for w in (self.lbl_time, self.lbl_energy, self.lbl_trans,
                  self.lbl_refl, self.lbl_norm, self.lbl_V0, self.lbl_dimension):
            s.addWidget(w)
        status.setLayout(s)
        v.addWidget(status)

        controls = QGroupBox("Controls")
        c = QVBoxLayout()

        btns = QHBoxLayout()
        self.btn_pause = QPushButton("Pause")
        self.btn_pause.clicked.connect(self._toggle_pause)
        self.btn_reset = QPushButton("Reset")
        self.btn_reset.clicked.connect(self._reset)
        btns.addWidget(self.btn_pause)
        btns.addWidget(self.btn_reset)
        c.addLayout(btns)

        self.speed = QSlider(Qt.Orientation.Horizontal)
        self.speed.setRange(20, 200)
        self.speed.setValue(100)
        c.addWidget(QLabel("Time scale"))
        c.addWidget(self.speed)

        self.barrier_slider = QSlider(Qt.Orientation.Horizontal)
        self.barrier_slider.setRange(0, 300)
        self.barrier_slider.setValue(20)
        self.barrier_slider.valueChanged.connect(self._update_barrier)
        c.addWidget(QLabel("Barrier height V₀"))
        c.addWidget(self.barrier_slider)

        self.btn_dimension = QPushButton("Mode: 1D Standard")
        self.btn_dimension.setStyleSheet("background-color: #7c3aed; color: white; font-weight: bold;")
        self.btn_dimension.clicked.connect(self._cycle_dimension)
        c.addWidget(self.btn_dimension)

        controls.setLayout(c)
        v.addWidget(controls)

        self.lbl_regime = QLabel()
        self.lbl_regime.setStyleSheet("font-weight:600; color:#facc15;")
        v.addWidget(self.lbl_regime)
        v.addStretch()
        return panel

    # =====================================================
    # LÓGICA
    # =====================================================
    def _cycle_dimension(self):
        if self.dimension_mode == "1D":
            self.dimension_mode = "3D_RADIAL"
            self.btn_dimension.setText("Mode: 3D Radial (Spherical)")
            self.view_stack.setCurrentIndex(0)

        elif self.dimension_mode == "3D_RADIAL":
            self.dimension_mode = "3D_SURFACE"
            self.btn_dimension.setText("Mode: 3D Surface (OpenGL)")
            self.view_stack.setCurrentIndex(1)
            self._update_barrier_visuals()

        else:
            self.dimension_mode = "1D"
            self.btn_dimension.setText("Mode: 1D Standard")
            self.view_stack.setCurrentIndex(0)

        self._reset()

    def _update_barrier(self, value):
        self.V0 = value / 10.0
        eng.set_barrier_height(self.V0)
        self.lbl_V0.setText(f"Barrier V₀ = {self.V0:.2f}")
        self._update_barrier_visuals()

    def _update_barrier_visuals(self):
        mask = eng.V > 0
        xb = eng.x[mask]

        # --- Atualizar 2D ---
        if xb.size > 0:
            min_b, max_b = xb.min(), xb.max()
            self.barrier_region_2d.setRegion((min_b, max_b))

        # --- Atualizar 3D ---
        if xb.size > 0:
            width = max_b - min_b
            center_x = (max_b + min_b) / 2

            self.barrier_box_3d.resetTransform()
            self.barrier_box_3d.setSize(x=width, y=self.y_width, z=80)
            self.barrier_box_3d.translate(center_x - width / 2, -self.y_width / 2, 0)
            self.barrier_box_3d.setVisible(True)
        else:
            self.barrier_box_3d.setVisible(False)

    def _update_simulation(self):
        if self.is_paused: return

        phys_mode = "3D_RADIAL" if self.dimension_mode == "3D_RADIAL" else "1D"

        self.psi = eng.evolve_step(self.psi, mode=phys_mode)
        self.psi = eng.normalize(self.psi, mode=phys_mode)
        self.time += eng.dt * (self.speed.value() / 100)

        self._update_display()

    def _update_display(self):
        x = eng.x
        prob = np.abs(self.psi) ** 2

        # Status
        T, R = eng.calculate_transmission(self.psi)
        self.lbl_time.setText(f"Time: {self.time:.2f}")
        self.lbl_energy.setText(f"Energy ≈ {0.5 * eng.k0 ** 2:.2f}")
        self.lbl_trans.setText(f"Transmission: {T:.1f}%")
        self.lbl_refl.setText(f"Reflection: {R:.1f}%")
        self.lbl_dimension.setText(f"View: {self.dimension_mode}")

        if self.V0 >= eng.V_INFINITY:
            self.lbl_regime.setText("🧱 Hard Wall")
        elif self.V0 > 0.5 * eng.k0 ** 2:
            self.lbl_regime.setText("🔒 Tunneling (E < V)")
        else:
            self.lbl_regime.setText("🚀 Scattering (E > V)")

        # Display Gráfico
        if self.dimension_mode == "3D_SURFACE":
            # --- 3D Update ---
            norm_val = np.trapz(prob, x)
            self.lbl_norm.setText(f"Norm: {norm_val:.4f}")

            # CRÍTICO: Converter para float32 antes de enviar para OpenGL
            z_data = np.tile(prob * self.Z_SCALE, (self.y_steps, 1)).T
            self.wave_surface.setData(z=z_data.astype(np.float32))

        else:
            # --- 2D Update ---
            norm_val = np.trapz(prob, x)
            self.lbl_norm.setText(f"Norm: {norm_val:.4f}")

            mask = eng.V > 0
            xb = eng.x[mask]
            if xb.size > 0:
                left = xb.min()
                right = xb.max()
            else:
                left, right = 9999, 9999

            self.curve_L.setData(x, np.where(x < left, prob, np.nan))
            self.curve_B.setData(x, np.where((x >= left) & (x <= right), prob, np.nan))
            self.curve_R.setData(x, np.where(x > right, prob, np.nan))

    def _toggle_pause(self):
        self.is_paused = not self.is_paused
        self.btn_pause.setText("Run" if self.is_paused else "Pause")

    def _reset(self):
        self.psi = self.psi0.copy()
        self.time = 0.0
        self._update_display()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Arial", 10))
    win = QuantumApp()
    win.show()
    sys.exit(app.exec())