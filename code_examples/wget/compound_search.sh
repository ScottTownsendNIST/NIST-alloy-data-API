# This wget example will retrieve a JSON data file containing the data output for a compound search involving the required elements "Ti" and "Ni" 
# with the optional element "Al" for the year 1993.
#
# Note that this example does require an authentication key to get the data. The one given here is an invalid authkey and will need to be replaced by
# a valid authentication key which may be requested free of charge from TRCalloy@nist.gov.
#
wget -dSO ../../output_examples/compound_data1.json --post-file=../../search_examples/compound_search1.json https://trc.nist.gov/MetalsAlloyAPI/search?authkey=e6f23531dc56b7a1687f2ba492254c5b
