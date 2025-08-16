import logging
import zipfile
from tempfile import mkdtemp

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_zip(zip_path: str) -> str:
    """
    Extracts a ZIP file to a new temporary directory.
    (This function remains unchanged)

    Args:
        zip_path (str): The local path to the ZIP file.

    Returns:
        str: The path to the temporary directory where files were extracted, or "" if it fails.
    """
    if not zip_path:
        return ""

    try:
        # Create a temporary directory for extraction
        temp_dir = mkdtemp()
        logging.info(f"Extracting ZIP file from {zip_path} to {temp_dir}")

        # Extract the ZIP file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        logging.info(f"Successfully extracted ZIP file to {temp_dir}")
        return temp_dir

    except FileNotFoundError:
        logging.error(f"ZIP file not found at: {zip_path}")
        return ""
    except zipfile.BadZipFile:
        logging.error(f"The file at {zip_path} is not a valid ZIP file.")
        return ""