import requests
import logging
import argparse
import json

# Setup the logging configuration
logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', level=logging.DEBUG)

# Create the argument parser
parser = argparse.ArgumentParser(description='Disable/enable Splunk objects (saved searches) via the REST API')
parser.add_argument('-destURL', help='URL of the Splunk instance, e.g., https://localhost:8089', required=True)
parser.add_argument('-destApp', help='Application name to be migrated to (defaults to srcApp)', required=True)
parser.add_argument('-destUsername', help='Username for the Splunk instance', required=True)
parser.add_argument('-destPassword', help='Password for the Splunk instance', required=True)
parser.add_argument('-debugMode', help='Turn on DEBUG level logging (default is INFO)', action='store_true')
parser.add_argument('-includeEntities', help='Comma-separated list of objects to include (enclosed in double quotes)')
parser.add_argument('-excludeEntities', help='Comma-separated list of objects to exclude (enclosed in double quotes)')
args = parser.parse_args()

# Set the logging level based on debugMode flag
logging.getLogger().setLevel(logging.DEBUG if args.debugMode else logging.INFO)

# Function to filter dictionary keys
def without_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}

# Excluded keys for cleanArgs dictionary
excludedList = ["destPassword"]
cleanArgs = without_keys(vars(args), excludedList)
logging.info("disableSplunkObjects run with arguments %s" % (cleanArgs))

# Parse includeEntities and excludeEntities arguments
includeEntities = args.includeEntities.split(',') if args.includeEntities else None
excludeEntities = args.excludeEntities.split(',') if args.excludeEntities else None

# Construct the REST API search query based on date options
search = "| rest \"/servicesNS/-/" + args.destApp + "/directory?count=-1\" splunk_server=local"
if args.absoluteDate:
    search += f" | where updated > \"{args.absoluteDate}\""
elif args.relativeDate:
    search += f" | where updated > relative_time(now(), \"{args.relativeDate}\")"
search += " | table title, eai:acl.sharing, eai:acl.owner, updated"

# Send the search request to the Splunk instance
url = args.destURL + "/services/search/jobs"
payload = {"search": search, "output_mode": "json", "exec_mode": "oneshot"}
res = requests.post(url, auth=(args.destUsername, args.destPassword), verify=False, data=payload)

# Check the response status code
if res.status_code != requests.codes.ok and res.status_code != 201:
    logging.error("URL %s status code %s reason %s, response '%s', in app %s" % (url, res.status_code, res.reason, res.text, args.destApp))
else:
    logging.debug("App %s with URL %s result: '%s'" % (args.destApp, url, res.text))

# Load the result and process each object
jsonRes = json.loads(res.text)
resList = jsonRes.get("results", [])
logging.debug("Received %s results" % (len(resList)))

for aRes in resList:
    name = aRes["title"]
    sharing = aRes["eai:acl.sharing"]
    owner = aRes["eai:acl.owner"]
    lastUpdated = aRes["updated"]

    # Check if the object should be included or excluded
    if includeEntities and name not in includeEntities:
        logging.debug("%s not in includeEntities list in app %s, skipping" % (name, args.destApp))
        continue
    if excludeEntities and name in excludeEntities:
        logging.debug("%s in excludeEntities list in app %s, skipping" % (name, args.destApp))
        continue

    # Determine if the object is an alert or a report
    isAlert = False
    if args.enableObj or args.disableObj:
        url = args.destURL + "/servicesNS/" + owner + "/" + args.destApp + "/saved/searches/" + name
        res = requests.get(url, auth=(args.destUsername, args.destPassword), verify=False)
        if res.status_code != requests.codes.ok:
            logging.error("URL %s status code %s reason %s, response '%s', in app %s" % (url, res.status_code, res.reason, res.text, args.destApp))
            break
        localRes = json.loads(res.text)
        if localRes["entry"][0]["content"].get("alert_condition"):
            logging.debug("%s of sharing level %s with owner %s appears to be an alert" % (name, sharing, owner))
            isAlert = True

    # Enable or disable the object if required
    actionTaken = False
    if args.enableObj:
        payload["disabled"] = "0" if isAlert else "1"
        payload["is_scheduled"] = "1" if not isAlert else "0"
        actionTaken = "enabled"
    elif args.disableObj:
        payload["disabled"] = "1" if isAlert else "0"
        payload["is_scheduled"] = "0" if not isAlert else "1"
        actionTaken = "disabled"

    if actionTaken:
        res = requests.post(url, auth=(args.destUsername, args.destPassword), verify=False, data=payload)
        if res.status_code != requests.codes.ok:
            logging.error("URL %s status code %s reason %s, response '%s', in app %s" % (url, res.status_code, res.reason, res.text, args.destApp))
            break

        logging.info("Name %s sharing %s owner %s updated %s in app %s is now %s" % (name, sharing, owner, lastUpdated, args.destApp, actionTaken))
    else:
        logging.info("No enable/disable flags used, name %s sharing %s owner %s updated %s is in scope in app %s" % (name, sharing, owner, lastUpdated, args.destApp))

logging.info("Done")
