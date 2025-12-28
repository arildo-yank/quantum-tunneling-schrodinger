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
    QPushButton, QSlider, QGroupBox, QStackedWidget,
    QDoubleSpinBox, QFormLayout
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPalette, QColor

import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtCore

# --- IMPORTAÇÕES DO PROJETO ---
import Schrödinger_engine as eng
import quantum_photosynthesis as bio_eng
from widgets import ExplainerPanel


class QuantumApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YANKCO Simulator (siliconera.ca)")
        self.resize(1600, 950)

        # --- MOTORES ---
        self.psi_phys = eng.psi0.copy()
        self.bio_model = None

        self.time = 0.0
        self.is_paused = False

        # Configuração Inicial
        self.V0 = 2.0
        eng.set_barrier_height(self.V0)

        # Modos
        self.dimension_mode = "1D"

        # Parâmetros visuais 3D
        self.Z_SCALE = 300.0
        self.y_steps = 40
        self.y_width = 30
        # Largura do espaço entre as barreiras no modo duplo
        self.gap_width = 15.0

        self._setup_theme()
        self._setup_ui()

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_simulation)
        self.timer.start(30)

        # Inicializa visual
        self._update_barrier_visuals()
        self._update_display()

        # Inicializa texto explicativo
        self.explainer.update_mode("1D")

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

        # Stacked Widget
        self.view_stack = QStackedWidget()
        self.plot_2d_widget = self._create_2d_plot()
        self.view_stack.addWidget(self.plot_2d_widget)
        self.plot_3d_widget = self._create_3d_view()
        self.view_stack.addWidget(self.plot_3d_widget)

        layout.addWidget(self.view_stack, 4)

    def _left_panel(self):
        panel = QWidget()
        v = QVBoxLayout(panel)

        # 1. Título
        self.title_lbl = QLabel("Quantum Tunneling")
        self.title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_lbl.setStyleSheet("font-size:18px; font-weight:600; color:#58a6ff; margin-bottom: 5px;")
        v.addWidget(self.title_lbl)

        # 2. Status Box
        status = QGroupBox("Real-time Metrics")
        s = QVBoxLayout()
        self.lbl_time = QLabel()
        self.lbl_trans = QLabel()
        self.lbl_refl = QLabel()
        self.lbl_norm = QLabel()
        self.lbl_dimension = QLabel()

        for w in (self.lbl_time, self.lbl_trans, self.lbl_refl, self.lbl_norm, self.lbl_dimension):
            w.setStyleSheet("color: #cbd5e1; font-size: 11px;")
            s.addWidget(w)
        status.setLayout(s)
        v.addWidget(status)

        # 3. Controls Box
        controls = QGroupBox("Simulation Control")
        c = QVBoxLayout()

        btns = QHBoxLayout()
        self.btn_pause = QPushButton("Pause")
        self.btn_pause.clicked.connect(self._toggle_pause)
        self.btn_reset = QPushButton("Reset")
        self.btn_reset.setStyleSheet("background-color: #dc2626;")
        self.btn_reset.clicked.connect(self._reset)
        btns.addWidget(self.btn_pause)
        btns.addWidget(self.btn_reset)
        c.addLayout(btns)

        c.addWidget(QLabel("Time Speed"))
        self.speed = QSlider(Qt.Orientation.Horizontal)
        self.speed.setRange(20, 200)
        self.speed.setValue(100)
        c.addWidget(self.speed)

        # Botão de Modo
        self.btn_dimension = QPushButton("Mode: 1D Standard")
        self.btn_dimension.setStyleSheet("background-color: #7c3aed; color: white; font-weight: bold; margin-top: 5px;")
        self.btn_dimension.clicked.connect(self._cycle_dimension)
        c.addWidget(self.btn_dimension)

        controls.setLayout(c)
        v.addWidget(controls)

        # 4. PARÂMETROS DETALHADOS
        params = QGroupBox("System Parameters")
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)

        spin_style = """
            QDoubleSpinBox {
                background-color: #1e293b; color: white; padding: 3px; 
                border: 1px solid #475569; border-radius: 4px;
            }
            QDoubleSpinBox:hover { border: 1px solid #58a6ff; }
        """

        self.spin_V0 = QDoubleSpinBox()
        self.spin_V0.setRange(0.0, 500.0)
        self.spin_V0.setValue(self.V0)
        self.spin_V0.setSingleStep(0.1)
        self.spin_V0.setStyleSheet(spin_style)
        self.spin_V0.valueChanged.connect(self._update_barrier_spin)
        form.addRow("V₀:", self.spin_V0)

        self.spin_width = QDoubleSpinBox()
        self.spin_width.setRange(1.0, 100.0)
        self.spin_width.setValue(eng.barreira_width)
        self.spin_width.setSingleStep(0.5)
        self.spin_width.setStyleSheet(spin_style)
        self.spin_width.valueChanged.connect(self._update_width)
        form.addRow("Largura:", self.spin_width)

        self.spin_energy = QDoubleSpinBox()
        self.spin_energy.setRange(0.1, 50.0)
        self.spin_energy.setValue(0.5 * eng.k0 ** 2)
        self.spin_energy.setSingleStep(0.1)
        self.spin_energy.setStyleSheet(spin_style)
        self.spin_energy.valueChanged.connect(self._update_energy)
        form.addRow("Energia:", self.spin_energy)

        self.spin_sigma = QDoubleSpinBox()
        self.spin_sigma.setRange(1.0, 30.0)
        self.spin_sigma.setValue(eng.sigma)
        self.spin_sigma.setStyleSheet(spin_style)
        self.spin_sigma.valueChanged.connect(self._update_sigma)
        form.addRow("Dispersão:", self.spin_sigma)

        params.setLayout(form)
        v.addWidget(params)

        self.lbl_regime = QLabel()
        self.lbl_regime.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_regime.setStyleSheet("font-weight:bold; color:#facc15; font-size: 13px;")
        v.addWidget(self.lbl_regime)

        # 5. PAINEL DE EXPLICAÇÃO CIENTÍFICA
        self.explainer = ExplainerPanel()
        v.addWidget(self.explainer)

        v.addStretch()
        return panel

    def _update_barrier_spin(self, value):
        self.V0 = value
        self._update_barrier_logic()

    def _update_width(self, value):
        eng.barreira_width = value
        self._update_barrier_logic()

    def _update_barrier_logic(self):
        # Decide qual barreira desenhar no motor
        if self.dimension_mode == "DOUBLE_BARRIER":
            eng.set_double_barrier_potential(self.V0, eng.barreira_width, self.gap_width)
        else:
            eng.set_barrier_height(self.V0)

        self._update_barrier_visuals()

        # Se for Bio, reseta tudo
        if self.dimension_mode == "BIO_QUANTUM":
            self._reset_logic()

    def _update_energy(self, value):
        if value > 0:
            eng.k0 = np.sqrt(2 * value)
            self._reset_logic()

    def _update_sigma(self, value):
        eng.sigma = value
        self._reset_logic()

    # =====================================================
    # CRIAÇÃO DOS WIDGETS GRAFICOS
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

        self.curve_L = plot.plot(pen=pg.mkPen('#22d3ee', width=2))
        self.curve_B = plot.plot(pen=pg.mkPen('#facc15', width=2))
        self.curve_R = plot.plot(pen=pg.mkPen('#22c55e', width=2))

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

        # --- ESTRATÉGIA MULTI-SUPERFÍCIE ---
        z0 = np.zeros((len(eng.x), self.y_steps), dtype=np.float32)

        self.surf_L = gl.GLSurfacePlotItem(z=z0, color=(0.2, 0.8, 1.0, 0.9), shader=None, computeNormals=False,
                                           smooth=False)
        self.surf_B = gl.GLSurfacePlotItem(z=z0, color=(1.0, 0.8, 0.0, 0.9), shader=None, computeNormals=False,
                                           smooth=False)
        self.surf_R = gl.GLSurfacePlotItem(z=z0, color=(0.1, 1.0, 0.2, 0.9), shader=None, computeNormals=False,
                                           smooth=False)

        x_range = eng.x.max() - eng.x.min()
        dx = x_range / (len(eng.x) - 1)
        dy = self.y_width / (self.y_steps - 1)

        for surf in [self.surf_L, self.surf_B, self.surf_R]:
            surf.scale(dx, dy, 1)
            surf.translate(eng.x.min(), -self.y_width / 2, 0)
            view.addItem(surf)

        self.barrier_box_3d = gl.GLBoxItem()
        self.barrier_box_3d.setColor(QColor(255, 140, 0, 100))
        view.addItem(self.barrier_box_3d)

        # Barreira 2 (Para o modo Double)
        self.barrier_2_box_3d = gl.GLBoxItem()
        self.barrier_2_box_3d.setColor(QColor(255, 0, 255, 100))  # Magenta
        self.barrier_2_box_3d.setVisible(False)
        view.addItem(self.barrier_2_box_3d)

        self.sink_box_3d = gl.GLBoxItem()
        self.sink_box_3d.setColor(QColor(0, 255, 0, 150))
        self.sink_box_3d.setVisible(False)
        view.addItem(self.sink_box_3d)

        font_3d = QFont("Arial", 16, QFont.Weight.Bold)

        # Criação correta dos Textos 3D
        self.txt_L = gl.GLTextItem(pos=(-30, 0, 70), text="R: 0%", color=(0.5, 0.9, 1.0, 1.0), font=font_3d)
        view.addItem(self.txt_L)

        self.txt_R = gl.GLTextItem(pos=(30, 0, 70), text="T: 0%", color=(0.5, 1.0, 0.5, 1.0), font=font_3d)
        view.addItem(self.txt_R)

        return view

    # =====================================================
    # LOGICA DE CICLO
    # =====================================================
    def _cycle_dimension(self):
        # Ciclo: 1D -> Radial -> Surface -> DOUBLE -> BIO -> 1D

        if self.dimension_mode == "1D":
            self.dimension_mode = "3D_RADIAL"
            self.btn_dimension.setText("Mode: 3D Radial (Spherical)")
            self.view_stack.setCurrentIndex(0)

        elif self.dimension_mode == "3D_RADIAL":
            self.dimension_mode = "3D_SURFACE"
            self.btn_dimension.setText("Mode: 3D Surface (OpenGL)")
            self.view_stack.setCurrentIndex(1)
            self._set_colors_physics()

        elif self.dimension_mode == "3D_SURFACE":
            self.dimension_mode = "DOUBLE_BARRIER"
            self.btn_dimension.setText("Mode: 🔮 Double Barrier (Resonance)")
            self.btn_dimension.setStyleSheet(
                "background-color: #d946ef; color: white; font-weight: bold; margin-top: 5px;")
            self.view_stack.setCurrentIndex(1)
            self._set_colors_double()

        elif self.dimension_mode == "DOUBLE_BARRIER":
            self.dimension_mode = "BIO_QUANTUM"
            self.btn_dimension.setText("Mode: 🌿 Quantum Photosynthesis")
            self.btn_dimension.setStyleSheet(
                "background-color: #10b981; color: white; font-weight: bold; margin-top: 5px;")
            self.view_stack.setCurrentIndex(1)

            # ATIVA MOTOR BIO
            self.bio_model = bio_eng.QuantumPhotosynthesis()
            self.psi_phys = self.bio_model.psi
            self.title_lbl.setText("🌿 Photosynthetic Complex")
            self.title_lbl.setStyleSheet("font-size:18px; font-weight:600; color:#10b981;")
            self._set_colors_bio()

        else:  # Volta para 1D
            self.dimension_mode = "1D"
            self.btn_dimension.setText("Mode: 1D Standard")
            self.btn_dimension.setStyleSheet(
                "background-color: #7c3aed; color: white; font-weight: bold; margin-top: 5px;")
            self.view_stack.setCurrentIndex(0)
            self.title_lbl.setText("Quantum Tunneling (Physics)")
            self.title_lbl.setStyleSheet("font-size:18px; font-weight:600; color:#58a6ff;")

        self._update_barrier_logic()  # Atualiza V no motor
        self.explainer.update_mode(self.dimension_mode)
        self._reset_logic()

    def _set_colors_physics(self):
        # Cores Físicas (Azul -> Amarelo -> Verde)
        self.surf_L.setData(color=(0.2, 0.8, 1.0, 0.9))
        self.surf_B.setData(color=(1.0, 0.8, 0.0, 0.9))
        self.surf_R.setData(color=(0.1, 1.0, 0.2, 0.9))
        self.barrier_box_3d.setColor(QColor(255, 140, 0, 100))  # Laranja Transparente
        self.barrier_2_box_3d.setVisible(False)
        self.sink_box_3d.setVisible(False)
        self.title_lbl.setText("Quantum Tunneling (Physics)")
        self.title_lbl.setStyleSheet("font-size:18px; font-weight:600; color:#58a6ff;")

        self.txt_L.setData(color=(0.5, 0.9, 1.0, 1.0))
        self.txt_R.setData(color=(0.5, 1.0, 0.5, 1.0))

    def _set_colors_double(self):
        # Ciano (Onda) e Magenta (Barreiras)
        self.surf_L.setData(color=(0.0, 1.0, 1.0, 0.9))
        self.surf_B.setData(color=(1.0, 0.0, 1.0, 0.5))  # Roxo no meio
        self.surf_R.setData(color=(0.0, 1.0, 1.0, 0.9))

        self.barrier_box_3d.setColor(QColor(255, 0, 255, 120))  # Magenta
        self.barrier_2_box_3d.setColor(QColor(255, 0, 255, 120))
        self.sink_box_3d.setVisible(False)

        self.title_lbl.setText("🔮 Quantum Resonance")
        self.title_lbl.setStyleSheet("font-size:18px; font-weight:600; color:#d946ef;")

    def _set_colors_bio(self):
        # Cores Bio (Dourado -> Branco -> Dourado)
        self.surf_L.setData(color=(1.0, 0.8, 0.2, 0.9))
        self.surf_B.setData(color=(1.0, 1.0, 1.0, 0.8))
        self.surf_R.setData(color=(1.0, 0.8, 0.2, 0.9))

        self.barrier_box_3d.setColor(QColor(0, 150, 50, 150))  # Verde Proteína
        self.barrier_2_box_3d.setVisible(False)
        self.sink_box_3d.setVisible(True)
        self.title_lbl.setText("🌿 Photosynthetic Complex")
        self.title_lbl.setStyleSheet("font-size:18px; font-weight:600; color:#10b981;")

        self.txt_L.setData(color=(1.0, 0.4, 0.4, 1.0))
        self.txt_R.setData(color=(0.4, 1.0, 0.4, 1.0))

    def _update_barrier_visuals(self):
        mask = eng.V > 0
        xb = eng.x[mask]

        # --- Atualizar 2D ---
        if xb.size > 0:
            self.barrier_region_2d.setRegion((xb.min(), xb.max()))
            if self.dimension_mode == "BIO_QUANTUM":
                self.barrier_region_2d.setBrush(pg.mkBrush(0, 200, 50, 80))
            elif self.dimension_mode == "DOUBLE_BARRIER":
                self.barrier_region_2d.setBrush(pg.mkBrush(255, 0, 255, 80))  # Magenta
            else:
                self.barrier_region_2d.setBrush(pg.mkBrush(255, 140, 0, 80))

                # --- Atualizar 3D ---
        if xb.size > 0 and self.view_stack.currentIndex() == 1:

            if self.dimension_mode == "DOUBLE_BARRIER":
                # Desenha DUAS barreiras
                w = eng.barreira_width
                gap = self.gap_width
                center = eng.barreira_center

                # Barreira 1 (Esquerda)
                self.barrier_box_3d.resetTransform()
                self.barrier_box_3d.setSize(x=w, y=self.y_width, z=80)
                self.barrier_box_3d.translate(center - gap / 2 - w / 2, -self.y_width / 2, 0)
                self.barrier_box_3d.setVisible(True)

                # Barreira 2 (Direita)
                self.barrier_2_box_3d.resetTransform()
                self.barrier_2_box_3d.setSize(x=w, y=self.y_width, z=80)
                self.barrier_2_box_3d.translate(center + gap / 2 + w / 2, -self.y_width / 2, 0)
                self.barrier_2_box_3d.setVisible(True)

            else:
                # Barreira Simples
                width = xb.max() - xb.min()
                cx = (xb.max() + xb.min()) / 2
                self.barrier_box_3d.resetTransform()
                self.barrier_box_3d.setSize(x=width, y=self.y_width, z=80)
                self.barrier_box_3d.translate(cx - width / 2, -self.y_width / 2, 0)
                self.barrier_box_3d.setVisible(True)
                self.barrier_2_box_3d.setVisible(False)

            # SINK (Bio)
            if self.dimension_mode == "BIO_QUANTUM" and self.bio_model:
                sw = self.bio_model.sink_width
                sc = self.bio_model.sink_center
                self.sink_box_3d.resetTransform()
                self.sink_box_3d.setSize(x=sw, y=self.y_width, z=40)
                self.sink_box_3d.translate(sc - sw / 2, -self.y_width / 2, 0)

            # Textos
            self.txt_L.setData(pos=(xb.min() - 25, 0, 70))
            self.txt_R.setData(pos=(xb.max() + 25, 0, 70))
            self.txt_L.setVisible(True)
            self.txt_R.setVisible(True)

        else:
            self.barrier_box_3d.setVisible(False)
            self.barrier_2_box_3d.setVisible(False)
            self.sink_box_3d.setVisible(False)
            self.txt_L.setVisible(False)
            self.txt_R.setVisible(False)

    def _update_simulation(self):
        if self.is_paused: return

        if self.dimension_mode == "BIO_QUANTUM" and self.bio_model:
            self.psi_phys = self.bio_model.evolve_step()
        else:
            mode = "3D_RADIAL" if self.dimension_mode == "3D_RADIAL" else "1D"
            self.psi_phys = eng.evolve_step(self.psi_phys, mode=mode)
            self.psi_phys = eng.normalize(self.psi_phys, mode=mode)

        self.time += eng.dt * (self.speed.value() / 100)
        self._update_display()

    def _update_display(self):
        x = eng.x
        prob = np.abs(self.psi_phys) ** 2

        # --- UPDATE 3D SURFACES ---
        if self.view_stack.currentIndex() == 1:
            z_full = np.tile(prob * self.Z_SCALE, (self.y_steps, 1)).T.astype(np.float32)

            mask = eng.V > 0
            xb = eng.x[mask]

            if xb.size > 0:
                l_edge, r_edge = xb.min(), xb.max()
                mask_L = (x < l_edge)[:, np.newaxis]
                mask_B = ((x >= l_edge) & (x <= r_edge))[:, np.newaxis]
                mask_R = (x > r_edge)[:, np.newaxis]

                self.surf_L.setData(z=np.where(mask_L, z_full, 0.0))
                self.surf_B.setData(z=np.where(mask_B, z_full, 0.0))
                self.surf_R.setData(z=np.where(mask_R, z_full, 0.0))
            else:
                self.surf_L.setData(z=z_full)
                self.surf_B.setData(z=np.zeros_like(z_full))
                self.surf_R.setData(z=np.zeros_like(z_full))

        # --- UPDATE TEXT & STATUS ---
        if self.dimension_mode == "BIO_QUANTUM" and self.bio_model:
            eff = self.bio_model.get_efficiency_percent()
            self.lbl_trans.setText(f"Harvested: {eff:.1f}%")
            self.lbl_refl.setText(f"Dissipated: {(100 - eff):.1f}%")
            self.txt_L.setData(text="Dissipation")
            self.txt_R.setData(text=f"Harvest: {eff:.1f}%")

        else:
            T, R = eng.calculate_transmission(self.psi_phys)
            self.lbl_trans.setText(f"Transmission: {T:.1f}%")
            self.lbl_refl.setText(f"Reflection: {R:.1f}%")
            self.txt_L.setData(text=f"R: {R:.1f}%")
            self.txt_R.setData(text=f"T: {T:.1f}%")

            if self.V0 >= eng.V_INFINITY:
                self.lbl_regime.setText("🧱 Hard Wall")
            elif self.dimension_mode == "DOUBLE_BARRIER":
                # Checa Ressonância (simplificado)
                self.lbl_regime.setText("🔮 Fabry-Pérot Interference")
            elif self.V0 > 0.5 * eng.k0 ** 2:
                self.lbl_regime.setText("🔒 Tunneling (E < V)")
            else:
                self.lbl_regime.setText("🚀 Scattering (E > V)")

        self.lbl_time.setText(f"Time: {self.time:.2f}")
        self.lbl_norm.setText(f"Norm: {np.trapz(prob, x):.4f}")
        self.lbl_dimension.setText(f"View: {self.dimension_mode}")

        # --- 2D UPDATE ---
        if self.view_stack.currentIndex() == 0:
            mask = eng.V > 0
            xb = eng.x[mask]
            if xb.size > 0:
                l, r = xb.min(), xb.max()
            else:
                l, r = 9999, 9999
            self.curve_L.setData(x, np.where(x < l, prob, np.nan))
            self.curve_B.setData(x, np.where((x >= l) & (x <= r), prob, np.nan))
            self.curve_R.setData(x, np.where(x > r, prob, np.nan))

    def _toggle_pause(self):
        self.is_paused = not self.is_paused
        self.btn_pause.setText("Run" if self.is_paused else "Pause")

    def _reset_logic(self):
        if self.dimension_mode == "BIO_QUANTUM":
            self.bio_model = bio_eng.QuantumPhotosynthesis()
            self.psi_phys = self.bio_model.psi
        else:
            self.psi_phys = eng.psi0.copy()
        self.time = 0.0
        self._update_display()

    def _reset(self):
        self._reset_logic()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Arial", 10))
    win = QuantumApp()
    win.show()
    sys.exit(app.exec())