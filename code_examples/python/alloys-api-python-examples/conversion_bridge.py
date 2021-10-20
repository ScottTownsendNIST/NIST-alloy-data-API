import ConversionLibrary as CL

def conversion_bridge(val, unc, var, in_unit, out_unit):
    tuple0 = ("", "", "", f"{val},{unc}", "", var, in_unit)
    tuple1 = ("", "", "", "", out_unit, "", "")
### NO CHANGE IN UNITS ###
    if in_unit == out_unit:
        converted = ['double', val, unc, out_unit, var]
### TEMPERATURE ###
    elif var == 'T':
        if out_unit == 'K':
            if tuple0[6] == 'C':
                converted = CL.Temperature_CtoK(tuple0)
            if tuple0[6] == 'F':
                converted = CL.Temperature_FtoK(tuple0)
            if tuple0[6] == 'R':
                converted = CL.Temperature_RtoK(tuple0)
        elif out_unit == 'C':
            if tuple0[6] == 'K':
                converted = CL.Temperature_KtoC(tuple0)
            if tuple0[6] == 'F':
                temp_con = CL.Temperature_FtoK(tuple0)
                temp_tup = ("","","",f"{temp_con[1]},{temp_con[2]}","",tuple0[5],temp_con[3])
                converted = CL.Temperature_KtoC(temp_tup)
            if tuple0[6] == 'R':
                temp_con = CL.Temperature_RtoK(tuple0)
                temp_tup = ("","","",f"{temp_con[1]},{temp_con[2]}","",tuple0[5],temp_con[3])
                converted = CL.Temperature_KtoC(temp_tup)
        elif out_unit == 'F':
            if tuple0[6] == 'K':
                converted = CL.Temperature_KtoF(tuple0)
            if tuple0[6] == 'C':
                temp_con = CL.Temperature_CtoK(tuple0)
                temp_tup = ("","","",f"{temp_con[1]},{temp_con[2]}","",tuple0[5],temp_con[3])
                converted = CL.Temperature_KtoF(temp_tup)
            if tuple0[6] == 'R':
                temp_con = CL.Temperature_RtoK(tuple0)
                temp_tup = ("","","",f"{temp_con[1]},{temp_con[2]}","",tuple0[5],temp_con[3])
                converted = CL.Temperature_KtoF(temp_tup)
        elif out_unit == 'R':
            if tuple0[6] == 'K':
                converted = CL.Temperature_KtoR(tuple0)
            if tuple0[6] == 'C':
                temp_con = CL.Temperature_CtoK(tuple0)
                temp_tup = ("","","",f"{temp_con[1]},{temp_con[2]}","",tuple0[5],temp_con[3])
                converted = CL.Temperature_KtoR(temp_tup)
            if tuple0[6] == 'F':
                temp_con = CL.Temperature_FtoK(tuple0)
                temp_tup = ("","","",f"{temp_con[1]},{temp_con[2]}","",tuple0[5],temp_con[3])
                converted = CL.Temperature_KtoR(temp_tup)
    ### ALL ELSE ###
    else:
        converted = CL.Into_Desired_Units(tuple0, tuple1)

    return(converted)