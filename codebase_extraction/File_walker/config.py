"""
config.py — Central configuration for File Walker module.

Stores constants for:
- Language detection mapping
- Folder exclusion
- File size thresholds
- Parallel processing settings
"""

# ------------------------------------------------------------
# 1️⃣ Language Mapping (Extension → Language)
# ------------------------------------------------------------
# Fast, lightweight detection. Used before content-based detection (`enry`).
EXTENSION_TO_LANGUAGE = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.java': 'Java',
    '.c': 'C',
    '.cpp': 'C++',
    '.h': 'C/C++ Header',
    '.html': 'HTML',
    '.css': 'CSS',
    '.json': 'JSON',
    '.yaml': 'YAML',
    '.yml': 'YAML',
    '.sh': 'Shell',
    '.go': 'Go',
    '.rb': 'Ruby',
    '.php': 'PHP',
    '.rs': 'Rust',
    '.dart': 'Dart',
    '.swift': 'Swift',
    '.kt': 'Kotlin',
    '.m': 'Objective-C',
    '.ipynb': 'Jupyter Notebook',  # Special handling in notebook_handler
}

# ------------------------------------------------------------
# 2️⃣ Excluded Folders
# ------------------------------------------------------------
# Prevents scanning unnecessary or heavy directories like dependencies or builds.
EXCLUDE_FOLDERS = {
    'venv', '__pycache__', 'node_modules', '.git', 'dist', 'build', '.idea', '.vscode'
}

# ------------------------------------------------------------
# 3️⃣ File Size Thresholds
# ------------------------------------------------------------
# If file > LARGE_FILE_MB → use memory-mapped reading (mmap)
LARGE_FILE_MB = 50  # 50 MB

# ------------------------------------------------------------
# 4️⃣ Parallel Processing Thresholds
# ------------------------------------------------------------
# If repo > PARALLEL_FILE_COUNT or avg file size > PARALLEL_AVG_FILE_KB → use ThreadPool
PARALLEL_FILE_COUNT = 500
PARALLEL_AVG_FILE_KB = 50  # 50 KB

# ------------------------------------------------------------
# 5️⃣ Hashing Algorithm
# ------------------------------------------------------------
# SHA-256 chosen for collision resistance; faster than SHA-512, safer than MD5/SHA-1.
HASH_ALGORITHM = 'sha256'

# ------------------------------------------------------------
# 6️⃣ Known Non-Code Extensions
# ------------------------------------------------------------
# A safe list of common binary/media extensions to prevent LLM calls.
KNOWN_NON_CODE_EXTENSIONS = {
    '.png': 'PNG Image',
    '.jpg': 'JPEG Image',
    '.jpeg': 'JPEG Image',
    '.gif': 'GIF Image',
    '.pdf': 'PDF Document',
    '.docx': 'Word Document',
    '.xlsx': 'Excel Spreadsheet',
    '.zip': 'ZIP Archive',
    '.rar': 'RAR Archive',
    '.mp3': 'MP3 Audio',
    '.mp4': 'MP4 Video',
    '.svg': 'SVG Image',
    '.ico': 'Icon File',
    '.woff2': 'Web Font',
    '.ttf': 'TrueType Font',
}

# ------------------------------------------------------------
# 7️⃣ MIME Type Category Map
# ------------------------------------------------------------
# Maps MIME types to (description, is_code) tuples.
# Used for file type detection and filtering.
_MIME_CATEGORY_MAP = [
    ("application/pdf", ("PDF document", False)),
    ("application/zip", ("ZIP archive", False)),
    ("application/x-tar", ("TAR archive", False)),
    ("application/x-gzip", ("GZIP archive", False)),
    ("application/x-7z-compressed", ("7z archive", False)),
    ("application/x-rar-compressed", ("RAR archive", False)),
    ("application/json", ("JSON document", True)),
    ("application/x-yaml", ("YAML document", True)),
    ("text/yaml", ("YAML document", True)),
    ("application/toml", ("TOML document", True)),
    ("text/markdown", ("Markdown", True)),
    ("text/x-python", ("Python", True)),
    ("text/x-shellscript", ("Shell script", True)),
    ("application/octet-stream", ("Binary file", False)),
]

# ------------------------------------------------------------
# 8️⃣ MIME Type Preregistration Map
# ------------------------------------------------------------
# Maps MIME types to preferred file extensions for quick lookup.
_MIME_PREREG = [
    ("application/json", ".json"),
    ("application/x-yaml", ".yaml"),
    ("application/x-yaml", ".yml"),
    ("application/toml", ".toml"),
    ("text/markdown", ".md"),
    ("application/x-sh", ".sh"),
    ("application/x-dockerfile", "Dockerfile"),
]