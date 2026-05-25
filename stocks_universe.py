import re

def parse_tags(tag_string):
    return re.findall(r"#uber[^\s]+", tag_string)


def get_stock_universe():

      
    defense_stocks = parse_tags("""
    #uberONDS #uberKratos #uberJEDI #uberAVAV #uberDRNZ
    #uberLockheedMartin #uberNorthropGrumman #uberRaytheon
    #uberGeneralDynamics #uberBAESystems #uberBoeing
    #uberThales #uberPalantir #uberSpaceX
    #uberSkunkWorks #uberPratt&Whitney #uberHoneywell
    """)

    ai_stocks = parse_tags("""
    #uberC3.ai #uberSnowflake #uberElasticNV
    #uberSalesforce #uberTwilio #uberUiPath
    #uberMeta #uberGoogle #uberMicrosoft
    #uberIBM #uberxAi #uberRiot
    """)

    semis_stocks = parse_tags("""
    #uberNvidia #uberAmd #uberIntel
    #uberBroadcom #uberQualcomm #uberTexasInstruments
    #uberDell #uberLenovo #uberAsus
    #uberGigabyte #uberMSI #uberCorsair
    #uberEVGA #uberHyperX #uberSamsung
    #uberSony #uberToshiba #uberAdata
    #uberApple #uberArista #uberGLW
    """)

    auto_stocks = parse_tags("""
    #uberTesla #uberLucid #uberBMW
    #uberMercedes #uberAudi #uberPorsche
    #uberFerrari #uberLamborghini #uberToyota
    #uberHonda #uberHyundai #uberVolvo
    #uberVW #uberRenault #uberSkoda
    #uberFord #uberMazda #uberJaguar
    #uberDacia #uberKgMobility #uberLynk&Co
    #uberUber
    """)

    consumer_staples_stocks = parse_tags("""
    #uberNestlé #uberProcter&Gamble #uberCostco #uberWalmart
    #uberCoca-Cola #uberPepsiCo #uberUnilever #uberMondelez
    #uberPhilipMorris #uberDiageo #uberL'Oréal
    """)

    consumer_staples_etfs = parse_tags("""
    #uberXtrackersMSCUSAConsumerStaples #uberInvescoUSConsumerStaplesSector
    #uberiSharesMSCIEuropeConsumerStaples #uberXtrackersMSCIEuropeConsumerStaplesScreened
    #uberXtrackersMSCIWorldConsumerStaples #uberiSharesSTOXXEurope600Food&Beverages
    """)

    energy_etfs = parse_tags("""
    #uberiSharesSTOXXEurope600Oil&Gas #uberXtrackersSTOXXEurope600Oil&Gas
    #uberiSharesOil&GasE&PUCITS #uberSPDRS&PUSEnergySelectSectorUCITS
    #uberSPDRMSCIEuropeEnergyUCITS
    """)
    
    energy_stocks = parse_tags("""
    #uberChevron #uberExxonMobil #uberShell
    #uberSiemens #uberSiemensEnergy
    #uberSchneiderElectric #uberGeneralElectric
    #uberBASFSE #uberHidroelectrica
    """)

    finance_stocks = parse_tags("""
    #uberBlackRock #uberVanguard #uberFidelity
    #uberGoldmanSachs #uberJPMorgan
    #uberMorganStanley #uberCharlesSchwab
    #uberFranklinResourcesInc #uberFondulProprietateaSA
    """)

    platform_stocks = parse_tags("""
    #uberAmazon #uberAlibaba #uberTenCent
    #uberAirbnb #uberFiverrInternationalLtd
    #uberUpworkInc
    """)

    biotech_stocks = parse_tags("""
    #uberNovoNordisk #uberVertex
    #uberUnitedTherapeutics
    """)

    region_stocks = parse_tags("""
    #uberAlibabaBABA #uberChengdu #uberShenyang
    """)

    metal_stocks = parse_tags("""
    #uberUnitedStatesSteelCorporationX #uberGhoryanMine #uberGmkNorilskNickel
    """)

    precious_metals_etfs = parse_tags("""
    #uberiSharesPhysicalGoldETC #uberAmundiPhysicalGoldETC
    #uberVanEckGoldMinersUCITSETF #uberVanEckJuniorGoldMinersUCITS
    """)

    reits_etfs = parse_tags("""
    #uberiSharesDevelopedMarketsPropertyYield #uberiSharesEuropeanPropertyYield
    """)

    european_banks_etfs = parse_tags("""
    #uberLyxorSTOXXEurope600Banks #uberiSharesEUROSTOXXBanks
    """)

    us_treasury_etfs = parse_tags("""
    #uberiSharesUSDTreasuryBond20+YearUCITS
    """)

    quality_tech_etfs = parse_tags("""
    #uberiSharesNasdaq100UCITS #uberiSharesS&P500InformationTechnologySector
    """)

    emerging_markets_etfs = parse_tags("""
    #uberiSharesCoreMSCIEMIMI #uberVanEckEmergingMarketsUCITS
    """)


    return (
        defense_stocks +
        ai_stocks +
        semis_stocks +
        auto_stocks +
        energy_stocks +
        finance_stocks +
        platform_stocks +
        biotech_stocks +
        region_stocks +
        metal_stocks
    )
