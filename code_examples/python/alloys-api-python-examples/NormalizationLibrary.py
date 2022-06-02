# This is the Normalization python library for Unit Tests of the TRC Data Objects. This library file
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
# a normalization of data. It important to note that python does not have doubles but only float data types but
# it is vital to maintain the expected input and return data type to the C++ in mind when writing these
# python functions. Eventhough the function will convert the string representation of a double/float value
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
# Import any python libraries needed to do the normalization work. NOTE the Conversion library necessary to convert temperture from various units to "K"
import math as m
import ConversionLibrary as CL

# This line is required so that the calling C++ program can know that the "Python" interpreter is to be used
rules_engine_language = "Python"

# Temperature normalization function
def Temperature(tuple0,tuple1,tuple2):
    # Note that year and temperature_scale MUST come after temperature in order to make things work correctly in the C++. This is due to the fact that
    # year and temperature_scale may not be defined in a specific data set but rather defined in the Citation/Paper level of the data objects and it will
    # not be possible to properly populate the year and temperature_scale tuples in the parameter list above if either one comes before an actual data set
    # data array!
    # parameter definition (temperature: double,year: int,temperature_scale: string)

    # Convert the 4th position of the parameter tuple1 to a temperature float value. Note tuples indices start at 0 and python has only floats not doubles!
    float_value_list = tuple0[3].split(',')
    temperature_input = float(float_value_list[0])
    uncertainty_input = float(float_value_list[1])
    units_input = tuple0[6];
    # Convert the 2nd position of the parameter tuple2 to a year int value. Note tuples indices start at 0
    int_value_list = tuple1[1].split(',')
    year = int(int_value_list[0])

    # Get the temperature_scale from the tuple. It could be an empty string which means that no temperature_scale was found in the DataContainer object calling this function
    temperature_scale = tuple2[4]

    #print("First print")
    #print(tuple0)
    #print(tuple1)
    #print(tuple2)
    #print(temperature_input)
    #print(uncertainty_input)
    #print(units_input)
    #print(year)
    #print(temperature_scale)
    #print("")

    # If temperature not a number or empty return the missing temperature value of -999 (no temperature scale should ever report a temperature of -999.0)
    if (temperature_input is None) or m.isnan(temperature_input):
        return ["double",-999.0,uncertainty_input,units_input,"temperature"]

    # If temperature units is not "K" then convert to "K" before doing any normalization!
    temperature = temperature_input
    uncertainty = uncertainty_input
    units = units_input
    if units == "C":
        # The units are Celcius but must have Kelvin
        temperature = CL.Temperature_CtoK(tuple0)[1]
        uncertainty = CL.Temperature_CtoK(tuple0)[2]
        units = "K"
    elif units == "F":
        # The units are Fahrenheit but must have Kelvin
        temperature = CL.Temperature_FtoK(tuple0)[1]
        uncertainty = CL.Temperature_FtoK(tuple0)[2]
        units = "K"
    elif units == "R":
        # The units are Rankine but must have Kelvin
        temperature = CL.Temperature_RtoK(tuple0)[1]
        uncertainty = CL.Temperature_RtoK(tuple0)[2]
        units = "K"
    elif units is None or units != "K":
        # Must have valid units so the normalization can happen correctly
        return ["double",temperature,uncertainty,units,"temperature"]

    #print("Second print")
    #print(temperature)
    #print(units)
    #print("")
    # Now if both the year and temperature_scale are missing or empty then no normalization can happen so just return the input value
    temperature_scales_list = ["ITS-27","IPTS-48","IPTS-68","ITS-90","EPT-76","NBS-39",
                               "NBS-55","NPL-61","He4-58","He4-36","PRMI-54","PSU-54"]
    if temperature_scale in temperature_scales_list:
        use_temp_scale = "true"
        use_year = "false"
    elif year is None or m.isnan(year) or year < 1927:
        return ["double",temperature,uncertainty,units,"temperature"]
    else:
        use_year = "true"
        use_temp_scale = "false"

    # Note that if the temperature scale is ITS-90 then just return the input number. 
    # Also if no temperature scale and year is 1990 or greater then also just return the input number.
    # Note that it returns the number in its original units
    if use_temp_scale == "true":
        if temperature_scale.upper() == "ITS-90":
            return ["double",temperature,uncertainty,units,"temperature"]

    if use_year == "true" and year >= 1990:
        return ["double",temperature,uncertainty,units,"temperature"]

    # Need to get number of digits of temperature as that is the number of digits to round the answer to for return.
    # Note that I need to isolate the digits before the decimal point which is done by converting temperature to a string
    # then find the position of the "." in the string and pull the substring out that is digits after the decimal and find
    # that string length which is the number of digits to round to in the answer.
    temperature_string = str(temperature)
    decimal_pos = temperature_string.find('.')
    temperature_digits = temperature_string[decimal_pos+1:len(temperature_string)]
    digits_length = len(temperature_digits)+1

    # Now need to determine via either polynomials or other functions a value for the temperature based either on year or temperature scale and
    # the current value of the temperature. This will normalize all temperature data so that it will be represented in the ITS-90 scale regardless
    # of what scale it was initially measured or year it was measured.
    if use_temp_scale == "true": 
        temperature = Normalize_Temperature(temperature,temperature_scale)
    elif use_year == "true": 
        # Refer to "temperature range years condensed.pdf" to see where these ranges come from.
        if year < 1948 and temperature >= 93:
            temperature = Normalize_Temperature(temperature,"ITS-27")
        elif year < 1968 and temperature >= 93:
            temperature = Normalize_Temperature(temperature,"IPTS-48")
        elif (year >= 1968 and year < 1976 and temperature >= 14) or (year >= 1968 and temperature > 27):            
            temperature = Normalize_Temperature(temperature,"IPTS-68")
        elif (year >= 1939 and year < 1955 and temperature <= 16) or (year >= 1939 and year < 1976 and temperature < 14 and temperature > 5):
            temperature = Normalize_Temperature(temperature,"NBS-39")
        elif year == 1954 and temperature < 93 and temperature > 16:
            # This could be PRMI-54 or PSU-54, which have different conversions.
            # I just chose to set it to PRMI-54.
            temperature = Normalize_Temperature(temperature,"PRMI-54") 
        elif year >= 1955 and year < 1961 and temperature >= 14 and temperature < 93:
            temperature = Normalize_Temperature(temperature,"NBS-55") 
        elif year >= 1961 and year < 1968 and temperature >= 14 and temperature < 93:          
            temperature = Normalize_Temperature(temperature,"NPL-61") 
        elif year >= 1958 and temperature <= 5:
            temperature = Normalize_Temperature(temperature,"He4-58") 
        elif year >= 1976 and temperature > 5 and temperature <= 27:
            temperature = Normalize_Temperature(temperature,"EPT-76") 

    #print("Third print")
    #print(temperature)
    #print(units)
    #print("")
    return ["double",temperature,uncertainty,units,"temperature"]

# Function to return a normalized temperature value from ITS-27,IPTS-48,IPTS-68, and ITS-75 to ITS-90
def Normalize_Temperature(temperature_input,temperature_scale):
    # This is an internal only function that will not be called by C++ but rather from the Temperature function
    # so there will be no parameter line
    # For ITS-27, ITPS-48, IPTS-68 create lists of tuples that hold the ITS-27, ITS-48, IPTS-68 to ITS90 normalization values. 
    # These tuples will look like (note this is the same for ITPS-48 and IPTS-68 but just with a different list of tuples)
    # (T27,T27_delta) or (93.15,0.020) where T27_delta is T90-T27. The list of these tuples will then use a
    # formula to calculate the linear approximation given an input T27 value that falls between two T27 values
    # in the list to then return a T90 value for that input T27 value: if temperature_input is 97.80 and is between 
    # the two tuple entries (93.15,.020) and (103.15,.017) then the temperature_delta  would be calculated as:
    #    temperature_input_delta = (T27_2_delta - T27_1_delta)/(T27_2 - T27_1) * (T27_input - T27_1) + T27_1_delta
    # or in real numbers
    #    temperature_input_delta = (.017-.020)/(103.15-93.15) * (97.80-93.15) + .02 = 0.01856
    # Finally temperature_output = temperature_input + temperature_input_delta
    # or
    #    T90 = 97.8+0.01856 = 97.81856 or rounded three decimal digits: 97.819
    # First step is to create the list of tuples of ITS-27 temperature and temperature_delta values
    if temperature_scale.upper() == "ITS-27":
        # ITS-27 to ITS-90 table
        temperature_table = [(93.15,0.020),(103.15,0.017),(113.15,0.007),(123.15,0.000),(133.15,0.001),
            (143.15,0.008),(153.15,0.017),(163.15,0.026),(173.15,0.035),(183.15,0.041),
            (193.15,0.045),(203.15,0.045),(213.15,0.042),(223.15,0.038),(233.15,0.032),
            (243.15,0.024),(253.15,0.016),(263.15,0.008),(273.15,0.000),(283.15,-0.006),
            (293.15,-0.012),(303.15,-0.016),(313.15,-0.020),(323.15,-0.023),(333.15,-0.026),
            (343.15,-0.026),(353.15,-0.027),(363.15,-0.027),(373.15,-0.026),(383.15,-0.024),
            (393.15,-0.023),(403.15,-0.020),(413.15,-0.018),(423.15,-0.016),(433.15,-0.012),
            (443.15,-0.009),(453.15,-0.005),(463.15,-0.001),(473.15,0.003),(483.15,0.007),
            (493.15,0.011),(503.15,0.014),(513.15,0.018),(523.15,0.021),(533.15,0.024),
            (543.15,0.028),(553.15,0.030),(563.15,0.032),(573.15,0.034),(583.15,0.035),
            (593.15,0.036),(603.15,0.036),(613.15,0.037),(623.15,0.036),(633.15,0.035),
            (643.15,0.034),(653.15,0.032),(663.15,0.030),(673.15,0.028),(683.15,0.024),
            (693.15,0.022),(703.15,0.019),(713.15,0.015),(723.15,0.012),(733.15,0.009),
            (743.15,0.007),(753.15,0.004),(763.15,0.002),(773.15,0.000),(783.15,-0.001),
            (793.15,-0.002),(803.15,-0.001),(813.15,0.000),(823.15,0.002),(833.15,0.007),
            (843.15,0.011),(853.15,0.018),(863.15,0.025),(873.15,0.035),(883.15,0.047),
            (893.15,0.060),(903.15,0.08),(913.15,0.19),(923.15,0.30),(933.15,0.42),
            (943.15,0.52),(953.15,0.63),(963.15,0.73),(973.15,0.83),(983.15,0.93),
            (993.15,1.02),(1003.15,1.09),(1013.15,1.16),(1023.15,1.23),(1033.15,1.29),
            (1043.15,1.32),(1053.15,1.37),(1063.15,1.40),(1073.15,1.42),(1083.15,1.44),
            (1093.15,1.44),(1103.15,1.43),(1113.15,1.43),(1123.15,1.42),(1133.15,1.41),
            (1143.15,1.39),(1153.15,1.36),(1163.15,1.36),(1173.15,1.34),(1183.15,1.33),
            (1193.15,1.32),(1203.15,1.32),(1213.15,1.31),(1223.15,1.30),(1233.15,1.28),
            (1243.15,1.27),(1253.15,1.27),(1263.15,1.26),(1273.15,1.25),(1283.15,1.25),
            (1293.15,1.24),(1303.15,1.22),(1313.15,1.21),(1323.15,1.20),(1333.15,1.18),
            (1373.15,1.04),(1473.15,0.90),(1573.15,0.35),(1673.15,-0.09),(1773.15,-0.54),
            (1873.15,-1.09),(1973.15,-1.64),(2073.15,-2.40),(2173.15,-3.06),(2273.15,-3.92),
            (2373.15,-4.69),(2473.15,-5.55),(2573.15,-6.53),(2673.15,-7.60),(2773.15,-8.57),
            (2873.15,-9.75),(2973.15,-11.0),(3073.15,-12.2),(3173.15,-13.6),(3273.15,-15.1),
            (3373.15,-16.6),(3473.15,-18.3),(3573.15,-19.9),(3673.15,-21.7),(3773.15,-23.7),
            (3873.15,-25.7),(3973.15,-27.9),(4073.15,-30.1),(4173.15,-32.4),(4273.15,-35.1)
        ]
    elif temperature_scale.upper() == "IPTS-48":
        # IPTS-48 to ITS-90 table
        temperature_table = [(93.15,0.020),(103.15,0.017),(113.15,0.007),(123.15,0.000),(133.15,0.001),
            (143.15,0.008),(153.15,0.017),(163.15,0.026),(173.15,0.035),(183.15,0.041),
            (193.15,0.045),(203.15,0.045),(213.15,0.042),(223.15,0.038),(233.15,0.032),
            (243.15,0.024),(253.15,0.016),(263.15,0.008),(273.15,0.000),(283.15,-0.006),
            (293.15,-0.012),(303.15,-0.016),(313.15,-0.020),(323.15,-0.023),(333.15,-0.026),
            (343.15,-0.026),(353.15,-0.027),(363.15,-0.027),(373.15,-0.026),(383.15,-0.024),
            (393.15,-0.023),(403.15,-0.020),(413.15,-0.018),(423.15,-0.016),(433.15,-0.012),
            (443.15,-0.009),(453.15,-0.005),(463.15,-0.001),(473.15,0.003),(483.15,0.007),
            (493.15,0.011),(503.15,0.014),(513.15,0.018),(523.15,0.021),(533.15,0.024),
            (543.15,0.028),(553.15,0.030),(563.15,0.032),(573.15,0.034),(583.15,0.035),
            (593.15,0.036),(603.15,0.036),(613.15,0.037),(623.15,0.036),(633.15,0.035),
            (643.15,0.034),(653.15,0.032),(663.15,0.030),(673.15,0.028),(683.15,0.024),
            (693.15,0.022),(703.15,0.019),(713.15,0.015),(723.15,0.012),(733.15,0.009),
            (743.15,0.007),(753.15,0.004),(763.15,0.002),(773.15,0.000),(783.15,-0.001),
            (793.15,-0.002),(803.15,-0.001),(813.15,0.000),(823.15,0.002),(833.15,0.007),
            (843.15,0.011),(853.15,0.018),(863.15,0.025),(873.15,0.035),(883.15,0.047),
            (893.15,0.060),(903.15,0.08),(913.15,0.15),(923.15,0.22),(933.15,0.30),
            (943.15,0.37),(953.15,0.45),(963.15,0.52),(973.15,0.59),(983.15,0.66),
            (993.15,0.73),(1003.15,0.78),(1013.15,0.83),(1023.15,0.88),(1033.15,0.92),
            (1043.15,0.94),(1053.15,0.97),(1063.15,0.99),(1073.15,1.01),(1083.15,1.02),
            (1093.15,1.01),(1103.15,1.00),(1113.15,1.00),(1123.15,0.99),(1133.15,0.98),
            (1143.15,0.97),(1153.15,0.95),(1163.15,0.95),(1173.15,0.94),(1183.15,0.95),
            (1193.15,0.95),(1203.15,0.96),(1213.15,0.97),(1223.15,0.98),(1233.15,0.98),
            (1243.15,0.99),(1253.15,1.01),(1263.15,1.03),(1273.15,1.05),(1283.15,1.07),
            (1293.15,1.09),(1303.15,1.11),(1313.15,1.13),(1323.15,1.15),(1333.15,1.17),
            (1343.15,1.19),(1373.15,1.20),(1473.15,1.40),(1573.15,1.50),(1673.15,1.60),
            (1773.15,1.80),(1873.15,1.90),(1973.15,2.10),(2073.15,2.20),(2173.15,2.30),
            (2273.15,2.50),(2373.15,2.70),(2473.15,2.90),(2573.15,3.10),(2673.15,3.20),
            (2773.15,3.40),(2873.15,3.7),(2973.15,3.8),(3073.15,4.0),(3173.15,4.2),
            (3273.15,4.4),(3373.15,4.6),(3473.15,4.8),(3573.15,5.1),(3673.15,5.3),
            (3773.15,5.5),(3873.15,5.8),(3973.15,6.0),(4073.15,6.3),(4173.15,6.6),(4273.15,6.8)
        ]
    elif temperature_scale.upper() == "IPTS-68":
        # Use a reusable function because this conversion is needed for other conversions
        # and it has a long table.
        return IPTS_68_To_ITS_90(temperature_input)
    elif temperature_scale.upper() == "HE4-58":
        # Use a reusable function because this conversion is needed for other conversions.
        return He4_58_To_ITS_90(temperature_input)
    elif temperature_scale.upper() == "HE3-62":
        # Below is the He3-62 to EPT-76 table. There is no official conversion from EPT-76
        # to ITS-90 below 5K.
        temperature_table = [
            (0.5, 0.0019), (0.6, 0.0021), (0.8, 0.0025), (1.0, 0.0029), (1.2, 0.0032), (1.4, 0.0035),
            (1.6, 0.0037), (1.8, 0.0039), (2.0, 0.0041), (2.2, 0.0044), (2.4, 0.0049), (2.6, 0.0054),
            (2.8, 0.0059), (3.0, 0.0063), (3.2, 0.0066)
        ]
    elif temperature_scale.upper() == "NBS-39":
        # NBS-39 gets a preliminary conversion to NPL-61, which is then converted to ITS-90.
        # Below is the NBS-39 to NPL-61 conversion table.
        temperature_table = [
            (10.0356, -0.0356), (10.5284, -0.0284), (11.0214, -0.0214), (11.5149, -0.0149), (12.0109, -0.0109), (12.5086, -0.0086), 
            (13.0082, -0.0082), (13.5093, -0.0093), (14.0112, -0.0112), (14.5121, -0.0121), (15.0117, -0.0117), (15.5098, -0.0098),
            (16.0069, -0.0069)
        ]
        temperature_61 = Interpolate_Table(temperature_input, temperature_table)
        return NPL_61_To_ITS_90(temperature_61)
    elif temperature_scale.upper() == "NPL-61":
        return NPL_61_To_ITS_90(temperature_input)
    elif temperature_scale.upper() == "EPT-76":
        # First value in tuple is T_76, second value is T_90 - T_76
        temperature_table = [
            (5, -0.0001),(6, -0.0002),(7, -0.0003),(8, -0.0004),(9, -0.0005),(10, -0.0006),(11, -0.0007),
            (12, -0.0008),(13, -0.001),(14, -0.0011),(15, -0.0013),(16, -0.0014),(17, -0.0016),(18, -0.0018),
            (19, -0.002),(20, -0.0022),(21, -0.0025),(22, -0.0027),(23, -0.003),(24, -0.0032),(25, -0.0035),
            (26, -0.0038),(27, -0.0041)
            ]
    elif temperature_scale.upper() == "NBS-55":
        temperature_table = [
            (14, -0.009), (15, -0.001), (16, 0.001), (17, 0.0), (18, 0.0), (19, -0.0),
            (20, -0.0), (21, 0.0), (22, 0.001), (23, 0.002), (24, 0.003), (25, 0.003),
            (26, 0.002), (27, 0.002), (28, 0.002), (29, 0.002), (30, 0.001), (31, 0.001),
            (32, 0.001), (33, 0.002), (34, 0.003), (35, 0.004), (36, 0.005), (37, 0.007),
            (38, 0.008), (39, 0.009), (40, 0.01), (41, 0.01), (42, 0.01), (43, 0.01),
            (44, 0.01), (45, 0.009), (46, 0.009), (47, 0.008), (48, 0.008), (49, 0.008),
            (50, 0.007), (51, 0.007), (52, 0.007), (53, 0.006), (54, 0.006), (55, 0.005),
            (56, 0.004), (57, 0.003), (58, 0.002), (59, 0.002), (60, 0.002), (61, 0.002),
            (62, 0.002), (63, 0.003), (64, 0.004), (65, 0.005), (66, 0.006), (67, 0.007),
            (68, 0.007), (69, 0.007), (70, 0.007), (71, 0.006), (72, 0.006), (73, 0.005),
            (74, 0.003), (75, 0.002), (76, 0.001), (77, -0.0), (78, -0.001), (79, -0.001),
            (80, -0.001), (81, -0.001), (82, 0.0), (83, 0.001), (84, 0.004), (85, 0.006),
            (86, 0.008), (87, 0.011), (88, 0.014), (89, 0.016), (90, 0.019), (91, 0.02)
        ]
    elif temperature_scale.upper() == "NPL-75":
        return NPL_75_To_ITS_90(temperature_input)
    elif temperature_scale.upper() == "XISU":
        # Below is the xisu to NPL-75 conversion table
        temperature_table = [
            (2.6, -0.0), (3.0, -0.0), (3.6001, -0.0001), (4.0001, -0.0001), (4.6001, -0.0001), (5.0001, -0.0001),
            (5.6002, -0.0002), (6.0002, -0.0002), (6.6003, -0.0003), (7.0003, -0.0003), (7.6004, -0.0004), (8.0004, -0.0004),
            (8.6005, -0.0005), (9.0005, -0.0005), (9.6006, -0.0006), (10.0007, -0.0006), (10.6007, -0.0007), (11.0008, -0.0008),
            (11.6009, -0.0009), (12.001, -0.001), (12.6011, -0.0011), (13.0011, -0.0011), (13.6013, -0.0012), (14.0013, -0.0013),
            (14.6015, -0.0014), (15.0015, -0.0015), (15.6017, -0.0017), (16.0018, -0.0018), (16.6019, -0.0019), (17.002, -0.002),
            (17.6021, -0.0022), (18.0023, -0.0022), (18.6024, -0.0024), (19.0025, -0.0025), (19.6027, -0.0027), (20.0028, -0.0028),
            (20.603, -0.003), (21.0031, -0.0031), (21.6033, -0.0033), (22.0034, -0.0034), (22.6036, -0.0036), (23.0037, -0.0037),
            (23.6039, -0.0039), (24.0041, -0.0041), (24.6043, -0.0043), (25.0044, -0.0044), (25.6047, -0.0047), (26.0048, -0.0048),
            (26.605, -0.005), (27.1052, -0.0052)
        ]
        temperature_75 = Interpolate_Table(temperature_input, temperature_table)
        return NPL_75_To_ITS_90(temperature_75)
    elif temperature_scale.upper() == "PRMI-54":
        temperature_table = [
            (14, -0.0532), (15, -0.0401), (16, -0.0324), (17, -0.0276), (18, -0.0248), (19, -0.0233),
            (20, -0.022), (21, -0.0203), (22, -0.0182), (23, -0.0161), (24, -0.0147), (25, -0.0136),
            (26, -0.013), (27, -0.0127), (28, -0.0127), (29, -0.0129), (30, -0.0135), (31, -0.0142),
            (32, -0.0147), (33, -0.0149), (34, -0.0149), (35, -0.0147), (36, -0.0143), (37, -0.014),
            (38, -0.0137), (39, -0.0131), (40, -0.0129), (41, -0.0127), (42, -0.0126), (43, -0.0126),
            (44, -0.0126), (45, -0.0126), (46, -0.0126), (47, -0.0122), (48, -0.0119), (49, -0.0113),
            (50, -0.0105), (51, -0.0095), (52, -0.0086), (53, -0.0076), (54, -0.0066), (55, -0.0057),
            (56, -0.0049), (57, -0.0046), (58, -0.0046), (59, -0.0049), (60, -0.0054), (61, -0.006),
            (62, -0.0067), (63, -0.0076), (64, -0.0082), (65, -0.0087), (66, -0.0089), (67, -0.0091),
            (68, -0.009), (69, -0.0087), (70, -0.0082), (71, -0.0079), (72, -0.0073), (73, -0.007),
            (74, -0.007), (75, -0.0069), (76, -0.0068), (77, -0.0067), (78, -0.0066), (79, -0.0067),
            (80, -0.0068), (81, -0.007), (82, -0.0072), (83, -0.0073), (84, -0.0065), (85, -0.0063),
            (86, -0.0059), (87, -0.0053), (88, -0.0046), (89, -0.0041), (90, -0.0037), (91, -0.0036)
        ]
    elif temperature_scale.upper() == "PSU-54":
        temperature_table = [
            (14, 0.0041), (15, 0.0132), (16, 0.0149), (17, 0.0148), (18, 0.0141), (19, 0.0138),
            (20, 0.0142), (21, 0.0151), (22, 0.0163), (23, 0.0176), (24, 0.019), (25, 0.0196),
            (26, 0.0193), (27, 0.0186), (28, 0.0181), (29, 0.0179), (30, 0.0178), (31, 0.0178),
            (32, 0.0182), (33, 0.0197), (34, 0.0212), (35, 0.0216), (36, 0.0218), (37, 0.0221),
            (38, 0.0224), (39, 0.0226), (40, 0.0227), (41, 0.0224), (42, 0.0218), (43, 0.0213),
            (44, 0.021), (45, 0.0208), (46, 0.0204), (47, 0.0196), (48, 0.0186), (49, 0.0172),
            (50, 0.0157), (51, 0.0154), (52, 0.0158), (53, 0.0166), (54, 0.0174), (55, 0.018),
            (56, 0.0186), (57, 0.0187), (58, 0.019), (59, 0.0197), (60, 0.0205), (61, 0.0213),
            (62, 0.0219), (63, 0.0224), (64, 0.023), (65, 0.0241), (66, 0.0245), (67, 0.0255),
            (68, 0.0266), (69, 0.0282), (70, 0.0294), (71, 0.0299), (72, 0.03), (73, 0.0297),
            (74, 0.0289), (75, 0.0286), (76, 0.0294), (77, 0.0303), (78, 0.031), (79, 0.0316),
            (80, 0.0321), (81, 0.0329), (82, 0.0339), (83, 0.0349), (84, 0.0373), (85, 0.0385),
            (86, 0.0396), (87, 0.0408), (88, 0.0418), (89, 0.0431), (90, 0.0445), (91, 0.0454)
        ]
    return Interpolate_Table(temperature_input, temperature_table)



def Interpolate_Table(temperature_input, temperature_table):
    # This is an internal only function that will not be called by C++ but rather from the Temperature function
    # so there will be no parameter line
    # First check if the input is in the range of the conversion table.
    # If not, just return the input, as it cannot be converted.
    if temperature_input < temperature_table[0][0] or temperature_input > temperature_table[-1][0]:
        return temperature_input
    # Now loop over the list of tuples and find the two tuples that have temperature values above and below the
    # input temperature 
    if temperature_input == temperature_table[0][0]:
        return temperature_input+temperature_table[0][1]
    elif temperature_input == temperature_table[-1][0]:
        return temperature_input+temperature_table[-1][1]
    else:
        found_tuple2 = "false"
        for temperature_tuple in temperature_table:
            if(temperature_tuple[0] <= temperature_input):
                temperature_1 = temperature_tuple[0]
                temperature_1_delta = temperature_tuple[1]
            elif(temperature_tuple[0] > temperature_input):
                found_tuple2 = "true"
                temperature_2 = temperature_tuple[0]
                temperature_2_delta = temperature_tuple[1]
                break
    # Now do the calculation of the temperature_input_delta
    temperature_input_delta = (temperature_2_delta-temperature_1_delta)/(temperature_2-temperature_1)*(temperature_input-temperature_1)+temperature_1_delta

    # Now calculate the temperature_output value
    temperature_output = temperature_input+temperature_input_delta     
    return temperature_output

def NPL_61_To_ITS_90(temperature_input):
    # This is an internal only function that will not be called by C++ but rather from the Temperature function
    # so there will be no parameter line
    temperature_table = [
        (14, -0.0072), (15, -0.0004), (16, -0.0031), (17, -0.0065), (18, -0.0039), (19, 0.0008),
        (20, 0.0006), (21, -0.0011), (22, -0.0021), (23, -0.0021), (24, -0.0019), (25, -0.0009),
        (26, -0.0003), (27, 0.0001), (28, 0.0001), (29, -0.0004), (30, -0.0013), (31, -0.0027),
        (32, -0.0042), (33, -0.0057), (34, -0.0068), (35, -0.0077), (36, -0.0081), (37, -0.0082),
        (38, -0.0079), (39, -0.0074), (40, -0.0068), (41, -0.0062), (42, -0.006), (43, -0.006),
        (44, -0.0063), (45, -0.007), (46, -0.0077), (47, -0.0085), (48, -0.0093), (49, -0.01),
        (50, -0.0103), (51, -0.0102), (52, -0.0096), (53, -0.0088), (54, -0.0073), (55, -0.0055),
        (56, -0.0033), (57, -0.0008), (58, 0.0018), (59, 0.0044), (60, 0.0068), (61, 0.0092),
        (62, 0.0111), (63, 0.0125), (64, 0.0137), (65, 0.0145), (66, 0.0147), (67, 0.0147),
        (68, 0.0144), (69, 0.0138), (70, 0.0131), (71, 0.0123), (72, 0.0115), (73, 0.0107),
        (74, 0.0099), (75, 0.0093), (76, 0.009), (77, 0.009), (78, 0.0094), (79, 0.0101),
        (80, 0.0111), (81, 0.0123), (82, 0.0136), (83, 0.015), (84, 0.0169), (85, 0.018),
        (86, 0.0188), (87, 0.0192), (88, 0.0193), (89, 0.019), (90, 0.0183), (91, 0.017)
    ]
    return Interpolate_Table(temperature_input, temperature_table)

def He4_58_To_ITS_90(temperature_input):
    # This is an internal only function that will not be called by C++ but rather from the Temperature function
    # so there will be no parameter line
    # He4-58 gets converted to EPT-76, which has no official conversion to
    # ITS-90 below 5K.
    # If T_76 is over 5K, we can then convert to ITS-90
    # Below is the conversion table for He4-58 to EPT-76.
    # The first element in each tuple is T_58, and the second element is T_76 - T_58
    temperature_table = [
        (0.5, 0.0019), (0.6, 0.0021), (0.8, 0.0025), (1.0, 0.0029), (1.2, 0.0032), (1.4, 0.0035),
        (1.6, 0.0037), (1.8, 0.0039), (2.0, 0.0041), (2.2, 0.0044), (2.4, 0.0049), (2.6, 0.0054),
        (2.8, 0.0059), (3.0, 0.0063), (3.2, 0.0066), (3.4, 0.0068), (3.6, 0.007), (3.8, 0.007),
        (4.0, 0.0071), (4.2, 0.0071), (4.5, 0.0071), (5.0, 0.0071)
    ]
    temperature_76 = Interpolate_Table(temperature_input, temperature_table)
    if temperature_76 >= 5:
        # Below is the first little bit of the EPT-76 to ITS-90 conversion table.
        temperature_table = [(5, -0.0001), (6, -0.0002)]
        return Interpolate_Table(temperature_76, temperature_table)
    else:
        return temperature_76

def NPL_75_To_ITS_90(temperature_input):
    # This is an internal only function that will not be called by C++ but rather from the Temperature function
    # so there will be no parameter line
    # For low temperatures, convert to He4-58, then convert
    # to EPT-76/ITS-90.
    if temperature_input <= 4.2221:
        temperature_table = [
            (2.6058, -0.0058), (2.8061, -0.0061), (3.0064, -0.0064), (3.2066, -0.0066), (3.4068, -0.0068), (3.6069, -0.0069),
            (3.807, -0.007), (4.0071, -0.0071), (4.2221, -0.0071)
        ]
        temperature_58 = Interpolate_Table(temperature_input, temperature_table)
        return He4_58_To_ITS_90(temperature_58)
    # For high temperatures, convert to IPTS-68 and then convert
    # to ITS-90.
    elif temperature_input >=13.80349:
        temperature_table = [
            (13.8035, 0.0065), (14.1937, 0.0054), (14.6955, 0.0039), (15.4955, 0.0036), (14.996, 0.0035), (16.2946, 0.0046),
            (17.0356, 0.0064), (17.6909, 0.0078), (18.3909, 0.0089), (18.9903, 0.0094), (19.5908, 0.0095)
        ]
        temperature_68 = Interpolate_Table(temperature_input, temperature_table)
        return IPTS_68_To_ITS_90(temperature_68)
    # For values outside this range, we don't have a definite conversion to ITS-90
    # so we just pass the input value.
    else:
        return temperature_input
def IPTS_68_To_ITS_90(temperature_input):
    # This is an internal only function that will not be called by C++ but rather from the Temperature function
    # so there will be no parameter line
    # IPTS-68 conversion
    # If the temperature is in the highest range of the conversion, we can use an explicit expression to save processing time.
    # If the temperature is not in that range, we use the table.
    if  temperature_input > 1337.580:
        coeff = 1.398E-7
        temperature_output = m.sqrt(temperature_input/coeff+1/4/coeff**2)-1/2/coeff
        return temperature_output
    else: 
        # Note that the first element of the tuple is T_68, and the second element is T_90 - T_68
        temperature_table = [
            (13.807, -0.007), (14.006, -0.006), (15.003, -0.003), (16.004, -0.004), (17.007, -0.007), (18.008, -0.008),
            (19.009, -0.009), (20.009, -0.009), (21.008, -0.008), (22.007, -0.007), (23.006, -0.006), (24.006, -0.006), 
            (25.005, -0.005), (26.005, -0.005), (27.005, -0.005), (28.005, -0.005), (29.006, -0.006), (30.006, -0.006), 
            (31.007, -0.007), (32.007, -0.007), (33.007, -0.007), (34.007, -0.007), (35.007, -0.007), (36.007, -0.007), 
            (37.007, -0.007), (38.006, -0.006), (39.006, -0.006), (40.006, -0.006), (41.006, -0.006), (42.006, -0.006), 
            (43.006, -0.006), (44.006, -0.006), (45.006, -0.006), (46.006, -0.006), (47.006, -0.006), (48.006, -0.006), 
            (49.006, -0.006), (50.006, -0.006), (51.005, -0.005), (52.005, -0.005), (53.004, -0.004), (54.003, -0.003), 
            (55.002, -0.002), (56.001, -0.001), (57.0, 0.0), (57.999, 0.001), (58.998, 0.002), (59.997, 0.003),
            (60.997, 0.003), (61.996, 0.004), (62.996, 0.004), (63.995, 0.005), (64.995, 0.005), (65.994, 0.006),
            (66.994, 0.006), (67.994, 0.006), (68.994, 0.006), (69.993, 0.007), (70.993, 0.007), (71.993, 0.007),
            (72.992, 0.008), (73.142, 0.008), (83.792, 0.008), (83.992, 0.008), (84.992, 0.008), (85.991, 0.009),
            (86.991, 0.009), (87.991, 0.009), (88.991, 0.009), (89.991, 0.009), (90.991, 0.009), (91.991, 0.009),
            (92.991, 0.009), (93.991, 0.009), (94.99, 0.01), (95.99, 0.01), (96.99, 0.01), (97.99, 0.01),
            (98.99, 0.01), (99.99, 0.01), (100.99, 0.01), (101.99, 0.01), (102.99, 0.01), (103.989, 0.011),
            (104.989, 0.011), (105.989, 0.011), (106.989, 0.011), (107.989, 0.011), (108.989, 0.011), (109.989, 0.011), 
            (110.989, 0.011), (111.989, 0.011), (112.989, 0.011), (113.989, 0.011), (114.988, 0.012), (115.988, 0.012), 
            (116.988, 0.012), (117.988, 0.012), (118.988, 0.012), (119.988, 0.012), (120.988, 0.012), (121.988, 0.012), 
            (122.988, 0.012), (123.988, 0.012), (124.988, 0.012), (125.988, 0.012), (126.988, 0.012), (127.987, 0.013), 
            (128.987, 0.013), (129.987, 0.013), (130.987, 0.013), (131.987, 0.013), (132.987, 0.013), (133.987, 0.013), 
            (134.987, 0.013), (135.987, 0.013), (136.987, 0.013), (137.987, 0.013), (138.987, 0.013), (139.987, 0.013), 
            (140.987, 0.013), (141.987, 0.013), (142.987, 0.013), (143.987, 0.013), (144.987, 0.013), (145.987, 0.013), 
            (146.986, 0.014), (147.986, 0.014), (148.986, 0.014), (149.986, 0.014), (150.986, 0.014), (151.986, 0.014), 
            (152.986, 0.014), (153.986, 0.014), (154.986, 0.014), (155.986, 0.014), (156.986, 0.014), (157.986, 0.014), 
            (158.986, 0.014), (159.986, 0.014), (160.986, 0.014), (161.986, 0.014), (162.986, 0.014), (163.986, 0.014), 
            (164.986, 0.014), (165.986, 0.014), (166.986, 0.014), (167.986, 0.014), (168.986, 0.014), (169.986, 0.014), 
            (170.986, 0.014), (171.986, 0.014), (172.986, 0.014), (173.986, 0.014), (174.986, 0.014), (175.986, 0.014), 
            (176.986, 0.014), (177.986, 0.014), (178.986, 0.014), (179.986, 0.014), (180.987, 0.013), (181.987, 0.013), 
            (182.987, 0.013), (183.987, 0.013), (184.987, 0.013), (185.987, 0.013), (186.987, 0.013), (187.987, 0.013), 
            (188.987, 0.013), (189.987, 0.013), (190.987, 0.013), (191.987, 0.013), (192.987, 0.013), (193.987, 0.013), 
            (194.987, 0.013), (195.987, 0.013), (196.987, 0.013), (197.988, 0.012), (198.988, 0.012), (199.988, 0.012), 
            (200.988, 0.012), (201.988, 0.012), (202.988, 0.012), (203.988, 0.012), (204.988, 0.012), (205.988, 0.012), 
            (206.988, 0.012), (207.988, 0.012), (208.989, 0.011), (209.989, 0.011), (210.989, 0.011), (211.989, 0.011), 
            (212.989, 0.011), (213.989, 0.011), (214.989, 0.011), (215.989, 0.011), (216.99, 0.01), (217.99, 0.01),
            (218.99, 0.01), (219.99, 0.01), (220.99, 0.01), (221.99, 0.01), (222.99, 0.01), (223.99, 0.01),
            (224.991, 0.009), (225.991, 0.009), (226.991, 0.009), (227.991, 0.009), (228.991, 0.009), (229.991, 0.009), 
            (230.992, 0.008), (231.992, 0.008), (232.992, 0.008), (233.992, 0.008), (234.992, 0.008), (235.992, 0.008), 
            (236.993, 0.007), (237.993, 0.007), (238.993, 0.007), (239.993, 0.007), (240.993, 0.007), (241.993, 0.007), 
            (242.994, 0.006), (243.994, 0.006), (244.994, 0.006), (245.994, 0.006), (246.994, 0.006), (247.995, 0.005), 
            (248.995, 0.005), (249.995, 0.005), (250.995, 0.005), (251.995, 0.005), (252.996, 0.004), (253.996, 0.004), 
            (254.996, 0.004), (255.996, 0.004), (256.996, 0.004), (257.997, 0.003), (258.997, 0.003), (259.997, 0.003), 
            (260.997, 0.003), (261.997, 0.003), (262.998, 0.002), (263.998, 0.002), (264.998, 0.002), (265.998, 0.002), 
            (266.999, 0.001), (267.999, 0.001), (268.999, 0.001), (269.999, 0.001), (270.999, 0.001), (272.0, 0.0),
            (273.0, 0.0), (274.0, 0.0), (275.0, 0.0), (276.001, -0.001), (277.001, -0.001), (278.001, -0.001),
            (279.001, -0.001), (280.002, -0.002), (281.002, -0.002), (282.002, -0.002), (283.002, -0.002), (284.003, -0.003),
            (285.003, -0.003), (286.003, -0.003), (287.003, -0.003), (288.004, -0.004), (289.004, -0.004), (290.004, -0.004),
            (291.004, -0.004), (292.005, -0.005), (293.005, -0.005), (294.005, -0.005), (295.005, -0.005), (296.006, -0.006),
            (297.006, -0.006), (298.006, -0.006), (299.006, -0.006), (300.007, -0.007), (301.007, -0.007), (302.007, -0.007),
            (303.008, -0.008), (304.008, -0.008), (305.008, -0.008), (306.008, -0.008), (307.009, -0.009), (308.009, -0.009),
            (309.009, -0.009), (310.009, -0.009), (311.01, -0.01), (312.01, -0.01), (313.01, -0.01), (314.01, -0.01),
            (315.011, -0.011), (316.011, -0.011), (317.011, -0.011), (318.012, -0.012), (319.012, -0.012), (320.012, -0.012),
            (321.012, -0.012), (322.013, -0.013), (323.013, -0.013), (324.013, -0.013), (325.013, -0.013), (326.014, -0.014),
            (327.014, -0.014), (328.014, -0.014), (329.014, -0.014), (330.015, -0.015), (331.015, -0.015), (332.015, -0.015),
            (333.016, -0.016), (334.016, -0.016), (335.016, -0.016), (336.016, -0.016), (337.017, -0.017), (338.017, -0.017),
            (339.017, -0.017), (340.017, -0.017), (341.018, -0.018), (342.018, -0.018), (343.018, -0.018), (344.018, -0.018),
            (345.019, -0.019), (346.019, -0.019), (347.019, -0.019), (348.019, -0.019), (349.02, -0.02), (350.02, -0.02),
            (351.02, -0.02), (352.021, -0.021), (353.021, -0.021), (354.021, -0.021), (355.021, -0.021), (356.022, -0.022),
            (357.022, -0.022), (358.022, -0.022), (359.022, -0.022), (360.023, -0.023), (361.023, -0.023), (362.023, -0.023),
            (363.023, -0.023), (364.023, -0.023), (365.024, -0.024), (366.024, -0.024), (367.024, -0.024), (368.024, -0.024),
            (369.025, -0.025), (370.025, -0.025), (371.025, -0.025), (372.025, -0.025), (373.026, -0.026), (374.026, -0.026),
            (375.026, -0.026), (376.026, -0.026), (377.027, -0.027), (378.027, -0.027), (379.027, -0.027), (380.027, -0.027),
            (381.027, -0.027), (382.028, -0.028), (383.028, -0.028), (384.028, -0.028), (385.028, -0.028), (386.028, -0.028),
            (387.029, -0.029), (388.029, -0.029), (389.029, -0.029), (390.029, -0.029), (391.03, -0.03), (392.03, -0.03),
            (393.03, -0.03), (394.03, -0.03), (395.03, -0.03), (396.031, -0.031), (397.031, -0.031), (398.031, -0.031), 
            (399.031, -0.031), (400.031, -0.031), (401.031, -0.031), (402.032, -0.032), (403.032, -0.032), (404.032, -0.032),
            (405.032, -0.032), (406.032, -0.032), (407.033, -0.033), (408.033, -0.033), (409.033, -0.033), (410.033, -0.033),
            (411.033, -0.033), (412.033, -0.033), (413.034, -0.034), (414.034, -0.034), (415.034, -0.034), (416.034, -0.034),
            (417.034, -0.034), (418.034, -0.034), (419.034, -0.034), (420.035, -0.035), (421.035, -0.035), (422.035, -0.035),
            (423.035, -0.035), (424.035, -0.035), (425.035, -0.035), (426.035, -0.035), (427.036, -0.036), (428.036, -0.036),
            (429.036, -0.036), (430.036, -0.036), (431.036, -0.036), (432.036, -0.036), (433.036, -0.036), (434.037, -0.037),
            (435.037, -0.037), (436.037, -0.037), (437.037, -0.037), (438.037, -0.037), (439.037, -0.037), (440.037, -0.037),
            (441.037, -0.037), (442.037, -0.037), (443.038, -0.038), (444.038, -0.038), (445.038, -0.038), (446.038, -0.038),
            (447.038, -0.038), (448.038, -0.038), (449.038, -0.038), (450.038, -0.038), (451.038, -0.038), (452.038, -0.038),
            (453.038, -0.038), (454.039, -0.039), (455.039, -0.039), (456.039, -0.039), (457.039, -0.039), (458.039, -0.039),
            (459.039, -0.039), (460.039, -0.039), (461.039, -0.039), (462.039, -0.039), (463.039, -0.039), (464.039, -0.039),
            (465.039, -0.039), (466.039, -0.039), (467.039, -0.039), (468.039, -0.039), (469.04, -0.04), (470.04, -0.04),
            (471.04, -0.04), (472.04, -0.04), (473.04, -0.04), (474.04, -0.04), (475.04, -0.04), (476.04, -0.04),
            (477.04, -0.04), (478.04, -0.04), (479.04, -0.04), (480.04, -0.04), (481.04, -0.04), (482.04, -0.04),
            (483.04, -0.04), (484.04, -0.04), (485.04, -0.04), (486.04, -0.04), (487.04, -0.04), (488.04, -0.04),
            (489.04, -0.04), (490.04, -0.04), (491.04, -0.04), (492.04, -0.04), (493.04, -0.04), (494.04, -0.04),
            (495.04, -0.04), (496.04, -0.04), (497.04, -0.04), (498.04, -0.04), (499.04, -0.04), (500.04, -0.04),
            (501.04, -0.04), (502.04, -0.04), (503.04, -0.04), (504.04, -0.04), (505.04, -0.04), (506.04, -0.04),
            (507.04, -0.04), (508.04, -0.04), (509.04, -0.04), (510.04, -0.04), (511.04, -0.04), (512.04, -0.04),
            (513.04, -0.04), (514.04, -0.04), (515.04, -0.04), (516.04, -0.04), (517.04, -0.04), (518.04, -0.04),
            (519.04, -0.04), (520.04, -0.04), (521.04, -0.04), (522.04, -0.04), (523.04, -0.04), (524.04, -0.04),
            (525.04, -0.04), (526.04, -0.04), (527.04, -0.04), (528.04, -0.04), (529.04, -0.04), (530.04, -0.04),
            (531.04, -0.04), (532.04, -0.04), (533.04, -0.04), (534.04, -0.04), (535.04, -0.04), (536.04, -0.04),
            (537.04, -0.04), (538.04, -0.04), (539.04, -0.04), (540.04, -0.04), (541.04, -0.04), (542.04, -0.04),
            (543.04, -0.04), (544.04, -0.04), (545.04, -0.04), (546.04, -0.04), (547.04, -0.04), (548.04, -0.04),
            (549.04, -0.04), (550.04, -0.04), (551.04, -0.04), (552.04, -0.04), (553.04, -0.04), (554.04, -0.04),
            (555.04, -0.04), (556.04, -0.04), (557.04, -0.04), (558.04, -0.04), (559.04, -0.04), (560.04, -0.04),
            (561.04, -0.04), (562.04, -0.04), (563.04, -0.04), (564.04, -0.04), (565.04, -0.04), (566.04, -0.04),
            (567.04, -0.04), (568.04, -0.04), (569.04, -0.04), (570.04, -0.04), (571.04, -0.04), (572.04, -0.04),
            (573.04, -0.04), (574.04, -0.04), (575.04, -0.04), (576.04, -0.04), (577.04, -0.04), (578.04, -0.04),
            (579.04, -0.04), (580.04, -0.04), (581.04, -0.04), (582.04, -0.04), (583.04, -0.04), (584.04, -0.04),
            (585.04, -0.04), (586.04, -0.04), (587.04, -0.04), (588.04, -0.04), (589.04, -0.04), (590.04, -0.04),
            (591.04, -0.04), (592.04, -0.04), (593.04, -0.04), (594.04, -0.04), (595.04, -0.04), (596.04, -0.04),
            (597.04, -0.04), (598.04, -0.04), (599.04, -0.04), (600.04, -0.04), (601.04, -0.04), (602.04, -0.04),
            (603.04, -0.04), (604.04, -0.04), (605.04, -0.04), (606.04, -0.04), (607.04, -0.04), (608.04, -0.04),
            (609.04, -0.04), (610.04, -0.04), (611.04, -0.04), (612.04, -0.04), (613.04, -0.04), (614.04, -0.04),
            (615.04, -0.04), (616.041, -0.041), (617.041, -0.041), (618.041, -0.041), (619.041, -0.041), (620.041, -0.041),
            (621.041, -0.041), (622.041, -0.041), (623.041, -0.041), (624.041, -0.041), (625.041, -0.041), (626.041, -0.041),
            (627.041, -0.041), (628.041, -0.041), (629.042, -0.042), (630.042, -0.042), (631.042, -0.042), (632.042, -0.042),
            (633.042, -0.042), (634.042, -0.042), (635.042, -0.042), (636.042, -0.042), (637.042, -0.042), (638.042, -0.042),
            (639.043, -0.043), (640.043, -0.043), (641.043, -0.043), (642.043, -0.043), (643.043, -0.043), (644.043, -0.043),
            (645.043, -0.043), (646.043, -0.043), (647.044, -0.044), (648.044, -0.044), (649.044, -0.044), (650.044, -0.044),
            (651.044, -0.044), (652.044, -0.044), (653.044, -0.044), (654.045, -0.045), (655.045, -0.045), (656.045, -0.045),
            (657.045, -0.045), (658.045, -0.045), (659.045, -0.045), (660.045, -0.045), (661.046, -0.046), (662.046, -0.046),
            (663.046, -0.046), (664.046, -0.046), (665.046, -0.046), (666.047, -0.047), (667.047, -0.047), (668.047, -0.047),
            (669.047, -0.047), (670.047, -0.047), (671.048, -0.048), (672.048, -0.048), (673.048, -0.048), (674.048, -0.048),
            (675.048, -0.048), (676.049, -0.049), (677.049, -0.049), (678.049, -0.049), (679.049, -0.049), (680.049, -0.049),
            (681.05, -0.05), (682.05, -0.05), (683.05, -0.05), (684.05, -0.05), (685.051, -0.051), (686.051, -0.051),
            (687.051, -0.051), (688.051, -0.051), (689.052, -0.052), (690.052, -0.052), (691.052, -0.052), (692.052, -0.052),
            (693.053, -0.053), (694.053, -0.053), (695.053, -0.053), (696.053, -0.053), (697.054, -0.054), (698.054, -0.054),
            (699.054, -0.054), (700.054, -0.054), (701.055, -0.055), (702.055, -0.055), (703.055, -0.055), (704.056, -0.056),
            (705.056, -0.056), (706.056, -0.056), (707.056, -0.056), (708.057, -0.057), (709.057, -0.057), (710.057, -0.057),
            (711.058, -0.058), (712.058, -0.058), (713.058, -0.058), (714.059, -0.059), (715.059, -0.059), (716.059, -0.059),
            (717.059, -0.059), (718.06, -0.06), (719.06, -0.06), (720.06, -0.06), (721.061, -0.061), (722.061, -0.061), 
            (723.061, -0.061), (724.062, -0.062), (725.062, -0.062), (726.062, -0.062), (727.063, -0.063), (728.063, -0.063),
            (729.063, -0.063), (730.064, -0.064), (731.064, -0.064), (732.064, -0.064), (733.065, -0.065), (734.065, -0.065),
            (735.065, -0.065), (736.066, -0.066), (737.066, -0.066), (738.066, -0.066), (739.067, -0.067), (740.067, -0.067),
            (741.068, -0.068), (742.068, -0.068), (743.068, -0.068), (744.069, -0.069), (745.069, -0.069), (746.069, -0.069),
            (747.07, -0.07), (748.07, -0.07), (749.07, -0.07), (750.071, -0.071), (751.071, -0.071), (752.072, -0.072), 
            (753.072, -0.072), (754.072, -0.072), (755.073, -0.073), (756.073, -0.073), (757.073, -0.073), (758.074, -0.074),
            (759.074, -0.074), (760.074, -0.074), (761.075, -0.075), (762.075, -0.075), (763.076, -0.076), (764.076, -0.076),
            (765.076, -0.076), (766.077, -0.077), (767.077, -0.077), (768.078, -0.078), (769.078, -0.078), (770.078, -0.078),
            (771.079, -0.079), (772.079, -0.079), (773.079, -0.079), (774.08, -0.08), (775.08, -0.08), (776.081, -0.081),
            (777.081, -0.081), (778.081, -0.081), (779.082, -0.082), (780.082, -0.082), (781.082, -0.082), (782.083, -0.083),
            (783.083, -0.083), (784.084, -0.084), (785.084, -0.084), (786.084, -0.084), (787.085, -0.085), (788.085, -0.085),
            (789.086, -0.086), (790.086, -0.086), (791.086, -0.086), (792.087, -0.087), (793.087, -0.087), (794.087, -0.087),
            (795.088, -0.088), (796.088, -0.088), (797.089, -0.089), (798.089, -0.089), (799.089, -0.089), (800.09, -0.09),
            (801.09, -0.09), (802.09, -0.09), (803.091, -0.091), (804.091, -0.091), (805.092, -0.092), (806.092, -0.092),
            (807.092, -0.092), (808.093, -0.093), (809.093, -0.093), (810.093, -0.093), (811.094, -0.094), (812.094, -0.094),
            (813.095, -0.095), (814.095, -0.095), (815.095, -0.095), (816.096, -0.096), (817.096, -0.096), (818.096, -0.096),
            (819.097, -0.097), (820.097, -0.097), (821.097, -0.097), (822.098, -0.098), (823.098, -0.098), (824.098, -0.098),
            (825.099, -0.099), (826.099, -0.099), (827.099, -0.099), (828.1, -0.1), (829.1, -0.1), (830.101, -0.101),
            (831.101, -0.101), (832.101, -0.101), (833.102, -0.102), (834.102, -0.102), (835.102, -0.102), (836.103, -0.103),
            (837.103, -0.103), (838.103, -0.103), (839.104, -0.104), (840.104, -0.104), (841.104, -0.104), (842.105, -0.105),
            (843.105, -0.105), (844.105, -0.105), (845.106, -0.106), (846.106, -0.106), (847.106, -0.106), (848.107, -0.107),
            (849.107, -0.107), (850.107, -0.107), (851.108, -0.108), (852.108, -0.108), (853.108, -0.108), (854.108, -0.108),
            (855.109, -0.109), (856.109, -0.109), (857.109, -0.109), (858.11, -0.11), (859.11, -0.11), (860.11, -0.11), 
            (861.111, -0.111), (862.111, -0.111), (863.111, -0.111), (864.112, -0.112), (865.112, -0.112), (866.112, -0.112),
            (867.113, -0.113), (868.113, -0.113), (869.113, -0.113), (870.114, -0.114), (871.114, -0.114), (872.114, -0.114),
            (873.115, -0.115), (874.115, -0.115), (875.115, -0.115), (876.116, -0.116), (877.116, -0.116), (878.116, -0.116),
            (879.117, -0.117), (880.117, -0.117), (881.117, -0.117), (882.118, -0.118), (883.118, -0.118), (884.118, -0.118),
            (885.119, -0.119), (886.119, -0.119), (887.119, -0.119), (888.12, -0.12), (889.12, -0.12), (890.12, -0.12), 
            (891.121, -0.121), (892.121, -0.121), (893.121, -0.121), (894.122, -0.122), (895.122, -0.122), (896.123, -0.123),
            (897.123, -0.123), (898.123, -0.123), (899.124, -0.124), (900.124, -0.124), (901.125, -0.125), (902.125, -0.125),
            (903.875, -0.125), (903.876, -0.126), (904.124, -0.124), (909.1, -0.1), (914.076, -0.076), (919.051, -0.051),
            (924.027, -0.027), (929.003, -0.003), (933.979, 0.021), (938.955, 0.045), (943.932, 0.068), (948.908, 0.092),
            (953.884, 0.116), (958.861, 0.139), (963.839, 0.161), (968.817, 0.183), (973.795, 0.205), (978.775, 0.225), 
            (983.755, 0.245), (988.737, 0.263), (993.72, 0.28), (998.704, 0.296), (1003.69, 0.31), (1008.677, 0.323),
            (1013.666, 0.334), (1018.656, 0.344), (1023.649, 0.351), (1028.643, 0.357), (1033.638, 0.362), (1038.636, 0.364),
            (1043.635, 0.365), (1048.636, 0.364), (1053.639, 0.361), (1058.644, 0.356), (1063.65, 0.35), (1068.658, 0.342),
            (1073.667, 0.333), (1078.678, 0.322), (1083.69, 0.31), (1088.703, 0.297), (1093.718, 0.282), (1098.733, 0.267),
            (1103.75, 0.25), (1108.767, 0.233), (1113.785, 0.215), (1118.803, 0.197), (1123.822, 0.178), (1128.841, 0.159),
            (1133.86, 0.14), (1138.88, 0.12), (1143.899, 0.101), (1148.918, 0.082), (1153.936, 0.064), (1158.955, 0.045),
            (1163.972, 0.028), (1168.989, 0.011), (1174.006, -0.006), (1179.022, -0.022), (1184.037, -0.037), (1189.051, -0.051),
            (1194.064, -0.064), (1199.077, -0.077), (1204.089, -0.089), (1209.1, -0.1), (1214.11, -0.11), (1219.119, -0.119),
            (1224.128, -0.128), (1229.136, -0.136), (1234.143, -0.143), (1239.15, -0.15), (1244.156, -0.156), (1249.162, -0.162),
            (1254.168, -0.168), (1259.174, -0.174), (1264.179, -0.179), (1269.184, -0.184), (1274.189, -0.189), (1279.194, -0.194),
            (1284.2, -0.2), (1289.205, -0.205), (1294.211, -0.211), (1299.216, -0.216), (1304.222, -0.222), (1309.228, -0.228),
            (1314.233, -0.233), (1319.239, -0.239), (1324.243, -0.243), (1329.247, -0.247), (1334.249, -0.249), (1337.58, -0.25)
        ]
        return Interpolate_Table(temperature_input, temperature_table)
