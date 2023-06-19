import sys
import splunk.Intersplunk
import re

# Regular expression pattern to match IP addresses
ipregex = r"(?P<ip>((25[0-5]|2[0-4]\d|[01]\d\d|\d?\d)\.){3}(25[0-5]|2[0-4]\d|[01]\d\d|\d?\d))"

def get_ips(line):
    # Extracts IP addresses from a line of text using regex
    # Returns a list of extracted IP addresses
    return [x[0] for x in re.findall(ipregex, line)]

def get_subnet(line):
    ips = get_ips(line)
    if not ips:
        return None
    ip = ips[0]
    parts = ip.split('.')
    # Join the first three parts of the IP address to form the subnet
    subnet = '.'.join(parts[:3])
    return subnet

try:
    # Get keywords and options passed to the script
    keywords, options = splunk.Intersplunk.getKeywordsAndOptions()
    field = "_raw"
    if keywords:
        field = keywords[0]

    # Retrieve the search results and associated settings
    results, dummyresults, settings = splunk.Intersplunk.getOrganizedResults()

    # Process each result
    for r in results:
        if field not in r:
            continue
        # Get the subnet for the specified field's value
        subnet = get_subnet(r[field])
        if subnet is not None:
            # Add a new field named "subnet" to the result
            r['subnet'] = subnet

except:
    # Handle any exceptions that occur during execution
    import traceback
    stack = traceback.format_exc()
    # Generate error results with the traceback information
    results = splunk.Intersplunk.generateErrorResults("Error: Traceback: " + str(stack))

# Output the modified results
splunk.Intersplunk.outputResults(results)
