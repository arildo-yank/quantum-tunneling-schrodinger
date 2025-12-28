# ⚛️ YANKCO Quantum Simulator: Ultimate Edition

## 1. Mathematical Architecture

The core simulation relies on the **Split-Step Fourier Method**, a spectral technique that separates the time-evolution operator into kinetic and potential components. This allows for high-precision, unitarity-preserving evolution.

### Dual-Engine System
The simulator now operates with two distinct physical engines:

1.  **Standard Hermitian Solver (`Schrödinger_engine.py`):**
    * Preserves probability norm ($\int |\psi|^2 dx = 1$).
    * Used for standard Tunneling and Double Barrier Resonance.
    * Supports **1D Cartesian** and **3D Radial** (Spherical Symmetry) modes.

2.  **Bio-Quantum Solver (`quantum_photosynthesis.py`):**
    * **Non-Hermitian Dynamics:** Introduces an imaginary potential term ($-i\Gamma$) to simulate energy absorption (The "Sink").
    * Models the **FMO Complex** (Fenna-Matthews-Olson) found in photosynthetic bacteria.
    * Calculates **Harvesting Efficiency** vs. **Dissipation**.

---

## 2. Visualization Pipeline (Mac-Stable 3D)

### 3D Surface Rendering (OpenGL)
To ensure stability on Apple Silicon (M1/M2/M3) and allow dynamic color changes without crashing, the visualization utilizes a **Multi-Surface Strategy**:

* **Segmented Mesh:** The wave is rendered as three separate physical meshes (Left, Barrier, Right).
* **Dynamic Coloring:** Each segment changes color independently based on the active physics mode.

### Visual Modes & Color Mapping

| Mode | Incident Wave | Barrier Region | Transmitted Wave | Visual Concept |
| :--- | :--- | :--- | :--- | :--- |
| **Standard Physics** | 🟦 **Blue** | 🟨 **Yellow** | 🟩 **Green** | Probability Flux |
| **Double Barrier** | 🟦 **Cyan** | 🟪 **Magenta** | 🟦 **Cyan** | Fabry-Pérot Resonance |
| **Bio-Quantum** | 🌟 **Gold** | ⬜ **White** | 🌟 **Gold** | Light / Exciton |

---

## 3. Physical Regimes

The simulator now supports three distinct physical phenomena controlled by the "Mode" system:

### A. Quantum Tunneling (Single Barrier)
* **Physics:** A particle encounters a potential barrier $ V > E $.
* **Key Phenomenon:** Exponential decay inside the barrier allows non-zero transmission probability.

### B. Double Barrier (Resonance) 
* **Physics:** Two barriers separated by a potential well (Quantum Dot).
* **Key Phenomenon:** **Resonant Tunneling**. At specific energies, constructive interference allows the wave to pass through the barriers with near 100% transmission, even if they are high. Analogous to the **Double Slit Experiment** in time/energy domain.

### C. Quantum Photosynthesis (Bio-Quantum)
* **Physics:** An exciton (energy packet) navigating a protein landscape.
* **Key Phenomenon:** **Quantum Coherence**. The wave explores all paths simultaneously (superposition) to find the reaction center (Green Sink Box) efficiently before dissipating.

---

## 4. User Interface & Controls

### Interactive Modules
1.  **Simulation Control:** Pause, Reset, and Time Speed.
2.  **Exact Parameters (SpinBoxes):** Allows precise numerical input for scientific testing:
    * Potential Height ($V_0$)
    * Barrier Width ($w$)
    * Initial Energy ($E$)
    * Wavepacket Spread ($\sigma$)
3.  **Explainer Panel:** A collapsible educational widget (`widgets.py`) that provides context-sensitive scientific explanations for laypeople, updating dynamically with the selected mode.

---

## 5. Technical Stack & Modular Structure

The project is structured to separate logic, math, and UI:

* `main.py`: The GUI controller, event loop, and OpenGL integration.
* `Schrödinger_engine.py`: The core physics solver (NumPy-based).
* `quantum_photosynthesis.py`: The biological extension engine.
* `widgets.py`: Custom UI components (Educational Panels).

**Dependencies:**
* Python 3.10+
* NumPy (v1.x / v2.x compatible)
* PyQt6 (GUI)
* PyQtGraph (Real-time Plotting & OpenGL)

---

## 6. Educational Philosophy

This software demonstrates that **Nature utilizes Quantum Mechanics**.
It bridges the gap between abstract physics equations and observable biological reality, showing that the same math that describes an electron in a transistor also describes how a leaf captures sunlight.