# This wget example will retrieve the list of compounds with data values in the TRC Alloys database. The output file will be a JSON file that contains
# an array of compound objects comprised of {compound_formula, compound_name, compound_data_count} Note that the compound_name is the NIST preferred name
# of the compound.
#
# i.e. {"compound_list": [{"compound_formula": "Ag", "compound_name": "silver", "compound_data_count": "83784"},...]}
# Note that this example does not require an authentication key to get the data.
#
wget -dSO ../../output_examples/compound_list.json https://trc.nist.gov/MetalsAlloyAPI/compoundlist
