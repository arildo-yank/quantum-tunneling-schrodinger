


# ⚛️ Quantum Tunneling Simulator: Architecture & Physics

## 1. Mathematical Engine (Split-Step Fourier)

The core simulation relies on the **Split-Step Fourier Method**, a spectral technique that separates the time-evolution operator into kinetic and potential components. This allows for high-precision, unitarity-preserving evolution.

### Dimensionality Handling

The engine operates in two physical modes using a unified solver:

* **1D Cartesian:** Solves the standard Schrödinger equation for .
* **3D Radial (Spherical Symmetry):** Solves for the reduced wavefunction , allowing the 1D engine to simulate a 3D spherically symmetric packet colliding with a spherical shell barrier.

---

## 2. Visualization Pipeline

### 2D Dashboard (PyQtGraph)

* **Real-time plotting:** Displays probability density .
* **Region segmentation:** Dynamically colors the wave based on its position relative to the barrier (Incident, Tunneling, Transmitted).

### 3D Surface Rendering (OpenGL)

Utilizes hardware-accelerated OpenGL to visualize the quantum state as a topographic terrain.

* **Extrusion Logic:** The 1D probability density is extruded along the Y-axis to create a surface.
* **Z-Scaling:** Applies a dynamic amplification factor (default `300x`) to make low-probability tunneling events visually perceptible as physical "terrain."
* **Color Mapping:**
* 🟦 **Blue:** Incident wave (Left of barrier)
* 🟨 **Yellow:** Evanescent wave (Inside barrier)
* 🟩 **Green:** Transmitted wave (Right of barrier)



---

## 3. The Barrier System

The potential  is dynamic and interactive.

**Regimes:**

1. **Finite Barrier:** . Allows for quantum tunneling () and scattering ().
2. **Hard Wall:** When  exceeds a threshold, the simulation switches to a Dirichlet boundary condition ( inside the barrier), perfectly reflecting the wave.

---

## 4. Initial Conditions

The particle is initialized as a Gaussian Wavepacket with minimal uncertainty product:

* ****: Initial position (starts far left).
* ****: Initial momentum (controls velocity towards the barrier).
* ****: Spatial spread.

---

## 5. Observables & Metrics

The simulator calculates physical observables in real-time via numerical integration (Trapezoidal rule):

* **Norm:**  (Must remain ).
* **Transmission ():** Probability of finding the particle past the barrier.
* **Reflection ():** Probability of finding the particle reflected.
* **Energy ():** Kinetic energy expectation value .

---

## 6. Technical Stack

* **Language:** Python 3.10+
* **Numerical Backend:** NumPy (Compatible with v1.x and v2.x via dynamic patching).
* **FFT:** SciPy / NumPy FFT.
* **GUI Framework:** PyQt6 (Widgets & Signal/Slot architecture).
* **Rendering:** PyOpenGL via `pyqtgraph.opengl`.

---

## 7. Educational Scope

This is **not** a pre-rendered animation. It is a **solver** running in real-time. It demonstrates:

* Wave-particle duality.
* The non-zero probability of passing through classically forbidden regions (Tunneling).
* The difference between radial (3D) and cartesian (1D) expansion.
* Conservation of probability current.