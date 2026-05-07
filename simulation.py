import numpy as np
import matplotlib.pyplot as plt

from stocks_universe import (
    stocks_universe,
    sector_groups
)

# ----------------------------
# Assets
# ----------------------------
all_assets = [
    tag.replace("#uber", "")
    for tag in stocks_universe
]

num_assets_total = len(all_assets)

# ----------------------------
# Build sector lookup
# ----------------------------
sector_map = {}

for sector_name, sector_assets in sector_groups.items():

    for tag in sector_assets:

        clean_name = tag.replace("#uber", "")

        sector_map[clean_name] = sector_name

# ----------------------------
# Simulation params
# ----------------------------
days = 365
initial_investment = 1000
num_seeds = 500

# ----------------------------
# Scenarios
# ----------------------------
scenarios = {
    "Bear": {"mean": (-0.0010, -0.0002), "vol": (0.015, 0.035), "sector_bias": {}},
    "Base": {"mean": (0.00015, 0.00045), "vol": (0.010, 0.020), "sector_bias": {}},
    "Bull": {"mean": (0.0006, 0.0015), "vol": (0.008, 0.018), "sector_bias": {}},
    "War / Crisis": {"mean": (-0.0020, -0.0005), "vol": (0.025, 0.05), "sector_bias": {"defense": +0.0010, "energy": +0.0005, "platform": -0.0007, "auto": -0.0005}},
    "Trump 2028": {"mean": (0.0003, 0.0010), "vol": (0.015, 0.035), "sector_bias": {"defense": +0.0010, "energy": +0.0007, "ai": +0.0005, "platform": -0.0004}}
}

results = {}

# ----------------------------
# Simulation engine
# ----------------------------
for scenario_name, params in scenarios.items():

    portfolio_matrix = np.zeros((num_seeds, days))

    for seed in range(num_seeds):

        rng = np.random.RandomState(seed)

        mean_returns = rng.uniform(
            *params["mean"],
            size=num_assets_total
        )

        # ----------------------------
        # Apply sector bias
        # ----------------------------
        for i, asset in enumerate(all_assets):

            sector = sector_map.get(asset, "misc")

            bias = params["sector_bias"].get(sector, 0)

            mean_returns[i] += bias

        vol = rng.uniform(
            *params["vol"],
            size=num_assets_total
        )

        weights = rng.dirichlet(
            np.ones(num_assets_total)
        )

        # ----------------------------
        # Asset returns
        # ----------------------------
        returns = rng.normal(
            mean_returns,
            vol,
            size=(days, num_assets_total)
        )

        # ----------------------------
        # Portfolio returns
        # ----------------------------
        portfolio_returns = returns @ weights

        # ----------------------------
        # Portfolio compounding
        # ----------------------------
        portfolio_values = (
            initial_investment *
            np.exp(np.cumsum(portfolio_returns))
        )

        portfolio_matrix[seed] = portfolio_values

    results[scenario_name] = portfolio_matrix.mean(axis=0)

# ----------------------------
# Output
# ----------------------------
for k, v in results.items():

    final_value = v[-1]

    final_return = (
        (final_value / initial_investment - 1) * 100
    )

    print(
        f"{k}: "
        f"${final_value:.2f} "
        f"({final_return:.2f}%)"
    )

# ----------------------------
# Plot
# ----------------------------
plt.figure(figsize=(14, 7))

for k, v in results.items():
    plt.plot(v, label=k)

plt.title("Portfolio Monte Carlo Simulation")
plt.xlabel("Days")
plt.ylabel("Portfolio Value ($)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
