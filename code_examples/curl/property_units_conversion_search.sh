# This curl example will retrieve a JSON data file containing the data output for a property value search involving the required property "T" and  
# units converted to SI units for the years 1970 to 1979.
#
# Note that this example does require an authentication key to get the data. The one given here is an invalid authkey and will need to be replaced by
# a valid authentication key which may be requested free of charge from TRCalloy@nist.gov.
#
curl -X POST "https://trc.nist.gov/MetalsAlloyAPI/search?authkey=e6f23531dc56b7a1687f2ba492254c5b" -d @../../search_examples/property_units_conversion.json -o ../../output_examples/property_units_conversion_data.json
