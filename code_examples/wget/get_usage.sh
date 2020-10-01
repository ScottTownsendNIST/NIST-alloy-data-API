# This wget example will retrieve a JSON document describing the usage URIs for many of the most common retrievals of the API.
#
# Note that this example does not require an authentication key to get the data.
#
wget -dSO ../../output_examples/usage.json https://trc.nist.gov/MetalsAlloyAPI/APIdocumentation/usage
