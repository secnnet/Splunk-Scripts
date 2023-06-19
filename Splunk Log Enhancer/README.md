# Splunk Log Enhancer

The Splunk Log Enhancer is a Python script that enhances log records in Splunk by adding a 'superhost' field. The 'superhost' field contains a modified version of the 'hostname' field based on the specified number of parts.

## Prerequisites

- Python 3.x
- Splunk

## Installation

1. Clone this repository or download the script file `splunk_log_enhancer.py`.

2. Ensure that you have Python 3.x installed on your system.

3. Install the required Python packages by running the following command:

    ```pip install -r requirements.txt
    ```
	
4. Configure the Splunk environment and provide necessary authentication details (if required) to access the log records.

## Usage

To use the Splunk Log Enhancer:

1. Open the `splunk_log_enhancer.py` script in a text editor.

2. Modify the script parameters as needed:

- `field`: Specify the field name containing the hostname (default: 'hostname').
- `parts`: Specify the number of parts to extract from the hostname (default: 2).

3. Save the changes to the script.

4. Execute the script using the following command:

    ```python splunk_log_enhancer.py
    ```
	
The script will connect to Splunk, retrieve the log records, enhance them by adding the 'superhost' field, and output the results.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please feel free to submit a pull request or open an issue in this repository.

## License

This project is licensed under the [MIT License](LICENSE).

