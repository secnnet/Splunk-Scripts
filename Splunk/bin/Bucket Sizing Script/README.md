# Splunk Bucket Sizing Script

This script performs bucket sizing calculations for Splunk indexes. It helps determine the recommended bucket size for each index based on various factors such as compression ratios, license usage, and data size. The script identifies indexes and configuration files that require changes in bucket sizing.

## Prerequisites

- Python 3.x
- Splunk environment with indexes configured

## Usage

1. Clone the repository or download the script.
2. Install the required dependencies: `pip install -r requirements.txt`
3. Modify the script to fit your specific Splunk environment and requirements.
4. Execute the script: `python bucket_sizing_script.py`

## Configuration

Make sure to update the following variables in the script according to your Splunk environment:

- `index_list`: A dictionary containing the indexes and their attributes.
- `index_limit`: Maximum number of indexes to process (optional).
- `bucket_contingency`: Contingency factor to adjust the recommended bucket size.
- `upper_comp_ratio_level`: Threshold for unusually large compression ratios.
- `min_size_to_calculate`: Minimum data size to perform alternative bucket size calculation.
- `num_of_indexers`: Number of Splunk indexers in the environment.
- `rep_factor_multiplier`: Replication factor multiplier for distributed Splunk environments.
- `do_not_lose_data_flag`: Flag indicating whether to prioritize data retention over bucket size.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This script is licensed under the [MIT License](LICENSE).

## Disclaimer

Please note that this script is provided as-is and OpenAI or the script author(s) cannot be held responsible for any issues or damages caused by its usage. Always test the script in a non-production environment before applying any changes to your Splunk deployment.

