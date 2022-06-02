from run_validation import run_validation
import json
import itertools
import pandas as pd

finished_props = [
    'VDN', 'VDC', 'VS', 'VSC', 'VM', 'VEX', 'VC', 'VA', 'P', 'PP', 'PC', 'RSS', 'IST', 'IIT', 'NVK', 'NVC', 'T',
    'TB', 'TC', 'TE', 'TM', 'TBN', 'TMN', 'TT', 'TR', 'NTC', 'NTD', 'NDC', 'CP', 'CPW', 'CPV', 'CPEH', 'CV',
    'CVW', 'HW', 'H', 'HTR', 'HSL', 'HTRW', 'HVP', 'HEX', 'HEXW', 'HP', 'HXM', 'HX', 'G', 'GEX', 'S', 'SEX',
    'LA', 'LB', 'LC', 'LAA', 'LAB', 'LAC', 'RLE', 'RVE', 'LEC', 'VTP', 'VPT', 'EH', 'ENT', 'EN', 'EHS', 'AP',
    'AC', 'MMS', 'MSS', 'MP', 'ER', 'ERX', 'EC', 'W', 'X', 'VOP', 'NOP', 'Z', 'VPA', 
    ]

fail_props = [
    'VDM', 'PUC', 'PX', 'PL', 'PU', 'PV', 'TPP', 'TL', 'TU', 'TPT', 'TX', 'TUC', 'CPA', 'CEX', 'CPEHW', 'CVV',
    'CS', 'CGM', 'HRX', 'HA', 'GP', 'GR', 'GA', 'UA', 'U', 'UV', 'LE', 'SA', 'SR', 'SP', 'SW', 'GRV', 'WB', 
    'WH', 'MPR', 'WL', 'MAS', 'ATM', 'MOL', 'STE', 'HRT', 'ZC', 'HT', 'KJ', 'KX', 'KP', 'VVE', 'NFL', 'WF', 
    'GT', 'TJT', 'LAR', 'HPT','RIX', 'PTV', 'KT', 'HRTS', 'PRTS'
    ]

props = [
    'VDN', 'VDM', 'VS', 'VSC', 'VM', 'VEX', 'VC', 'VA', 'P', 'PP', 'PC', 'RSS', 'IST', 'IIT', 'NVK', 'NVC', 'T',
    'VDC', 'PUC', 'TB', 'TC', 'TE', 'TM', 'TBN', 'TMN', 'TT', 'TR', 'NTC', 'NTD', 'NDC', 'CP', 'CPW', 'CPV',
    'PX', 'PL', 'PU', 'PV', 'TPP', 'TL', 'TU', 'TPT', 'TX', 'TUC', 'CPA', 'CEX', 'CPEH', 'CPEHW', 'CV', 'CVW',
    'CVV', 'CS', 'CGM', 'HW', 'H', 'HTR', 'HSL', 'HRX', 'HTRW', 'HVP', 'HA', 'HEX', 'HEXW', 'HP', 'HXM', 'HX', 'G',
    'GP', 'GR', 'GA', 'GEX', 'UA', 'U', 'UV', 'LE', 'S', 'SA', 'SEX', 'SR', 'SP', 'SW', 'LA', 'LB', 'LC', 'LAA',
    'LAB', 'LAC', 'RLE', 'RVE', 'LEC', 'VTP', 'VPT', 'EH', 'ENT', 'EN', 'EHS', 'AP', 'AC', 'GRV', 'WB', 'WH', 'MMS',
    'MSS', 'MP', 'MPR', 'ER', 'ERX', 'EC', 'WL', 'MAS', 'ATM', 'MOL', 'W', 'X', 'VOP', 'NOP', 'STE', 'HRT', 'Z',
    'ZC', 'VPA', 'HT', 'KJ', 'KX', 'KP', 'VVE', 'NFL', 'WF', 'GT', 'TJT', 'LAR', 'HPT', 'RIX', 'PTV', 'KT',
    'HRTS', 'PRTS'
    ]

finish_check = []
fail_check = []
full_error = {}
errors = {}
props = []
data_id = []
cit_id = []
data_vals = []
err_mess = []
err_tab = []
for a in finished_props:
    #try:
        validate = run_validation(a)
        errors = validate[0]
        props = validate[1]
        data_id = validate[2]
        cit_id = validate[3]
        data_vals = validate[4]
        err_mess = validate[5]
        full_error[a] = errors
        finish_check.append(a)
        for i,j,k,l,m in itertools.zip_longest(props, data_id, cit_id, data_vals, err_mess):
            err_tab.append({
                'Property': i,
                'Data Set ID': j,
                'Citation ID': k,
                'Data Value': l,
                'Error': m
            })
    #except json.decoder.JSONDecodeError:
        fail_check.append(a)
        
with open('Error_Folder/all_errors.json', 'w') as fp:
    json.dump(full_error, fp)



df = pd.DataFrame(err_tab)
df.to_csv('Error_Folder/error_tab.csv', index = False)