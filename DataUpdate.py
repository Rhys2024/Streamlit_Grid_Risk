import pandas_datareader.data as web
import pandas as pd
import refr

import datetime
import json

start = datetime.datetime(2010, 1, 1)
end = datetime.date.today()


single_col = ['momentum', 'st_rev', 'lt_rev']

# 'OP' : {'monthly' : 'Portfolios_Formed_on_OP'},
available_franch_factors = {'size' : {'monthly' : 'Portfolios_Formed_on_ME',
                               'daily' : 'Portfolios_Formed_on_ME_Daily'},
                     'value' : {'monthly' : 'Portfolios_Formed_on_BE-ME',
                                'daily' : 'Portfolios_Formed_on_BE-ME_Daily'},
                     'momentum' : {'monthly' : 'F-F_Momentum_Factor',
                                   'daily' : 'F-F_Momentum_Factor_daily'},
                     'st_rev' : {'monthly' :'F-F_ST_Reversal_Factor',
                                 'daily' : 'F-F_ST_Reversal_Factor_daily'},
                     'lt_rev' : {'monthly' : 'F-F_LT_Reversal_Factor',
                                 'daily' : 'F-F_LT_Reversal_Factor_daily'},
                     'EPS' : {'monthly' : 'Portfolios_Formed_on_E-P'},
                     'investment' : {'monthly' : 'Portfolios_Formed_on_INV'},
                     'Cash_Flow_to_Price' : {'monthly' : 'Portfolios_Formed_on_CF-P'},
                     'residual_variance' : {'monthly' :'Portfolios_Formed_on_RESVAR'},
                     'variance' : {'monthly' :'Portfolios_Formed_on_VAR'},
                     'beta' : {'monthly' : 'Portfolios_Formed_on_BETA'},
                     'accruals' : {'monthly' : 'Portfolios_Formed_on_AC'},
                     'net_shares_issued' : {'monthly' : 'Portfolios_Formed_on_NI'},
                     'industry' : {'monthly' : '49_Industry_Portfolios',
                                   'daily' : '49_Industry_Portfolios_daily'}
                    }



# 'intial_claims' : 'W',
fred_freqs = {
    'volatility' : {'VIX' : 'D', 'market_vol' : 'D', 'oil_vol' : 'D', 'small_cap_vol' : 'D'},
    'real rates' : {'10Y_real_rate' : 'D', '5Y_real_rate' : 'D', '7Y_real_rate' : 'D', 
                    '20Y_real_rate' : 'D', '30Y_real_rate' : 'D'},
    'inflation' : {'10Y_inflation' : 'D', '5Y_inflation' : 'D', '5_5_forward_inflation' : 'D',
                   'cpi' : 'M', 'BAA_to_10Y' : 'D'},
    'yield curves' : {'10Y_2Y' : 'D', '10Y_3M' : 'D'},
    'currency' : {'USD_index' : 'D', 'USD_aboard_index' : 'D' , 
                  'USD_Emerging_Mkt_index' : 'D', 'USD_to_Euro_spot' : 'D', 
                  'USD_to_Yuan_spot' : 'D', 'USD_to_Yen_spot' : 'D', 
                  'USD_to_Canadian_spot' : 'D', 'USD_to_Won_spot' : 'D', 
                  'USD_to_pound_spot' : 'D', 'USD_to_Rupee' : 'D'},
    'money velocity' : {'M1_velocity' : 'Q', 'M2_velocity' : 'Q'},
    'employment' : { 'labor_market_index' : 'M', 
                    'US_job_postings_Indeed' : 'D', 'unemployment_rate' : 'M'},
    'trade' : {'US_Exports' : 'Q', 'US_Imports' : 'Q', 'US_international_investment' : 'Q',
               'US_Assets' : 'Q', 'US_Financial_Darivatives_less_reserves' : 'Q', 
               'US_Trade_Balance' : 'M'},
    'commodities' : {'US_oil' : 'D', 'EU_oil' : 'D', 'US_Gas_Prices' : 'D',
                     'Global_Energy_Index' : 'M', 'Global_Wheat_Price' : 'M', 
                     'Global_Raw_Material_Price' : 'M', 'Global_Copper_Price' : 'M'},
    'crypto' : {'BTC' : 'D', 'ETH' : 'D', 'LTC' : 'D'},
    'uncertainty' : {'US_economic_uncertainty' : 'D', 
                     'equity_related_uncertainty' : 'D',
                     'GDP_uncertainty' : 'M'},
    'GDP' : {'Real_Gross_GDP' : 'Q', 'US_GDP' : 'Q', 
             'Real_Gross_GDP_per_capita' : 'Q',
             'Japan_GDP' : 'Q'}
}


# 'intial_claims' : 'IC4WSA', 
fred_data = {
    'volatility' : {'VIX' : 'VIXCLS', 'market_vol' : 'VXVCLS', 'oil_vol' : 'OVXCLS', 'small_cap_vol' : 'RVXCLS'},
    'real rates' : {'10Y_real_rate' : 'DFII10', '5Y_real_rate' : 'DFII5', '7Y_real_rate' : 'DFII7', 
                    '20Y_real_rate' : 'DFII20', '30Y_real_rate' : 'DFII30'},
    'inflation' : {'10Y_inflation' : 'T10YIE', '5Y_inflation' : 'T5YIE', '5_5_forward_inflation' : 'T5YIFR',
                   'cpi' : 'MEDCPIM158SFRBCLE', 'BAA_to_10Y' : 'BAA10Y'},
    'yield curves' : {'10Y_2Y' : 'T10Y2Y', '10Y_3M' : 'T10Y3M'},
    'currency' : {'USD_index' : 'DTWEXBGS', 'USD_aboard_index' : 'DTWEXAFEGS' , 
                  'USD_Emerging_Mkt_index' : 'DTWEXEMEGS', 'USD_to_Euro_spot' : 'DEXUSEU', 
                  'USD_to_Yuan_spot' : 'DEXCHUS', 'USD_to_Yen_spot' : 'DEXJPUS', 
                  'USD_to_Canadian_spot' : 'DEXCAUS', 'USD_to_Won_spot' : 'DEXKOUS', 
                  'USD_to_pound_spot' : 'DEXUSUK', 'USD_to_Rupee' : 'DEXINUS'},
    'money velocity' : {'M1_velocity' : 'M1V', 'M2_velocity' : 'M2V'},
    'employment' : {'labor_market_index' : 'FRBKCLMCIM', 
                    'US_job_postings_Indeed' : 'IHLCHGUS', 'unemployment_rate' : 'UNRATE'},
    'trade' : {'US_Exports' : 'IEAXGS', 'US_Imports' : 'IEAMGSN', 'US_international_investment' : 'IIPUSNETIQ',
               'US_Assets' : 'IIPPORTAQ', 'US_Financial_Darivatives_less_reserves' : 'IIPFINANCNQ', 
               'US_Trade_Balance' : 'BOPGSTB'},
    'commodities' : {'US_oil' : 'DCOILWTICO', 'EU_oil' : 'DCOILBRENTEU', 'US_Gas_Prices' : 'GASREGW',
                     'Global_Energy_Index' : 'PNRGINDEXM', 'Global_Wheat_Price' : 'PWHEAMTUSDM', 
                     'Global_Raw_Material_Price' : 'PRAWMINDEXM', 'Global_Copper_Price' : 'PCOPPUSDM'},
    'crypto' : {'BTC' : 'CBBTCUSD', 'ETH' : 'CBETHUSD', 'LTC' : 'CBLTCUSD'},
    'uncertainty' : {'US_economic_uncertainty' : 'USEPUINDXD', 
                     'equity_related_uncertainty' : 'WLEMUINDXD',
                     'GDP_uncertainty' : 'GEPUCURRENT'},
    'GDP' : {'Real_Gross_GDP' : 'GDPC1', 'US_GDP' : 'GDP', 
             'Real_Gross_GDP_per_capita' : 'A939RX0Q048SBEA',
             'Japan_GDP' : 'JPNRGDPEXP'}
}


benchmarks = {'Indices' : {'SP-500' : '^GSPC',
                           'Nasdaq' : '^IXIC',
                           'Dow Jones' : '^DJI',
                           'Russell 2000' : '^RUT',
                           'FTSE 100' : '^FTSE', 
                           'Nikkei 225' : '^N225'},
              }



def verify_df(temp_data):
    
    assert temp_data.index.name == 'Date'
    #assert temp_data.isna()
    
    
    pass


fred_data_library  = {i : list(fred_data[i].keys()) for i in fred_data}


def update_factor_data(start = datetime.datetime(2010, 1, 1), 
                       end = datetime.date.today(), split = 'monthly'):
    
    fact_data = pd.DataFrame()

    for fact in refr.available_franch_factors:

        factor_dataset_name = available_franch_factors[fact][split]

        dataset = 0 if fact in single_col else 1
        
        subset = web.DataReader(factor_dataset_name, 'famafrench', start, end)[dataset]

        if fact not in single_col:
            fact_data[fact] = subset['Hi 30'] - subset['Lo 30']
        else:
            fact_data[fact] = subset[subset.columns[0]]

    fact_data = fact_data.dropna()
    
    return fact_data





def get_factor_data(factor, split = 'Daily', start = datetime.datetime(2010, 1, 1), 
                    end = datetime.date.today(), 
                    save_data=False, eq_weight = False):
    
    assert factor in refr.available_franch_factors, "factor must be in 'available_franch_factors'"
    
    refr_name = refr.available_franch_factors[factor][split]

    #start = pd.to_datetime(start)
    #end = pd.to_datetime(end)

    dataset = 0 if factor in single_col else 1

    if eq_weight:
        data_dict = web.DataReader(refr_name, 'famafrench', start, end)
        
        if len(data_dict) > 2:
            data = data_dict[1]
        else:
            data = data_dict[0]
    else:
        #  / 100
        data = web.DataReader(refr_name, 'famafrench', start, end)[0]
    
    if save_data:
        
        # Users/rhys/Desktop/grid_risk_management/
        if eq_weight:
            data.to_csv(f'data/{factor} - {split} - Equal-Weight.csv')
        else:
            data.to_csv(f'data/{factor} - {split}.csv')
        
        print(f'{factor} - {split} Data Saved!')

    
    return data


def get_fred_series(series_name, sub_category = None,
                    start = datetime.datetime(2010, 1, 1), 
                    end = datetime.date.today(), save_data=False):
    
    assert sub_category, 'must assign subcategory'
    assert isinstance(save_data, bool), "input 'save_data' must be a boolean"
    
    
    series = web.get_data_fred(refr.fred_data[series_name][sub_category]['symbol'], start, end)
    
    series.columns = [sub_category]
    series.index.name = 'Date'
    
    if save_data:
        #/Users/rhys/Desktop/grid_risk_management/
        series.to_csv(f'data/{series_name} - {sub_category}.csv')
        print(f'{series_name} - {sub_category} Data Saved!')
    
    return series


def update_factor_col_mapping():
    
    col_maps = {}
        
        
    for factor in refr.available_franch_factors:
        
        for split in refr.available_franch_factors[factor]:
            
            
            name = f'{factor} - {split}'
            
            # /Users/rhys/Desktop/grid_risk_management/
            temp_data = pd.read_csv(f'data/{name}.csv', 
                                    index_col='Date')
            
            if '<= 0' in temp_data.columns or '< 0' in temp_data.columns:
                
                drops = [col for col in temp_data.columns if '< 0' in col or '<= 0' in col]
                temp_data = temp_data.drop(columns=drops)
            
            col_maps[name] = list(temp_data.columns)
    
    with open("cols_for_factor.json", "w") as write_file:
        json.dump(col_maps, write_file, indent=4)


def FullUpdate(test=True):
    
    save_data = not test
    
    for key in refr.fred_data:
        print(key)
        for sub_key in refr.fred_data[key]:
            get_fred_series(key, sub_key, save_data=save_data)
    
    for factor in refr.available_franch_factors:
        
        print(factor)
        
        for split in refr.available_franch_factors[factor]:
            
            get_factor_data(factor, split, 
                            start='1926-01-04', 
                            end = '2023-11-03', 
                            save_data=save_data)
      
    update_factor_col_mapping()
    
    print('\n\nUpdate Complete!!\n\n')
    
    pass


def create_full_df():
    
    list_of_frames = []
    #cols_list = []
    
    for factor in refr.available_franch_factors:
        
        for split in refr.available_franch_factors[factor]:
            
            names = [f'{factor} - {split}', f'{factor} - {split} - Equal-Weight']
            
            for name in names:
            
                if 'Daily' in name:
                    
                    # /Users/rhys/Desktop/grid_risk_management/
                    
                    temp_data = pd.read_csv(f'data/{name}.csv', 
                                        index_col='Date', parse_dates=True) / 100
                    
                    #cols_list = []
                    
                    temp_data.columns = pd.MultiIndex.from_tuples([(name, col) for col in temp_data.columns])
                    
                    list_of_frames.append(temp_data)
    
    
    for key in refr.fred_data:
        for sub_key in refr.fred_data[key]:
            
            name = f'{key} - {sub_key}'
            
            #print(refr.fred_data[key][sub_key])
            
            if refr.fred_data[key][sub_key]['freq'] != 'D':
                continue
            
            # /Users/rhys/Desktop/grid_risk_management/
            temp_data = pd.read_csv(f'data/{name}.csv', 
                                    index_col='Date', parse_dates=True)
            
            #cols_list = []
            
            temp_data.columns = pd.MultiIndex.from_tuples([(name, col) for col in temp_data.columns])
            
            list_of_frames.append(temp_data)
    
    
    for key in benchmarks:
        
        for bench in benchmarks[key]:
            
            name = f'{key} - {bench}'
            
            # /Users/rhys/Desktop/grid_risk_management/
            temp_data = pd.read_csv(f'data/{name}.csv', 
                                    index_col='Date', parse_dates=True)
            
            #cols_list = []
            
            temp_data.columns = pd.MultiIndex.from_tuples([(name, col) for col in temp_data.columns])
            
            list_of_frames.append(temp_data)
    
    
    full_data = pd.concat(list_of_frames, 
                            axis = 1
                            ).sort_index() 
    
    full_data.index.names = ['Date']
    
    full_data.to_csv('/Users/rhys/Desktop/grid_risk_management/data/full_daily_data.csv', 
                     index=True, index_label='Date')
    


if __name__ == '__main__':
    
    import matplotlib.pyplot as plt
    
    poop = pd.read_csv('/Users/rhys/Desktop/grid_risk_management/data/full_daily_data.csv',
                          header=[0, 1],
                          index_col=0,
                          parse_dates=True)
    
    poop['Commodities - US Gas Prices']['US Gas Prices'].dropna().plot()
    
    plt.show()
    
    #pass
    