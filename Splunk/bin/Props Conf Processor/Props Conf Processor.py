import os
import re
import argparse
import logging
from logging.config import dictConfig

# Configure logging
logging_config = {
    'version': 1,
    'formatters': {
        'f': {'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'f', 'level': logging.DEBUG},
        'file': {'class': 'logging.handlers.RotatingFileHandler', 'filename': '/tmp/event_breaker_config.log',
                 'formatter': 'f', 'maxBytes': 2097152, 'level': logging.DEBUG}
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': logging.DEBUG,
    },
}

dictConfig(logging_config)
logger = logging.getLogger()

# Command-line argument parsing
parser = argparse.ArgumentParser(description='Extract LINE_BREAKER entries from Splunk props.conf files.')
parser.add_argument('-srcDir', help='Source directory containing Splunk application directories', required=True)
parser.add_argument('-destDirRoot', help='Root directory for the output', required=True)
parser.add_argument('-debugMode', help='Turn on DEBUG level logging (defaults to INFO)', action='store_true')
args = parser.parse_args()

# Set logging level based on debug mode
if args.debugMode:
    logging.getLogger().setLevel(logging.DEBUG)
else:
    logging.getLogger().setLevel(logging.INFO)

# Function to list only directories within a given directory
def listdirs(directory):
    return [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]

# Extract directory structure with props.conf files
def extract_directory_structure(src_dir):
    app_dirs_required = {}
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file == 'props.conf':
                app_dir = os.path.relpath(root, src_dir)
                if app_dir not in app_dirs_required:
                    app_dirs_required[app_dir] = []
                app_dirs_required[app_dir].append(root)
                logger.debug(f"Adding file {file} from directory {root}")
    return app_dirs_required

# Extract LINE_BREAKER entries and create EVENT_BREAKER versions
def extract_event_breakers(app_dirs_required):
    regex_line_breaker = re.compile(r"^\s*LINE_BREAKER(.*)")
    regex_should_linemerge = re.compile(r"^\s*SHOULD_LINEMERGE\s*=\s*([^ \r\n]+)\s*")

    output_files = {}
    for app_dir, subdirs in app_dirs_required.items():
        for subdir in subdirs:
            props_file = os.path.join(subdir, 'props.conf')
            logger.info(f"Processing file: {props_file}")
            with open(props_file, 'r') as file:
                current_stanza = ""
                line_breaker_found = False
                event_breaker = False
                output_lines = []

                for line in file:
                    line = line.strip()

                    # Check if it's a stanza entry
                    if line.startswith('['):
                        # Add a newline to the end of the last stanza
                        if current_stanza and output_lines:
                            output_lines.append('')

                        current_stanza = line
                        logger.debug(f"Working with stanza {current_stanza} in file {props_file}")
                        continue

                    # Check for LINE_BREAKER or SHOULD_LINEMERGE=false
                    match_line_breaker = regex_line_breaker.match(line)
                    match_should_linemerge = regex_should_linemerge.match(line)
                    if match_line_breaker or match_should_linemerge:
                        line_breaker_found = True

                        if match_line_breaker:
                            # Remove non-capturing regexes if present
                            line_breaker = match_line_breaker.group(1).replace("?:", "")
                            output_line = f"EVENT_BREAKER {line_breaker}"
                        else:
                            should_linemerge = match_should_linemerge.group(1).lower()
                            if should_linemerge == "false" or should_linemerge == "0":
                                output_line = "EVENT_BREAKER_ENABLE = true"
                                event_breaker = True
                            else:
                                continue

                        # Append the line to the output lines
                        output_lines.append(output_line)

                if event_breaker and not line_breaker_found:
                    output_lines.append("EVENT_BREAKER = ([\\r\\n]+)")
                elif line_breaker_found and not event_breaker:
                    logger.warn(f"For {current_stanza} in {subdir}, there was a LINE_BREAKER, but SHOULD_LINEMERGE is not set to false. It won't work as expected. Fix it!")

                if output_lines:
                    output_files[app_dir] = output_lines

    return output_files

# Create output directories and write the modified props.conf files
def create_output_directories(output_files, dest_dir_root):
    for app_dir, lines in output_files.items():
        output_dir = os.path.join(dest_dir_root, app_dir)
        logger.debug(f"Creating directory: {output_dir}")

        try:
            os.makedirs(output_dir, exist_ok=True)
        except OSError as e:
            logger.error(f"Failed to create directory: {output_dir}")
            raise e

        props_file_path = os.path.join(output_dir, 'props.conf')
        with open(props_file_path, 'w') as output_file:
            for line in lines:
                output_file.write(line + '\n')

# Main script execution
if __name__ == '__main__':
    # Extract directory structure with props.conf files
    app_dirs_required = extract_directory_structure(args.srcDir)

    # Extract LINE_BREAKER entries and create EVENT_BREAKER versions
    output_files = extract_event_breakers(app_dirs_required)

    # Create output directories and write the modified props.conf files
    create_output_directories(output_files, args.destDirRoot)
