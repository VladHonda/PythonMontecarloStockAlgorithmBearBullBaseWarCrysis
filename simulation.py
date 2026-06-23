import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# CONFIG
# ==========================================================

DAYS = 365
SEEDS = 2000
INITIAL = 1000
N_FACTORS = 7

weights = np.array([0.28, 0.16, 0.12, 0.10, 0.12, 0.12, 0.10], dtype=np.float32)
weights /= weights.sum()

# ==========================================================
# REGIMES
# ==========================================================

REGIMES = {
    0: ("bull",   0.00095, 0.0062),
    1: ("normal", 0.00050, 0.0080),
    2: ("bear",  -0.00060, 0.0115),
    3: ("crisis", -0.0023, 0.0195)
}

TRANSITION = np.array([
    [0.90, 0.07, 0.02, 0.01],
    [0.06, 0.86, 0.07, 0.01],
    [0.03, 0.11, 0.81, 0.05],
    [0.05, 0.16, 0.24, 0.55]
], dtype=np.float32)

# ==========================================================
# CORRELATION
# ==========================================================

BASE_CORR = np.array([
    [1.00, 0.38, 0.22, 0.32, 0.37, -0.18, 0.28],
    [0.38, 1.00, 0.27, 0.22, 0.12,  0.02, 0.12],
    [0.22, 0.27, 1.00, 0.28, 0.22,  0.08, 0.18],
    [0.32, 0.22, 0.28, 1.00, 0.28, -0.08, 0.35],
    [0.37, 0.12, 0.22, 0.28, 1.00, -0.12, 0.22],
    [-0.18,0.02, 0.08,-0.08,-0.12, 1.00,-0.10],
    [0.28, 0.12, 0.18, 0.35, 0.22, -0.10, 1.00]
], dtype=np.float32)

def make_psd(A):
    A = (A + A.T) / 2
    eigvals, eigvecs = np.linalg.eigh(A)
    eigvals = np.clip(eigvals, 1e-6, None)
    return eigvecs @ np.diag(eigvals) @ eigvecs.T

L_BASE = np.linalg.cholesky(make_psd(BASE_CORR))
L_CRISIS = np.linalg.cholesky(make_psd(BASE_CORR * 1.32))

# ==========================================================
# HELPERS
# ==========================================================

def build_regime_path(days):
    states = np.zeros(days, dtype=np.int32)
    for t in range(1, days):
        states[t] = np.random.choice(4, p=TRANSITION[states[t-1]])
    return states

def student_t(shape, df=6.5):
    z = np.random.normal(size=shape)
    g = np.random.chisquare(df, size=shape)
    return z / np.sqrt(g / df)

def black_swan(days):
    shock = np.zeros(days)
    if np.random.rand() < 0.04:
        start = np.random.randint(35, days - 30)
        mag = np.random.uniform(-0.20, 0.16)
        dur = np.random.randint(4, 8)
        # ramp pentru netezire
        ramp = np.linspace(0.5, 1.0, dur)
        shock[start:start+dur] = mag * ramp
    return shock

def structural_shift(days):
    effect = np.zeros((days, N_FACTORS))
    if np.random.rand() < 0.22:
        t0 = np.random.randint(80, 290)
        effect[t0:, 0] -= 0.00040
        effect[t0:, 3] += 0.00017
        effect[t0:, 4] += 0.00010
    return effect

# ==========================================================
# SIMULATION
# ==========================================================

def simulate():
    states = build_regime_path(DAYS)
    means = np.array([REGIMES[s][1] for s in states])
    vols  = np.array([REGIMES[s][2] for s in states])

    shocks = student_t((SEEDS, DAYS, N_FACTORS))
    factor_returns = np.zeros_like(shocks)

    for t in range(DAYS):
        L = L_CRISIS if states[t] == 3 else L_BASE
        factor_returns[:, t, :] = shocks[:, t, :] @ L.T

    factor_returns = factor_returns * vols[None, :, None] + means[None, :, None]

    # Persistență moderată
    for t in range(1, DAYS):
        factor_returns[:, t, :] += 0.055 * factor_returns[:, t-1, :]

    # Evenimente rare
    factor_returns += black_swan(DAYS)[None, :, None]
    factor_returns += structural_shift(DAYS)

    # Crashes rare și moderate
    crash_mask = np.random.rand(SEEDS, DAYS) < 0.0011
    crash_size = np.random.uniform(-0.11, -0.045, (SEEDS, DAYS))
    factor_returns += crash_mask[:, :, None] * crash_size[:, :, None]

    # Portfolio return
    port_ret = factor_returns @ weights
    
    # Limitare realistă (max ~2.2% pe zi)
    port_ret = np.clip(port_ret, -0.022, 0.022)

    values = INITIAL * np.exp(np.cumsum(port_ret, axis=1))
    return values


# ==========================================================
# RUN & PLOT
# ==========================================================

np.random.seed(None)        # ← important: random la fiecare run
values = simulate()

final = values[:, -1]
mean_path = values.mean(axis=0)
p5  = np.percentile(values, 5, axis=0)
p95 = np.percentile(values, 95, axis=0)

plt.figure(figsize=(13, 7))

for path in values[:110]:
    plt.plot(path, color="gray", alpha=0.065)

plt.plot(mean_path, color="#1f77b4", linewidth=3, label="Mean Path")
plt.fill_between(range(DAYS), p5, p95, color="#1f77b4", alpha=0.20, label="5% – 95% band")

title = (f"Start: {INITIAL:,} | Mean Final: {mean_path[-1]:,.0f} | "
         f"Median: {np.median(final):,.0f} | "
         f"Worst: {final.min():,.0f} | Best: {final.max():,.0f}")

plt.title("Portfolio Simulation - Balanced Regime Switching", fontsize=14)
plt.xlabel("Days")
plt.ylabel("Portfolio Value")
plt.legend(title=title, loc="upper left")
plt.grid(True, alpha=0.3)

plt.show()

# Console stats
print(f"Mean Final     : {mean_path[-1]:.0f}")
print(f"Median Final   : {np.median(final):.0f}")
print(f"5th percentile : {p5[-1]:.0f}")
print(f"95th percentile: {p95[-1]:.0f}")
print(f"Worst          : {final.min():.0f}")
print(f"Best           : {final.max():.0f}")
