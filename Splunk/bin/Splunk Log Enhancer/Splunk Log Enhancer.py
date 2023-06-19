import sys
import splunk.Intersplunk
import re

# Regular expression pattern to match IP addresses
ipregex = r"(?P<ip>((25[0-5]|2[0-4]\d|[01]\d\d|\d?\d)\.){3}(25[0-5]|2[0-4]\d|[01]\d\d|\d?\d))"
ip_rex = re.compile(ipregex)

def super_domain(host, output_parts):
    """
    Modify the host by extracting 'output_parts' from the beginning
    or end of the host parts based on whether it is an IP address or not.
    """
    parts = host.split(".")
    num_parts = len(parts)

    # If the number of output parts is greater than the number of parts, return the original host
    if output_parts > num_parts:
        return host

    if ip_rex.match(host):
        # If the host is an IP address, join parts from the beginning up to output_parts
        host = '.'.join(parts[:-output_parts])
    else:
        # If the host is not an IP address, join the last output_parts parts
        host = '.'.join(parts[-output_parts:])

    return host

def add_superhost(results, field, num_parts):
    """
    Add a 'superhost' field to each result dictionary based on the 'field' value.
    """
    for r in results:
        if field not in r:
            continue
        d = super_domain(r[field], num_parts)
        r['superhost'] = d
        yield r

try:
    # Retrieve keywords and options passed to the script
    keywords, options = splunk.Intersplunk.getKeywordsAndOptions()

    # Retrieve the 'field' option and use 'hostname' as the default value
    field = options.get('field', 'hostname')

    # Retrieve the 'parts' option and convert it to an integer, use 2 as the default value
    num_parts = int(options.get('parts', 2))

    # Retrieve the results from Splunk
    results, dummyresults, settings = splunk.Intersplunk.getOrganizedResults()

    # Apply the 'add_superhost' function to the results
    results = list(add_superhost(results, field, num_parts))

except:
    import traceback
    stack = traceback.format_exc()
    results = splunk.Intersplunk.generateErrorResults("Error: Traceback: " + str(stack))

# Output the results
splunk.Intersplunk.outputResults(results)
