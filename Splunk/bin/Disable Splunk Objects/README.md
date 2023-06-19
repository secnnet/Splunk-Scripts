# Props Conf Processor

Props Conf Processor is a Python script that extracts LINE_BREAKER entries from Splunk `props.conf` files and generates modified versions with EVENT_BREAKER configurations. This script helps in managing log processing configurations in Splunk applications.

## Features

- Recursively searches for `props.conf` files in a specified directory.
- Identifies stanzas containing LINE_BREAKER entries and extracts relevant information.
- Handles scenarios where LINE_BREAKER is present but SHOULD_LINEMERGE is not set to false.
- Generates modified versions of `props.conf` files with EVENT_BREAKER configurations.
- Maintains the directory structure of the input directory in the output directory.
- Provides logging functionality with configurable log levels.

## Usage

1. Ensure that you have Python 3.x installed on your system.
2. Clone this repository or download the `props_conf_processor.py` script.
3. Open a terminal or command prompt and navigate to the directory containing the script.
4. Run the script with the following command:

`python props_conf_processor.py -srcDir <source_directory> -destDirRoot <output_directory> [-debugMode]`

Replace `<source_directory>` with the path to the directory containing Splunk applications and `<output_directory>` with the desired root directory for the output. Add the `-debugMode` flag to enable DEBUG level logging.

5. The script will process the `props.conf` files, generate modified versions with EVENT_BREAKER configurations, and save them in the specified output directory.

## License

This project is licensed under the [MIT License](LICENSE).

## Disclaimer

This script is provided as-is without any warranty. Use it at your own risk.










