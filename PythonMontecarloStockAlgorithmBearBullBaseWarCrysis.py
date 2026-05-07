import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# Investment tags
# ----------------------------
investment_tags = """#uberAdata #uberAirbnb #uberAlibaba #uberAmd #uberAmazon #uberApple #uberArista #uberAsus #uberAudi #uberBAESystems #uberBASFSE #uberBlackRock
#uberBMW #uberBoeing #uberBroadcom #uberC3.ai #uberChengdu #uberCharlesSchwab #uberChevron #uberCorsair #uberDacia #uberDell
#uberElasticNV #uberEVGA #uberExxonMobil #uberFerrari #uberFidelity #uberFiverrInternationalLtd #uberFondulProprietateaSA
#uberFord #uberFranklinResourcesInc #uberGeneralDynamics #uberGeneralElectric #uberGhoryanMine #uberGigabyte #uberGmkNorilskNickel
#uberGoldmanSachs #uberGoogle #uberHidroelectrica #uberHonda #uberHoneywell #uberHyperX #uberHyundai #uberIBM #uberIntel
#uberJaguar #uberJPMorgan #uberKgMobility #uberLamborghini #uberLenovo #uberLockheedMartin #uberLucid #uberLynk&Co
#uberMazda #uberMercedes #uberMeta #uberMicrosoft #uberMorganStanley #uberMSI #uberNorthropGrumman #uberNovoNordisk #uberNvidia
#uberPalantir #uberPorsche #uberPratt&Whitney #uberQualcomm #uberRaytheon #uberRenault #uberRiot #uberSalesforce #uberSamsung
#uberSchneiderElectric #uberShell #uberShenyang #uberSiemens #uberSiemensEnergy #uberSkoda #uberSkunkWorks #uberSnowflake
#uberSony #uberTenCent #uberTesla #uberTexasInstruments #uberThales #uberToshiba #uberToyota #uberTwilio #uberUber
#uberUiPath #uberUnitedTherapeutics #uberUpworkInc #uberVanguard #uberVerisign #uberVertex #uberVolvo #uberVW #uberGLW #uberSpaceX #uberxAi #uberX #uberKratos #uberJEDI #uberAVAV""".replace("\n", " ").split()

all_assets = [tag.replace("#uber","") for tag in investment_tags]
num_assets_total = len(all_assets)

days = 365
initial_investment = 1000
num_seeds = 1000

# ----------------------------
# Scenario parameters
# ----------------------------
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
        "mean": (-0.0020, -0.0005),  # mostly negative returns
        "vol": (0.025, 0.05)         # very high volatility
    }
}

results = {}

for scenario_name, params in scenarios.items():
    portfolio_matrix = np.zeros((num_seeds, days))

    for seed in range(num_seeds):
        np.random.seed(seed)
        
        mean_returns = np.random.uniform(params["mean"][0], params["mean"][1], size=num_assets_total)
        std_devs = np.random.uniform(params["vol"][0], params["vol"][1], size=num_assets_total)
        
        weights = np.random.dirichlet(np.ones(num_assets_total))
        
        returns = np.random.normal(mean_returns, std_devs, size=(days, num_assets_total))
        cumulative_returns = (1 + returns).cumprod(axis=0)
        
        portfolio_values = initial_investment * (cumulative_returns @ weights)
        portfolio_matrix[seed] = portfolio_values

    results[scenario_name] = portfolio_matrix.mean(axis=0)

# ----------------------------
# Print final returns
# ----------------------------
for scenario_name, values in results.items():
    final_value = values[-1]
    final_return = (final_value / initial_investment - 1) * 100
    print(f"{scenario_name} scenario: ${final_value:.2f} ({final_return:.2f}%)")

# ----------------------------
# Plot all scenarios
# ----------------------------
plt.figure(figsize=(12, 6))
for scenario_name, values in results.items():
    plt.plot(values, label=scenario_name)
plt.title(f"Portfolio Monte Carlo Simulation: Bear / Base / Bull / War")
plt.xlabel("Days")
plt.ylabel("Portfolio Value ($)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
