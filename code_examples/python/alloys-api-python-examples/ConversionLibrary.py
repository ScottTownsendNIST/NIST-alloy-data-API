# This is the Conversion python library for Unit Tests of the TRC Data Objects. This library file
# will be parsed by the calling C++ program at runtime (NOT compile time). Because of this each
# function must be formatted in a specific manner so it can be parsed by the calling C++ application.
# For instance every python function definition must be of the format:
#       def "function_name"(tuple1,tuple2,...,tupleN):
#
# where the parameters each must be a tuple of the form (Note if using python 3 and above long is now int 
# so all long string values will need to be converted as int(long_value) not long(long_value) as in python 2):
#       (bool_value:string,int_value:string,long_value:string,float_value:string,string_value:string,variable_name:string,variable_units:string)
#
# and the python function will then use or convert then use the specific "value" that has data defined
# for it. Suppose the function needs a temperature float value and a heat capacity float value then the
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
# a conversion of data.  It important to note that python does not have doubles but only float data types but
# it is vital to maintain the expected input and return data type to the C++ in mind when writing these
# python functions. Even though the function will convert the string representation of a double/float value
# from the C++ to a float data type, the "parameter definition" and return data type must reflect the C++
# data type which might be either a float or a double! In general the C++ tends to use the C++ double
# over the float type.
#
# Return value is always a list object. Each returned data object in the list MUST comprise 5 return items in the list:
# 
#      [variable1_type,variable1_value,variable1_uncert,variable1_units,variable1_name,...,variableN_type,variableN_value,variableN_uncert,variableN_units,variableN_name]
#
# and may return many data values which means that the size of the list MUST always be a factor of 5. It will be checked in the C++ code and issue an exception if it is not.
# I.E.
#      return ["double",101.5,0.003,"kPa","pressure","double",1325.2,.05,"K","temperature"]
#
#
# Import any python libraries needed to do the conversion work
import math as m
import os
import json
from pint import UnitRegistry
from pint.errors import DimensionalityError
from pint.errors import UndefinedUnitError

# Create the unit registry object that can be used to easily convert units.
ur = UnitRegistry()

# Open and read the TRC specific Units conversion file
TRC_units_conversion_file = os.path.dirname(os.path.realpath(__file__))+"/TRC_units_conversion.txt"
ur.load_definitions(TRC_units_conversion_file)

# This line is required so that the calling C++ program can know that the "Python" interpreter is to be used
rules_engine_language = "Python"

# Accessing the units can be done in variable assignment like
# x = 2.54*ur.cm
# Conversion can be done like so:
# x = x.to(ur.inches)
# Or it can automatically be done in place:
# x.ito(ur.inches)

# Temperature conversion from C to K function
# the temperature value should be a float. If empty or not a number return -999
# Remember that all numeric input values are really strings that contain the numeric value 
# and it's uncertainty. I.E. a float_value could be "10.3,.03". Likewise all output
# of numeric data must be a list with the numeric value and uncertainty.
def Temperature_CtoK(tuple0):
    # parameter definition (temperature: double)

    # Convert the 4th position of the parameter tuple to a temperature float value. Note tuples indices start at 0
    float_value_list = tuple0[3].split(',')
    temperature = float(float_value_list[0])
    uncertainty = float(float_value_list[1])
    #print(temperature)
    #print(uncertainty)

    # If the units of the temperature is NOT "C" then return -999 as this is a C to K conversion routine!
    temperature_units = tuple0[6]
    #print(temperature_units)
    if temperature_units is None or temperature_units != "C":
        return ["double",-999,uncertainty,"K","temperature"]

    # If temperature not a number or empty return a number < -273.15 to let the calling application know an error happened
    if temperature is None or m.isnan(temperature):
        return ["double",-999,uncertainty,"K","temperature"]

    if temperature > -273.15:
        return ["double",temperature+273.15,uncertainty,"K","temperature"]
    else:
        return ["double",0.0,uncertainty,"K","temperature"]

# Temperature conversion from F to K function
# the temperature value should be a float. If empty or not a number return -999
# Remember that all numeric input values are really strings that contain the numeric value 
# and it's uncertainty. I.E. a float_value could be "10.3,.03". Likewise all output
# of numeric data must be a list with the numeric value and uncertainty.
def Temperature_FtoK(tuple0):
    # parameter definition (temperature: double)

    # Convert the 4th position of the parameter tuple to a temperature float value. Note tuples indices start at 0
    float_value_list = tuple0[3].split(',')
    temperature = float(float_value_list[0])
    uncertainty = float(float_value_list[1])
    #print(temperature)
    #print(uncertainty)

    # If the units of the temperature is NOT "F" then return -999 as this is a F to K conversion routine!
    temperature_units = tuple0[6]
    #print(temperature_units)
    if temperature_units is None or temperature_units != "F":
        return ["double",-999,uncertainty,"K","temperature"]

    # If temperature not a number or empty return a number < -273.15 to let the calling application know an error happened
    if temperature is None or m.isnan(temperature):
        return ["double",-999,uncertainty,"K","temperature"]

    temperature = (temperature-32)*(5/9)+273.15
    return ["double",temperature,uncertainty*(5/9),"K","temperature"]

# Temperature conversion from R to K function
# the temperature value should be a float. If empty or not a number return -999
# Remember that all numeric input values are really strings that contain the numeric value 
# and it's uncertainty. I.E. a float_value could be "10.3,.03". Likewise all output
# of numeric data must be a list with the numeric value and uncertainty.
def Temperature_RtoK(tuple0):
    # parameter definition (temperature: double)

    # Convert the 4th position of the parameter tuple to a temperature float value. Note tuples indices start at 0
    float_value_list = tuple0[3].split(',')
    temperature = float(float_value_list[0])
    uncertainty = float(float_value_list[1])
    #print(temperature)
    #print(uncertainty)

    # If the units of the temperature is NOT "R" then return -999 as this is a R to K conversion routine!
    temperature_units = tuple0[6]
    #print(temperature_units)
    if temperature_units is None or temperature_units != "R":
        return ["double",-999,uncertainty,"K","temperature"]

    # If temperature not a number or empty return a number < -273.15 to let the calling application know an error happened
    if temperature is None or m.isnan(temperature):
        return ["double",-999,uncertainty,"K","temperature"]

    temperature = temperature*(5/9)
    return ["double",temperature,uncertainty*(5/9),"K","temperature"]

# Temperature conversion from K to C function
# the temperature value should be a float. If empty or not a number return -999
# Remember that all numeric input values are really strings that contain the numeric value 
# and it's uncertainty. I.E. a float_value could be "10.3,.03". Likewise all output
# of numeric data must be a list with the numeric value and uncertainty.
def Temperature_KtoC(tuple0):
    # parameter definition (temperature: double)

    # Convert the 4th position of the parameter tuple to a temperature float value. Note tuples indices start at 0
    float_value_list = tuple0[3].split(',')
    temperature = float(float_value_list[0])
    uncertainty = float(float_value_list[1])
    print(temperature)
    print(uncertainty)

    # If the units of the temperature is NOT "K" then return -999 as this is a K to C conversion routine!
    temperature_units = tuple0[6]
    print(temperature_units)
    if temperature_units is None or temperature_units != "K":
        return ["double",-999,uncertainty,"C","temperature"]

    # If temperature not a number or empty return a number < -273.15 to let the calling application know an error happened
    if temperature is None or m.isnan(temperature):
        return ["double",-999,uncertainty,"C","temperature"]

    if temperature > 0:
        return ["double",temperature-273.15,uncertainty,"C","temperature"]
    else:
        return ["double",-273.15,uncertainty,"C","temperature"]

# Temperature conversion from K to F function
# the temperature value should be a float. If empty or not a number return -999
# Remember that all numeric input values are really strings that contain the numeric value 
# and it's uncertainty. I.E. a float_value could be "10.3,.03". Likewise all output
# of numeric data must be a list with the numeric value and uncertainty.
def Temperature_KtoF(tuple0):
    # parameter definition (temperature: double)

    # Convert the 4th position of the parameter tuple to a temperature float value. Note tuples indices start at 0
    float_value_list = tuple0[3].split(',')
    temperature = float(float_value_list[0])
    uncertainty = float(float_value_list[1])
    print(temperature)
    print(uncertainty)

    # If the units of the temperature is NOT "K" then return -999 as this is a K to F conversion routine!
    temperature_units = tuple0[6]
    print(temperature_units)
    if temperature_units is None or temperature_units != "K":
        return ["double",-999,uncertainty,"F","temperature"]

    # If temperature not a number or empty return a number < -273.15 to let the calling application know an error happened
    if temperature is None or m.isnan(temperature):
        return ["double",-999,uncertainty,"F","temperature"]

    temperature = (temperature-273.15)*(9/5)+32
    return ["double",temperature,uncertainty*(9/5),"F","temperature"]
    
# Temperature conversion from K to R function
# the temperature value should be a float. If empty or not a number return -999
# Remember that all numeric input values are really strings that contain the numeric value 
# and it's uncertainty. I.E. a float_value could be "10.3,.03". Likewise all output
# of numeric data must be a list with the numeric value and uncertainty.
def Temperature_KtoR(tuple0):
    # parameter definition (temperature: double)

    # Convert the 4th position of the parameter tuple to a temperature float value. Note tuples indices start at 0
    float_value_list = tuple0[3].split(',')
    temperature = float(float_value_list[0])
    uncertainty = float(float_value_list[1])
    print(temperature)
    print(uncertainty)

    # If the units of the temperature is NOT "K" then return -999 as this is a K to R conversion routine!
    temperature_units = tuple0[6]
    print(temperature_units)
    if temperature_units is None or temperature_units != "K":
        return ["double",-999,uncertainty,"R","temperature"]

    # If temperature not a number or empty return a number < -273.15 to let the calling application know an error happened
    if temperature is None or m.isnan(temperature):
        return ["double",-999,uncertainty,"R","temperature"]

    temperature = (temperature-273.15)*(9/5)
    return ["double",temperature,uncertainty*(9/5),"R","temperature"]
    
# Automatically converts whatever input value
# it receives into base SI units.
def Into_SI_Units(tuple0):
    # parameter definition (value: double)

    return Into_DB_Units(tuple0)

    value_input = tuple0[3].split(',')
    value_name = tuple0[5]
    original_units = tuple0[6]
    original_value = float(value_input[0])
    original_uncertainty = float(value_input[1])
    
    # Now before call PINT to do any conversion check for temperature units
    if original_units == 'C':
        return ['double', original_value+273.15, original_uncertainty, 'K', value_name]
    elif original_units == 'F':
        return ['double', (original_value-32)*(5/9)+273.15, original_uncertainty*(5/9), 'K', value_name]
    elif original_units == 'K':
        return ['double', original_value,original_uncertainty, 'K', value_name]
    elif original_units == 'R':
        return ['double', original_value*(5/9), original_uncertainty*(5/9), 'K', value_name]
    # If the units contains 'C' but is not equal to just 'C',
    # we can simply replace 'C' with 'K' because the conversion
    # is only a shift
    elif original_units.find('C') != -1:
        original_units = original_units.replace('C','K')
    # If it contains 'F', we have to multiply or divide by the conversion
    # factor depending on whether 'F' is in the numerator or denominator
    elif original_units.find('F') != -1:
        if original_units.find('*F') != -1:
            original_units = original_units.replace('*F','*K')
            original_value *= 5/9
            original_uncertainty *= 5/9
        elif original_units.find('/F') != -1:
            original_units = original_units.replace('/F','/K')
            original_value /= 5/9
            original_uncertainty /= 5/9
        else:
            original_units = original_units.replace('F','K')
            original_value *= 5/9
            original_uncertainty *= 5/9
    # The conversion for 'R' is the same as for 'F'
    elif original_units.find('R') != -1:
        if original_units.find('*R') != -1:
            original_original_units = original_units.replace('*R','*K')
            original_value *= 5/9
            original_uncertainty *= 5/9
        elif original_units.find('/R') != -1:
            original_original_units = original_units.replace('/R','/K')
            original_value /= 5/9
            original_uncertainty /= 5/9
        else:
            original_units = original_units.replace('R','K')
            original_value *= 5/9
            original_uncertainty *= 5/9
                
    if value_name.find('P') == 1 and value_name.find('PHSF') == -1:
        if original_units == "kPa":
            return ['double', original_value,original_uncertainty, original_units, value_name]
        elif original_units == "atm":
            original_units = 'atmosphere'
    
    converted_value = (original_value*ur[original_units]).to_base_units().magnitude
    converted_uncertainty = (original_uncertainty*ur[original_units]).to_base_units().magnitude
    new_units = ('{0.units}'.format((original_value*ur[original_units]).to_base_units())).replace(' ','')
    return ['double', converted_value, converted_uncertainty, new_units, value_name]

# Automatically converts the input from tuple0
# into Database units. The property value will be in the string as only numeric data will be processed since non-numeric data will not need units converted...
def Into_DB_Units(tuple0):
    # parameter definition (value: double)

    value_input = tuple0[3].split(',')
    value_name = tuple0[5] # the value_name is the property symbol
    original_units = tuple0[6]
    original_value = float(value_input[0])
    original_uncertainty = float(value_input[1])
    # If the original_units is S (keep the units as they are in the correct units) or D (unknown)
    # just return the input values
    if original_units == 'S' or original_units == 'D' or original_units == 'Unknown':
        return ['double',original_value,original_uncertainty,original_units,value_name]

    converted_list = Convert_To_DB_Units(original_value, original_uncertainty, original_units, value_name)
    if isinstance(converted_list[0],float) == False:
        converted_value = float('nan')
    else:
        converted_value = converted_list[0]

    if isinstance(converted_list[1],float) == False:
        converted_uncertainty = float('nan')
    else:
        converted_uncertainty = converted_list[1]
    
    converted_units = converted_list[2]
    #print(converted_value, converted_uncertainty, converted_units, value_name)
    return ['double', converted_value, converted_uncertainty, converted_units, value_name]

# Automatically converts the input from tuple0
# into the units given by tuple1.
def Into_Desired_Units(tuple0, tuple1):
    # parameter definition (value: double, units: string)
    
    #Note: This function will generally not work for temperature conversions.
    value_input = tuple0[3].split(',')
    value_name = tuple0[5]
    original_units = tuple0[6]
    original_value = float(value_input[0])
    original_uncertainty = float(value_input[1])
    # Note: the new units may be at the 4th index depending on whether you pass it
    # in the string location or in the units location. I assumed they would be
    # in the string location.
    new_units = tuple1[4]
    converted_value = (original_value*ur[original_units]).to(new_units).magnitude
    converted_uncertainty = (original_uncertainty*ur[original_units]).to(new_units).magnitude
    return ['double', converted_value, converted_uncertainty, new_units, value_name]

# Takes a value from Python and converts it into database units.
# Since it's only called internally, we don't need the parameter definition.
# prop_sym is the database property symbol.
def Convert_To_DB_Units(value, uncertainty, original_units, prop_sym):
    # Define the units to be the original units first
    units = original_units
    
    # Load the UnitsStandard.json and UnitsSpecial.json files in to JSON objects
    try:
        units_standard_json_file = os.path.dirname(os.path.realpath(__file__))+"/UnitsStandard.json"
        units_standard_handle = open(units_standard_json_file,'r')
        units_standard_data=units_standard_handle.read()
    
        # Now parse the data into JSON objects
        try:
            units_standard_json = json.loads(units_standard_data)

            # Now need to do a try block to catch any cases where the prop_sym is NOT in the json
            try:
                units = units_standard_json[prop_sym.upper()]
            except KeyError:
                if original_units == 'C' or original_units == 'K' or original_units == 'F' or original_units == 'R':
                    units = ''
        except json.JSONDecodeError:
            if original_units == 'C' or original_units == 'K' or original_units == 'F' or original_units == 'R':
                units = ''

    except OSError as err:
        if original_units == 'C' or original_units == 'K' or original_units == 'F' or original_units == 'R':
            units = ''

    # If the units are already in DB units, we don't need to convert.
    if original_units == units:
        return [value,uncertainty,original_units]
    else:
        # Special case conversions
        # Manually define the conversions
        
        # We have to do temperature unit conversions manually because pint
        # does not handle conversions with shifts.
        # If the unit is just temperature, we just perform the conversion to Kelvin.
        if original_units == 'C':
            return [value+273.15,uncertainty,'K']
        elif original_units == 'F':
            return [(value-32)*(5/9)+273.15,uncertainty*(5/9),'K']
        elif original_units == 'K':
            return [value,uncertainty,'K']
        elif original_units == 'R':
            return [value*(5/9),uncertainty*(5/9),'K']
        
        # Since units W/m/K may have multiple conversions (i.e. from cal/cm/S/K and btu/ft/hr/F)
        # and pint only allows one conversion must do the second conversion manually here
        if units.find('W/m/K') != -1:
            #print('original_units: '+original_units)
            #print('units: '+units)
            if original_units.find('calorie/cm/S/K') != -1:
                return [value*419,uncertainty*419,units]
            elif original_units.find('cal/cm/S/K') != -1:
                return [value*419,uncertainty*419,units]
            elif original_units.find('Btu/ft/hr/F') != -1 or original_units.find('btu/ft/hr/F') != -1:
                return [value*1.7307,uncertainty*1.7307,units]
        
        # Convert Mass units for CPW, CVW, CPHEW to database units
        if units.find('J/K/kg') != -1:
            #print('original_units: '+original_units)
            #print('units: '+units)
            if original_units.find('J/K/g') != -1 or original_units.find('J/g/K') != -1:
                return [value*0.001,uncertainty*0.001,units]
            elif original_units.find('calorie/g/K') != -1 or original_units.find('calorie/K/g') != -1:
                return [value*0.24,uncertainty*0.24,units]
            elif original_units.find('kilocalorie/kg/K') != -1 or original_units.find('kilocalorie/K/kg') != -1:
                return [value*0.24,uncertainty*0.24,units]
            elif original_units.find('kilocalorie/g/K') != -1 or original_units.find('kilocalorie/K/g') != -1:
                return [value*240,uncertainty*240,units]
            elif original_units.find('calorie/kg/K') != -1 or original_units.find('calorie/K/kg') != -1:
                return [value*0.00024,uncertainty*0.00024,units]
            elif original_units.find('Btu/R/lb') != -1 or original_units.find('btu/F/lb') != -1:
                return [value*0.00024,uncertainty*0.00024,units]
            elif original_units.find('Btu/lb/R') != -1 or original_units.find('btu/lb/F') != -1:
                return [value*0.00024,uncertainty*0.00024,units]
        
        # Convert Mass units for HW, HTRW, HEXW to database units
        if units.find('kJ/kg') != -1:
            #print('original_units: '+original_units)
            #print('units: '+units)
            if original_units.find('J/g') != -1:
                return [value,uncertainty,units]
            elif original_units.find('kJ/g') != -1:
                return [value*0.001,uncertainty*0.001,units]
            elif original_units.find('J/kg') != -1:
                return [value*1000,uncertainty*1000,units]
            elif original_units.find('calorie/g') != -1:
                return [value*0.24,uncertainty*0.24,units]
            elif original_units.find('kilocalorie/kg') != -1:
                return [value*0.24,uncertainty*0.24,units]
            elif original_units.find('kilocalorie/g') != -1:
                return [value*240,uncertainty*240,units]
            elif original_units.find('calorie/kg') != -1:
                return [value*0.00024,uncertainty*0.00024,units]
            elif original_units.find('Btu/lb') != -1:
                return [value*0.43,uncertainty*0.43,units]

        # Since units J/K/mol may have multiple conversions (i.e. from J/g, cal/g/K, and Btu/R/lb)
        # and pint only allows one conversion must do the second conversion manually here
        if units.find('J/K/mol') != -1:
            #print('original_units: '+original_units)
            #print('units: '+units)
            if original_units.find('calorie/cm/S/K') != -1:
                return [value*4.184,uncertainty*4.184,units]
            elif original_units.find('cal/cm/S/K') != -1:
                return [value*4.184,uncertainty*4.184,units]
            elif original_units.find('Btu/K/lb') != -1 or original_units.find('btu/K/lb') != -1:
                return [value*2.326,uncertainty*2.326,units]
            elif original_units.find('Btu/C/lb') != -1 or original_units.find('btu/C/lb') != -1:
                return [value*2.326,uncertainty*2.326,units]
            elif original_units.find('Btu/R/lb') != -1 or original_units.find('btu/R/lb') != -1:
                return [value*4.1868,uncertainty*4.1868,units]
            elif original_units.find('Btu/F/lb') != -1 or original_units.find('btu/F/lb') != -1:
                return [value*4.1868,uncertainty*4.1868,units]
            elif original_units.find('J/g') != -1:
                return [value,uncertainty,units]
            elif original_units.find('calorie/g/K') != -1:
                return [value*4.184,uncertainty*4.184,units]
            elif original_units.find('cal/g/K') != -1:
                return [value*4.184,uncertainty*4.184,units]
        
        # Since kJ/mol units may have multiple conversions (i.e. from J/g and Btu/lb)
        # and pint only allows one conversion must do the second conversion manually here
        if units.find('kJ/mol') != -1:
            #print('original_units: '+original_units)
            #print('units: '+units)
            if original_units.find('Btu/lb') != -1 or original_units.find('btu/lb') != -1:
                return [value*2.326,uncertainty*2.326,units]
            elif original_units.find('J/g') != -1:
                return [value,uncertainty,units]
            elif original_units.find('calorie/g') != -1:
                return [value/4186806.0,uncertainty/4186806.0,units]

        # Do conversion of microOhm*cm or Ohm*cm units to Ohm*m
        if units.find('Ohm*m') != -1 or units.find('ohm*m') != -1:
            #print('original_units: '+original_units)
            #print('units: '+units)
            if original_units.find('microOhm*cm') != -1 or original_units.find('microohm*cm') != -1:
                return [value/(10**8),uncertainty/(10**8),units]
            elif original_units.find('microOhm*m') != -1 or original_units.find('microohm*m') != -1:
                return [value/(10**6),uncertainty/(10**6),units]
            elif original_units.find('Ohm*cm') != -1 or original_units.find('ohm*cm') != -1:
                return [value/(10**2),uncertainty/(10**2),units]

        # Do conversion of kg/cm**2 units to kPa
        if units.find('kPa') != -1:
            #print('original_units: '+original_units)
            #print('units: '+units)
            if original_units.find('kg/cm**2') != -1:
                return [value*98.0665,uncertainty*98.0665,units]

        # Do conversion of Gause or kiloGauss to Tesla: 1 Gauss = .0001 Tesla and 1 kiloG = .1 Telsa
        if units.find('T') != -1:
            if original_units.find('Gauss') != -1 or original_units.find('gauss') != -1:
                return [value*.0001,uncertainty*.0001,units]
            elif original_units.find('kiloGauss') != -1 or original_units.find('kilogauss') != -1 or original_units.find('kiloG') != -1 or original_units.find('kG') != -1:
                return [value*.1,uncertainty*.1,units]

        # Do conversion of Oersted to Ampere/meter: 1 Gauss = .0001 Tesla and 1 kiloG = .1 Telsa
        if units.find('Ampere/m') != -1 or units.find('ampere/m') != -1:
            if original_units.find('Oersted') != -1 or original_units.find('oersted') != -1:
                return [value*79.5578,uncertainty*79.5578,units]

        # Since GDC sometimes has mistakes like K/h which is Kelvin/Hour which must be K/hr
        # so handle these mistakes
        if original_units == 'K/h':
            original_units = 'K/hr'

        # Since the database might have angstroms written as 'A' which pint thinks
        # is Amperes, we should convert A to be 'angstrom' (as long as the
        # unit in question is Angstroms, which it is for the properties WL,LA,LB,LC).
        if prop_sym == 'WL' or prop_sym == 'LA' or prop_sym == 'LB' or prop_sym == 'LC':
            #print("Trying to figure out what is going on with angstromg!!")
            #print('original_units: '+original_units)
            #print('units: '+units)
            #print("")
            if original_units.find('A') != -1 and original_units.find('Angstrom') == -1 and original_units.find('angstrom') == -1:
                original_units = original_units.replace('A','angstrom')
            elif original_units.find('Angstrom') != -1:
                original_units = original_units.replace('Angstrom','angstrom')
            if units.find('A') != -1 and units.find('Angstrom') == -1 and units.find('angstrom') == -1:
                # Do conversion of kX units to angstrom
                if original_units.find('kX') != -1:
                    return [value*1.00202,uncertainty*1.00202,'angstrom']
                else:
                    units = units.replace('A','angstrom')
            elif units.find('Angstrom') != -1:
                # Do conversion of kX units to angstrom
                if original_units.find('kX') != -1:
                    return [value*1.00202,uncertainty*1.00202,'angstrom']
                else:
                    units = units.replace('Angstrom','angstrom')
            elif units.find('angstrom') != -1 and original_units.find('kX') != -1:
                return [value*1.00202,uncertainty*1.00202,'angstrom']

        # Since the database might have amperes written as 'A' for property WH, we should convert to 'amperes'
        # to avoid confusion. Now 'A' is seen as Amperes by pint but the confusion is just too great to leave it
        if prop_sym == 'WH':
            if original_units.find('A') != -1 and original_units.find('Ampere') == -1 and original_units.find('ampere') == -1:
                original_units = original_units.replace('A','ampere')
            elif original_units.find('Ampere') != -1:
                original_units = original_units.replace('Ampere','ampere')
            if units.find('A') != -1 and units.find('Ampere') == -1 and units.find('ampere') == -1:
                units = units.replace('A','ampere')
            elif units.find('Ampere') != -1:
                units = units.replace('Ampere','ampere')

        if prop_sym == 'EC':
            if original_units == 'S/cm':
                units = 'S/m'
                return [value*100.0,uncertainty*100.0,units]

        # If the original value is dimensionless, we only want to return the value if the
        # units match the property units.
        if original_units == 'None' and units == 'None':
            return [value,uncertainty,'None']
        elif original_units == 'Unknown' and units == 'None':
            return [value,uncertainty,'None']
        elif original_units == 'None' and units != 'None':
            return [None,None,'None']
        elif original_units == 'Unknown' and units != 'None':
            return [None,None,'None']
        
        # Main conversion
        # Use pint to do the conversion.
        try:
            return [(value*ur[original_units]).to(units).magnitude,(uncertainty*ur[original_units]).to(units).magnitude,units]
        except DimensionalityError:
            try:
                temp_original_units = original_units.replace('/','_')
                temp_original_units = temp_original_units.replace('*','_')
                temp_units = units.replace('/','_')
                temp_units = temp_units.replace('*','_')
                return [(value*ur[temp_original_units]).to(temp_units).magnitude,(uncertainty*ur[temp_original_units]).to(temp_units).magnitude,units]
            except Exception as err:
                print("Exception: {0}".format(err))
                print("prop_sym: "+prop_sym)
                print("value: "+str(value))
                print("uncertainty: "+str(uncertainty))
                print("original_units: "+original_units)
                print("units: "+units)
                return [value,uncertainty,original_units]
        except UndefinedUnitError:
            try:
                temp_original_units = original_units.replace('/','_')
                temp_original_units = temp_original_units.replace('*','_')
                temp_units = units.replace('/','_')
                temp_units = temp_units.replace('*','_')
                return [(value*ur[temp_original_units]).to(temp_units).magnitude,(uncertainty*ur[temp_original_units]).to(temp_units).magnitude,units]
            except Exception as err:
                print("Exception: {0}".format(err))
                print("prop_sym: "+prop_sym)
                print("value: "+str(value))
                print("uncertainty: "+str(uncertainty))
                print("original_units: "+original_units)
                print("units: "+units)
                return [value,uncertainty,original_units]
        except Exception as err:
            print("Exception: {0}".format(err))
            print("prop_sym: "+prop_sym)
            print("value: "+str(value))
            print("uncertainty: "+str(uncertainty))
            print("original_units: "+original_units)
            print("units: "+units)
            return [value,uncertainty,original_units]

# This function, given a list of elements and a list of their subscripts in a compound,
# returns the molar weight of the compound.
# Since it is an internal function, it does not need the parameter definition.
def Get_Molar_Weight(elements, subscripts=None):
    # The below values come from the 90th edition of the Handbook of Chemistry and Physics
    molar_weights = {'Ac': 227.0277, 'Al': 26.98153868, 'Am': 243.0614, 'Sb': 121.7601, 'Ar': 39.9481, 'As': 74.921602, 'At': 209.9871, 'Ba': 137.3277, 'Bk': 247.0703, 
                    'Be': 9.0121823, 'Bi': 208.980401, 'Bh': 264.12, 'B': 10.8117, 'Br': 79.9041, 'Cd': 112.4118, 'Ca': 40.0784, 'Cf': 251.0796, 'C': 12.01078, 
                    'Ce': 140.1161, 'Cs': 132.90545192, 'Cl': 35.4532, 'Cr': 51.99616, 'Co': 58.9331955, 'Cu': 63.5463, 'Cm': 247.0704, 'Ds': 271, 'Db': 262.1141, 
                    'Dy': 162.5001, 'Es': 252.0830, 'Er': 167.2593, 'Eu': 151.9641, 'Fm': 257.0951, 'F': 18.99840325, 'Fr': 223.0197, 'Gd': 157.253, 'Ga': 69.7231, 
                    'Ge': 72.641, 'Au': 196.9665694, 'Hf': 178.492, 'Hs': 277, 'He': 4.0026022, 'Ho': 164.930322, 'H': 1.007947, 'In': 114.8183, 'I': 126.904473, 
                    'Ir': 192.2173, 'Fe': 55.8452, 'Kr': 83.7982, 'La': 138.905477, 'Lr': 262.1097, 'Pb': 207.21, 'Li': 6.9412, 'Lu': 174.96681, 'Mg': 24.30506, 
                    'Mn': 54.9380455, 'Mt': 268.1388, 'Md': 258.0984, 'Hg': 200.592, 'Mo': 95.962, 'Nd': 144.2423, 'Ne': 20.17976, 'Np': 237.0482, 'Ni': 58.69344, 
                    'Nb': 92.906382, 'N': 14.00672, 'No': 259.1010, 'Os': 190.233, 'O': 15.99943, 'Pd': 106.421, 'P': 30.9737622, 'Pt': 195.0849, 'Pu': 244.0642, 
                    'Po': 208.9824, 'K': 39.09831, 'Pr': 140.907652, 'Pm': 144.9127, 'Pa': 231.035882, 'Ra': 226.0254, 'Rn': 222.0176, 'Re': 186.2071, 'Rh': 102.905502, 
                    'Rg': 272.1535, 'Rb': 85.46783, 'Ru': 101.072, 'Rf': 261.1088, 'Sm': 150.362, 'Sc': 44.9559126, 'Sg': 266.1219, 'Se': 78.963, 'Si': 28.08553, 
                    'Ag': 107.86822, 'Na': 22.989769282, 'Sr': 87.621, 'S': 32.0655, 'Ta': 180.947882, 'Tc': 97.9072, 'Te': 127.603, 'Tb': 158.925352, 'Tl': 204.38332, 
                    'Th': 232.038062, 'Tm': 168.934212, 'Sn': 118.7107,'Ti': 47.8671, 'W': 183.841, 'Uub': 285, 'Uuh': 289, 'Uuq': 289, 'U': 238.028913, 'V': 50.84151, 
                    'Xe': 131.2936, 'Yb': 173.0545, 'Y': 88.905852, 'Zn': 65.382, 'Zr': 91.2242}
    # If only one element is passed, we just need to return the molar weight 
    # of that element
    if subscripts == None or type(elements) == str:
        return molar_weights[elements]
    # If more than one element is passed, the molar weight is the sum of all
    # the molar weights of the atoms.
    else:
        molar_weight = 0
        for i in range(len(subscripts)):
            molar_weight += subscripts[i]*molar_weights[elements[i]]
        return molar_weight

# This function converts a list of mol fractions to weight fractions and
# vice versa.
# Internal function, so we don't need the parameter definition line.
# You can pass the function a dummy value for elements if you want
# to provide your own molar weights (e.g. for compounds)
def Convert_Molar_Mass_Frac(elements, fractions, is_mass_frac, molar_weights = None):
    # If the molar weights are not given, we find them based on the elements. 
    # Otherwise, we use the list of molar weights given.
    if molar_weights == None:
        molar_weights = []
        for element in elements:
            molar_weights.append(Get_Molar_Weight(element))
    if is_mass_frac:
        mol_fractions = []
        for i in range(len(fractions)):
            mol_fractions.append(fractions[i]/molar_weights[i]/(sum([fractions[j]/molar_weights[j] for j in range(len(fractions))])))
        return mol_fractions
    else:
        weight_fractions = []
        for i in range(len(fractions)):
            weight_fractions.append(fractions[i]*molar_weights[i]/(sum([fractions[j]*molar_weights[j] for j in range(len(fractions))])))
        return weight_fractions

# Molar to mass value conversion function
# Called by another function in Python, so we don't need the parameter definition line.
# If it receives a unit that includes mols, it converts
# the mols to kg. If it receives a unit that includes
# microg, mg, kg, Mg, or g, it converts to mols. 
def Molar_Mass_Conversion(value, original_units, molar_weight):
    original_units = original_units.replace('mole', 'mol')
    prefixes = {'micro': 1e-6, 'u': 1e-6, 'm': 1e-3, '': 1, 'k': 1e3, 'M': 1e6}
    # For conversion to mass, if the mol is in the denominator, we divide by the atomic weight;
    # if it's in the numerator, we multiply by the atomic weight.
    # We also multiply or divide by 1000 to put it in kg.
    if (original_units.find('mol') != -1):
        if (original_units.find('*mol') != -1):
            value = value*molar_weight/1000
            new_units = original_units.replace('*mol','*kg')
        elif (original_units.find('/mol') != -1):
            value = value/molar_weight*1000
            new_units = original_units.replace('/mol','/kg')
        else:
            # If the first two conditions aren't met, then the
            # mol must be at the beginning of the string
            value = value*molar_weight/1000
            new_units = original_units.replace('mol','kg')
        return [value, new_units]

    # The mass conversion is reciprocal to the molar conversion, but we have to
    # be more careful searching for mass because of the prefixes.
    elif (original_units.find('g') != -1):
        # Check all the prefixes. If one of the prefixes matches, return the converted values.
        for prefix in ['micro', 'u', '', 'm', 'k', 'M']:
            if (original_units.find('*'+prefix+'g') != -1):
                value = value/molar_weight*prefixes[prefix]
                new_units = original_units.replace('*'+prefix+'g','*mol')
                return [value, new_units]
            elif (original_units.find('/'+prefix+'g') != -1):
                value = value*molar_weight/prefixes[prefix]
                new_units = original_units.replace('/'+prefix+'g','/mol')
                return [value, new_units]
            # If the first two conditions aren't met, then the
            # prefix+g must be at the beginning of the string
            elif (original_units.find(prefix+'g') == 0):
                value = value/molar_weight*prefixes[prefix]
                new_units = original_units.replace(prefix+'g','mol')
                return [value, new_units]
    else:
        # If the string doesn't contain mol or kg, we simply
        # return the input value and original units
        return [value, original_units]
    return [value, new_units]

# This is an internally called function, so it does not need a parameter definition.
# It's passed an array of strings in a format like ['0.85Al2O3','0.10SiO2','0.05Al'].
# The decimal at the start of the string is the fraction of that compound in the mixture,
# which is followed by the chemical formula for that compound.
# Returns an array of fractions and molar weights for each compound.
def Parse_Compound_List(compounds):
    fractions = []
    molar_weights = []
    for compound in compounds:
        elements = []
        subscripts = []
        elemInd = []
        for index, char in enumerate(compound):
            if char.isupper():
                elemInd.append(index)
                try:
                    # If a lowercase letter follows the capital letter,
                    # then we append both letters to the element name
                    if compound[index+1].islower():
                        elements.append(compound[index:index+2])
                    # Otherwise the element must have a single letter symbol
                    else:
                        elements.append(char)
                except:
                    # If there's an exception, it's because we tried to access 
                    # a character past the end of the compound string,
                    # meaning the element must have a single letter symbol.
                    elements.append(char)
                # If a capital letter directly follows another letter, there
                # must be an implied 1 subscript between the two.
                if compound[index-1].isalpha() and index > 0:
                    subscripts.append(1.0)
                # Otherwise, we take the range between the two element names
                # to get the subscript.
                elif len(elements) > 1:
                    subscripts.append(float(compound[elemInd[-2]+len(elements[-2]):elemInd[-1]]))
        # We need to add the subscript at the end of the compound if there is one,
        # since the above for loop does not check for that.
        if compound[-1].isdigit():
            subscripts.append(float(compound[elemInd[-1]+len(elements[-1]):]))
        # If there's no number at the end, the subscript is an implied 1.
        else:
            subscripts.append(1.0)

        molar_weights.append(Get_Molar_Weight(elements, subscripts))
        if len(compounds) == 1:
            fractions.append(1)
        else:
            fractions.append(float(compound[:elemInd[0]]))
    return fractions, molar_weights
    
# Processes the value to be passed to the actual
# conversion function for molar/mass conversion.
def Process_Value_For_Molar_Conversion(tuple0, tuple1, tuple2):
    # parameter definition (value: double, compound: string, mass fraction: bool)
    # For the compound string, the format should be as follows:
    # Begin with the fraction of each compound, separating different compounds
    # with commas. For instance, the string could be "0.85Al2O3,0.10SiO2,0.05Al"
    # The numbers following elements will be converted to molar fraction, but the coefficients could
    # be in mass fraction or mole fraction. The coefficients should begin with "0." to make
    # parsing easier.
    # If you want to pass only a single element, just put the chemical symbol in the compound string
    # (i.e. "Cu")
    # The mass fraction bool is true if the coefficients for the compounds are mass fractions, 
    # and false if the coefficients are mol fractions.
    value_input = tuple0[3].split(',')
    value_name = tuple0[5]
    original_units = tuple0[6]
    original_value = float(value_input[0])
    original_uncertainty = float(value_input[1])
    compounds = tuple1[4].split(',')
    is_mass_frac = (tuple2[0] == 'True')
    fractions, molar_weights = Parse_Compound_List(compounds)
    effective_molar_weight = 0
    # If the coefficients are given as mass fraction, we first convert to mol 
    # fraction to be able to calculate the effective molecular weight
    if is_mass_frac:
        mol_fractions = Convert_Molar_Mass_Frac(None, fractions, is_mass_frac, molar_weights)
    else:
        mol_fractions = fractions
        
    # We use a simplistic calculation for the effective molar weight.
    # This ignores the fact that compounds can have different molar weights
    # with the same fractional compositions. We simply add the mol fraction
    # of each component times that component's molar weight.
    for i in range(len(fractions)):
        effective_molar_weight += mol_fractions[i]*molar_weights[i]
    converted_value, new_units = Molar_Mass_Conversion(original_value, original_units, effective_molar_weight)
    converted_uncertainty, new_units = Molar_Mass_Conversion(original_uncertainty, original_units, effective_molar_weight)
    return ['double', converted_value, converted_uncertainty, new_units, value_name]
