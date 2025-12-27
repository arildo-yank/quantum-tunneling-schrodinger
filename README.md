Aqui está a versão definitiva do seu **`README.md`**.

Eu unifiquei a descrição técnica do projeto com a lista de **Aplicações Reais** (que você enviou em português), traduzindo tudo para o inglês técnico para manter o padrão profissional do GitHub/Portfólio.

Também atualizei a lista de **Features** para incluir as novidades que acabamos de programar (OpenGL, 3D Radial e Terreno).

---

# CERN · Quantum Tunneling Simulator (Ultimate Edition)

A professional-grade, real-time **Quantum Tunneling Simulator** based on the time-dependent Schrödinger equation (TDSE).

This software visualizes how quantum particles behave when encountering energy barriers, demonstrating phenomena that are impossible in classical physics—such as tunneling through "walls" and wave-packet interference.

Built with **Python**, **NumPy**, **PyQt6**, and **OpenGL** for high-performance scientific visualization.

---

## 🔬 Physics Engine

The simulator solves the **Time-Dependent Schrödinger Equation**:

It utilizes the **Split-Step Fourier Method**, a spectral algorithm that is:

1. **Unconditionally Stable:** Time steps do not cause explosions.
2. **Unitary:** Probability is conserved ().
3. **Fast:** Uses FFT (Fast Fourier Transform) for  complexity.

---

## ✨ Key Features

### 1. Multi-Dimensional Visualization

* **1D Cartesian:** Standard textbook visualization of wave packets.
* **3D Radial:** Simulates spherical symmetry ().
* **3D Surface (OpenGL):** A topographic "mountain" view of the probability density, rendered with hardware acceleration for analyzing wave spread and tunneling leakage.

### 2. Interactive Potential Barriers

* **Finite Barrier:** Allows for partial transmission and reflection.
* **Hard Wall:** Automatically switches to infinite potential (Dirichlet boundary) when  is high.
* **Real-time Controls:** Adjust barrier height () and time-scale on the fly.

### 3. Real-Time Observables

* Calculates **Transmission ()** and **Reflection ()** coefficients instantly.
* Monitors **Energy Expectation** .
* Detects physical regimes: **Tunneling** () vs **Scattering** ().

---

## 🌍 Real-World Applications (Why this matters?)

This simulator demonstrates the exact physical principle behind technologies and natural phenomena that shape our universe:

### 1. Modern Electronics (Transistors) ⚛️

* **Context:** 5nm and 3nm chips (Apple Silicon, NVIDIA, AMD).
* **Physics:** Electrons tunnel through insulating barriers (gate oxide), causing "leakage current." This is the fundamental physical limit of Moore's Law.

### 2. Scanning Tunneling Microscope (STM) 🔬

* **Context:** Nanotechnology labs (IBM, CERN).
* **Physics:** A conductive tip detects atoms without touching them. The current depends exponentially on the tunneling distance, allowing for atomic-scale imaging.

### 3. Nuclear Fusion (The Sun) ☀️

* **Context:** Astrophysics and ITER.
* **Physics:** Protons naturally repel each other. Tunneling allows them to breach the **Coulomb Barrier** and fuse, powering stars. Without this, the Sun would not shine.

### 4. Alpha Decay ☢️

* **Context:** Nuclear physics and carbon dating.
* **Physics:** Alpha particles do not have enough classical energy to escape the nucleus, yet they tunnel out over time, defining the half-life of elements.

### 5. Quantum Biology & Chemistry 🧬

* **Context:** Photosynthesis and enzymatic reactions.
* **Physics:** Electrons and protons tunnel through potential barriers within cells to accelerate chemical reactions essential for life.

---

## 🚀 Installation & Usage

### 1. Prerequisites

Ensure you have Python 3.10+ installed.

```bash
pip install numpy scipy pyqt6 pyqtgraph PyOpenGL PyOpenGL_accelerate

```

### 2. Running the Simulator

Launch the main application to access the unified dashboard (2D and 3D modes):

```bash
python main.py

```

### 3. Controls

* **Space / Pause Button:** Freeze time.
* **Mode Switch:** Toggle between 1D, 3D Radial, and 3D Surface views.
* **Sliders:** Adjust simulation speed and barrier height.

---

## 📚 Educational Scope

This tool is designed for:

* **Undergraduate Physics:** Visualizing wave mechanics.
* **Computational Physics:** Demonstrating spectral methods.
* **Public Outreach:** Showing the non-intuitive nature of the quantum world.

> *"If you are not shocked by quantum physics, you have not understood it."* — Niels Bohr

---

**Developed by Arildo Yank** *Field Service Engineer & Software Developer*