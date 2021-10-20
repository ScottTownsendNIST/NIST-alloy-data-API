# This is the Validation python library for Unit Tests of the TRC Data Objects. This library file
# will be parsed by the calling C++ program at runtime (NOT compile time). Because of this each
# function must be formatted in a specific manner so it can be parsed by the calling C++ application.
# For instance every python function definition must be of the format:
#       def "function_name"(tuple1,tuple2,...,tupleN):
#
# where the parameters each must be a tuple of the form (Note if using python 3 and above long is now int 
# so all long string values will need to be converted as int(long_value) not long(long_value) as in python 2):
#       (bool_value:string,int_value:string,long_value:string,float_value:string,string_value:string,variable_name:string,variable_units:string)
#
# and the python function will then use or convert then use the specific "value" in the array that has data defined
# for it. Suppose the function needs a temperature float value and a heat capcity float value then the
# funtion would have two tuple parameters with both tuples having empty strings in positions 1,2,3, and 5
# and a float value string in position 4. Then the function must convert position 4 of both tuples to float
# variables for use in that function! NOTE that ALL numeric values really are a tuple in string form where
# the first part of the string is the numeric value and the second part is the uncertainty! The uncertainty
# is always a double. I.E. a float_value could be "10.1,.003", an int_value could be "3,.5", etc. Now
# boolean and string values are NOT tuple values.

#
# This is done so that the C++ program can pass data in an apriori generic dynamic way without needing to
# know the specifics of each python function at compile time. 
# In light of this, each function must also specify a comment line with the true definitions of each parameter 
# of the form (no quotes in the actual line as the following comment will be parsed otherwise!):
#       # "parameter definition ("variable1_name": "variable1_type","variable2_name": "variable2_type")"
#
# I.E.
#       # "parameter definition (temperature: double,specific volume: float)"
#
# This line will be parsed by the calling C++ program at runtime and the information stored in conjunction
# with the "function_name" and "return_value" for use in properly calling this python function to perform
# a validation of data. Note that all validation functions need to return a string of "True" or "False"!
# It important to note that python does not have doubles but only float data types but
# it is vital to maintain the expected input data type to the C++ in mind when writing these python
# python functions. Eventhough the function will convert the string representation of a double/float value
# from the C++ to a float data type in the "pararmeter definition", the data type must reflect the C++
# data type which might be either a float or a double! In general the C++ tends to use the C++ double
# over the float type.
# NOTE that since the validate returns just a boolean it has no units however it is needed to pass a string 
# with the data value that failed so use the units string (ONLY in a VALIDATE function!!!) as the
# means to pass the data value that fails! Since the Rules Engine object does not know apriori
# anything about script functions and their output, a general output format is used for all types 
# of script functions (validation, normalization, conversion) and the normalization and conversion 
# functions will use the units as units. The validation script functions can not add a new string value 
# to the output so that is why the units string for validation functions will hold the data values and 
# uncertainties that fail.
#
# Return value is always a list object. Each returned data object in the list MUST comprise 5 return items in the list:
# 
#      [variable1_type,variable1_value,variable1_uncert,variable1_units,variable1_name,...,variableN_type,variableN_value,variableN_uncert,variableN_units,variableN_name]
#
# and may return many data values which means that the size of the list MUST always be a factor of 5. It will be checked in the C++ code and issue an exception if it is not.
# I.E.
#      return ["bool","True",0.0,"unknown","ValidationCheck"]
#
#
# Import any python libraries needed to do the conversion work
import math as m
import ConversionLibrary as CL
# We use the conversion library to automatically convert the input values into database units for comparison.
# This line is required so that the calling C++ program can know that the "Python" interpreter is to be used
rules_engine_language = "Python"
# It takes in the value you want to validate in the tuple, converts it to
# database units, and checks if the converted value is within the
# given bounds. To do the conversion, we need the database property symbol, prop_sym.
# If the parameter inclusive is passed as True, we include the bounds in the allowed values.
# Otherwise, we fail to validate if the value equals the bounds.
def General_Validation(tuple0, prop_sym, lower_bound, upper_bound, inclusive=False, is_int = False):
    # parameter definition (value: double)

    if is_int:
        value = int(float(tuple0[1]))
    else:
        float_value_list = tuple0[3].split(',')
        value = float(float_value_list[0])
    units = tuple0[6]
    if units == '':
        units = 'None'
    name = tuple0[5].lower()
    value_list = CL.Convert_To_DB_Units(value, 0, units, prop_sym)
    #print(value_list)
    value = value_list[0]
    fail_string = "value: " + str(value)
    # If the value is not a number or empty return False
    if value is None or  m.isnan(value):
        return ["bool","False",0.0,fail_string,name]
    if inclusive:
        # Here we use >=/<= for the inclusive range
        if (value <= upper_bound) and (value >= lower_bound):
            return ["bool","True",0.0,"unknown",name]
        else:
            return ["bool","False",0.0,fail_string,name]
    else:
        # Check if the value is in the supplied range. We reject the value if
        # it equals the bound (which allows us to reject 0 values easier)
        if (value < upper_bound) and (value > lower_bound):
            return ["bool","True",0.0,"unknown",name]
        else:
            return ["bool","False",0.0,fail_string,name]

# This validation function checks the specific density, which has units of kg/m^3
# Checks for REASONABLE values. 
def Validate_VDN(tuple0):
    # parameter definition (specific density: double)
    # Reasonable values are greater than 100 and less than 5e4 kg/m^3 (Li is around 534 kg/m^3, Os is 22600 kg/m^3)
    return General_Validation(tuple0, 'VDN', 100, 5e4)

# This validation function checks the Critical density, which has units of kg/m^3
# Checks for REASONABLE values. 
def Validate_VDC(tuple0):
    # parameter definition (Critical density: double)
    # Reasonable values are greater than 100 and less than 5e4 kg/m^3 (used the same range as specific density)
    return General_Validation(tuple0, 'VDC', 100, 5e4)

# This validation function checks the specific volume, which has units of m^3/kg
# Checks for REASONABLE values.
def Validate_VS(tuple0):
    # parameter definition (specific volume: double)
    # Reasonable values are just the reciprocal of the density values
    return General_Validation(tuple0, 'VS', 2e-5, 0.01)

# This validation function checks the Critical specific volume, which has units of m^3/kg
# Checks for REASONABLE values.
def Validate_VSC(tuple0):
    # parameter definition (Critical specific volume: double)
    # Here I just used the same range as the specific volume.
    return General_Validation(tuple0, 'VSC', 2e-5, 0.01)

# This validation function checks the molar volume, which has units of m^3/mol
# Checks for REASONABLE values.
def Validate_VM(tuple0):
    # parameter definition (Molar volume: double)
    # Reasonable values can be found by multiplying the mass specific volume
    # bounds by the lowest and highest atomic weights (Li about 7 g/mol, Am about 250 g/mol).
    # We also need to divide VS by 1000 to convert to grams first.
    return General_Validation(tuple0, 'VM', 1e-7, 2.5e-3)

# This validation function checks the Excess volume, which has units of m^3/mol
# Checks for REASONABLE values.
def Validate_VEX(tuple0):
    # parameter definition (Excess volume: double)
    # Used the same range as VM but allowed negative values
    return General_Validation(tuple0, 'VEX', -2.5e-3, 2.5e-3)

# This validation function checks the Critical molar volume, which has units of m^3/mol
# Checks for REASONABLE values.
def Validate_VC(tuple0):
    # parameter definition (Critical molar volume: double)
    # Here I used the same range as VM
    return General_Validation(tuple0, 'VC', 1e-7, 2.5e-3)

# This validation function checks the Apparent molar volume, which has units of m^3/mol
# Checks for REASONABLE values.
def Validate_VA(tuple0):
    # parameter definition (Apparent molar volume: double)
    # Here I just used the same bounds as molar volume.
    return General_Validation(tuple0, 'VA', 1e-7, 2.5e-3)

# This validation function checks the molar density, which has units of mol/m^3
# Checks for REASONABLE values.
def Validate_VDM(tuple0):
    # parameter definition (Molar density: double)
    # Reasonable values are the reciprocal of the VM bounds
    return General_Validation(tuple0, 'VDM', 400, 1e7)

# This validation function checks the pressure, which has units of kPa
# Checks for REASONABLE values.
def Validate_P(tuple0):
    # parameter definition (pressure: double)
    # Reasonable values are greater than 0 and less than 1e9 kPa
    return General_Validation(tuple0, 'P', 0, 1e9)

# This validation function checks the Partial Pressure, which has units of kPa
# Checks for REASONABLE values.
def Validate_PP(tuple0):
    # parameter definition (Partial Pressure: double)
    # Reasonable values are greater than 0 and less than 1e9 kPa
    return General_Validation(tuple0, 'PP', 0, 1e9)

# This validation function checks the Critical pressure, which has units of kPa
# Checks for REASONABLE values.
def Validate_PC(tuple0):
    # parameter definition (Critical pressure: double)
    # Reasonable values are greater than 0 and less than 1e9 kPa
    return General_Validation(tuple0, 'PC', 0, 1e9)

# This validation function checks the Upper consolute pressure, which has units of kPa
# Checks for REASONABLE values.
def Validate_PUC(tuple0):
    # parameter definition (Upper consolute pressure: double)
    # Reasonable values are greater than 0 and less than 1e9 kPa
    return General_Validation(tuple0, 'PUC', 0, 1e9)

# This validation function checks the reference pressure, which has units of kPa
# Checks for REASONABLE values.
def Validate_PX(tuple0):
    # parameter definition (reference pressure: double)
    # Reasonable values are greater than 0 and less than 1e9 kPa
    return General_Validation(tuple0, 'PX', 0, 1e9)

# This validation function checks the lower pressure, which has units of kPa
# Checks for REASONABLE values.
def Validate_PL(tuple0):
    # parameter definition (Lower pressure for a DX: double)
    # Reasonable values are greater than 0 and less than 1e9 kPa
    return General_Validation(tuple0, 'PL', 0, 1e9)

# This validation function checks the Upper pressure for a DX, which has units of kPa
# Checks for REASONABLE values.
def Validate_PU(tuple0):
    # parameter definition (Upper pressure for a DX: double)
    # Reasonable values are greater than 0 and less than 1e9 kPa
    return General_Validation(tuple0, 'PU', 0, 1e9)

# This validation function checks the Vapor or sublimation pressure, which has units of kPa
# Checks for REASONABLE values. This range is VERY wide.
def Validate_PV(tuple0):
    # parameter definition (Vapor or sublimation pressure: double)
    # Reasonable values are greater than 0 and less than 1e9 kPa
    return General_Validation(tuple0, 'PV', 0, 1e9)

# This validation function checks the Triple point pressure, which has units of kPa
# Checks for REASONABLE values. This range is VERY wide.
def Validate_TPP(tuple0):
    # parameter definition (Triple point pressure: double)
    # Reasonable values are greater than 0 and less than 1e9 kPa
    return General_Validation(tuple0, 'P', 0, 1e9)

# This validation function checks the speed of sound, which has units of m/s
# Checks for REASONABLE values.
def Validate_RSS(tuple0):
    # parameter definition (speed of sound: double)
    # Reasonable values are greater than 100 and less than 20000 m/s (diamond goes up to 12000)
    return General_Validation(tuple0, 'RSS', 100, 20000)

# This validation function checks the surface tension, which has units of N/m
# Checks for REASONABLE values.
def Validate_IST(tuple0):
    # parameter definition (surface tension: double)
    # Reasonable values are greater than 0 and less than 3 N/m
    return General_Validation(tuple0, 'IST', 0, 3)

# This validation function checks the interfacial tension, which has units of N/m
# Checks for REASONABLE values.
def Validate_IIT(tuple0):
    # parameter definition (interfacial tension: double)
    # Reasonable values are greater than 0 and less than 10 N/m (highest we have is 2.27)
    return General_Validation(tuple0, 'IIT', 0, 10)

# This validation function checks the kinematic viscosity, which has units of m^2/s
# Checks for REASONABLE values.
def Validate_NVK(tuple0):
    # parameter definition (Kinematic viscosity: double)
    # Reasonable values are between 0 and 1e-5 m^2/s (highest we have is 1.7e-6)
    return General_Validation(tuple0, 'NVK', 0, 1e-5)
    
# This validation function checks the viscosity, which has units of Pa*s
# Checks for REASONABLE values.
def Validate_NVC(tuple0):
    # parameter definition (viscosity: double)
    # Reasonable values are between 0 and 0.3 Pa*s (highest we have is 7.61e-2)
    return General_Validation(tuple0, 'NVC', 0, 0.3)

# This validation function checks the temperature, which has units of K
# Checks for REASONABLE values.
def Validate_T(tuple0):
    # parameter definition (temperature: double)
    # Reasonable values are greater than 0 and less than 14000 K
    return General_Validation(tuple0, 'T', 0, 14000)

# This validation function checks the lower temperature, which has units of K
# Checks for REASONABLE values.
def Validate_TL(tuple0):
    # parameter definition (Lower temperature: double)
    # Reasonable values are greater than 0 and less than 14000 K
    return General_Validation(tuple0, 'TL', 0, 14000)

# This validation function checks the upper temperature, which has units of K
# Checks for REASONABLE values.
def Validate_TU(tuple0):
    # parameter definition (Upper temperature: double)
    # Reasonable values are greater than 0 and less than 14000 K
    return General_Validation(tuple0, 'TU', 0, 14000)

# This validation function checks the boiling temperature, which has units of K
# Checks for REASONABLE values.
def Validate_TB(tuple0):
    # parameter definition (Boiling temperature: double)
    # Reasonable values are greater than 0 and less than 14000 K
    return General_Validation(tuple0, 'TB', 0, 14000)

# This validation function checks the critical temperature, which has units of K
# Checks for REASONABLE values.
def Validate_TC(tuple0):
    # parameter definition (Critical temperature: double)
    # Reasonable values are greater than 0 and less than 14000 K
    return General_Validation(tuple0, 'TC', 0, 14000)

# This validation function checks the eutectic temperature, which has units of K
# Checks for REASONABLE values.
def Validate_TE(tuple0):
    # parameter definition (Eutectic temperature: double)
    # Reasonable values are greater than 0 and less than 14000 K
    return General_Validation(tuple0, 'TE', 0, 14000)

# This validation function checks the monotectic temperature, which has units of K
# Checks for REASONABLE values.
def Validate_TM(tuple0):
    # parameter definition (Monotectic temperature: double)
    # Reasonable values are greater than 0 and less than 14000 K
    return General_Validation(tuple0, 'TM', 0, 14000)

# This validation function checks the normal boiling temperature, which has units of K
# Checks for REASONABLE values.
def Validate_TBN(tuple0):
    # parameter definition (Normal boiling temperature: double)
    # Reasonable values are greater than 0 and less than 14000 K
    return General_Validation(tuple0, 'TBN', 0, 14000)

# This validation function checks the normal melting temperature, which has units of K
# Checks for REASONABLE values.
def Validate_TMN(tuple0):
    # parameter definition (Normal melting temperature: double)
    # Reasonable values are greater than 0 and less than 14000 K
    return General_Validation(tuple0, 'TMN', 0, 14000)

# This validation function checks the phase transition temperature, which has units of K
# Checks for REASONABLE values.
def Validate_TT(tuple0):
    # parameter definition (phase transition temperature: double)
    # Reasonable values are greater than 0 and less than 14000 K
    return General_Validation(tuple0, 'TT', 0, 14000)

# This validation function checks the Triple point temperature, which has units of K
# Checks for REASONABLE values.
def Validate_TPT(tuple0):
    # parameter definition (Triple point temperature: double)
    # Reasonable values are greater than 0 and less than 14000 K
    return General_Validation(tuple0, 'T', 0, 14000)

# This validation function checks the radiance temperature, which has units of K
# Checks for REASONABLE values.
def Validate_TR(tuple0):
    # parameter definition (radiance temperature: double)
    # Reasonable values are greater than 0 and less than 14000 K
    return General_Validation(tuple0, 'TR', 0, 14000)

# This validation function checks the reference temperature, which has units of K
# Checks for REASONABLE values.
def Validate_TX(tuple0):
    # parameter definition (reference temperature: double)
    # Reasonable values are greater than 0 and less than 14000 K
    return General_Validation(tuple0, 'TX', 0, 14000)

# This validation function checks the upper consolute temperature, which has units of K
# Checks for REASONABLE values.
def Validate_TUC(tuple0):
    # parameter definition (upper consolute temperature: double)
    # Reasonable values are greater than 0 and less than 14000 K
    return General_Validation(tuple0, 'TUC', 0, 14000)

# This validation function checks the thermal conductivity, which has units of W/m/K
# Checks for REASONABLE values.
def Validate_NTC(tuple0):
    # parameter definition (thermal conductivity: double)
    # Reasonable values are greater than 0 and less than 1e5 W/m/K (Al goes up to 2.27e4)
    return General_Validation(tuple0, 'NTC', 0, 1e5)

# This validation function checks the thermal diffusivity, which has units of m^2/s
# Checks for REASONABLE values.
def Validate_NTD(tuple0):
    # parameter definition (Thermal diffusivity: double)
    # Reasonable values are between 0 and 3e-3 m^2/s (highest we have is 5e-4)
    return General_Validation(tuple0, 'NTD', 0, 3e-3)

# This validation function checks the Self diffusion coefficient, which has units of mm^2/ks
# Checks for REASONABLE values.
def Validate_NDC(tuple0):
    # parameter definition (Self diffusion coefficient: double)
    # Reasonable values are greater than 0 and less than 100 (1e-9m^2/s)
    # I checked the values from 
    # https://www.sciencedirect.com/science/article/pii/0022311578902349
    return General_Validation(tuple0, 'NDC', 0, 100)

# This validation function checks the molar specific heat, which has units of J/mol/K
# Checks for REASONABLE values.
def Validate_CP(tuple0):
    # parameter definition (Heat capacity at constant pressure Cp: double)
    # Reasonable values are greater than 0 and less than 4000 J/mol/K (calculated from CPW range and highest atomic weight)
    return General_Validation(tuple0, 'CP', 0, 4e3)

# This validation function checks the mass specific heat, which has units of J/K/kg
# Checks for REASONABLE values.
def Validate_CPW(tuple0):
    # parameter definition (Heat capacity at constant pressure Cp per unit mass: double)
    # Reasonable values are greater than 0 and less than 2e4 J/K/kg (highest value we have is 5.11e3)
    return General_Validation(tuple0, 'CPW', 0, 2e4)

# This validation function checks the Cp per unit volume, which has units of J/K/m^3
# Checks for REASONABLE values.
def Validate_CPV(tuple0):
    # parameter definition (Heat capacity at constant pressure Cp per unit volume: double)
    # Reasonable values are between 0 and 1e7 J/K/m^3 (highest we have is 2.3e6, lowest is 1.45e6)
    return General_Validation(tuple0, 'CPV', 0, 1e7)

# This validation function checks the Apparent molar heat capacity, which has units of J/mol/K
# Checks for REASONABLE values.
def Validate_CPA(tuple0):
    # parameter definition (Apparent molar heat capacity: double)
    # Reasonable values are greater than 0 and less than 4000 J/mol/K (I just used the same as the CP range)
    return General_Validation(tuple0, 'CPA', 0, 4e3)

# This validation function checks the Excess heat capacity, which has units of J/mol/K
# Checks for REASONABLE values.
def Validate_CEX(tuple0):
    # parameter definition (Excess heat capacity: double)
    # Reasonable values are greater than -4000 and less than 4000 J/mol/K 
    # (used the CP range but allowed negative values)
    return General_Validation(tuple0, 'CEX', -4e3, 4e3)

# This validation function checks the Cp/e(hemispherical total), which has units of J/mol/K
# Checks for REASONABLE values.
def Validate_CPEH(tuple0):
    # parameter definition (Cp/e(hemispherical total): double)
    # Reasonable values are greater than 0 and less than 2000 J/mol/K (highest we have is 283)
    return General_Validation(tuple0, 'CPEH', 0, 2e3)

# This validation function checks the Cp/e(hemispherical total) per unit mass, which has units of J/kg/K
# Checks for REASONABLE values.
def Validate_CPEHW(tuple0):
    # parameter definition Cp/e(hemispherical total) per unit mass: double)
    # Reasonable values are greater than 0 and less than 34000 J/kg/K (converted from CPEH range
    # for Nickel)
    return General_Validation(tuple0, 'CPEHW', 0, 3.4e4)

# This validation function checks the specific heat at constant volume, which has units of J/K/mol
# Checks for REASONABLE values.
def Validate_CV(tuple0):
    # parameter definition (Heat capacity at constant volume Cv: double)
    # Reasonable values are greater than 0 and less than 100 J/K/mol (highest we have is 28.2)
    return General_Validation(tuple0, 'CV', 0, 100)

# This validation function checks the specific heat at constant volume per unit mass, which has units of J/K/kg
# Checks for REASONABLE values.
def Validate_CVW(tuple0):
    # parameter definition (Heat capacity at constant volume per unit mass: double)
    # Reasonable values are greater than 0 and less than 20000 J/K/kg (calculated assuming lowest atomic weight from CV range)
    return General_Validation(tuple0, 'CVW', 0, 20000)

# This validation function checks the Heat capacity at constant volume Cv per unit volume, which has units of J/K/m^3
# Checks for REASONABLE values.
def Validate_CVV(tuple0):
    # parameter definition (Heat capacity at constant volume Cv per unit volume: double)
    # Reasonable values are greater than 0 and less than 4e8 J/K/m^3 (calculated from CVW range using highest density)
    return General_Validation(tuple0, 'CVV', 0, 4e8)

# This validation function checks the Heat capacity at vapor saturation pressure Csat, which has units of J/mol/K
# Checks for REASONABLE values.
def Validate_CS(tuple0):
    # parameter definition (Heat capacity at vapor saturation pressure Csat: double)
    # Reasonable values are greater than 0 and less than 4000 J/mol/K (used the CP range)
    return General_Validation(tuple0, 'CS', 0, 4e3)

# This validation function checks the Heat capacity ratio Cp/Cv, which has units of None
# Checks for REASONABLE values.
def Validate_CGM(tuple0):
    # parameter definition (Heat capacity ratio Cp/Cv: double)
    # Reasonable values are greater than 1 and less than 2, inclusive (this is mostly a guess)
    return General_Validation(tuple0, 'CGM', 1, 2, inclusive = True)

# This validation function checks the Enthalpy per unit mass, which has units of kJ/kg
# Checks for REASONABLE values.
def Validate_HW(tuple0):
    # parameter definition (Enthalpy per unit mass: double)
    # Reasonable values are between -6e4 and +6e4 kJ/kg 
    # (from following the slope of enthalpy of Be out to 12000K)
    return General_Validation(tuple0, 'HW', -6e4, 6e4)

# This validation function checks the Enthalpy, which has units of kJ/mol
# Checks for REASONABLE values.
def Validate_H(tuple0):
    # parameter definition (Enthalpy: double)
    # Reasonable values are between -1e4 and +1e4 kJ/mol (though this range is likely
    # unnecessarily wide. I just have issues plotting all enthalpy datasets to check)
    return General_Validation(tuple0, 'H', -1e4, 1e4)

# This validation function checks the Enthalpy of transition or fusion, which has units of kJ/mol
# Checks for REASONABLE values.
def Validate_HTR(tuple0):
    # parameter definition (Enthalpy of transition or fusion: double)
    # Reasonable values are between 0 and 1e3 kJ/mol
    return General_Validation(tuple0, 'HTR', 0, 1e3)

# This validation function checks the Enthalpy of solution, which has units of kJ/mol
# Checks for REASONABLE values.
def Validate_HSL(tuple0):
    # parameter definition (Enthalpy of solution: double)
    # Reasonable values are between -1e4 and +1e4 kJ/mol (I just used the enthalpy range)
    return General_Validation(tuple0, 'HSL', -1e4, 1e4)

# This validation function checks the Enthalpy of reaction, which has units of kJ/mol
# Checks for REASONABLE values.
def Validate_HRX(tuple0):
    # parameter definition (Enthalpy of reaction: double)
    # Reasonable values are between -1e4 and +1e4 kJ/mol (I just used the enthalpy range)
    return General_Validation(tuple0, 'H', -1e4, 1e4)

# This validation function checks the Enthalpy of transition or fusion per unit mass, which has units of kJ/kg
# Checks for REASONABLE values.
def Validate_HTRW(tuple0):
    # parameter definition (Enthalpy of transition or fusion per unit mass: double)
    # Reasonable values are between 0 and 2e3 kJ/kg (highest we have is 417)
    return General_Validation(tuple0, 'HTRW', 0, 2e3)

# This validation function checks the Enthalpy of vaporization or sublimation, which has units of kJ/mol
# Checks for REASONABLE values.
def Validate_HVP(tuple0):
    # parameter definition (Enthalpy of vaporization or sublimation: double)
    # Reasonable values are between 0 and 2e3 kJ/mol (highest we  have is 611)
    return General_Validation(tuple0, 'HVP', 0, 2e3)

# This validation function checks the Apparent enthalpy, which has units of kJ/mol
# Checks for REASONABLE values.
def Validate_HA(tuple0):
    # parameter definition (Apparent enthalpy: double)
    # Reasonable values are between -1e4 and 1e4 kJ/mol (I just took the range from enthalpy)
    return General_Validation(tuple0, 'HA', -1e4, 1e4)

# This validation function checks the Excess enthalpy, which has units of kJ/mol
# Checks for REASONABLE values.
def Validate_HEX(tuple0):
    # parameter definition (Excess enthalpy: double)
    # Reasonable values are between -1e4 and 1e4 kJ/mol (I just took the range from enthalpy)
    return General_Validation(tuple0, 'HEX', -1e4, 1e4)

# This validation function checks the Excess enthalpy per unit mass, which has units of kJ/kg
# Checks for REASONABLE values.
def Validate_HEXW(tuple0):
    # parameter definition (Excess enthalpy per unit mass: double)
    # Reasonable values are between -6e4 and 6e4 kJ/kg (I just took the range from enthalpy per unit mass)
    return General_Validation(tuple0, 'HEXW', -6e4, 6e4)

# This validation function checks the Partial molar enthalpy, which has units of kJ/mol
# Checks for REASONABLE values.
def Validate_HP(tuple0):
    # parameter definition (Partial molar enthalpy: double)
    # Reasonable values are between -200 and 200 kJ/mol (we have values between -35.5 and 5.6)
    return General_Validation(tuple0, 'HP', -200, 200)

# This validation function checks the Molar Enthalpy Change, which has units of J/mol
# Checks for REASONABLE values.
def Validate_HXM(tuple0):
    # parameter definition (Molar Enthalpy Change: double)
    # Reasonable values are between -200 and 200 J/mol (we have values between -32.9 and 69.2)
    return General_Validation(tuple0, 'HXM', -200, 200)

# This validation function checks the Enthalpy Change, which has units of J
# Checks for REASONABLE values.
def Validate_HX(tuple0):
    # parameter definition (Enthalpy Change: double)
    # Reasonable values are between -1e4 and 1e4 J (we have values between 0 and 2066)
    return General_Validation(tuple0, 'HX', -200, 200)

# This validation function checks the Gibbs energy of reaction, which has units of kJ/mol
# Checks for REASONABLE values.
def Validate_G(tuple0):
    # parameter definition (Gibbs energy of reaction: double)
    # Reasonable values are between -100 and 100 kJ/mol (We have values between -15.4 and 0)
    return General_Validation(tuple0, 'G', -100, 100)

# This validation function checks the Partial molar Gibbs energy, which has units of kJ/mol
# Checks for REASONABLE values.
def Validate_GP(tuple0):
    # parameter definition (Partial molar Gibbs energy: double)
    # Reasonable values are between -100 and 100 kJ/mol (We have values between -12.5 and 0)
    return General_Validation(tuple0, 'GP', -100, 100)

# This validation function checks the Relative partial molar Gibbs energy, which has units of kJ/mol
# Checks for REASONABLE values.
def Validate_GR(tuple0):
    # parameter definition (Relative partial molar Gibbs energy: double)
    # Reasonable values are between -100 and 100 kJ/mol (used the GP range)
    return General_Validation(tuple0, 'GR', -100, 100)

# This validation function checks the Apparent Gibbs energy, which has units of kJ/mol
# Checks for REASONABLE values.
def Validate_GA(tuple0):
    # parameter definition (Apparent Gibbs energy: double)
    # Reasonable values are between -100 and 100 kJ/mol (used the GP range)
    return General_Validation(tuple0, 'GA', -100, 100)

# This validation function checks the Excess Gibbs energy, which has units of kJ/mol
# Checks for REASONABLE values.
def Validate_GEX(tuple0):
    # parameter definition (Excess Gibbs energy: double)
    # Reasonable values are between -100 and 100 kJ/mol (used the same range as G)
    return General_Validation(tuple0, 'GEX', -100, 100)

# This validation function checks the Helmholtz energy, which has units of kJ/mol
# Checks for REASONABLE values.
def Validate_UA(tuple0):
    # parameter definition (Helmholtz energy: double)
    # Reasonable values are between -100 and +100 kJ/mol (used the same range as G)
    return General_Validation(tuple0, 'UA', -100, 100)

# This validation function checks the Internal energy of reaction (mole basis), which has units of kJ/mol
# Checks for REASONABLE values.
def Validate_U(tuple0):
    # parameter definition (Internal energy of reaction (mole basis): double)
    # Reasonable values are between -100 and +100 kJ/mol (used the same range as G)
    return General_Validation(tuple0, 'U', -100, 100)

# This validation function checks the Internal energy of reaction at constant volume (mass basis), which has units of J/g
# Checks for REASONABLE values.
def Validate_UV(tuple0):
    # parameter definition (Internal energy of reaction at constant volume (mass basis): double)
    # Reasonable values are between -20000 and +20000 J/g (converted from U assuming atomic weight of 5 g/mol)
    return General_Validation(tuple0, 'UV', -20000, 20000)

# This validation function checks the Lattice energy at 0 K, which has units of kJ/mol
# Checks for REASONABLE values.
def Validate_LE(tuple0):
    # parameter definition (Lattice energy at 0 K: double)
    # Reasonable values are between -15000 and +15000 kJ/mol (included positive and negative
    # values because people define it different ways.)
    return General_Validation(tuple0, 'LE', -15000, 15000)

# This validation function checks the Entropy, which has units of J/K/mol
# Checks for REASONABLE values.
def Validate_S(tuple0):
    # parameter definition (Entropy: double)
    # Reasonable values are between 0 and 1e3 J/K/mol (highest we  have is 141.7)
    return General_Validation(tuple0, 'S', 0, 1e3)

# This validation function checks the Apparent entropy, which has units of J/K/mol
# Checks for REASONABLE values.
def Validate_SA(tuple0):
    # parameter definition (Apparent entropy: double)
    # Reasonable values are between 0 and 1e3 J/K/mol (I just took the range from entropy)
    return General_Validation(tuple0, 'SA', 0, 1e3)

# This validation function checks the Excess entropy, which has units of J/K/mol
# Checks for REASONABLE values.
def Validate_SEX(tuple0):
    # parameter definition (Excess entropy: double)
    # Reasonable values are between -1e3 and 1e3 J/K/mol 
    # (I just took the range from entropy and allowed negative values)
    return General_Validation(tuple0, 'SEX', -1e3, 1e3)

# This validation function checks the Entropy of reaction, which has units of J/K/mol
# Checks for REASONABLE values.
def Validate_SR(tuple0):
    # parameter definition (Entropy of reaction: double)
    # Reasonable values are between 0 and 1e3 J/K/mol (same range as S)
    return General_Validation(tuple0, 'S', 0, 1e3)

# This validation function checks the Partial molar entropy, which has units of J/K/mol
# Checks for REASONABLE values.
def Validate_SP(tuple0):
    # parameter definition (Partial molar entropy: double)
    # Reasonable values are between 0 and 1e3 J/K/mol (same range as S)
    return General_Validation(tuple0, 'SP', 0, 1e3)


# This validation function checks the Entropy per unit mass, which has units of J/K/kg
# Checks for REASONABLE values.
def Validate_SW(tuple0):
    # parameter definition (Entropy per unit mass: double)
    # Reasonable values are between 0 and 2e5 J/K/kg (based on converting S range assuming lowest atomic weight)
    return General_Validation(tuple0, 'SW', 0, 2e5)

# This validation function checks the lattice parameter A, which has units of angstrom
# Checks for REASONABLE values.
def Validate_LA(tuple0):
    # parameter definition (Lattice parameter A: double)
    # Reasonable values are greater than 0.5 and less than 20 A (highest we have is 11.9 for lattice C, lowest is 1.57 for lattice C)
    return General_Validation(tuple0, 'LA', 0.5, 20)

# This validation function checks the lattice parameter B, which has units of angstrom
# Checks for REASONABLE values.
def Validate_LB(tuple0):
    # parameter definition (Lattice parameter B: double)
    # Reasonable values are greater than 0.5 and less than 20 A (used same range as lattice A)
    return General_Validation(tuple0, 'LB', 0.5, 20)

# This validation function checks the lattice parameter C, which has units of angstrom
# Checks for REASONABLE values.
def Validate_LC(tuple0):
    # parameter definition (Lattice parameter C: double)
    # Reasonable values are greater than 0.5 and less than 20 A (used same range as lattice A)
    return General_Validation(tuple0, 'LC', 0.5, 20)

# This validation function checks the lattice angle A, which has units of degrees
# Checks for POSSIBLE values.
def Validate_LAA(tuple0):
    # parameter definition (Lattice angle Alpha: double)
    # Possible values are greater than 0 and less than 180
    return General_Validation(tuple0, 'LAA', 0, 180)

# This validation function checks the lattice angle B, which has units of degrees
# Checks for POSSIBLE values.
def Validate_LAB(tuple0):
    # parameter definition (Lattice angle Beta: double)
    # Possible values are greater than 0 and less than 180
    return General_Validation(tuple0, 'LAB', 0, 180)

# This validation function checks the lattice angle C, which has units of degrees
# Checks for POSSIBLE values.
def Validate_LAC(tuple0):
    # parameter definition (Lattice angle Gamma: double)
    # Possible values are greater than 0 and less than 180
    return General_Validation(tuple0, 'LAC', 0, 180)

# This validation function checks the relative linear expansion, which has units of None.
# Checks for REASONABLE values.
def Validate_RLE(tuple0):
    # parameter definition (Relative linear expansion: double)
    # Reasonable values are between -0.3 and +0.3. (reaches up to ~0.1 at very high temperatures)
    return General_Validation(tuple0, 'RLE', -0.3, 0.3)

# This validation function checks the relative volumetric expansion, which has units of None.
# Checks for REASONABLE values.
def Validate_RVE(tuple0):
    # parameter definition (Relative volumetric expansion: double)
    # Reasonable values are between -1 and +1 (relative linear expansion of 0.3 can give
    # relative volumetric expansion a bit over 2).
    return General_Validation(tuple0, 'RVE', -1, 1)

# This validation function checks the linear expansion coefficient, which has units of 1/K.
# Checks for REASONABLE values.
def Validate_LEC(tuple0):
    # parameter definition (Linear expansion coefficient: double)
    # Reasonable values are between -1e-5 and +1e-4 (Si has slight negative linear expansion coefficient)
    return General_Validation(tuple0, 'LEC', -1e-5, 1e-4)

# This validation function checks the Isobaric coefficient of volume expansion, which has units of 1/K.
# Checks for REASONABLE values.
def Validate_VTP(tuple0):
    # parameter definition (Isobaric coefficient of volume expansion: double)
    # Reasonable values are between -1e-5 and 4e-4 (highest is 1.88e-4)
    return General_Validation(tuple0, 'VTP', -1e-5, 4e-4)

# This validation function checks the Isothermal compressibility, which has units of 1/kPa.
# Checks for REASONABLE values.
def Validate_VPT(tuple0):
    # parameter definition (Isothermal compressibility: double)
    # Reasonable values are between -4e-8 and 2e-7 1/kPa (highest is 3.97e-8)
    return General_Validation(tuple0, 'VPT', -4e-8, 2e-7)

# This validation function checks the total hemispherical emittance, which has units of None
# Checks for POSSIBLE values (except in weird edge cases that are only valid locally).
def Validate_EH(tuple0):
    # parameter definition (Total hemispherical emittance: double)
    # Reasonable values are between 0 and 1 (inclusive)
    return General_Validation(tuple0, 'EH', 0, 1, inclusive=True)

# This validation function checks the total normal emittance, which has units of None
# Checks for POSSIBLE values (except in weird edge cases that are only valid locally).
def Validate_ENT(tuple0):
    # parameter definition (Total normal emittance: double)
    # Reasonable values are between 0 and 1 (inclusive)
    return General_Validation(tuple0, 'ENT', 0, 1, inclusive=True)

# This validation function checks the spectral normal emittance, which has units of None
# Checks for POSSIBLE values (except in weird edge cases that are only valid locally).
def Validate_EN(tuple0):
    # parameter definition (Spectral normal emittance: double)
    # Reasonable values are between 0 and 1 (inclusive)
    return General_Validation(tuple0, 'EN', 0, 1, inclusive=True)

# This validation function checks the spectral hemispherical emittance, which has units of None
# Checks for POSSIBLE values (except in weird edge cases that are only valid locally).
def Validate_EHS(tuple0):
    # parameter definition (Spectral hemispherical emittance: double)
    # Reasonable values are between 0 and 1 (inclusive)
    return General_Validation(tuple0, 'EHS', 0, 1, inclusive=True)

# This validation function checks the activity, which has units of None
# Checks for REASONABLE values.
def Validate_AP(tuple0):
    # parameter definition (Activity: double)
    # Reasonable values are between 0 and 5 (inclusive)
    return General_Validation(tuple0, 'AP', 0, 5, inclusive=True)

# This validation function checks the Activity coefficient, which has units of None
# Checks for REASONABLE values.
def Validate_AC(tuple0):
    # parameter definition (Activity coefficient: double)
    # Reasonable values are between 0 and 1000 (inclusive, maybe? This is also a rough range
    # since I don't know much about activity coefficient)
    return General_Validation(tuple0, 'AC', 0, 1000, inclusive=True)

# This validation function checks the gravitational acceleration, which has units of m/s^2
# Checks for REASONABLE values.
def Validate_GRV(tuple0):
    # parameter definition (Gravitational acceleration: double)
    # Reasonable values are between 0 and 10000 m/s^2
    return General_Validation(tuple0, 'GRV', 0, 10000)

# This validation function checks the Magnetic field density, which has units of T
# Checks for REASONABLE values.
def Validate_WB(tuple0):
    # parameter definition (Magnetic field density: double)
    # Reasonable values are between 0 and 100 T
    return General_Validation(tuple0, 'WB', 0, 100)

# This validation function checks the Magnetic field strength, which has units of A/m
# Checks for REASONABLE values.
def Validate_WH(tuple0):
    # parameter definition (Magnetic field strength: double)
    # Reasonable values are between 0 and 100/mu_0 = 8e7 A/m (from WB range)
    return General_Validation(tuple0, 'WH', 0, 8e7)

# This validation function checks the Molar magnetic susceptibility, which has units of m^3/mol
# Checks for REASONABLE values.
def Validate_MMS(tuple0):
    # parameter definition (Molar magnetic susceptibility: double)
    # Reasonable values are between -1e-6 and 1e-6 m^3/mol (based on CRC Handbook,
    # Dy has highest MMS at room temp (1.85e-7 m^3/mol))
    return General_Validation(tuple0, 'MMS', -1e-6, 1e-6)

# This validation function checks the Mass magnetic susceptibility, which has units of m^3/kg
# Checks for REASONABLE values.
def Validate_MSS(tuple0):
    # parameter definition (Mass magnetic susceptibility: double)
    # Reasonable values are between -5e-8 and 5e-6 m^3/kg (Conversion of Dy MMS to MSS gives
    # 1.13e-6 m^3/kg. I made the lower bound smaller because diamagnetic materials
    # aren't as strongly magnetic)
    return General_Validation(tuple0, 'MSS', -5e-8, 5e-6)

# This validation function checks the Magnetic permeability, which has units of H/m
# Checks for REASONABLE values.
def Validate_MP(tuple0):
    # parameter definition (Magnetic permeability: double)
    # Reasonable values are between 0 and 1.0097*mu_0*2 H/m (Conversion of Dy MSS to MP gives
    # 1.0097*mu_0, and it's 0 for a superconductor)
    return General_Validation(tuple0, 'MP', 0, 2.54e-6)

# This validation function checks the Relative magnetic permeability, which has units of None
# Checks for REASONABLE values.
def Validate_MPR(tuple0):
    # parameter definition (Relative magnetic permeability: double)
    # Reasonable values are between 0 and 1.02 (Conversion of Dy MSS to MP gives
    # 1.0097*mu_0 for MP)
    return General_Validation(tuple0, 'MPR', 0, 1.02)

# This validation function checks the electrical resistivity, which has units of ohm*m
# Checks for REASONABLE values.
def Validate_ER(tuple0):
    # parameter definition (Electrical resistivity: double)
    # Reasonable values are between 0 and 5e3 ohm*m (highest we have is 1e3 for Si,
    # ignoring ridiculously high values we have on a ceramic)
    return General_Validation(tuple0, 'ER', 0, 5e3)

# This validation function checks the electrical resistivity at ref. geom., which has units of ohm*m
# Checks for REASONABLE values.
def Validate_ERX(tuple0):
    # parameter definition (Electrical resistivity at reference geometry: double)
    # Reasonable values are between 0 and 5e3 ohm*m (here we use the same range as ER)
    return General_Validation(tuple0, 'ERX', 0, 5e3)

# This validation function checks the electrical conductivity, which has units of S/m
# Checks for REASONABLE values.
def Validate_EC(tuple0):
    # parameter definition (Electrical conductivity: double)
    # Reasonable values are between 0 and 1e12 S/m (highest we have is 5.18e10)
    return General_Validation(tuple0, 'EC', 0, 1e12)

# This validation function checks the wavelength, which has units of angstrom
# Checks for REASONABLE values.
def Validate_WL(tuple0):
    # parameter definition (Wavelength: double)
    # Reasonable values are between 500 and 1e4 angstrom
    return General_Validation(tuple0, 'WL', 500, 1e4)

# This validation function checks the Mass, which has units of g
# Checks for REASONABLE values.
def Validate_mas(tuple0):
    # parameter definition (Mass: double)
    # Reasonable values are between 0 and 1e6 g
    return General_Validation(tuple0, 'mas', 0, 1e6)

# This validation function checks the Number of atoms added, which has units of mol
# Checks for REASONABLE values.
def Validate_atm(tuple0):
    # parameter definition (Number of atoms added: double)
    # Reasonable values are between 0 and 1000 mols, inclusive (rough range)
    return General_Validation(tuple0, 'atm', 0, 1e3, inclusive = True)

# This validation function checks the Number of molecules added, which has units of mol
# Checks for REASONABLE values.
def Validate_mol(tuple0):
    # parameter definition (Number of molecules added: double)
    # Reasonable values are between 0 and 1000 mols, inclusive (rough range)
    return General_Validation(tuple0, 'mol', 0, 1e3, inclusive = True)

# This validation function checks the Weight fraction, which has units of None
# Checks for REASONABLE values.
def Validate_W(tuple0):
    # parameter definition (Weight fraction: double)
    # Reasonable values are between 0 and 1, not inclusive (since we
    # want separate data sets for pures)
    return General_Validation(tuple0, 'W', 0, 1)

# This validation function checks the Mole fraction, which has units of None
# Checks for REASONABLE values.
def Validate_X(tuple0):
    # parameter definition (Mole fraction: double)
    # Reasonable values are between 0 and 1, not inclusive (since we
    # want separate data sets for pures)
    return General_Validation(tuple0, 'X', 0, 1)

# This validation function checks the Volume fraction of phase, which has units of None
# Checks for REASONABLE values.
def Validate_VOP(tuple0):
    # parameter definition (Volume fraction of phase: double)
    # Reasonable values are between 0 and 1, not inclusive (
    # since we want separate data sets for pures)
    return General_Validation(tuple0, 'VOP', 0, 1)

# This validation function checks the Number of phases, which has units of None
# Checks for REASONABLE values.
def Validate_NOP(tuple0):
    # parameter definition (Number of phases: integer)
    # Reasonable values are between 1 and 3, inclusive
    # (three phases can exist at triple point, for example)
    return General_Validation(tuple0, 'NOP', 1, 3, inclusive = True, is_int = True)

# This validation function checks the Step, which has units of None
# Checks for REASONABLE values.
def Validate_ste(tuple0):
    # parameter definition (Step: integer)
    # Reasonable values are between 1 and 3, inclusive
    # (three phases can exist at triple point, for example)
    return General_Validation(tuple0, 'ste', 0, 1000, inclusive = True, is_int = True)

# This validation function checks the Heating rate, which has units of K/s
# Checks for REASONABLE values.
def Validate_hrt(tuple0):
    # parameter definition (Heating rate: double)
    # Reasonable values are between -1e4 and 1e8 K/s (I assume we can heat a lot
    # faster than we can cool things)
    return General_Validation(tuple0, 'hrt', -1e4, 1e8, inclusive = True)

# This validation function checks the Compressibility factor, which has units of None
# Checks for REASONABLE values.
def Validate_Z(tuple0):
    # parameter definition (Compressibility factor: double)
    # Reasonable values are between 0 and 1e-4 (highest we have is 1.56e-5)
    return General_Validation(tuple0, 'Z', 0, 1e-4)

# This validation function checks the Critical compressibility factor, which has units of None
# Checks for REASONABLE values.
def Validate_ZC(tuple0):
    # parameter definition (Critical compressibility factor: double)
    # Reasonable values are between 0 and 1e-4 (used same range as Z)
    return General_Validation(tuple0, 'ZC', 0, 1e-4)

# This validation function checks the Adiabatic compressibility, which has units of None
# Checks for REASONABLE values.
def Validate_VPA(tuple0):
    # parameter definition (Adiabatic compressibility: double)
    # Reasonable values are between 0 and 1e-4 (used same range as Z)
    return General_Validation(tuple0, 'VPA', 0, 1e-4)

# This validation function checks the Enthalpy function {H(T)-H(0)}/T, which has units of J/K/mol
# Checks for REASONABLE values.
def Validate_HT(tuple0):
    # parameter definition (Enthalpy function {H(T)-H(0)}/T: double)
    # Reasonable values are between UNKNOWN AND UNKNOWN
    return General_Validation(tuple0, 'H/T', -1e12, 1e12)

# This validation function checks the Equilibrium constant - molarity basis, which has units of (mol/dm^3)^n
# Checks for REASONABLE values.
def Validate_KJ(tuple0):
    # parameter definition (Equilibrium constant - molarity basis: double)
    # Reasonable values are between UNKNOWN AND UNKNOWN
    return General_Validation(tuple0, 'KJ', -1e12, 1e12)

# This validation function checks the Equilibrium constant - mole fraction basis, which has units of None
# Checks for REASONABLE values.
def Validate_KX(tuple0):
    # parameter definition (Equilibrium constant - mole fraction basis: double)
    # Reasonable values are between UNKNOWN AND UNKNOWN
    return General_Validation(tuple0, 'KX', -1e12, 1e12)

# This validation function checks the Equilibrium constant - pressure basis, which has units of kPa^n
# Checks for REASONABLE values.
def Validate_KP(tuple0):
    # parameter definition (Equilibrium constant - pressure basis: double)
    # Reasonable values are between UNKNOWN AND UNKNOWN
    return General_Validation(tuple0, 'KP', -1e12, 1e12)

# This validation function checks the Excess virial coefficient, which has units of m^3/mol
# Checks for REASONABLE values.
def Validate_VVE(tuple0):
    # parameter definition (Excess virial coefficient: double)
    # Reasonable values are between UNKNOWN AND UNKNOWN
    return General_Validation(tuple0, 'VVE', -1e12, 1e12)

# This validation function checks the Fluidity, which has units of None
# Checks for REASONABLE values.
def Validate_NFL(tuple0):
    # parameter definition (Fluidity: double)
    # Reasonable values are between UNKNOWN AND UNKNOWN
    return General_Validation(tuple0, 'NFL', -1e12, 1e12)

# This validation function checks the Frequency, which has units of MHz
# Checks for REASONABLE values.
def Validate_WF(tuple0):
    # parameter definition (Frequency: double)
    # Reasonable values are between 0 AND UNKNOWN
    return General_Validation(tuple0, 'WF', 0, 1e12)

# This validation function checks the Gibbs energy function {G(T)-H(0)}/T, which has units of J/K/mol
# Checks for REASONABLE values.
def Validate_GT(tuple0):
    ##parameter definition (Gibbs energy function {G(T)-H(0)}/T: double)
    # parameter definition (Gibbs energy function: double)
    # Reasonable values are between UNKNOWN AND UNKNOWN
    return General_Validation(tuple0, 'G/T', -1e12, 1e12)

# This validation function checks the Joule-Thomson coefficient, which has units of K/kPa
# Checks for REASONABLE values.
def Validate_TJT(tuple0):
    # parameter definition (Joule-Thomson coefficient: double)
    # Reasonable values are between UNKNOWN AND UNKNOWN
    return General_Validation(tuple0, 'TJT', -1e12, 1e12)

# This validation function checks the Langmuir surface area, which has units of m^2/g
# Checks for REASONABLE values.
def Validate_LAR(tuple0):
    # parameter definition (Langmuir surface area: double)
    # Reasonable values are between 0 AND UNKNOWN
    return General_Validation(tuple0, 'LAR', 0, 1e12)

# This validation function checks the Pressure coefficient of enthalpy, which has units of J/kPa/mol
# Checks for REASONABLE values.
def Validate_HPT(tuple0):
    # parameter definition (Pressure coefficient of enthalpy: double)
    # Reasonable values are between UNKNOWN AND UNKNOWN
    return General_Validation(tuple0, 'HPT', -1e12, 1e12)

# This validation function checks the Refractive index (other wavelength), which has units of None
# Checks for REASONABLE values.
def Validate_RIX(tuple0):
    ##parameter definition (Refractive index (other wavelength): double)
    # parameter definition (Refractive index: double)
    # Reasonable values are between 1 AND UNKNOWN
    return General_Validation(tuple0, 'RIX', 1, 1e12)

# This validation function checks the Thermal pressure coefficient, which has units of kPa/K
# Checks for REASONABLE values.
def Validate_PTV(tuple0):
    # parameter definition (Thermal pressure coefficient: double)
    # Reasonable values are between UNKNOWN AND UNKNOWN
    return General_Validation(tuple0, 'PTV', -1e12, 1e12)

# This validation function checks the Thermodynamic equilibrium constant, which has units of None
# Checks for REASONABLE values.
def Validate_KT(tuple0):
    # parameter definition (Thermodynamic equilibrium constant: double)
    # Reasonable values are between UNKNOWN AND UNKNOWN
    return General_Validation(tuple0, 'KT', -1e12, 1e12)

# This validation function checks the Heating rate(sign), which has units of None
# Checks for POSSIBLE values.
def Validate_hrts(tuple0):
    ##parameter definition (Heating rate(sign): string)
    # parameter definition (Heating rate: string)
    name = tuple0[5].lower()
    value = tuple0[4]
    fail_string = "value: "+value
    if value == '+' or value == '-':
        return ["bool","True",0.0,"",name]
    else:
        return ["bool","False",0.0,"",name]

# This validation function checks the Pressurizing rate(sign), which has units of None
# Checks for POSSIBLE values.
def Validate_prts(tuple0):
    ##parameter definition (Pressurizing rate(sign): string)
    # parameter definition (Pressurizing rate: string)
    name = tuple0[5].lower()
    value = tuple0[4]
    fail_string = "value: "+value
    if value == '+' or value == '-':
        return ["bool","True",0.0,"",name]
    else:
        return ["bool","False",0.0,"",name]
