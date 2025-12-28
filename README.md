# ⚛️ YANKCO · Quantum Tunnelling Simulator (Ultimate Edition)

A professional-grade, real-time **Quantum Tunnelling Simulator** based on the time-dependent Schrödinger equation (TDSE).

This software bridges the gap between abstract quantum mechanics and observable reality, visualizing how particles behave when encountering energy barriers. It demonstrates phenomena impossible in classical physics—such as tunnelling through "walls", wave-packet interference, and quantum biological transport.

Built with **Python**, **NumPy**, **PyQt6**, and **OpenGL** for high-performance scientific visualization.

---

## 🔬 Dual-Engine Architecture

The simulator now operates with two distinct physical engines to cover different aspects of quantum reality:

### 1. Standard Hermitian Solver (Physics Engine)
* **Method:** Split-Step Fourier.
* **Characteristics:** Preserves probability norm ($\int |\psi|^2 dx = 1$).
* **Use Case:** Standard tunnelling, scattering, and resonant tunnelling (Double Barrier).

### 2. Bio-Quantum Solver (Photosynthesis Engine)
* **Method:** Non-Hermitian Dynamics with Imaginary Potentials.
* **Characteristics:** Simulates energy absorption/harvesting (The "Sink").
* **Use Case:** Modeling the FMO Complex in photosynthesis, calculating **Harvesting Efficiency** vs. **Dissipation**.

---

## ✨ Visualization & Modes

The simulation offers **5 distinct visualization modes**, rendering real-time 3D surfaces with dynamic colouring based on the physics regime:

| Mode | Visualization | Physics Concept | Color Scheme |
| :--- | :--- | :--- | :--- |
| **1D Cartesian** | Flat Plot | Standard Wave Mechanics | 🟦 Blue / 🟩 Green |
| **3D Radial** | Spherical | Expansion from a point source | 🟦 Blue / 🟩 Green |
| **3D Surface** | Topographic | Terrain view of probability density | 🟦 Blue / 🟩 Green |
| **Double Barrier** | Dual Walls | **Fabry-Pérot Resonance** (Interference) | 🟦 Cyan / 🟪 Magenta |
| **Bio-Quantum** | Energy Flow | **Quantum Coherence** in Biology | 🌟 Gold / ⬜ White |

---

## 🎛️ Interactive Controls

### 1. Precision Parameters
Unlike basic sliders, this edition includes **Exact Input Fields (SpinBoxes)** for laboratory-grade control:
* **Potential ($V_0$):** Height of the barrier(s).
* **Width ($w$):** Thickness of the barrier or protein gap.
* **Energy ($E$):** Initial kinetic energy of the particle.
* **Spread ($\sigma$):** Uncertainty of the wavepacket.

### 2. Educational Explainer Panel
A collapsible widget that provides context-sensitive scientific explanations for laypeople, updating dynamically as you switch modes (e.g., explaining "Resonance" when in Double Barrier mode).

---

## 🌍 Real-World Applications

This simulator demonstrates the exact physical principles behind technologies and natural phenomena:

### 1. Modern Electronics (Transistors) ⚛️
* **Context:** 5nm and 3nm chips (Apple Silicon, NVIDIA, AMD).
* **Physics:** Electrons tunnel through insulating barriers (gate oxide), causing "leakage current." This is the fundamental limit of Moore's Law.

### 2. Scanning Tunnelling Microscope (STM) 🔬
* **Context:** Nanotechnology labs (IBM, CERN).
* **Physics:** A conductive tip detects atoms without touching them. The current depends exponentially on the tunnelling distance.

### 3. Nuclear Fusion (The Sun) ☀️
* **Context:** Astrophysics and ITER.
* **Physics:** Protons repel each other. Tunnelling allows them to breach the **Coulomb Barrier** and fuse, powering stars. Without this, the Sun would not shine.

### 4. Quantum Biology (Photosynthesis) 🧬
* **Context:** Plants and Bacteria (FMO Complex).
* **Physics:** Modeled in the **"Bio-Quantum"** mode. Excitons use quantum superposition to explore all paths simultaneously, finding the reaction center with near 100% efficiency.

### 5. Resonant Tunnelling Diodes 🔮
* **Context:** High-frequency oscillators (Terahertz).
* **Physics:** Modeled in the **"Double Barrier"** mode. Waves pass through two barriers perfectly when their energy matches the system's resonance frequency.

---

## 🚀 Installation & Usage

### 1. Prerequisites
Ensure you have Python 3.10+ installed.

```bash
pip install numpy scipy pyqt6 pyqtgraph PyOpenGL PyOpenGL_accelerate
