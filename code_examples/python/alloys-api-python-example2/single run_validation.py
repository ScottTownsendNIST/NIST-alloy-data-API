import json

props = [
    'VDN', 'VDC', 'VS', 'VSC', 'VM', 'VEX', 'VC', 'VA', 'P', 'PP', 'PC', 'RSS', 'IST', 'IIT', 'NVK', 'NVC', 'T',
    'TB', 'TC', 'TE', 'TM', 'TBN', 'TMN', 'TT', 'TR', 'NTC', 'NTD', 'NDC', 'CP', 'CPW', 'CPV', 'CPEH', 'CV',
    'CVW', 'HW', 'H', 'HTR', 'HSL', 'HTRW', 'HVP', 'HEX', 'HEXW', 'HP', 'HXM', 'HX', 'G', 'GEX', 'S', 'SEX',
    'LA', 'LB', 'LC', 'LAA', 'LAB', 'LAC', 'RLE', 'RVE', 'LEC', 'VTP', 'VPT', 'EH', 'ENT', 'EN', 'EHS', 'AP',
    'AC', 'MMS', 'MSS', 'MP', 'ER', 'ERX', 'EC', 'W', 'X', 'VOP', 'NOP', 'Z', 'VPA', 
    ]

all_errors = {}

for a in props:
    with open(f'Error_Folder/{a}_errors.json', 'r') as fp:
        temp = json.load(fp)
    all_errors[a] = temp

with open(f'Error_Folder/all_errors.json', 'w') as fp:
    json.dump(all_errors, fp) 