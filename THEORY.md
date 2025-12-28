# 📐 Mathematical Theory & Algorithmic Derivation

This document details the physical and mathematical foundations of the simulation engine. It explains how the continuous Time-Dependent Schrödinger Equation (TDSE) is discretized and solved numerically using the **Split-Step Fourier Method (SSFM)**.

---

## 1. The Governing Equation

The behavior of a non-relativistic quantum particle is governed by the TDSE:

$$
i \hbar \frac{\partial}{\partial t} \psi(x, t) = \hat{H} \psi(x, t)
$$

Where the Hamiltonian operator $\hat{H}$ consists of kinetic ($\hat{T}$) and potential ($\hat{V}$) energy operators:

$$
\hat{H} = \hat{T} + \hat{V} = -\frac{\hbar^2}{2m} \frac{\partial^2}{\partial x^2} + V(x)
$$

---

## 2. Time Evolution Operator

Formal integration of the TDSE gives the time evolution operator:

$$
\psi(x, t + \Delta t) = e^{-i \hat{H} \Delta t / \hbar} \psi(x, t)
$$

Substituting $\hat{H} = \hat{T} + \hat{V}$:

$$
\psi(x, t + \Delta t) = e^{-i (\hat{T} + \hat{V}) \Delta t / \hbar} \psi(x, t)
$$

### The Commutation Problem

Since the position operator $\hat{V}$ (diagonal in real space) and the momentum operator $\hat{T}$ (diagonal in momentum space) **do not commute** ($[\hat{T}, \hat{V}] \neq 0$), we cannot simply write $e^{\hat{A}+\hat{B}} = e^{\hat{A}}e^{\hat{B}}$.

---

## 3. The Strang Splitting (Split-Step Method)

To solve this, we use the **Baker-Campbell-Hausdorff formula**. For small time steps $\Delta t$, we can approximate the operator using the **Strang Splitting** (or symmetric Trotter splitting), which introduces an error of order $\mathcal{O}(\Delta t^3)$:

$$
e^{-i (\hat{T} + \hat{V}) \Delta t / \hbar} \approx e^{-i \hat{V} \Delta t / 2\hbar} e^{-i \hat{T} \Delta t / \hbar} e^{-i \hat{V} \Delta t / 2\hbar}
$$

This splitting allows us to apply the operators sequentially in the domains where they are diagonal (simple multiplication).

### The Algorithm Step-by-Step

1.  **Half-Step Potential (Real Space):**
    Apply the potential phase factor for half a time step.
    $$\psi_1 = e^{-i V(x) \Delta t / 2\hbar} \cdot \psi(x, t)$$

2.  **Fourier Transform (Switch to k-space):**
    Move to momentum space using FFT to make the kinetic operator diagonal.
    $$\tilde{\psi}_1(k) = \text{FFT}(\psi_1)$$

3.  **Full-Step Kinetic (Momentum Space):**
    Apply the kinetic evolution. In k-space, $\hat{T} = \frac{\hbar^2 k^2}{2m}$.
    $$\tilde{\psi}_2(k) = e^{-i \frac{\hbar k^2}{2m} \Delta t} \cdot \tilde{\psi}_1(k)$$

4.  **Inverse Fourier Transform (Switch back to x-space):**
    $$\psi_2(x) = \text{IFFT}(\tilde{\psi}_2)$$

5.  **Half-Step Potential (Real Space):**
    Apply the remaining half of the potential.
    $$\psi(x, t + \Delta t) = e^{-i V(x) \Delta t / 2\hbar} \cdot \psi_2(x)$$

---

## 4. Stability and Unitarity

Unlike Finite Difference methods (e.g., Crank-Nicolson), the Split-Step Fourier Method is **unconditionally stable** and **unitary**.

* **Unitarity:** Since the evolution operators are unitary exponentials ($U^\dagger U = I$ where $\hat{H}$ is Hermitian), the norm of the wavefunction is preserved exactly (up to floating-point precision errors):
    $$\frac{d}{dt} \int |\psi|^2 dx = 0$$

* **Precision:** The spatial derivative is calculated with spectral accuracy (infinite order accuracy for smooth functions), limited only by the grid resolution ($dx$).

---

## 5. 3D Radial Symmetry Implementation

For the 3D mode, we assume spherical symmetry where $\psi(\mathbf{r}) = \psi(r)$. The Laplacian in spherical coordinates is:

$$
\nabla^2 \psi = \frac{1}{r^2} \frac{\partial}{\partial r} \left( r^2 \frac{\partial \psi}{\partial r} \right)
$$

By substituting $u(r) = r\psi(r)$, the radial Schrödinger equation becomes:

$$
-\frac{\hbar^2}{2m} \frac{\partial^2 u}{\partial r^2} + V(r)u = E u
$$

This equation is mathematically identical to the 1D Cartesian equation (for $r > 0$). Therefore, we can reuse the same 1D solver engine to evolve $u(r,t)$, provided we enforce the boundary condition $u(0,t) = 0$.

---

## 6. Boundary Conditions

The use of the Fast Fourier Transform (FFT) implicitly enforces **Periodic Boundary Conditions**:

$$\psi(x) = \psi(x + L)$$

To prevent the wavepacket from "wrapping around" the screen and interfering with itself (aliasing), the simulation domain $L$ must be sufficiently large, and an absorbing boundary (imaginary potential) can be optionally added at the edges if needed (though not strictly required for short-duration tunneling experiments).