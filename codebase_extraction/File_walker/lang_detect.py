# lang_detect.py
from __future__ import annotations
import logging
import re
from pathlib import Path
from typing import List, Tuple, Dict
from pygments.lexers import guess_lexer_for_filename
from pygments.util import ClassNotFound

from codebase_extraction.File_walker.config import EXTENSION_TO_LANGUAGE
from codebase_extraction.File_walker.lang_cache import (
    get_cached_language,
    add_extension_mapping,
    add_filename_mapping,
)
from codebase_extraction.File_walker.mime_detect import detect_file_type
from codebase_extraction.File_walker.llm_fallback import guess_languages_for_extensions

logger = logging.getLogger(__name__)

# Global state for this module invocation
_unknown_files: List[Tuple[str, Path]] = []
_LLM_CONFIDENCE_THRESHOLD = 0.60
_LLM_BATCH_SIZE = 8

# Common shebang patterns → language
_SHEBANG_MAP = [
    (r"^#!.*\bpython[0-9.]*\b", "Python"),
    (r"^#!.*\b(node|nodejs)\b", "JavaScript"),
    (r"^#!.*\bruby\b", "Ruby"),
    (r"^#!.*\bperl\b", "Perl"),
    (r"^#!.*\b(sh|bash|zsh|ksh)\b", "Bash"),
    (r"^#!.*\bphp\b", "PHP"),
    (r"^#!.*\bdeno\b", "TypeScript"),  # often TS/JS
]

# Normalize Pygments → canonical labels when it matters
_PYGMENTS_RENAMES = {
    "Bourne Again Shell": "Bash",
    "Bash": "Bash",
    "Shell Session": "Shell",
    "JSON": "JSON document",
    "YAML": "YAML document",
    "reStructuredText": "reStructuredText",
    "Markdown": "Markdown",
}

def _read_head(file_path: Path, max_bytes: int = 4096) -> str:
    try:
        return file_path.read_text(encoding="utf-8", errors="ignore")[:max_bytes]
    except Exception:
        try:
            return file_path.open("rb").read(max_bytes).decode("utf-8", errors="ignore")
        except Exception:
            return ""

def _check_shebang(head: str) -> str | None:
    first_line = head.splitlines()[0] if head else ""
    for pattern, lang in _SHEBANG_MAP:
        if re.search(pattern, first_line):
            return lang
    return None

def _normalize_lang(name: str | None) -> str:
    if not name:
        return "unknown"
    return _PYGMENTS_RENAMES.get(name, name)

def detect_language(file_path: Path, rel_path: str = None) -> str:
    # 1) Extension fast-path
    ext = file_path.suffix.lower()
    if ext in EXTENSION_TO_LANGUAGE:
        lang = EXTENSION_TO_LANGUAGE[ext]
        logger.debug("Language by extension: %s -> %s", ext, lang)
        return lang

    # 2) Cache
    cached = get_cached_language(file_path)
    if cached:
        logger.debug("Language from cache for %s: %s", file_path, cached)
        return cached

    # 3) MIME binary short-circuit
    category, is_text = detect_file_type(file_path)
    if category != "unknown" and not is_text:
        logger.debug("Binary by MIME for %s: %s", file_path, category)
        return category

    # 4) Shebang hint
    head = _read_head(file_path)
    shebang_lang = _check_shebang(head)
    if shebang_lang:
        logger.debug("Shebang detected for %s: %s", file_path, shebang_lang)
        return shebang_lang

    # 5) Pygments guess (text only)
    try:
        code = head  # already truncated
        lexer = guess_lexer_for_filename(file_path.name, code)
        if lexer:
            lang = _normalize_lang(lexer.name)
            logger.debug("Pygments guess for %s: %s", file_path, lang)
            return lang
    except ClassNotFound:
        pass
    except Exception as e:
        logger.debug("Pygments failed for %s: %s", file_path, e)

    # 6) Unknown → queue for LLM
    _unknown_files.append((rel_path or file_path.name, file_path))
    logger.debug("Queued for LLM: %s", file_path)
    return "unknown"

def _chunk_dict(d: Dict[str, str], size: int):
    it = iter(d.items())
    while True:
        batch = dict()
        try:
            for _ in range(size):
                k, v = next(it)
                batch[k] = v
        except StopIteration:
            if batch:
                yield batch
            break
        yield batch

def resolve_unknowns(file_map: dict):
    """
    Mutates file_map[rel]['language'] in place using LLM results.
    Expects file_map[rel] to exist with a 'language' key.
    """
    global _unknown_files
    if not _unknown_files:
        logger.info("No unknown files to resolve.")
        return

    logger.info("Resolving %d unknowns...", len(_unknown_files))

    # --- MIME second pass for unknowns (cheap re-check) ---
    still_unknown_text: List[Tuple[str, Path]] = []
    for rel, abs_path in _unknown_files:
        category, is_text = detect_file_type(abs_path)
        if category != "unknown" and not is_text:
            file_map[rel]["language"] = category
            ext = abs_path.suffix.lower()
            if ext:
                EXTENSION_TO_LANGUAGE.setdefault(ext, category)
                add_extension_mapping(ext, category, source="mime")
            logger.debug("Resolved by MIME (second pass): %s -> %s", rel, category)
        else:
            still_unknown_text.append((rel, abs_path))

    if not still_unknown_text:
        _unknown_files = []
        logger.info("All unknowns resolved by MIME second pass.")
        return

    # --- Group text unknowns for LLM ---
    group_samples: Dict[str, str] = {}
    group_meta: Dict[str, Dict[str, str]] = {}
    SAMPLE_BYTES = 800

    def read_sample(p: Path) -> str:
        return _read_head(p, SAMPLE_BYTES)

    for rel, abs_path in still_unknown_text:
        ext = abs_path.suffix.lower()
        if ext:
            key = f"EXT::{ext}"
            if key not in group_samples:
                group_samples[key] = read_sample(abs_path)
                group_meta[key] = {"mode": "ext", "value": ext}
        else:
            fname = abs_path.name
            key = f"FNAME::{fname}"
            if key not in group_samples:
                group_samples[key] = read_sample(abs_path)
                group_meta[key] = {"mode": "filename", "value": fname}

    # --- Batch to LLM with chunking ---
    if not group_samples:
        _unknown_files = []
        return

    logger.info("Sending %d groups to LLM...", len(group_samples))
    resolved_any = False

    for batch in _chunk_dict(group_samples, _LLM_BATCH_SIZE):
        llm_results = guess_languages_for_extensions(batch) or {}
        for key, result in llm_results.items():
            if not isinstance(result, dict):
                continue
            conf = float(result.get("confidence", 0.0) or 0.0)
            lang = (result.get("language") or "unknown").strip()
            meta = group_meta.get(key, {})
            mode = meta.get("mode")
            val = meta.get("value")

            if conf < _LLM_CONFIDENCE_THRESHOLD or lang.lower() == "unknown":
                logger.debug("LLM low confidence for %s: %.2f (%s)", key, conf, lang)
                continue

            if mode == "ext" and val:
                EXTENSION_TO_LANGUAGE.setdefault(val, lang)
                add_extension_mapping(val, lang, source="llm")
                for rel, abs_path in still_unknown_text:
                    if abs_path.suffix.lower() == val and file_map[rel]["language"] == "unknown":
                        file_map[rel]["language"] = lang
                        resolved_any = True
                        logger.debug("Resolved by LLM (ext): %s -> %s", rel, lang)

            elif mode == "filename" and val:
                add_filename_mapping(val, lang, source="llm")
                for rel, abs_path in still_unknown_text:
                    if abs_path.name == val and file_map[rel]["language"] == "unknown":
                        file_map[rel]["language"] = lang
                        resolved_any = True
                        logger.debug("Resolved by LLM (filename): %s -> %s", rel, lang)

    if not resolved_any:
        logger.info("LLM could not confidently resolve remaining unknowns.")

    # Important: clear global queue to avoid duplicates on next run
    _unknown_files = []
