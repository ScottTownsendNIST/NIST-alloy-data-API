# This curl example will retrieve a JSON data file containing the data output for a citation search involving the journal name "International Journal of Thermophysics"   
# for the year 2005.
#
# Note that this example does require an authentication key to get the data. The one given here is an invalid authkey and will need to be replaced by
# a valid authentication key which may be requested free of charge from TRCalloy@nist.gov.
#
curl -X POST "https://trc.nist.gov/MetalsAlloyAPI/search?authkey=e6f23531dc56b7a1687f2ba492254c5b" -d @../../search_examples/citation_by_journal_search.json -o ../../output_examples/citation_by_journal_data.json
