import numpy as np
import matplotlib.pyplot as plt
from stocks_universe import get_stock_universe

# ----------------------------
# Load universe
# ----------------------------
stocks_universe = get_stock_universe()

all_assets = [tag.replace("#uber", "") for tag in stocks_universe]
num_assets_total = len(all_assets)

# ----------------------------
# Simulation params
# ----------------------------
days = 365
initial_investment = 1000
num_seeds = 500

scenarios = {
    "Bear": {"mean": (-0.0010, -0.0002), "vol": (0.015, 0.035)},
    "Base": {"mean": (0.00015, 0.00045), "vol": (0.010, 0.020)},
    "Bull": {"mean": (0.0006, 0.0015), "vol": (0.008, 0.018)},
    "War / Crisis": {"mean": (-0.0020, -0.0005), "vol": (0.025, 0.05)}
}

results = {}

# ----------------------------
# Simulation engine
# ----------------------------
for scenario_name, params in scenarios.items():
    portfolio_matrix = np.zeros((num_seeds, days))

    for seed in range(num_seeds):
        rng = np.random.RandomState(seed)

        mean_returns = rng.uniform(*params["mean"], size=num_assets_total)
        vol = rng.uniform(*params["vol"], size=num_assets_total)

        weights = rng.dirichlet(np.ones(num_assets_total))

        returns = rng.normal(mean_returns, vol, size=(days, num_assets_total))

        portfolio_returns = returns @ weights
        portfolio_values = initial_investment * np.exp(np.cumsum(portfolio_returns))

        portfolio_matrix[seed] = portfolio_values

    results[scenario_name] = portfolio_matrix.mean(axis=0)

# ----------------------------
# Output
# ----------------------------
for k, v in results.items():
    print(f"{k}: ${v[-1]:.2f} ({(v[-1]/initial_investment - 1)*100:.2f}%)")

# ----------------------------
# Plot
# ----------------------------
plt.figure(figsize=(12, 6))

for k, v in results.items():
    plt.plot(v, label=k)

plt.title("Portfolio Monte Carlo Simulation")
plt.xlabel("Days")
plt.ylabel("Portfolio Value")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
