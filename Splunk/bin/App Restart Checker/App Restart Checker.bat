#!/bin/bash

# Script to determine whether or not a restart of a specific application or directory inside Splunk is required in accordance with
# https://docs.splunk.com/Documentation/Splunk/latest/Indexer/Updatepeerconfigurations#Restart_or_reload_after_configuration_bundle_changes.3F

# Get the current date and time
date=$(date +"%Y-%m-%d %H:%M:%S.%3N %z")

# Function to check if a value exists in a list
exists_in_list() {
    local LIST=$1
    local DELIMITER=" "
    local VALUE=$2
    echo "$LIST" | tr "$DELIMITER" '\n' | grep -F -q -x "$VALUE"
}

# Display script usage
usage() {
    echo "Usage: ./$(basename "$0") -d <directory>"
}

# Check for command-line arguments
if [ $# -eq 0 ]; then
  usage
  exit 0
fi

# Process command-line options
while getopts "d:" option; do
    case "${option}" in
        d)
            dir=$(echo "${OPTARG}" | tr ',' ' ')
            ;;
        *)
            usage
            exit 0
            ;;
    esac
done

# List of configuration files to reload
reload_conf=$(grep "reload.*= simple" /opt/splunk/etc/system/default/app.conf | cut -d "." -f2 | awk '{ print $1".conf" }' | sort | uniq)
# Additional configuration files that may require a restart
reload_conf+=" authentication.conf authorize.conf collections.conf indexes.conf messages.conf props.conf transforms.conf web.conf workload_pools.conf workload_rules.conf workload_policy.conf inputs.conf restmap.conf"

# Flag to track if a restart is required for any app
restart_required_any="False"

echo "${date} Restart script begins"

# Check if distsearch.conf file needs to be ignored based on certain conditions
dist_search_ignore="True"
files=$(ls ${app}/default/distsearch.conf ${app}/local/distsearch.conf 2>/dev/null)
if [ -n "$files" ]; then
    for file in $files; do
        count=$(grep "^\[" "$file" 2>/dev/null | grep -v "\[replication[ABDW]" | wc -l)
        if [ "$count" -ne 0 ]; then
            dist_search_ignore="False"
        fi
    done
fi

# Check if server.conf file needs to be ignored based on certain conditions
server_conf_ignore="True"
files=$(ls ${app}/default/server.conf ${app}/local/server.conf 2>/dev/null)
if [ -n "$files" ]; then
    for file in $files; do
        count=$(grep -vE "^(#|\[|\s*$)" "$file" 2>/dev/null | grep -v "conf_replication_" | wc -l)
        if [ "$count" -ne 0 ]; then
            server_conf_ignore="False"
        fi
    done
fi

# Iterate over each directory specified
for app in $dir; do
    restart_required="False"
    default=$(ls "${app}/default" 2>/dev/null | grep -vE "No such file|data")
    local=$(ls "${app}/local" 2>/dev/null | grep -vE "No such file|data")
    combined="$default $local"

    # Check if the app has custom triggers for reload
    custom_app_reload_default=$(grep "^reload\..*= simple" "${app}/default/app.conf" 2>/dev/null | cut -d "." -f2 | awk '{ print $1".conf" }')
    custom_app_reload_local=$(grep "^reload\..*= simple" "${app}/local/app.conf" 2>/dev/null | cut -d "." -f2 | awk '{ print $1".conf" }')
    custom_app_reload="$custom_app_reload_default $custom_app_reload_local"

    # Add server.conf and distsearch.conf to custom triggers if they can be ignored
    if [ "$server_conf_ignore" = "True" ]; then
        custom_app_reload+=" server.conf"
    fi
    if [ "$dist_search_ignore" = "True" ]; then
        custom_app_reload+=" distsearch.conf"
    fi

    # Check if files need to be reloaded or if a restart is required
    for file in $combined; do
        if exists_in_list "$reload_conf" "$file"; then
            echo "${date} ${app}/$file in system/default/app.conf, reload=true"
        elif exists_in_list "$custom_app_reload" "$file"; then
            echo "${date} ${app}/$file in ${app}/app.conf, reload=true"
        else
            echo "${date} ${app}/$file not found, reload=false"
            restart_required="True"
            restart_required_any="True"
        fi
    done

    echo "${date} app=${app} restart_required=${restart_required}"
done

echo "${date} restart_required=${restart_required_any}"
