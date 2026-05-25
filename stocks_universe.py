import re

def parse_tags(tag_string):
    return re.findall(r"#uber[^\s]+", tag_string)

def get_stock_universe():
    return parse_tags("""
        # --- DEFENSE ---
        #uberONDS #uberKratos #uberJEDI #uberAVAV #uberDRNZ
        #uberLockheedMartin #uberNorthropGrumman #uberRaytheon
        #uberGeneralDynamics #uberBAESystems #uberBoeing
        #uberThales #uberPalantir #uberSpaceX
        #uberSkunkWorks #uberPratt&Whitney #uberHoneywell

        # --- AI & SEMIS & TECH ---
        #uberC3.ai #uberSnowflake #uberElasticNV #uberSalesforce 
        #uberTwilio #uberUiPath #uberMeta #uberGoogle #uberMicrosoft 
        #uberIBM #uberxAi #uberRiot #uberNvidia #uberAmd #uberIntel
        #uberBroadcom #uberQualcomm #uberTexasInstruments #uberDell 
        #uberLenovo #uberAsus #uberGigabyte #uberMSI #uberCorsair
        #uberEVGA #uberHyperX #uberSamsung #uberSony #uberToshiba 
        #uberAdata #uberApple #uberArista #uberGLW #uberIsharesNasdaq100UCITS 
        #uberIsharesS&P500InformationTechnologySector

        # --- AUTO ---
        #uberTesla #uberLucid #uberBMW #uberMercedes #uberAudi 
        #uberPorsche #uberFerrari #uberLamborghini #uberToyota #uberHonda 
        #uberHyundai #uberVolvo #uberVW #uberRenault #uberSkoda 
        #uberFord #uberMazda #uberJaguar #uberDacia #uberKgMobility 
        #uberLynk&Co #uberUber

        # --- CONSUMER STAPLES ---
        #uberNestlé #uberProcter&Gamble #uberCostco #uberWalmart
        #uberCoca-Cola #uberPepsiCo #uberUnilever #uberMondelez
        #uberPhilipMorris #uberDiageo #uberL'Oréal
        #uberXtrackersMSCUSAConsumerStaples #uberInvescoUSConsumerStaplesSector
        #uberIsharesMSCIEuropeConsumerStaples #uberXtrackersMSCIEuropeConsumerStaplesScreened
        #uberXtrackersMSCIWorldConsumerStaples #uberIsharesSTOXXEurope600Food&Beverages

        # --- ENERGY ---
        #uberChevron #uberExxonMobil #uberShell #uberSiemens 
        #uberSiemensEnergy #uberSchneiderElectric #uberGeneralElectric
        #uberBASFSE #uberHidroelectrica #uberIsharesSTOXXEurope600Oil&Gas 
        #uberXtrackersSTOXXEurope600Oil&Gas #uberIsharesOil&GasE&PUCITS 
        #uberSPDRS&PUSEnergySelectSectorUCITS #uberSPDRMSCIEuropeEnergyUCITS

        # --- FINANCE & BANKS ---
        #uberBlackRock #uberVanguard #uberFidelity #uberGoldmanSachs 
        #uberJPMorgan #uberMorganStanley #uberCharlesSchwab
        #uberFranklinResourcesInc #uberFondulProprietateaSA
        #uberLyxorSTOXXEurope600Banks #uberIsharesEUROSTOXXBanks

        # --- PLATFORMS & BIOTECH & REGIONS ---
        #uberAmazon #uberAlibaba #uberTenCent #uberAirbnb 
        #uberFiverrInternationalLtd #uberUpworkInc #uberNovoNordisk 
        #uberVertex #uberUnitedTherapeutics #uberAlibabaBABA 
        #uberChengdu #uberShenyang

        # --- METALS & PRECIOUS METALS ---
        #uberUnitedStatesSteelCorporationX #uberGhoryanMine #uberGmkNorilskNickel
        #uberIsharesPhysicalGoldETC #uberAmundiPhysicalGoldETC
        #uberVanEckGoldMinersUCITSETF #uberVanEckJuniorGoldMinersUCITS

        # --- REITS, TREASURY & EMERGING MARKETS ---
        #uberIsharesDevelopedMarketsPropertyYield #uberIsharesEuropeanPropertyYield
        #uberIsharesUSDTreasuryBond20+YearUCITS #uberIsharesCoreMSCIEMIMI 
        #uberVanEckEmergingMarketsUCITS
    """)
