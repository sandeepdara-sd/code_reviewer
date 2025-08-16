# file_walker/llm_fallback.py
import os
from dotenv import load_dotenv
import json
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# === Configurable values ===
SNIPPET_BYTES = 4096   # how much of the file to send to the LLM
CONFIDENCE_THRESHOLD = 0.60  # only cache if confidence >= this


try:
    import google.generativeai as genai
    GOOGLE_AVAILABLE = True
except Exception:
    GOOGLE_AVAILABLE = False

def _read_snippet(file_path: Path, max_bytes: int = SNIPPET_BYTES) -> str:
    """
    Read the first `max_bytes` bytes of the file in text-safe way.
    If it's a notebook, user should pass notebook snippet externally.
    """
    try:
        with open(file_path, "rb") as fh:
            raw = fh.read(max_bytes)
        # try decode, fallback ignoring errors
        try:
            return raw.decode("utf-8")
        except UnicodeDecodeError:
            return raw.decode("utf-8", errors="ignore")
    except Exception as e:
        logger.error("Failed to read snippet from %s: %s", file_path, e)
        return ""


def _build_prompt(file_name: str, group_samples:dict) -> str:
    """
    Builds a deterministic instructive prompt that asks for a concise JSON response.
    We also include a few code-practice heuristics to guide the LLM.
    """
    #system = (
    #    "You are a precise code-language detection assistant. "
    #    "Given a filename and a short snippet of the file content, "
    #    "return a JSON object with fields: language or file format name (common name), "
    #    "confidence (0-1), extension_suggestion (like .py or .js or .pdf or .png or empty), and short notes. "
    #    "Respond ONLY with a valid JSON object and nothing else."
    #)
    # 5 code-practice hints to improve reasoning:
    #practices = (
    #    "Use these heuristics: "
    #    "(1) Shebang or file header (e.g., #!/usr/bin/env python) indicates language; "
    #    "(2) import/require statements reveal ecosystem; "
    #    "(3) file extension patterns (.tf, Dockerfile, Makefile) often indicate language; "
    #    "(4) comment syntax (#, //, /* */, --) helps narrow choices; "
    #    "(5) typical library names (pandas, React import, javax) are strong signals."
    #)
    #prompt = (
    #    f"{system}\n{practices}\n\n"
    #    f"filename: {file_name}\n\n"
    #    f"content_snippet:\n'''{snippet}'''\n\n"
    #    "Return JSON like: {\"language\":\"Python\",\"confidence\":0.95,\"extension_suggestion\":\".py\",\"notes\":\"has import pandas\"}"
    #)
    # 1. Build prompt using best prompt strategy
    instruction = (
        "You are a precise multilingual code and file format identification system. "
        "Your task is to detect the most likely programming language or file format "
        "for each provided key and code/content snippet."
    )

    context = (
        "Keys are prefixed with 'EXT::' for file extension groups, or 'FNAME::' for filename groups. "
        "Values are short snippets from files in that group. "
        "Use your knowledge of syntax, keywords, shebang lines, comment styles, "
        "and common libraries to decide. "
        "For binary or non-text formats, output the format name (e.g., PNG image, PDF document). "
        "If uncertain, give your best guess but keep confidence below 0.5."
    )

    examples = {
        "EXT::.py": {
            "language": "Python",
            "confidence": 0.96,
            "extension_suggestion": ".py",
            "notes": "Uses 'import pandas', Python syntax"
        },
        "FNAME::Dockerfile": {
            "language": "Dockerfile",
            "confidence": 0.98,
            "extension_suggestion": "",
            "notes": "Starts with FROM instruction"
        }
    }

    role = (
        "Act as an expert software archeologist and linguist for source code. "
        "You are meticulous, concise, and avoid hallucinations."
    )

    output_format = (
        "Respond ONLY with a single valid JSON object mapping each input key "
        "to a dictionary with fields: language (string), confidence (0-1 float), "
        "extension_suggestion (string, may be empty), and notes (short explanation). "
        "No prose outside the JSON."
    )

    # 2. Construct the prompt
    examples_str = json.dumps(examples, indent=2)
    input_str = json.dumps(group_samples, indent=2)

    prompt = (
        f"{instruction}\n\n"
        f"{context}\n\n"
        f"{role}\n\n"
        "### Examples:\n"
        f"{examples_str}\n\n"
        "### Input to process:\n"
        f"{input_str}\n\n"
        f"{output_format}"
    )
    return prompt


def _call_llm(prompt: str, model: Optional[str] = None) -> Optional[str]:
    """
    Calls an available LLM provider. Currently supports OpenAI (if OPENAI_API_KEY set).
    Returns raw string response (expected JSON string), or None if no provider configured.
    """


    if GOOGLE_AVAILABLE and os.environ.get("GEMINI_API_KEY"):
         try:
             genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
             model = genai.GenerativeModel('gemini-2.5-flash')
             logging.info("Gemini AI initialized for enhanced detection")
             resp = model.generate_content(prompt)
             return resp.text
         except Exception as e:
             logger.error("Google Gemini call failed: %s", e)
             return None

    logger.warning("No LLM provider configured (set OPENAI_API_KEY or implement Google).")
    return None


#def guess_language_with_llm(file_path: Path, snippet: Optional[str] = None) -> Optional[dict]:
#    """
#    Attempts to guess the language via LLM. Returns dict: {language, confidence, extension_suggestion, notes}
#    or None if LLM not configured or LLM couldn't produce usable output.
#    """
#    snippet = snippet or _read_snippet(file_path)
#    if not snippet:
#        logger.debug("Empty snippet for %s, skipping LLM guess", file_path)
#        return None
#    prompt = _build_prompt(file_path.name, snippet)
#    raw = _call_llm(prompt)
#    if not raw:
#        return None
    # Parse JSON from response robustly
#    try:
        # LLM is expected to return JSON only, but we tolerate whitespace
#        parsed = json.loads(raw)
#    except Exception:
        # try to extract JSON substring
#        import re
#        m = re.search(r"\{.*\}", raw, re.S)
#        if m:
#            try:
#                parsed = json.loads(m.group(0))
#            except Exception as e:
#                logger.error("Failed to parse JSON from LLM raw response: %s", e)
#                return None
#        else:
#            logger.error("LLM response did not contain JSON: %s", raw[:200])
#            return None

def guess_languages_for_extensions(group_samples: dict) -> Optional[dict]:
    """
    Batch language detection via LLM.
    group_samples: { "EXT::.py": "print('hello')", "FNAME::Dockerfile": "FROM ubuntu\n..." }
    Returns: { group_key: {language, confidence, extension_suggestion, notes}, ... }
    """
    if not group_samples:
        return {}

    prompt = _build_prompt("Batch Language Detection", group_samples)

    # 3. Call LLM
    raw = _call_llm(prompt)

    if not raw:
        return {}

    # 4. Parse JSON safely
    try:
        parsed = json.loads(raw)
        return parsed
    except Exception:
        import re
        m = re.search(r"\{.*\}", raw, re.S)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception as e:
                logger.error("Batch LLM: Failed to parse JSON: %s", e)
        logger.error("Batch LLM: Response not JSON: %s", raw[:200])
        return {}

    # Normalize and validate
    language = parsed.get("language")
    confidence = float(parsed.get("confidence", 0.0)) if parsed.get("confidence") is not None else 0.0
    extension_suggestion = parsed.get("extension_suggestion", "").strip()
    notes = parsed.get("notes", "")

    result = {
        "language": language,
        "confidence": confidence,
        "extension_suggestion": extension_suggestion,
        "notes": notes
    }
    logger.info("LLM guessed language=%s (conf=%.2f) for %s", language, confidence, file_path)
    return result if language else None
