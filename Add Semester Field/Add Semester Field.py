#!/usr/bin/env python
"""
Add semester - Add a semester field, so you can do
| addsemester | stats max(clients) by semester
"""

import sys
import splunk.Intersplunk
import datetime

def get_semester(d):
    # Determine the semester based on the date
    year = d.year
    month = d.month
    day = d.day

    if month < 5 or (month == 5 and day <= 15):
        return "Spring %d" % year
    if month <= 8:
        return "Summer %d" % year
    else:
        return "Fall %d" % year

def get_results():
    # Retrieve keywords and options from Splunk search
    keywords, options = splunk.Intersplunk.getKeywordsAndOptions()
    cutoff = int(options.get('cutoff', 0))

    # Get the search results
    results, dummyresults, settings = splunk.Intersplunk.getOrganizedResults()

    # Iterate over each result and add the semester field
    for r in results:
        try:
            ts = r["_time"]
            d = datetime.date.fromtimestamp(int(ts))
            r["semester"] = get_semester(d)
        except (KeyError, ValueError) as e:
            # Handle specific exceptions: KeyError and ValueError
            # Set the semester field to a default value if an exception occurs
            r["semester"] = "N/A"  # Or any appropriate default value

    return results

try:
    # Call the get_results function
    results = get_results()
except Exception as e:
    import traceback
    stack = traceback.format_exc()
    results = splunk.Intersplunk.generateErrorResults("Error: " + str(e) + "\nTraceback: " + str(stack))

# Output the modified results
splunk.Intersplunk.outputResults(results)
