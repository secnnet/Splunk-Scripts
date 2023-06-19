# Splunk Add Records Script

The Splunk Add Records Script is a Python script that processes search results obtained from Splunk and adds information about when a new record is reached. It is designed to enhance the analysis and understanding of the data by providing additional details about record milestones.

## Usage

To use the script, follow these steps:

1. Copy the script code and save it in a file with a meaningful name, such as `add_records_info.py`.

2. Ensure you have Python installed on your system.

3. In Splunk, perform a search and pipe the results to the script using the following syntax:

    ```
    <your_search> | <script_file> <field_name>
    ```

    - `<your_search>`: Replace this with your actual Splunk search query.

    - `<script_file>`: Specify the path to the saved script file (`add_records_info.py`).

    - `<field_name>`: Optionally, provide the name of the field in the search results to use for tracking records. If not specified, the script will default to the `_raw` field.

4. Run the search to execute the script and observe the modified search results. The script will add the following fields to each result:

    - `record`: Indicates whether the result is a new record (`True` or `False`).
    - `since_record`: The number of results since the last new record.
    - `increase`: The difference between the current value and the previous maximum value.
    - `last_record`: The timestamp of the last new record.
    - `consecutive_records`: The number of consecutive new records encountered.

## Input Validation

The script includes input validation to handle potential errors or unexpected input gracefully. The following validations are performed:

- Field Presence Validation: The script checks if the specified field (or `_raw` if not specified) is present in the input data. If the field is missing, a `ValueError` is raised, and an error message is generated.

- Float Conversion Validation: When attempting to convert the field values to floats, the script uses a try-except block to catch any `ValueError`. If the conversion fails for a specific result, that result is skipped, allowing the script to handle cases where the field values cannot be converted to floats.

## Requirements

- Python 3.x
- Splunk

## License

This script is licensed under the [MIT License](LICENSE).

