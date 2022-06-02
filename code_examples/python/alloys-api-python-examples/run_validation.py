def run_validation(prop):
    import json
    import requests
    headers = {
        'content-type':'application/x-www-form-urlencoded;',
        'Access-Control-Allow-Origin':'*',
    }

    search_data = {"property_search_code":prop}
    api_key = open('D:/Bryan/Desktop/NIST/TRC-Alloys API Key.txt').read()
    url = f'http://trcsrv2.boulder.nist.gov/MetalsAlloyAPI/search?authkey={api_key}'
    compound_data_response = requests.post(url, json=search_data, headers=headers)
    import re

    with open('error_check.json', 'w') as fp:
        fp.write((re.sub(r'[^\x00-\x7f]',r'', compound_data_response.text)))

    with open('error_check.json') as json_file:
        data = json.load(json_file)

    from conversion_bridge import conversion_bridge
    from validation_bridge import validation_bridge

    temp_y = "N/A" # temporary value which houses variable ID for the property

    valid = {}
    props = []
    data_id = []
    cit_id = []
    data_vals = []
    err_mess = []

    for a in data['TRC_data']:
        for b in a['systems']: # system data tends to be the material compositions, so other aspects can vary within a system with each data set
            try:
                for c in b['data_sets']:
                    for v in c['variables']: # this section of the code is designated to identifying the variable and property for use currently
                        if v['variable_name'] == prop:
                            temp_y = v['variable_id']
                            rep_u = v['representation']
                            if (str(rep_u)[0] == 'R') or (str(rep_u)[0] == 'X'):
                                y_un = '1'
                            else:
                                y_un = v['units']
                            if "'reference_temperature':" in str(v):
                                ref_temp = v['reference_temperature']
                            else:
                                ref_temp = "N/A"
                    for d in c['data']: # goes through data tables and eventially data values
                        if (f"'variable_id': {temp_y}" in str(c['data'])): # only enters if both property and variable are compatible
                            if d['variable_id'] == temp_y:
                                for e in d['data_values']:
                                    if e['value'] == None:
                                        continue
                                    else:
                                        if "'uncertainty':" in str(e): # adds the uncertainty value for use in the data framework
                                            # temp_data_y = conversion_bridge(e['value'], e['uncertainty'], prop, y_un, prop_un)
                                            # verify = validation_bridge(temp_data_y[1], prop, y_un, rep_u)
                                            verify = validation_bridge(e['value'], prop, y_un, rep_u)
                                            if verify[0][1] == 'False':
                                                if str(c['data_set_id']) not in valid:
                                                    valid[str(c['data_set_id'])] = {}
                                                valid[str(c['data_set_id'])][str(e['value'])] = verify[1]
                                                props.append(prop)
                                                data_id.append(str(c['data_set_id']))
                                                cit_id.append(str(a['citation']['citation_id']))
                                                data_vals.append(str(e['value']))
                                                err_mess.append(verify[1])
                                        else:
                                            # temp_data_y = conversion_bridge(e['value'], 0, prop, y_un, prop_un)
                                            if prop != 'NOP':
                                                if str(c['data_set_id']) not in valid:
                                                    valid[str(c['data_set_id'])] = {}
                                                valid[str(c['data_set_id'])][str(e['value'])] = 'No Uncertainty for Value'
                                                props.append(prop)
                                                data_id.append(str(c['data_set_id']))
                                                cit_id.append(str(a['citation']['citation_id']))
                                                data_vals.append(str(e['value']))
                                                err_mess.append('No Uncertainty for Value')
            except KeyError:
                valid[str(c['data_set_id'])] = 'SECTION MISSING'
                props.append(prop)
                data_id.append(str(c['data_set_id']))
                cit_id.append(str(a['citation']['citation_id']))
                data_vals.append('N/A')
                err_mess.append('SECTION MISSING')
                    
    return(valid, props, data_id, cit_id, data_vals, err_mess)