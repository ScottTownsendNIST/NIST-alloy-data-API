# This curl example will retrieve a JSON data file containing the data output for a compound search involving the required compounds "Ti" and "Ni" with  
# optional element "Al" from the years 1955 to 2016 and the data all pulled from graph.
#
# Note that this example does require an authentication key to get the data. The one given here is an invalid authkey and will need to be replaced by
# a valid authentication key which may be requested free of charge from TRCalloy@nist.gov.
#
curl -X POST "https://trc.nist.gov/MetalsAlloyAPI/search?authkey=e6f23531dc56b7a1687f2ba492254c5b" -d @../../search_examples/compound_search2.json -o ../../output_examples/compound_data2.json
