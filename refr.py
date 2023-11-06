

single_col_factors = ['momentum', 'st_rev', 'lt_rev']


benchmarks = {'Indices' : {'SP-500' : '^GSPC',
                           'Nasdaq' : '^IXIC',
                           'Dow Jones' : '^DJI',
                           'Russell 2000' : '^RUT',
                           'FTSE 100' : '^FTSE', 
                           'Nikkei 225' : '^N225'},
              }


#Operating Profitability' : {'Monthly' : 'Portfolios_Formed_on_OP'},
available_franch_factors = {'Size' : {'Monthly' : 'Portfolios_Formed_on_ME',
                               'Daily' : 'Portfolios_Formed_on_ME_Daily'},
                     'Value' : {'Monthly' : 'Portfolios_Formed_on_BE-ME',
                                'Daily' : 'Portfolios_Formed_on_BE-ME_Daily'},
                     'Momentum' : {'Monthly' : 'F-F_Momentum_Factor',
                                   'Daily' : 'F-F_Momentum_Factor_daily'},
                     'Short Term Reversal' : {'Monthly' :'F-F_ST_Reversal_Factor',
                                 'Daily' : 'F-F_ST_Reversal_Factor_daily'},
                     'Long Term Reversal' : {'Monthly' : 'F-F_LT_Reversal_Factor',
                                 'Daily' : 'F-F_LT_Reversal_Factor_daily'},
                     'Earnings per Share' : {'Monthly' : 'Portfolios_Formed_on_E-P'},
                     'Investment' : {'Monthly' : 'Portfolios_Formed_on_INV'},
                     'Cash Flow to Price' : {'Monthly' : 'Portfolios_Formed_on_CF-P'},
                     'Residual Variance' : {'Monthly' :'Portfolios_Formed_on_RESVAR'},
                     'Variance' : {'Monthly' :'Portfolios_Formed_on_VAR'},
                     'Beta' : {'Monthly' : 'Portfolios_Formed_on_BETA'},
                     'Accruals' : {'Monthly' : 'Portfolios_Formed_on_AC'},
                     'Net Shares Issued' : {'Monthly' : 'Portfolios_Formed_on_NI'},
                     'Industry' : {'Monthly' : '49_Industry_Portfolios',
                                   'Daily' : '49_Industry_Portfolios_daily'}
                    }


fred_data = {
    'Index' : {'Market Price' : {'symbol' : 'SP500', 'freq' : 'D'}},
    'Volatility': {'VIX': {'symbol': 'VIXCLS', 'freq': 'D'},
  'Market Vol': {'symbol': 'VXVCLS', 'freq': 'D'},
  'Oil Vol': {'symbol': 'OVXCLS', 'freq': 'D'},
  'Small Cap Vol': {'symbol': 'RVXCLS', 'freq': 'D'}},
 'Real Rates': {'10-Year Real Rate': {'symbol': 'DFII10', 'freq': 'D'},
  '5-Year Real Rate': {'symbol': 'DFII5', 'freq': 'D'},
  '7-Year Real Rate': {'symbol': 'DFII7', 'freq': 'D'},
  '20-Year Real Rate': {'symbol': 'DFII20', 'freq': 'D'},
  '30-Year Real Rate': {'symbol': 'DFII30', 'freq': 'D'}},
 'Inflation': {'10Y_inflation': {'symbol': 'T10YIE', 'freq': 'D'},
  '5Y Inflation': {'symbol': 'T5YIE', 'freq': 'D'},
  '5_5 Forward Inflation': {'symbol': 'T5YIFR', 'freq': 'D'},
  'CPI': {'symbol': 'MEDCPIM158SFRBCLE', 'freq': 'M'},
  'BAA_to_10Y': {'symbol': 'BAA10Y', 'freq': 'D'}},
 'Yield Curves': {'10Y-2Y': {'symbol': 'T10Y2Y', 'freq': 'D'},
  '10Y-3M': {'symbol': 'T10Y3M', 'freq': 'D'}},
 'currency': {'US Dollar index': {'symbol': 'DTWEXBGS', 'freq': 'D'},
  'USD_aboard_index': {'symbol': 'DTWEXAFEGS', 'freq': 'D'},
  'USD_Emerging_Mkt_index': {'symbol': 'DTWEXEMEGS', 'freq': 'D'},
  'USD_to_Euro_spot': {'symbol': 'DEXUSEU', 'freq': 'D'},
  'USD_to_Yuan_spot': {'symbol': 'DEXCHUS', 'freq': 'D'},
  'USD_to_Yen_spot': {'symbol': 'DEXJPUS', 'freq': 'D'},
  'USD_to_Canadian_spot': {'symbol': 'DEXCAUS', 'freq': 'D'},
  'USD_to_Won_spot': {'symbol': 'DEXKOUS', 'freq': 'D'},
  'USD_to_pound_spot': {'symbol': 'DEXUSUK', 'freq': 'D'},
  'USD_to_Rupee': {'symbol': 'DEXINUS', 'freq': 'D'}},
 'Money Velocity': {'M1_velocity': {'symbol': 'M1V', 'freq': 'Q'},
  'M2_velocity': {'symbol': 'M2V', 'freq': 'Q'}},
 'Employment': {'Labor Market Index': {'symbol': 'FRBKCLMCIM', 'freq': 'M'},
  'US Job Postings Indeed': {'symbol': 'IHLCHGUS', 'freq': 'D'},
  'Unemployment Rate': {'symbol': 'UNRATE', 'freq': 'M'}},
 'Trade': {'US_Exports': {'symbol': 'IEAXGS', 'freq': 'Q'},
  'US Imports': {'symbol': 'IEAMGSN', 'freq': 'Q'},
  'US International Investment': {'symbol': 'IIPUSNETIQ', 'freq': 'Q'},
  'US Assets': {'symbol': 'IIPPORTAQ', 'freq': 'Q'},
  'US Financial Darivatives Less Reserves': {'symbol': 'IIPFINANCNQ',
   'freq': 'Q'},
  'US Trade Balance': {'symbol': 'BOPGSTB', 'freq': 'M'}},
 'Commodities': {'US Oil': {'symbol': 'DCOILWTICO', 'freq': 'D'},
  'EU Oil': {'symbol': 'DCOILBRENTEU', 'freq': 'D'},
  'US Gas Prices': {'symbol': 'GASREGW', 'freq': 'D'},
  'Global Energy': {'symbol': 'PNRGINDEXM', 'freq': 'M'},
  'Global Wheat': {'symbol': 'PWHEAMTUSDM', 'freq': 'M'},
  'Global Raw Material': {'symbol': 'PRAWMINDEXM', 'freq': 'M'},
  'Global Copper': {'symbol': 'PCOPPUSDM', 'freq': 'M'}},
 'Producer Price Index': {'Commodities': {'symbol': 'PPIACO', 'freq': 'M'},
  'Manufaturing': {'symbol': 'PCUOMFGOMFG', 'freq': 'M'},
  'Transportation': {'symbol': 'PCUATRANSATRANS', 'freq': 'M'},
  'Retail': {'symbol': 'PCUARETTRARETTR', 'freq': 'M'},
  'Wholesale': {'symbol': 'PCUAWHLTRAWHLTR', 'freq': 'M'},
  'Mining': {'symbol': 'PCUOMINOMIN', 'freq': 'M'}},
 'Crypto': {'BTC': {'symbol': 'CBBTCUSD', 'freq': 'D'},
  'ETH': {'symbol': 'CBETHUSD', 'freq': 'D'},
  'LTC': {'symbol': 'CBLTCUSD', 'freq': 'D'}},
 'Uncertainty': {'US Economic Uncertainty': {'symbol': 'USEPUINDXD',
   'freq': 'D'},
  'Equity Related Uncertainty': {'symbol': 'WLEMUINDXD', 'freq': 'D'},
  'GDP Uncertainty': {'symbol': 'GEPUCURRENT', 'freq': 'M'}},
 'GDP': {'Real Gross GDP': {'symbol': 'GDPC1', 'freq': 'Q'},
  'US GDP': {'symbol': 'GDP', 'freq': 'Q'},
  'Real Gross GDP per capita': {'symbol': 'A939RX0Q048SBEA', 'freq': 'Q'},
  'Japan GDP': {'symbol': 'JPNRGDPEXP', 'freq': 'Q'}}}



# == 'D'
daily_macro_options = [
                    f"{key} - {sub_key}" for
                    key in fred_data 
                    for sub_key in fred_data[key]
                    if fred_data[key][sub_key]['freq'] in ['D', 'M']
                    ]

