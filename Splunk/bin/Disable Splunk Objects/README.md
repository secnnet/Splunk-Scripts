# Splunk Object Migrator

The Splunk Object Migrator script is a Python script that enables you to migrate Splunk configuration, specifically saved searches (reports and alerts), from one Splunk search head to another using the Splunk REST API. The script allows you to selectively disable or enable specific objects during the migration process.

## Features

- Retrieve a list of objects (saved searches) from a source Splunk instance using the REST API.
- Selectively include or exclude objects based on specified criteria.
- Perform migrations to a destination Splunk instance.
- Enable or disable specific objects during the migration process.
- Logging capabilities with different log levels (INFO and DEBUG).

## Prerequisites

Before using the script, ensure you have the following:

- Python 3.x installed on your system.
- Required Python packages installed. You can install them using `pip install -r requirements.txt`.

## Usage

1. Clone or download the script to your local machine.
2. Install the required Python packages by running the following command in your terminal:

`pip install -r requirements.txt`


3. Open a terminal or command prompt and navigate to the directory where the script is located.
4. Run the script with the following command:

`python splunk_object_migrator.py -destURL <destination_url> -destApp <destination_app> -destUsername <destination_username> -destPassword <destination_password> [optional_arguments]`


Replace the `<destination_url>`, `<destination_app>`, `<destination_username>`, and `<destination_password>` with the appropriate values for your setup.

5. Optional arguments:

- `-debugMode`: Enable DEBUG level logging for more detailed information (default is INFO level).
- `-includeEntities <object_list>`: Specify a comma-separated list of objects to include. Only these objects will be migrated.
- `-excludeEntities <object_list>`: Specify a comma-separated list of objects to exclude. All other objects within the app will be migrated except for these.
- Additional options for date filtering and object enable/disable actions as per script documentation.

6. Monitor the script output and log files for progress and any errors or warnings.

## License

This script is licensed under the [MIT License](LICENSE).

## Disclaimer

The script is provided as-is without any warranty. Use it at your own risk. Make sure to review and test the script in a non-production environment before using it in a production environment.

Feel free to modify and customize the script according to your requirements.

For detailed information on the script and its functionality, refer to the script source code and comments.
