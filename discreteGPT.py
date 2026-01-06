import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# Discrete Time Axis
# ----------------------------
N_MIN, N_MAX = -10, 10
n = np.arange(N_MIN, N_MAX + 1)

# ----------------------------
# Base Discrete Signal x[n]
# ----------------------------
def get_x_n(n):
    """
    x[n] = [1,2,3,2,1] centered at n=0
           + spike at n=4
    """
    x = np.zeros_like(n, dtype=float)
    x[np.abs(n) <= 2] = 3 - np.abs(n[np.abs(n) <= 2])
    x[n == 4] = 2
    return x

# ----------------------------
# Discrete Operations
# ----------------------------
def time_shift(x, k):
    """y[n] = x[n-k]"""
    if k > 0:      # delay
        return np.concatenate((np.zeros(k), x[:-k]))
    elif k < 0:    # advance
        return np.concatenate((x[-k:], np.zeros(-k)))
    return x

def time_reverse(x):
    """y[n] = x[-n]"""
    return x[::-1]

def even_odd_decomposition(x):
    """x[n] = xe[n] + xo[n]"""
    xr = time_reverse(x)
    xe = 0.5 * (x + xr)
    xo = 0.5 * (x - xr)
    return xe, xo

def downsample(x, M):
    """
    y[n] = x[M n]
    Keeps every M-th sample
    """
    y = np.zeros_like(x)
    y[::M] = x[::M]
    return y

def upsample(x, L):
    """
    y[n] = x[n/L] if n multiple of L, else 0
    """
    y = np.zeros(len(x) * L)
    y[::L] = x
    return y

def time_scale_signal_interpolate(x, k=2):
    N = len(x)
    y = np.zeros(N * k - (k - 1))

    for i in range(len(y)):
        if i % k == 0:
            y[i] = x[i // k]
        else:
            left = i // k
            right = left + 1
            if right < len(x):
                y[i] = (x[left] + x[right]) / 2
            else:
                y[i] = x[left]

    return y


# ----------------------------
# Plotting Utility
# ----------------------------
def plot_stem(n, x, title, color):
    markerline, stemlines, baseline = plt.stem(n, x, basefmt="k")
    plt.setp(markerline, color=color)
    plt.setp(stemlines, color=color)
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.xticks(n)
    plt.ylim(min(x) - 0.5, max(x) + 0.5)

# ----------------------------
# Main Function
# ----------------------------
def main():
    x = get_x_n(n)
    xe, xo = even_odd_decomposition(x)

    plt.figure(figsize=(14, 12))

    # 1. Original Signal
    plt.subplot(4, 2, 1)
    plot_stem(n, x, "Original Signal x[n]", "tab:blue")

    # 2. Time Reversal
    plt.subplot(4, 2, 2)
    plot_stem(n, time_reverse(x), "Time Reversal x[-n]", "tab:orange")

    # 3. Time Shift
    plt.subplot(4, 2, 3)
    plot_stem(n, time_shift(x, 3), "Time Shift x[n-3] (Delay)", "tab:green")

    # 4. Downsampling
    plt.subplot(4, 2, 4)
    plot_stem(n, downsample(x, 2), "Downsampling x[2n]", "tab:red")

    # 5. Even Component
    plt.subplot(4, 2, 5)
    plot_stem(n, xe, "Even Component xe[n]", "tab:purple")

    # 6. Odd Component
    plt.subplot(4, 2, 6)
    plot_stem(n, xo, "Odd Component xo[n]", "tab:brown")

    # 7. Upsampling
    xu = upsample(x, 2)
    nu = np.arange(len(xu)) + 2 * N_MIN
    plt.subplot(4, 2, 7)
    plot_stem(nu, xu, "Upsampling x[n/2] (L = 2)", "tab:pink")

    plt.tight_layout()
    plt.show()

    # Verification
    print("Reconstruction Error (should be 0):", np.sum(x - (xe + xo)))

# ----------------------------
# Run Program
# ----------------------------
if __name__ == "__main__":
    main()
