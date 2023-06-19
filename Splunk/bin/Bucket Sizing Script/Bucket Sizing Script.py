import logging
import datetime

logger = logging.getLogger()


def run_bucket_sizing(index_list, index_limit, bucket_contingency, upper_comp_ratio_level,
                      min_size_to_calculate, num_of_indexers, rep_factor_multiplier, do_not_lose_data_flag):
    todays_date = datetime.datetime.now().strftime("%Y-%m-%d")

    indexes_requiring_changes = {}
    conf_files_requiring_changes = []

    counter = 0
    for index_name, index in index_list.items():
        if index_limit and counter >= index_limit:
            break

        # Calculate recommended bucket size
        recommended_bucket_size = determine_recommended_bucket_size(index_name)
        recommended_bucket_size *= bucket_contingency

        # Check if compression ratio is unusually large
        index_comp_ratio = index.index_comp_ratio
        if index_comp_ratio > upper_comp_ratio_level:
            logger.info(f"index={index_name}, index_compression_ratio={index_comp_ratio} exceeds max_index_compression_ratio={upper_comp_ratio_level}. "
                        f"Setting index_compression_ratio={upper_comp_ratio_level}")
            index_comp_ratio = upper_comp_ratio_level

        # Calculate alternative bucket size if data size is large enough
        if index.splunk_max_disk_usage_mb > min_size_to_calculate:
            alt_bucket_size_calc = calculate_alternative_bucket_size(index)
            if alt_bucket_size_calc > recommended_bucket_size:
                recommended_bucket_size = alt_bucket_size_calc

        # Check if change in bucket size is required
        requires_change = False
        if index.bucket_size.find("auto") == -1:
            logger.warn(f"Not an auto-sized bucket for index={index_name}. This index will be excluded from sizing")
            continue

        bucket_auto_size = float(index.bucket_size.split("_")[0])
        perc_diff = (100 / bucket_auto_size) * recommended_bucket_size

        if requires_bucket_increase(perc_diff, index):
            requires_change = "bucket"
            if not hasattr(index, "change_comment"):
                index.change_comment = {}
            index.change_comment['bucket'] = f"# Bucket size increase required. Estimated: {index.recommended_bucket_size}. Auto-tuned on {todays_date}\n"
            index.recommended_bucket_size = "auto_high_volume"
            index.max_data_size = "10240_auto"
            logger.info(f"index={index_name} requires a bucket size increase. "
                        f"Current bucket size: {index.bucket_size}. Recommended bucket size: {index.recommended_bucket_size}")

        elif requires_bucket_decrease(recommended_bucket_size, index):
            requires_change = "bucket"
            if not hasattr(index, "change_comment"):
                index.change_comment = {}
            index.change_comment['bucket'] = f"# Bucket size decrease required. Estimated: {index.recommended_bucket_size}. Auto-tuned on {todays_date}\n"
            index.recommended_bucket_size = "auto"
            index.max_data_size = "750_auto"
            logger.info(f"index={index_name} requires a bucket size decrease. "
                        f"Current bucket size: {index.bucket_size}. Recommended bucket size: {index.recommended_bucket_size}")

        if requires_change:
            indexes_requiring_changes[index_name] = requires_change

            conf_file = index.conf_file
            if conf_file not in conf_files_requiring_changes:
                conf_files_requiring_changes.append(conf_file)

        counter += 1

    return indexes_requiring_changes, conf_files_requiring_changes


def determine_recommended_bucket_size(index_name):
    # Perform queries and calculations to determine recommended bucket size for the index
    # Replace this with your actual implementation
    pass


def calculate_alternative_bucket_size(index):
    # Calculate alternative bucket size based on index attributes
    # Replace this with your actual implementation
    pass


def requires_bucket_increase(perc_diff, index):
    # Check if bucket size increase is required
    # Replace this with your actual implementation
    pass


def requires_bucket_decrease(recommended_bucket_size, index):
    # Check if bucket size decrease is required
    # Replace this with your actual implementation
    pass
