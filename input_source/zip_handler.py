import logging
import zipfile
from tempfile import mkdtemp
from plyer import filechooser # Import filechooser from plyer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ask_for_zip_file() -> str:
    """
    Opens the native OS file dialog to ask the user to select a ZIP file.

    Returns:
        str: The path to the selected ZIP file, or an empty string if canceled.
    """
    logging.info("Opening native OS file dialog to select a ZIP file...")

    # Use plyer to open the file chooser
    selected_paths = filechooser.open_file(
        title="Select a ZIP file to analyze",
        filters=[("ZIP files", "*.zip")]
    )

    # filechooser.open_file() returns a list of paths
    if not selected_paths:
        logging.warning("No file selected. ZIP handling cancelled.")
        return ""

    # Return the first selected path
    zip_path = selected_paths[0]
    logging.info(f"File selected: {zip_path}")
    return zip_path

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