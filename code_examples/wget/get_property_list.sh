# This wget example will retrieve the list of properties available in the TRC Alloys database. The output file will be a JSON file that contains
# an array of property objects comprised of {property_code, property_name} The property_code will be used in some data searches that restrict data
# by the property
#
# i.e. {"property_list": [{"property_code": "PTV", "property_name": "Thermal pressure coefficient"},...]}
# Note that this example does not require an authentication key to get the data.
#
wget -dSO ../../output_examples/property_list.json https://trc.nist.gov/MetalsAlloyAPI/propertylist
