#!/bin/sh

# This script transfers files using rsync with resume functionality

if [ $# -lt 1 ]; then
    echo "Error: Need index argument"
    exit 1
fi

indexname=$1

# Limit at which to throttle the rsync transfer
bandwidthlimit="4096"
if [ $# -gt 1 ]; then
  bandwidthlimit=$2
fi

successFile="/tmp/successfultransferlist_${indexname}.txt"
tmpFile="/tmp/tmpfile_${indexname}.txt"

# Get a list of files to transfer from source directories
# /path/to/hotSourceVol: Replace with the actual path to the hot source volume directory.
find "/path/to/hotSourceVol/${indexname}/" -name "[dr]b*" | grep -v "\.rbsentinel" | grep -vE "/db$" | grep -v grep > "$tmpFile"

# /path/to/coldSourceVol: Replace with the actual path to the cold source volume directory.
find "/path/to/coldSourceVol/${indexname}/" -name "[dr]b*" | grep -v "\.rbsentinel" | grep -vE "/colddb$" | grep -v grep >> "$tmpFile"

# Check if a successFile exists and remove files that have already been successfully transferred
if [ -s "$successFile" ]; then
    sort "$successFile" > "${successFile}.sorted"
    sort "$tmpFile" > "${tmpFile}.sorted"
    comm -23 "${tmpFile}.sorted" "${successFile}.sorted" > "${tmpFile}.2"
    mv "${tmpFile}.2" "$tmpFile"
fi

destDir="/path/to/destination/${indexname}/hot"

# Create the destination directory on the destination host
# user@desthost: Replace with the username and hostname of the destination host.
ssh -n -o "BatchMode yes" -o StrictHostKeyChecking=no -o ServerAliveInterval=30 -o ConnectTimeout=10 user@desthost "mkdir -p $destDir"

# Iterate over each file in tmpFile and transfer if it meets the criteria
while IFS= read -r file; do
    time=$(echo "$file" | cut -d "/" -f6 | cut -d "_" -f3)
    epochTime=FIXME  # Replace with the appropriate epoch time

    if [ "$time" -gt "$epochTime" ]; then
        echo "$(date +"%Y-%m-%d %H:%M:%S"): File $file is in scope for transfer, initiating transfer"
        rsync -r -p -t -g --delete --exclude=.snapshots --bwlimit="$bandwidthlimit" "$file" user@desthost:"$destDir"

        if [ $? -eq 0 ]; then
            echo "$(date +"%Y-%m-%d %H:%M:%S"): File $file transfer completed successfully"
            echo "$file" >> "$successFile"
        fi
    fi
done < "$tmpFile"
