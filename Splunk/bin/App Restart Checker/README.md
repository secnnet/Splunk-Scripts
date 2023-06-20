# Splunk Restart Checker

The Splunk Restart Checker is a Bash script that helps determine if a restart is required for a particular Splunk application or directory. It analyzes configuration files and identifies whether any changes necessitate a restart or reload of the application.

## Usage

1. Clone the repository or download the Bash script.
2. Make sure the script has executable permissions (`chmod +x splunk_restart_checker.sh`).
3. Run the script with the desired options:

    ```
    ./splunk_restart_checker.sh -d <directory>
    ```

- Use the `-d` option to specify the directory or a comma-separated string of directories to check for restart requirements.

4. Review the output, which will indicate whether a restart is required for each application in the specified directory/directories.

## Dependencies

The Splunk Restart Checker has the following dependencies:

- Bash (Bourne Again SHell)
- Splunk (installed on the local system)
- Access to Splunk configuration files (e.g., `/opt/splunk/etc/system/default/app.conf`, `${app}/default/app.conf`, etc.)
