# This example python code will read data from a json string and submit the results to a HTTP request call using the requests python library which may need to be loaded
# separately as it is not apart of the basic python library set. The example code will get all "Cu" and "Ni" alloy data from the years 1934 to 1965 from the database.
import requests

# Define the headers to send down to the API URI
headers={'content-type':'application/x-www-form-urlencoded;','Access-Control-Allow-Origin':'*','User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0'}

# Define the search data JSON to send to the API URI
search_data={"exclude_all":"True","required_compounds":["Cu","Ni"],"start_year": 1934,"end_year": 2016}

# Define the URL to send the request
# Note that this example does require an authentication key to get the data. The one given here is an invalid authkey and will need to be replaced by
# a valid authentication key which may be requested free of charge from TRCalloy@nist.gov.
url='https://trc.nist.gov/MetalsAlloyAPI/search?authkey=e6f23531dc56b7a1687f2ba492254c5b'

# Get the compound data from a requests post
compound_data_response = requests.post(url, json=search_data, headers=headers)

# Now analyze, write out, examine, or graph the compound data as needed. It must be noted that
# that the compound_data object is a "response" object and the actual output JSON is in the
# text field of that object. So use compound_data_response.text to use the actual output JSON
output_file = open('../../output_examples/compound_data3.json','w')
output_file.write(compound_data_response.text)
output_file.close()
