# Add Semester Field to Splunk Search Results

This script adds a "semester" field to Splunk search results based on the timestamp values of the data. It enables users to perform statistical operations or filtering by semester in their Splunk queries.

## Usage

1. Ensure you have Python installed on your system.

2. Copy the `add_semester_field.py` script to your local environment or server where you run Splunk.

3. In your Splunk search, pipe the output to the `add_semester_field.py` script using the "| script" command.

    Example:
    ```
    | your_search | script add_semester_field.py
    ```

4. The script will modify the search results by adding a "semester" field to each result, representing the corresponding semester based on the timestamp values.

5. Use the "semester" field in subsequent Splunk commands, such as statistical calculations or filtering.

    Example:
    ```
    | your_search | stats max(clients) by semester
    ```

## Dependencies

- Python 3.x
- Splunk SDK (splunk.Intersplunk module)

## Notes

- The script assumes that the timestamp field in the search results is named "_time". Modify the script if your timestamp field has a different name.

- If a result does not have a valid timestamp or encounters an error, the script sets the "semester" field to a default value (e.g., "N/A").

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.
