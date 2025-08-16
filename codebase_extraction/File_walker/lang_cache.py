# file_walker/lang_cache.py

import json
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

DEFAULT_CACHE_PATH = Path(".lang_map_cache.json")


def load_cache(path: Optional[Path] = None) -> dict:
    """
    Loads the language cache from a JSON file.

    Args:
        path (Optional[Path]): Path to the cache file. Uses default if None.

    Returns:
        dict: Cache data with 'extensions' and 'filenames' keys.
    """
    path = Path(path or DEFAULT_CACHE_PATH)
    if not path.exists():
        logger.debug("Language cache file not found: %s", path)
        return {"extensions": {}, "filenames": {}}
    try:
        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
            if "extensions" not in data:
                data = {"extensions": data, "filenames": {}}
            return data
    except Exception as e:
        logger.error("Failed to load language cache %s: %s", path, e)
        return {"extensions": {}, "filenames": {}}


def save_cache(data: dict, path: Optional[Path] = None) -> None:
    """
    Saves the language cache to a JSON file.

    Args:
        data (dict): Cache data to save.
        path (Optional[Path]): Path to the cache file. Uses default if None.
    """
    path = Path(path or DEFAULT_CACHE_PATH)
    try:
        with path.open("w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)
        logger.info("Saved language cache to %s", path)
    except Exception as e:
        logger.error("Failed to save language cache %s: %s", path, e)


def get_cached_language(file_path: Path, cache: Optional[dict] = None) -> Optional[str]:
    """
    Retrieves the cached language for a file based on its extension or filename.

    Args:
        file_path (Path): Path to the file.
        cache (Optional[dict]): Cache data. Loads from file if None.

    Returns:
        Optional[str]: Language name if found, else None.
    """
    cache = cache or load_cache()
    ext = file_path.suffix.lower()
    if ext and ext in cache.get("extensions", {}):
        return cache["extensions"][ext]
    name = file_path.name
    if name in cache.get("filenames", {}):
        return cache["filenames"][name]
    return None


def add_extension_mapping(ext: str, language: str, cache_path: Optional[Path] = None, source=None) -> None:
    """
    Adds or updates a language mapping for a file extension in the cache.

    Args:
        ext (str): File extension (e.g., '.py').
        language (str): Language name (e.g., 'Python').
        cache_path (Optional[Path]): Path to the cache file. Uses default if None.
    """
    cache = load_cache(cache_path)
    entry = {"language": language}
    if source:
        entry["source"] = source
    cache.setdefault("extensions", {})[ext.lower()] = entry
    save_cache(cache, cache_path)


def add_filename_mapping(filename: str, language: str, cache_path: Optional[Path] = None, source=None) -> None:
    """
    Adds or updates a language mapping for a specific filename in the cache.

    Args:
        filename (str): Exact filename (e.g., 'Makefile').
        language (str): Language name (e.g., 'Make').
        cache_path (Optional[Path]): Path to the cache file. Uses default if None.
    """
    cache = load_cache(cache_path)
    entry = {"language": language}
    if source:
        entry["source"] = source
    cache.setdefault("filenames", {})[filename] = entry
    save_cache(cache, cache_path)

def save_language_cache(lang_map: dict, cache_file=".lang_map_cache.json"):
    try:
        existing = {}
        if Path(cache_file).exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                existing = json.load(f)

        existing.update(lang_map)  # Merge new detections
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(existing, f, indent=2)
        logging.info(f"Language cache saved to {cache_file} with {len(existing)} entries.")
    except Exception as e:
        logging.error(f"Error saving language cache: {e}")