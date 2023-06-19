import logging

logger = logging.getLogger()

def index_tuning_presteps(utility, index_list, index_ignore_list, earliest_license, latest_license, index_name_restriction, index_limit, indexerhostnamefilter, useIntrospectionData, indexes_not_getting_sized):
    logger.info("Running index_tuning_presteps")
    conf_files_to_check = {}

    # Step 1: Identify relevant configuration files
    for index in index_list:
        conf_file = index_list[index].conf_file
        # Ignore known system files that should not be modified
        if "/etc/system/default/" not in conf_file and "_cluster/default/" not in conf_file:
            conf_files_to_check[conf_file] = True

    logger.debug("conf_files_to_check=\"%s\"" % conf_files_to_check)

    # Step 2: Parse configuration files for sizing comments
    logger.info("Running parse_conf_files_for_sizing_comments()")
    utility.parse_conf_files_for_sizing_comments(index_list, conf_files_to_check)

    counter = 0
    index_count = len(index_list)

    if index_limit < index_count:
        index_count = index_limit

    # Step 3: Process each index
    for index_name in index_list:
        # If there is a restriction on which indexes to process, skip others
        if index_name_restriction and index_name != index_name_restriction:
            continue

        logger.debug("iteration_count=%s of iteration_count=%s within loop" % (counter, index_count))

        # Quit the loop if the index limit has been reached
        if counter > index_limit:
            break

        # Step 3a: Determine license usage per day
        logger.info("index=%s running determine_license_usage_per_day" % index_name)
        index_list[index_name].avg_license_usage_per_day, index_list[index_name].first_seen, index_list[index_name].max_license_usage_per_day = \
            utility.determine_license_usage_per_day(index_name, earliest_license, latest_license)

        # Step 3b: Determine compression ratio and related metrics
        logger.info("index=%s running determine_compression_ratio" % index_name)
        index_list[index_name].index_comp_ratio, index_list[index_name].splunk_max_disk_usage_mb, index_list[index_name].oldest_data_found, index_list[index_name].newest_data_found = \
            utility.determine_compression_ratio(index_name, indexerhostnamefilter, useIntrospectionData)

        index_list[index_name].summary_index = False
        avg_license_usage_per_day = index_list[index_name].avg_license_usage_per_day

        # Step 3c: Identify summary indexes
        if avg_license_usage_per_day == 0:
            json_result = utility.run_search_query("| metadata index=%s type=sourcetypes | table sourcetype" % index_name)

            # If no results or specific conditions indicate a summary index, set summary-related attributes
            if "results" in json_result and len(json_result["results"]) == 1 and json_result["results"][0]["sourcetype"] == "stash":
                json_result = utility.run_search_query(""" search index=_introspection \"data.name\"=\"%s\"
                | bin _time span=1d
                | stats max(data.total_size) AS total_size by host, _time
                | streamstats current=f window=1 max(total_size) AS prev_total by host
                | eval diff=total_size - prev_total
                | stats avg(diff) AS avgchange by host
                | stats avg(avgchange) AS overallavg""" % index_name)

                if "results" in json_result and len(json_result["results"]) == 1:
                    summary_usage_change_per_day = float(json_result["results"][0]["overallavg"])
                    logger.info("index=%s is a summary index, average_change_per_day=%s from introspection logs" % (index_name, summary_usage_change_per_day))
                    index_list[index_name].summary_usage_change_per_day = summary_usage_change_per_day
                index_list[index_name].summary_index = True

        counter += 1

    # Step 4: Remove indexes specified in the ignore list
    logger.debug("The following indexes will be ignored as per configuration index_ignore_list=\"%s\"" % index_ignore_list)
    for index in index_ignore_list:
        if index in index_list:
            indexes_not_getting_sized[index] = index_list[index]
            del index_list[index]
            logger.debug("Removing index=\"%s\" from index_list" % index)

    # (Optional) Step 5: Exclude metric indexes from tuning
    # Note: The code is commented out as it is not required
    """
    for index_name in index_list:
        datatype = index_list[index_name].datatype
        if datatype != 'event':
            logger.info("index=%s is excluded from tuning due to not been of type events, type=%s" % (index_name, datatype))
            indexes_not_getting_sized[index_name] = index_list[index_name]
            del index_list[index_name]
    """
