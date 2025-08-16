# mime_detect.py
from __future__ import annotations
import mimetypes
import logging
from typing import Tuple
from codebase_extraction.File_walker.config import _MIME_PREREG, _MIME_CATEGORY_MAP

logger = logging.getLogger(__name__)

try:
    import magic  # python-magic (optional)
    MAGIC_AVAILABLE = True
except Exception:
    MAGIC_AVAILABLE = False

for mt, ext in _MIME_PREREG:
    try:
        mimetypes.add_type(mt, ext, strict=False)
    except Exception:
        pass


def _normalize_mime(mime_type: str | None) -> str | None:
    if not mime_type:
        return None
    # Strip charset if present: e.g., "text/plain; charset=utf-8"
    return mime_type.split(";")[0].strip().lower()

def detect_file_type(file_path) -> Tuple[str, bool]:
    """
    Detect file type using MIME and return a human-readable category.
    Returns:
        (category: str, is_text: bool)
    """
    mime_type = None

    # 1) Try python-magic (best)
    if MAGIC_AVAILABLE:
        try:
            mime_type = magic.from_file(str(file_path), mime=True)
        except Exception as e:
            logger.debug("magic failed for %s: %s", file_path, e)

    # 2) Fallback: mimetypes
    if not mime_type:
        try:
            mime_type, _ = mimetypes.guess_type(str(file_path))
        except Exception:
            mime_type = None

    mime_type = _normalize_mime(mime_type)

    # 3) Nothing detected
    if not mime_type:
        return "unknown", False

    # 4) Known buckets first
    for mt, (label, is_text) in _MIME_CATEGORY_MAP:
        if mime_type == mt:
            return label, is_text

    # 5) Broad categories
    if mime_type.startswith("image/"):
        return f"{mime_type.split('/')[-1].upper()} image", False
    if mime_type.startswith("video/"):
        return f"{mime_type.split('/')[-1].upper()} video", False
    if mime_type.startswith("audio/"):
        return f"{mime_type.split('/')[-1].upper()} audio", False

    # 6) Generic text-ish
    if mime_type.startswith("text/"):
        # Promote some common subtypes
        subtype = mime_type.split("/")[-1]
        if subtype in {"plain", "csv"}:
            return f"{subtype.upper()} text", True
        return "Text file", True

    # 7) Fallback: return the raw mime (non-text)
    return mime_type, False
