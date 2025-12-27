

# 📐 Mathematical Theory & Algorithmic Derivation

This document details the physical and mathematical foundations of the simulation engine. It explains how the continuous Time-Dependent Schrödinger Equation (TDSE) is discretized and solved numerically using the **Split-Step Fourier Method (SSFM)**.

---

## 1. The Governing Equation

The behavior of a non-relativistic quantum particle is governed by the TDSE:

Where the Hamiltonian operator  consists of kinetic () and potential () energy operators:

---

## 2. Time Evolution Operator

Formal integration of the TDSE gives the time evolution operator:

Substituting :

### The Commutation Problem

Since the position operator  (diagonal in real space) and the momentum operator  (diagonal in momentum space) **do not commute** (), we cannot simply write .

---

## 3. The Strang Splitting (Split-Step Method)

To solve this, we use the **Baker-Campbell-Hausdorff formula**. For small time steps , we can approximate the operator using the **Strang Splitting** (or symmetric Trotter splitting), which introduces an error of order :

This splitting allows us to apply the operators sequentially in the domains where they are diagonal (simple multiplication).

### The Algorithm Step-by-Step

1. **Half-Step Potential (Real Space):**
Apply the potential phase factor for half a time step.

2. **Fourier Transform (Switch to k-space):**
Move to momentum space using FFT to make the kinetic operator diagonal.

3. **Full-Step Kinetic (Momentum Space):**
Apply the kinetic evolution. In k-space, .

4. **Inverse Fourier Transform (Switch back to x-space):**

5. **Half-Step Potential (Real Space):**
Apply the remaining half of the potential.


---

## 4. Stability and Unitarity

Unlike Finite Difference methods (e.g., Crank-Nicolson), the Split-Step Fourier Method is **unconditionally stable** and **unitary**.

* **Unitarity:** Since the evolution operators are unitary exponentials ( where  is Hermitian), the norm of the wavefunction is preserved exactly (up to floating-point precision errors):

* **Precision:** The spatial derivative is calculated with spectral accuracy (infinite order accuracy for smooth functions), limited only by the grid resolution ().

---

## 5. 3D Radial Symmetry Implementation

For the 3D mode, we assume spherical symmetry where . The Laplacian in spherical coordinates is:

By substituting , the radial Schrödinger equation becomes:

This equation is mathematically identical to the 1D Cartesian equation (for ). Therefore, we can reuse the same 1D solver engine to evolve , provided we enforce the boundary condition .

---

## 6. Boundary Conditions

The use of the Fast Fourier Transform (FFT) implicitly enforces **Periodic Boundary Conditions**:

To prevent the wavepacket from "wrapping around" the screen and interfering with itself (aliasing), the simulation domain  must be sufficiently large, and an absorbing boundary (imaginary potential) can be optionally added at the edges if needed (though not strictly required for short-duration tunneling experiments).