import shutil
import logging
from input_source.git_handler import clone_repo
from input_source.zip_handler import extract_zip
from input_source.archive_handler import extract_gz, extract_tar
import os
# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

AUTO_DELETE_TEMP = True  # Toggle for auto-deletion

def process_input(source: str) -> str:
    """
    Processes the input source, which can be a Git repository URL or a local ZIP file path.

    Args:
        source (str): The input source string.

    Returns:
        str: The path to the temporary directory containing the source code.
             Returns an empty string if processing fails.
    """
    logging.info(f"Processing input: {source}")

    # Check if the source is a Git repository URL
    if source.startswith(('http://', 'https://')):
        if not source.endswith('.git'):
            logging.info("Appending .git suffix to repo URL.")
            source += '.git'
        return clone_repo(source)

    # Check if the source is a ZIP file
    elif source.endswith('.zip'):
        if not os.path.exists(source):
            logging.error("ZIP file not found.")
            return ""
        return extract_zip(source)
    # Check if the source is a TAR file
    elif source.endswith(('.tar', '.tar.gz', '.tgz', '.tar.bz2')):
        if os.path.exists(source):
            return extract_tar(source)
        logging.error(" TAR file not found.")
        return ""
    # Check if the source is a GZ file
    elif source.endswith('.gz'):
        if os.path.exists(source):
            return extract_gz(source)
        logging.error(" GZ file not found.")
        return ""
    # Check if the source is a local folder path
    elif os.path.isdir(source):
        logging.info("Detected local folder path.")
        return source

    else:
        logging.error("Unsupported input type. Please provide a Git URL or a ZIP file path.")
        return ""


def cleanup_temp_dir(path: str):
    try:
        shutil.rmtree(path, ignore_errors=True)
        logging.info(f"Temporary directory deleted: {path}")
    except Exception as e:
        logging.error(f"Failed to delete temp directory {path}: {e}")