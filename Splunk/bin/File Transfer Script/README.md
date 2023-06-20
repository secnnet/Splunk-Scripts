# File Transfer Script

This script is designed to facilitate file transfers using rsync with resume functionality. It allows you to transfer files from hot and cold source volumes to a specified destination directory, while excluding certain files and directories.

## Usage

1. Ensure that you have the necessary permissions to access the source and destination directories.
2. Update the script with the appropriate values for the following variables:
   - `indexname`: The index name or identifier for the file transfer.
   - `bandwidthlimit`: The bandwidth limit for the rsync transfer (default is set to 4096).
   - `hotSourceVol`: Replace with the actual path to the hot source volume directory.
   - `coldSourceVol`: Replace with the actual path to the cold source volume directory.
   - `destDir`: Replace with the actual path to the destination directory.
   - `epochTime`: Replace with the appropriate epoch time for file filtering.
   - `user@desthost`: Replace with the username and hostname of the destination host.
3. Run the script using the following command:

`/file_transfer_script.sh <indexname> [bandwidthlimit]`

- `<indexname>`: The index name or identifier for the file transfer.
- `[bandwidthlimit]` (optional): The desired bandwidth limit for the rsync transfer. If not provided, the default value will be used.

## Notes

- This script assumes that you have the necessary SSH keys set up to establish a connection with the destination host.
- Make sure to replace the placeholders in the script (such as `/path/to/hotSourceVol`, `/path/to/coldSourceVol`, `FIXME`, and `user@desthost`) with the appropriate values for your specific setup.

Feel free to modify the script according to your requirements and use it to efficiently transfer files using rsync.

For any questions or issues, please open an issue in this repository.
