import logging
from input_source.git_handler import clone_repo
from input_source.zip_handler import extract_zip

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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
    if source.startswith(('http://', 'https://')) and source.endswith('.git'):
        logging.info("Detected Git repository URL.")
        return clone_repo(source)

    # Check if the source is a ZIP file
    elif source.endswith('.zip'):
        logging.info("Detected ZIP file path.")
        return extract_zip(source)

    else:
        logging.error("Unsupported input type. Please provide a Git URL or a ZIP file path.")
        return ""