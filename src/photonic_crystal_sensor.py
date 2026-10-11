"""
Photonic Crystal Refractive-Index Sensor
----------------------------------------

"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

# -----------------------------
# Baseline physical parameters
# -----------------------------
N_A = 1.45
N_B = 2.00
D_A_NM = 120.0
D_B_NM = 90.0
D_DEFECT_NM = 250.0
N_PERIODS = 5

N_ENV = 1.00       # incident medium
N_SUB = 1.00       # substrate
N_SENSING_BASE = 1.33

LAMBDA_MIN_NM = 500.0
LAMBDA_MAX_NM = 900.0
N_LAMBDA = 4001

WAVELENGTHS_NM = np.linspace(
    LAMBDA_MIN_NM, LAMBDA_MAX_NM, N_LAMBDA
)


def layer_matrix(n, thickness_nm, wavelength_nm):
    """
    Characteristic matrix for a non-magnetic dielectric layer
    at normal incidence.

    q = n
    delta = 2*pi*n*d/lambda

    Matrix:
        [[cos(delta), i*sin(delta)/q],
         [i*q*sin(delta), cos(delta)]]
    """
    delta = 2.0 * np.pi * n * thickness_nm / wavelength_nm
    c = np.cos(delta)
    s = np.sin(delta)

    return np.array([
        [c, 1j * s / n],
        [1j * n * s, c]
    ], dtype=complex)


def stack_matrix(layers, wavelength_nm):
    """Multiply characteristic matrices in physical order."""
    M = np.eye(2, dtype=complex)

    for n, d_nm in layers:
        M = M @ layer_matrix(n, d_nm, wavelength_nm)

    return M


def transmission(layers, wavelength_nm, n_in=N_ENV, n_out=N_SUB):
    """
    Power transmittance at normal incidence.

    For:
        M = [[A, B],
             [C, D]]

    t = 2*n_in /
        (n_in*A + n_in*n_out*B + C + n_out*D)

    T = (n_out/n_in)*|t|^2
    """
    M = stack_matrix(layers, wavelength_nm)
    A, B = M[0, 0], M[0, 1]
    C, D = M[1, 0], M[1, 1]

    denom = n_in*A + n_in*n_out*B + C + n_out*D
    t = 2.0 * n_in / denom
    T = (n_out / n_in) * abs(t)**2

    return float(np.real_if_close(T))


def build_structure(n_sensing):
    """
    Symmetric photonic-crystal cavity:
        (A/B)^N + defect + (B/A)^N

    The defect is the sensing region.
    """
    left = [(N_A, D_A_NM), (N_B, D_B_NM)] * N_PERIODS
    right = [(N_B, D_B_NM), (N_A, D_A_NM)] * N_PERIODS
    return left + [(n_sensing, D_DEFECT_NM)] + right


def calculate_spectrum(n_sensing):
    layers = build_structure(n_sensing)
    T = np.array([
        transmission(layers, wl)
        for wl in WAVELENGTHS_NM
    ])
    return T


def find_resonance(wavelengths, T, min_prominence=0.02):
    """
    Find the strongest transmission peak.

    Returns wavelength and transmission of the selected peak.
    """
    peaks, props = find_peaks(
        T,
        prominence=min_prominence,
        distance=max(5, len(T)//200)
    )

    if len(peaks) == 0:
        idx = int(np.argmax(T))
        return wavelengths[idx], T[idx]

    # Select highest-transmission peak
    best = peaks[np.argmax(T[peaks])]
    return wavelengths[best], T[best]


def plot_baseline_spectrum():
    T = calculate_spectrum(N_SENSING_BASE)
    resonance_wl, resonance_T = find_resonance(WAVELENGTHS_NM, T)

    plt.figure(figsize=(9, 5))
    plt.plot(WAVELENGTHS_NM, T, linewidth=1.5)
    plt.axvline(
        resonance_wl,
        linestyle="--",
        linewidth=1.0,
        label=f"Resonance ≈ {resonance_wl:.2f} nm"
    )
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Transmission")
    plt.title("Photonic Crystal Transmission Spectrum")
    plt.grid(alpha=0.25)
    plt.legend()
    plt.tight_layout()
    plt.savefig(RESULTS / "transmission_spectrum.png", dpi=300)
    plt.close()

    return resonance_wl, resonance_T


def sweep_refractive_index():
    """
    Sweep sensing index and track the resonance wavelength.
    """
    indices = np.linspace(1.30, 1.38, 17)
    rows = []

    for n in indices:
        T = calculate_spectrum(n)
        wl_res, peak_T = find_resonance(WAVELENGTHS_NM, T)
        rows.append({
            "sensing_refractive_index": n,
            "resonance_wavelength_nm": wl_res,
            "peak_transmission": peak_T
        })

    df = pd.DataFrame(rows)
    df.to_csv(RESULTS / "results.csv", index=False)

    return df


def plot_resonance_shift(df):
    plt.figure(figsize=(8, 5))
    plt.plot(
        df["sensing_refractive_index"],
        df["resonance_wavelength_nm"],
        "o-",
        linewidth=1.5,
        markersize=4
    )
    plt.xlabel("Sensing refractive index (RIU)")
    plt.ylabel("Resonance wavelength (nm)")
    plt.title("Resonance Shift with Refractive Index")
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(RESULTS / "resonance_shift.png", dpi=300)
    plt.close()


def sensitivity_analysis(df):
    """
    Linear fit:
        lambda_res = S*n + intercept

    S is bulk sensitivity in nm/RIU.
    """
    x = df["sensing_refractive_index"].to_numpy()
    y = df["resonance_wavelength_nm"].to_numpy()

    slope, intercept = np.polyfit(x, y, 1)
    y_fit = slope*x + intercept

    ss_res = np.sum((y - y_fit)**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    r2 = 1 - ss_res / ss_tot if ss_tot != 0 else np.nan

    plt.figure(figsize=(8, 5))
    plt.scatter(x, y, s=28, label="Simulation")
    plt.plot(
        x, y_fit, linewidth=1.5,
        label=f"Linear fit: S={slope:.2f} nm/RIU, R²={r2:.5f}"
    )
    plt.xlabel("Sensing refractive index (RIU)")
    plt.ylabel("Resonance wavelength (nm)")
    plt.title("Photonic Crystal Sensor Sensitivity")
    plt.grid(alpha=0.25)
    plt.legend()
    plt.tight_layout()
    plt.savefig(RESULTS / "sensitivity_fit.png", dpi=300)
    plt.close()

    return slope, intercept, r2


def save_summary(resonance_wl, resonance_T, sensitivity, r2):
    text = f"""PHOTONIC CRYSTAL SENSOR - BASELINE RESULTS

Baseline sensing index: {N_SENSING_BASE:.4f} RIU
Resonance wavelength: {resonance_wl:.4f} nm
Peak transmission: {resonance_T:.6f}

Bulk sensitivity: {sensitivity:.4f} nm/RIU
Linear-fit R^2: {r2:.6f}

Structure:
(A/B)^{N_PERIODS} / Defect / (B/A)^{N_PERIODS}

A: n={N_A}, d={D_A_NM} nm
B: n={N_B}, d={D_B_NM} nm
Defect: d={D_DEFECT_NM} nm
"""
    (RESULTS / "summary.txt").write_text(text, encoding="utf-8")


def main():
    print("Running photonic crystal sensor simulation...")

    resonance_wl, resonance_T = plot_baseline_spectrum()
    df = sweep_refractive_index()
    plot_resonance_shift(df)
    sensitivity, intercept, r2 = sensitivity_analysis(df)
    save_summary(resonance_wl, resonance_T, sensitivity, r2)

    print("\n--- BASELINE RESULTS ---")
    print(f"Resonance wavelength : {resonance_wl:.3f} nm")
    print(f"Peak transmission    : {resonance_T:.4f}")
    print(f"Sensitivity          : {sensitivity:.3f} nm/RIU")
    print(f"R^2                  : {r2:.6f}")
    print(f"\nResults saved to: {RESULTS}")


if __name__ == "__main__":
    main()
