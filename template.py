import numpy as np
import matplotlib.pyplot as plt
 
# ----------------------------
# Signal parameters
# ----------------------------
T_MIN, T_MAX, N = -4.0, 4.0, 4001
 
# ----------------------------
# Base signal x(t)
# ----------------------------
def x_of_t(t: np.ndarray) -> np.ndarray:
    """
    Base signal x(t)
    Combination of triangular pulses and ramp
    """
    # Triangular pulse centered at 0
    tri0 = np.zeros_like(t, dtype=float)
    m0 = np.abs(t) <= 1.0
    tri0[m0] = 1.0 - np.abs(t[m0])
 
    # Windowed ramp (odd-ish component)
    ramp = np.zeros_like(t, dtype=float)
    m1 = np.abs(t) <= 1.0
    ramp[m1] = t[m1]
 
    # Shifted triangular pulse
    tri_shift = np.zeros_like(t, dtype=float)
    u = t - 1.2
    m2 = np.abs(u) <= 1.0
    tri_shift[m2] = 1.0 - np.abs(u[m2])
 
    return tri0 + 0.6 * ramp + 0.4 * tri_shift
 
# ----------------------------
# Time-domain operations
# ----------------------------
def time_reverse(x: np.ndarray) -> np.ndarray:
    return x[::-1]
 
def even_odd_decompose(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    xr = time_reverse(x)
    xe = 0.5 * (x + xr)
    xo = 0.5 * (x - xr)
    return xe, xo
 
def time_shift(t: np.ndarray, x: np.ndarray, t0: float) -> np.ndarray:
    return np.interp(t - t0, t, x, left=0.0, right=0.0)
 
def time_scale(t: np.ndarray, x: np.ndarray, a: float) -> np.ndarray:
    return np.interp(a * t, t, x, left=0.0, right=0.0)
 
def general_time_transform(t: np.ndarray, x: np.ndarray, a: float = 1.0, t0: float = 0.0) -> np.ndarray:
    return np.interp(a * t - t0, t, x, left=0.0, right=0.0)
 
# ----------------------------
# Symmetry checks
# ----------------------------
def is_even(x: np.ndarray, tol=1e-6) -> bool:
    return np.allclose(x, x[::-1], atol=tol)
 
def is_odd(x: np.ndarray, tol=1e-6) -> bool:
    return np.allclose(x, -x[::-1], atol=tol)
 
# ----------------------------
# Plotting utilities
# ----------------------------
def plot_three(t: np.ndarray, x: np.ndarray, xe: np.ndarray, xo: np.ndarray):
    plt.figure()
    plt.plot(t, x, label="x(t)")
    plt.plot(t, xe, label="xe(t)")
    plt.plot(t, xo, label="xo(t)")
    plt.title("Even–Odd Decomposition")
    plt.xlabel("t")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.legend()
 
def plot_pair(t: np.ndarray, x: np.ndarray, xr: np.ndarray, title="Time Reversal"):
    plt.figure()
    plt.plot(t, x, label="x(t)")
    plt.plot(t, xr, label="x(-t)")
    plt.title(title)
    plt.xlabel("t")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.legend()
 
# ----------------------------
# Main
# ----------------------------
def main():
    t = np.linspace(T_MIN, T_MAX, N)
    x = x_of_t(t)
 
    # Time reversal and even-odd decomposition
    xr = time_reverse(x)
    xe, xo = even_odd_decompose(x)
 
    # Plot basic results
    plot_pair(t, x, xr)
    plot_three(t, x, xe, xo)
 
    # Time shift
    xs = time_shift(t, x, t0=1.0)
    plot_pair(t, x, xs, title="Time Shift: x(t-1)")
 
    # Time scaling
    xc = time_scale(t, x, a=2.0)
    plot_pair(t, x, xc, title="Time Scale: x(2t)")
 
    # General transform (scaling + shift + reversal)
    xg = general_time_transform(t, x, a=-1.5, t0=0.8)
    plot_pair(t, x, xg, title="General Transform: x(-1.5t - 0.8)")
 
    # Symmetry checks
    print("x(t) is even:", is_even(x))
    print("x(t) is odd:", is_odd(x))
    print("xe(t) is even:", is_even(xe))
    print("xo(t) is odd:", is_odd(xo))
 
    plt.show()
 
if __name__ == "__main__":
    main()
 