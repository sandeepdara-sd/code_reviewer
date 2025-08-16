import os
import tarfile
import gzip
import shutil
import tempfile
import logging

def extract_tar(source_path: str) -> str:
    temp_dir = tempfile.mkdtemp()
    try:
        with tarfile.open(source_path, "r:*") as tar:
            tar.extractall(path=temp_dir)
        logging.info(f"✅ Extracted TAR archive to {temp_dir}")
        return temp_dir
    except Exception as e:
        logging.error(f"❌ Failed to extract TAR: {e}")
        return ""

def extract_gz(source_path: str) -> str:
    temp_dir = tempfile.mkdtemp()
    try:
        filename = os.path.basename(source_path).replace(".gz", "")
        output_path = os.path.join(temp_dir, filename)

        with gzip.open(source_path, 'rb') as f_in, open(output_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        logging.info(f"✅ Extracted GZ to {output_path}")
        return temp_dir
    except Exception as e:
        logging.error(f"❌ Failed to extract GZ: {e}")
        return ""

# bz2 can be similar to gz if needed later
