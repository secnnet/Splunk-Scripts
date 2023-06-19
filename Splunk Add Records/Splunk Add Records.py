import sys
import splunk.Intersplunk
import re

try:
    # Retrieve keywords and options passed to the script
    keywords, options = splunk.Intersplunk.getKeywordsAndOptions()

    # Set the default field to "_raw", or override it with the first keyword if provided
    field = "_raw"
    if keywords:
        field = keywords[0]

    # Retrieve the search results, dummy results, and settings
    results, dummyresults, settings = splunk.Intersplunk.getOrganizedResults()

    # Sort the results based on the '_time' field
    results.sort(key=lambda x: x['_time'])

    # Validate if the specified field is present in the results
    if field not in results[0]:
        raise ValueError(f"Field '{field}' not found in the input data.")

    # Initialize variables
    max_value = 0
    last_record_time = None
    since_record = 0
    consecutive_records = 0

    # Iterate over each result
    for r in results:
        if field not in r:
            # Skip the result if the field is not present
            continue

        # Validate if the field value can be converted to a float
        try:
            value = float(r[field])
        except ValueError:
            # Skip the result if the conversion fails
            continue

        if value > max_value:
            # If the value is greater than the current maximum, it's a new record

            # Set additional information in the result
            r['record'] = True
            r['since_record'] = since_record
            r['increase'] = value - max_value
            r['last_record'] = last_record_time
            r['consecutive_records'] = consecutive_records

            # Update the maximum value and record details
            max_value = value
            last_record_time = r['_time']
            since_record = 1
            consecutive_records += 1
        else:
            # If the value is not greater than the current maximum, it's not a new record

            # Increment counters
            since_record += 1
            consecutive_records = 0

    # Sort the results again based on '_time', but in reverse order
    results.sort(key=lambda x: x['_time'], reverse=True)

except ValueError as ve:
    # Handle validation errors
    results = splunk.Intersplunk.generateErrorResults(str(ve))

except:
    import traceback

    # Generate an error message with traceback if an error occurs
    stack = traceback.format_exc()
    results = splunk.Intersplunk.generateErrorResults("Error: Traceback: " + str(stack))

# Output the modified results or error message
splunk.Intersplunk.outputResults(results)
