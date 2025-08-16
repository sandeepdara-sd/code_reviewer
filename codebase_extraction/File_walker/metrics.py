"""
metrics.py — File metrics utilities for File Walker.

Features:
- Count total lines efficiently
- Get file size
- Generate SHA-256 hash
"""

import hashlib
import logging
import mmap
from pathlib import Path
from .config import LARGE_FILE_MB, HASH_ALGORITHM


def get_file_size(file_path: Path) -> int:
    """
    Returns file size in bytes.

    Args:
        file_path (Path): Path to the file.

    Returns:
        int: File size in bytes.
    """
    try:
        return file_path.stat().st_size
    except Exception as e:
        logging.error(f"Error getting file size for {file_path}: {e}")
        return 0


def count_lines(file_path: Path) -> int:
    """
    Counts the total number of lines in a file.

    Uses mmap for large files to optimize memory usage.

    Args:
        file_path (Path): Path to the file.

    Returns:
        int: Total line count.
    """
    try:
        size_in_mb = get_file_size(file_path) / (1024 * 1024)

        if size_in_mb > LARGE_FILE_MB:
            # Use memory-mapped reading for large files
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                    return sum(1 for _ in iter(mm.readline, b""))
        else:
            # Standard method for small files
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return sum(1 for _ in f)

    except Exception as e:
        logging.error(f"Error counting lines in {file_path}: {e}")
        return 0


def hash_file(file_path: Path) -> str:
    """
    Generates a SHA-256 hash of the file's content.

    Args:
        file_path (Path): Path to the file.

    Returns:
        str: Hex digest of the file hash.
    """
    try:
        hash_func = hashlib.new(HASH_ALGORITHM)
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()

    except Exception as e:
        logging.error(f"Error hashing file {file_path}: {e}")
        return ""
