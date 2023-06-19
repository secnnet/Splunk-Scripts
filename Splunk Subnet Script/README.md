# IP Subnet Truncator

The IP Subnet Truncator is a Python script that truncates IP addresses to their corresponding /24 subnets. This script is designed to be used in conjunction with Splunk, a data analysis and visualization platform.

## Usage

1. Ensure that you have Python installed on your system.

2. Clone the repository or download the `ip_subnet_truncator.py` file to your local machine.

3. Install the required dependencies by running the following command:

    ```pip install splunk-sdk 
    ```

4. Modify the script if necessary:
- Customize the regular expression pattern in `ipregex` if you need to match IP addresses in a different format.
- Adjust the field name in the `field` variable if you want to process a different field from the Splunk search results.

5. Execute the script by running the following command:

    ```python ip_subnet_truncator.py	
    ```

6. The script will integrate with Splunk and process the specified field in the search results. It will add a new field named "subnet" to each result, containing the truncated /24 subnet of the IP address.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request. We appreciate your feedback and contributions.

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute the code according to the terms of the license.

## Acknowledgements

The IP Subnet Truncator script is built using the [Splunk SDK for Python](https://github.com/splunk/splunk-sdk-python). We acknowledge the Splunk team for their excellent work in providing the SDK.
