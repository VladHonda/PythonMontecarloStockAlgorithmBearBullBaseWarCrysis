import numpy as np
import matplotlib.pyplot as plt
import re

# ----------------------------
# Clean tag parser (IMPORTANT FIX)
# ----------------------------
def parse_tags(tag_string):
    return re.findall(r"#uber[^\s]+", tag_string)


# ----------------------------
# Investment tags
# ----------------------------
investment_tags_defense = parse_tags("""
#uberONDS #uberKratos #uberJEDI #uberAVAV
#uberLockheedMartin #uberNorthropGrumman #uberRaytheon
#uberGeneralDynamics #uberBAESystems #uberBoeing
#uberThales #uberPalantir #uberSpaceX
#uberSkunkWorks #uberPratt&Whitney #uberHoneywell
""")

investment_tags_ai = parse_tags("""
#uberC3.ai #uberSnowflake #uberElasticNV
#uberSalesforce #uberTwilio #uberUiPath
#uberMeta #uberGoogle #uberMicrosoft
#uberIBM #uberxAi #uberRiot
""")

investment_tags_semis = parse_tags("""
#uberNvidia #uberAmd #uberIntel
#uberBroadcom #uberQualcomm #uberTexasInstruments
#uberDell #uberLenovo #uberAsus
#uberGigabyte #uberMSI #uberCorsair
#uberEVGA #uberHyperX #uberSamsung
#uberSony #uberToshiba #uberAdata
#uberApple #uberArista #uberGLW
""")

investment_tags_auto = parse_tags("""
#uberTesla #uberLucid #uberBMW
#uberMercedes #uberAudi #uberPorsche
#uberFerrari #uberLamborghini #uberToyota
#uberHonda #uberHyundai #uberVolvo
#uberVW #uberRenault #uberSkoda
#uberFord #uberMazda #uberJaguar
#uberDacia #uberKgMobility #uberLynk&Co
#uberUber
""")

investment_tags_energy = parse_tags("""
#uberChevron #uberExxonMobil #uberShell
#uberSiemens #uberSiemensEnergy
#uberSchneiderElectric #uberGeneralElectric
#uberBASFSE #uberHidroelectrica
#uberGhoryanMine #uberGmkNorilskNickel
""")

investment_tags_finance = parse_tags("""
#uberBlackRock #uberVanguard #uberFidelity
#uberGoldmanSachs #uberJPMorgan
#uberMorganStanley #uberCharlesSchwab
#uberFranklinResourcesInc #uberFondulProprietateaSA
""")

investment_tags_platforms = parse_tags("""
#uberAmazon #uberAlibaba #uberTenCent
#uberAirbnb #uberFiverrInternationalLtd
#uberUpworkInc
""")

investment_tags_biotech = parse_tags("""
#uberNovoNordisk #uberVertex
#uberUnitedTherapeutics
""")

investment_tags_regions = parse_tags("""
#uberChengdu #uberShenyang
""")

investment_tags_misc = parse_tags("""
#uberX
""")


# ----------------------------
# Combined assets
# ----------------------------
investment_tags = (
    investment_tags_defense +
    investment_tags_ai +
    investment_tags_semis +
    investment_tags_auto +
    investment_tags_energy +
    investment_tags_finance +
    investment_tags_platforms +
    investment_tags_biotech +
    investment_tags_regions +
    investment_tags_misc
)

all_assets = [tag.replace("#uber", "") for tag in investment_tags]
num_assets_total = len(all_assets)

# ----------------------------
# Simulation params
# ----------------------------
days = 365
initial_investment = 1000
num_seeds = 500  # reduced for speed

scenarios = {
    "Bear": {
        "mean": (-0.0010, -0.0002),
        "vol": (0.015, 0.035)
    },
    "Base": {
        "mean": (0.00015, 0.00045),
        "vol": (0.010, 0.020)
    },
    "Bull": {
        "mean": (0.0006, 0.0015),
        "vol": (0.008, 0.018)
    },
    "War / Crisis": {
        "mean": (-0.0020, -0.0005),
        "vol": (0.025, 0.05)
    }
}

results = {}

# ----------------------------
# Simulation
# ----------------------------
for scenario_name, params in scenarios.items():
    portfolio_matrix = np.zeros((num_seeds, days))

    for seed in range(num_seeds):
        rng = np.random.RandomState(seed)

        mean_returns = rng.uniform(
            params["mean"][0],
            params["mean"][1],
            size=num_assets_total
        )

        vol = rng.uniform(
            params["vol"][0],
            params["vol"][1],
            size=num_assets_total
        )

        weights = rng.dirichlet(np.ones(num_assets_total))

        # log-return model (more stable than (1+r))
        returns = rng.normal(mean_returns, vol, size=(days, num_assets_total))
        cumulative = np.exp(np.cumsum(returns, axis=0))

        portfolio_values = initial_investment * (cumulative @ weights)
        portfolio_matrix[seed] = portfolio_values

    results[scenario_name] = portfolio_matrix.mean(axis=0)

# ----------------------------
# Results
# ----------------------------
for scenario_name, values in results.items():
    final_value = values[-1]
    final_return = (final_value / initial_investment - 1) * 100
    print(f"{scenario_name}: ${final_value:.2f} ({final_return:.2f}%)")

# ----------------------------
# Plot
# ----------------------------
plt.figure(figsize=(12, 6))

for scenario_name, values in results.items():
    plt.plot(values, label=scenario_name)

plt.title("Portfolio Monte Carlo Simulation (All Scenarios)")
plt.xlabel("Days")
plt.ylabel("Portfolio Value ($)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
