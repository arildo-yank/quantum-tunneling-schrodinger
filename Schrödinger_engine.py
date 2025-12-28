import numpy as np
from numpy.fft import fft, ifft

# =========================================================
# COMPATIBILIDADE NUMPY 2.x
# =========================================================
if not hasattr(np, "trapz"):
    np.trapz = np.trapezoid

# =========================================================
# PARÂMETROS
# =========================================================
L = 100.0
N = 1024
dx = L / N
x = np.linspace(-L / 2, L / 2, N)

# Coordenada radial (r deve ser sempre positivo)
r = np.abs(x)

dt = 0.05
barreira_width = 2.0
barreira_center = 10.0
V_INFINITY = 1e6
_is_hard_wall = False

# =========================================================
# FUNÇÃO DE ONDA INICIAL
# =========================================================
x0 = -20.0
sigma = 2.0
k0 = 3.0

norm_factor = 1.0 / np.sqrt(sigma * np.sqrt(np.pi))
psi0 = (
        norm_factor
        * np.exp(-0.5 * ((x - x0) / sigma) ** 2)
        * np.exp(1j * k0 * x)
)

# =========================================================
# ESPAÇO DE MOMENTO E POTENCIAL
# =========================================================
k = 2 * np.pi * np.fft.fftfreq(N, d=dx)
evolution_kinetic = np.exp(-1j * (k ** 2 / 2) * dt)
V = np.zeros(N)


def _barrier_mask():
    return (
            (x > (barreira_center - barreira_width / 2)) &
            (x < (barreira_center + barreira_width / 2))
    )


def set_barrier_height(V0: float):
    global V, _is_hard_wall
    V[:] = 0.0
    mask = _barrier_mask()

    if V0 >= V_INFINITY:
        V[mask] = V_INFINITY
        _is_hard_wall = True
    else:
        V[mask] = V0
        _is_hard_wall = False


set_barrier_height(2.0)


# =========================================================
# ENGINES
# =========================================================
def evolve_step_1d(psi: np.ndarray) -> np.ndarray:
    psi = psi * np.exp(-1j * V * (dt / 2))
    psi_k = fft(psi)
    psi_k *= evolution_kinetic
    psi = ifft(psi_k)
    psi = psi * np.exp(-1j * V * (dt / 2))
    if _is_hard_wall:
        psi[_barrier_mask()] = 0.0
    return psi


def evolve_step_3d_radial(u: np.ndarray) -> np.ndarray:
    """
    Evolui a função auxiliar u(r) = r*psi(r).
    """
    u = u * np.exp(-1j * V * (dt / 2))
    u_k = fft(u)
    u_k *= evolution_kinetic
    u = ifft(u_k)
    u = u * np.exp(-1j * V * (dt / 2))

    # FIX: Condição de contorno na origem (x=0) e não no índice 0
    # O índice do centro do array (onde x=0 e r=0) é N//2
    center_idx = N // 2
    u[center_idx] = 0.0

    # Para consistência visual, zeramos u onde r=0 (evita picos numéricos)
    u[r < 1e-10] = 0.0

    if _is_hard_wall:
        u[_barrier_mask()] = 0.0

    return u


def evolve_step(psi: np.ndarray, mode="1D") -> np.ndarray:
    if mode == "1D":
        return evolve_step_1d(psi)
    elif mode == "3D_RADIAL":
        return evolve_step_3d_radial(psi)
    return psi


# =========================================================
# CÁLCULOS FÍSICOS
# =========================================================
def calculate_transmission(psi: np.ndarray):
    prob = np.abs(psi) ** 2
    left_mask = x < (barreira_center - barreira_width / 2)
    right_mask = x > (barreira_center + barreira_width / 2)
    R = np.sum(prob[left_mask]) * dx
    T = np.sum(prob[right_mask]) * dx
    return T * 100.0, R * 100.0


# --- ADICIONAR NO FINAL DE Schrödinger_engine.py ---

def set_double_barrier(v0, width, gap):
    """
    Cria duas barreiras separadas por um 'gap' (Poço Quântico).
    Isso gera padrões de interferência e ressonância (Fabry-Pérot).
    """
    global V, barreira_center, barreira_width
    V = np.zeros_like(x)

    # Muro 1 (Esquerda)
    start1 = barreira_center - gap / 2 - width
    end1 = barreira_center - gap / 2

    # Muro 2 (Direita)
    start2 = barreira_center + gap / 2
    end2 = barreira_center + gap / 2 + width

    mask = ((x >= start1) & (x <= end1)) | ((x >= start2) & (x <= end2))
    V[mask] = v0
# No final do arquivo Schrödinger_engine.py

def set_double_barrier_potential(v0, width, gap):
    """
    Define o potencial V(x) como uma barreira dupla.
    v0: Altura das barreiras.
    width: Largura de cada barreira.
    gap: Distância entre as duas barreiras.
    """
    global V
    V = np.zeros_like(x)

    # Limites da primeira barreira (esquerda)
    b1_start = barreira_center - gap / 2 - width
    b1_end = barreira_center - gap / 2

    # Limites da segunda barreira (direita)
    b2_start = barreira_center + gap / 2
    b2_end = barreira_center + gap / 2 + width

    # Aplica o potencial onde estão as barreiras
    mask = ((x >= b1_start) & (x <= b1_end)) | ((x >= b2_start) & (x <= b2_end))
    V[mask] = v0
def normalize(psi: np.ndarray, mode="1D") -> np.ndarray:
    """
    FIX: Correção na normalização 3D.
    Se estamos evoluindo u(r), a probabilidade |u|^2 já contém o fator geométrico r^2.
    Portanto, a integral é simplesmente ∫|u|^2 dr.
    """
    prob = np.abs(psi) ** 2

    # Em ambos os casos (1D psi ou 3D u), integramos a densidade direta
    norm = np.trapz(prob, x)

    if norm > 0:
        psi /= np.sqrt(norm)

    return psi