def dataset_build(var, prop, element_ids, rep):

    import json
    # This loads the decoder table file into a dict for use within the code
    with open('decoder_table.json') as json_file:
        decoder_table = json.load(json_file)
    
    import pandas as pd
    import itertools
    from conversion_bridge import conversion_bridge
    from validation_bridge import validation_bridge

    temp_x = "N/A" # temporary value which houses variable ID for the variable
    temp_y = "N/A" # temporary value which houses variable ID for the property
    x_lab = decoder_table['PRP'][var] # axis label to name x
    y_lab = decoder_table['PRP'][prop] # axis label to name y
    state_dict = {} # dict which relates state codes to states of matter
    dataset = [] # data which will be converted to the pandas framwork
    num1 = 0
    num2 = 0
    num3 = 0
    num4 = 0
    num5 = 0
    num6 = 0

    for a in data['TRC_data']:
        for b in a['systems']: # system data tends to be the material compositions, so other aspects can vary within a system with each data set
            try: # some intermetallics not explicitly recognized, so the try is to catch data sets which do not have a compound
                # only enters if the metal or alloy is the same as listed, is not inclusive of all alloys that contain that element
                if (Counter(b['compound_ids']) == Counter(element_ids)): 
                    num3 += 1
                    for p in b['phases']:
                        state_dict[p['phase_id']] = p['type'] # this is where the ids and states are related to be called later
                    for c in b['data_sets']:
                        num5 += 1
                        x_axt = []
                        y_axt = []
                        stat_id = []
                        y_unc = []
                        valid = []
                        add_data = False
                        method = ""
                        for s in c['states']:
                            stat_id.append(state_dict[s['phase_id']]) # recognizes and lists phase(s) for a given data point
                            if s['specimen_id'] in spec_par: # this section is for listing recognizing the descriptions and purities of specimen
                                if len(element_ids) > 1: # this is to go through the data if searching through an alloy
                                    init_desc = []
                                    pure = []
                                    p_un = []
                                    for t, u in itertools.zip_longest(spec_par[s['specimen_id']],range(len(element_ids)+1)):
                                        if t == None:
                                            temp_desc = t
                                            init_desc.append(t)
                                            pure.append(t)
                                        else:
                                            temp_desc = spec_desc[t]
                                            init_desc.append(spec_desc[t])
                                            temp_pure = ""
                                            for i in temp_desc:
                                                if i.isdigit() or i == ".":
                                                    temp_pure = temp_pure + str(i)
                                            if "." in temp_pure:
                                                pure.append(float(temp_pure))
                                            elif temp_pure == '' or temp_pure == None:
                                                temp_pure = None
                                                pure.append(temp_pure)
                                            else:
                                                pure.append(int(temp_pure))
                                        if (temp_desc == None) or (temp_pure == None):
                                            p_un.append(None)
                                        elif 'weight %' in temp_desc:
                                            p_un.append('Weight %')
                                        elif 'mole %' in temp_desc:
                                            p_un.append('Mole %')
                                        else:
                                            p_un.append("Not Specified %")
                                else: # this is for identifyig description and purity if a pure element
                                    init_desc = spec_desc[spec_par[s['specimen_id']][0]]
                                    pure = ""
                                    for i in init_desc:
                                        if i.isdigit() or i == ".":
                                            pure = pure + str(i)
                                    if "." in pure:
                                        pure = float(pure)
                                    elif pure == '':
                                        pure = None
                                    else:
                                        pure = int(pure)
                                    if 'weight %' in init_desc:
                                        p_un = 'Weight %'
                                    elif 'mole %' in init_desc:
                                        p_un = 'Mole %'
                                    elif pure == None:
                                        p_un = None
                                    else:
                                        p_un = "Not Specified %"
                            else: # lists specimen ID for easy recognition if it was not properly added to the spec_par dict
                                init_desc = s['specimen_id'] 
                                num6 += 1
                        for v in c['variables']: # this section of the code is designated to identifying the variable and property for use currently
                            if v['variable_name'] == prop:
                                num1 += 1
                                temp_y = v['variable_id']
                                rep_u = v['representation']
                                if (str(rep)[0] == 'R') or (str(rep)[0] == 'X'):
                                    y_un = '1'
                                else:
                                    y_un = v['units']
                                if 'method' in str(v):
                                    if str(v['method']).upper() in str(decoder_table['Method']):
                                        method = decoder_table['Method'][v['method'].upper()]
                                    else:
                                        method = v['method']
                                else:
                                    method = "N/A"
                                if "'reference_temperature':" in str(v):
                                    ref_temp = v['reference_temperature']
                                else:
                                    ref_temp = "N/A"
                            if v['variable_name'] == var:
                                num2 += 1
                                temp_x = v['variable_id']
                                if v['units'] == 'D':
                                    x_un = decoder_table['UnitsSpecial'][v['units']]
                                else:
                                    x_un = v['units']
                        for d in c['data']: # goes through data tables and eventially data values
                            if (f"'variable_id': {temp_x}" in str(c['data'])) and (f"'variable_id': {temp_y}" in str(c['data'])): # only enters if both property and variable are compatible
                                if d['variable_id'] == temp_y:
                                    for e in d['data_values']:
                                        if e['value'] == None:
                                            y_axt.append(None)
                                            y_unc.append(None)
                                            valid.append(None)
                                        else:
                                            if "'uncertainty':" in str(e): # adds the uncertainty value for use in the data framework
                                                temp_data_y = conversion_bridge(e['value'], e['uncertainty'], prop, y_un, des_un_prop)
                                                verify = validation_bridge(temp_data_y[1], prop, y_un, rep)
                                                y_axt.append(temp_data_y[1])
                                                y_unc.append(temp_data_y[2])
                                                valid.append(verify[0][1])
                                            else:
                                                temp_data_y = conversion_bridge(e['value'], 0, prop, y_un, des_un_prop)
                                                verify = validation_bridge(temp_data_y[1], prop, y_un, rep)
                                                y_axt.append(temp_data_y[1])
                                                y_unc.append(None)
                                                valid.append(verify[0][1])
                                if d['variable_id'] == temp_x:
                                    for f in d['data_values']:
                                        temp_data_x = conversion_bridge(f['value'], 0, var, x_un, des_un_var)
                                        x_axt.append(temp_data_x[1]) # these are the data values for the variable being added to the framework
                                add_data = True # adds a check to make sure that the table knows to add current data set
                                num4 += 1
                        if add_data == True:
                            for i,j,k,l in itertools.zip_longest(x_axt,y_axt,y_unc,valid):
                                if i == None:
                                    i = x_axt[0]
                                    # These are all of the individual and varying aspects being added to the pandas framework, not all are currently
                                    # used but are present for use if wanted.
                                dataset.append({ 
                                    f'{x_lab}: {des_un_var}': i, # x-axis variable values
                                    f'{y_lab}: {des_un_prop}': j, # y-axis property values
                                    'Uncertainty': k, # uncertainty for property
                                    'Ref Temp': ref_temp, # reference temperature for relative values (K)
                                    'Data Set ID': str(c['data_set_id']), # Data Set ID for which each value belongs to
                                    'State': stat_id, # encoded state(s) for each point
                                    'Representation': rep_u, # encoded representation for each point
                                    'Method': method, # method for which data was collected
                                    'Description': init_desc, # initial description of data
                                    'Purity': pure, # purity value for alloys, in list structure [Purity Element 1, Purity Element 2, ..., Purity Alloy]
                                    'Purity Units': p_un, # format for purity, corresponds directly to each purity value i.e. weight percent, molar percent, not specified
                                    'Year': a['citation']['year'], # year of paper's publication
                                    'Valid': l
                                })
            except KeyError:
                #print(a['citation'])
                continue

    print(num3, num1, num2, num4, num5, num6)
    df = pd.DataFrame(dataset) # builds the pandas dataframe