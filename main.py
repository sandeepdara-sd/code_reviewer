# main.py
import logging
from pathlib import Path
from input_source.input_handler import process_input , cleanup_temp_dir, AUTO_DELETE_TEMP
from codebase_extraction.File_walker.walker import walk_directory, clear_lang_cache

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    print("\n🤖 AI Code Review — File Walker Test\n")

    input_path = input("Enter GitHub repo URL or local ZIP path: ").strip()
    extracted_path = process_input(input_path)

    if not extracted_path or not Path(extracted_path).exists():
        logging.error("❌ Failed to process input source.")
        return

    logging.info(f"✅ Codebase available at: {extracted_path}")

    # CALL the walker
    result = walk_directory(Path(extracted_path))

    # Backwards-compatible handling:
    # - If result is a dict with "file_map", use it.
    # - If result is directly the file_map, handle that too.
    if isinstance(result, dict) and "file_map" in result:
        file_map = result["file_map"]
        summary = result.get("summary", {})
        skipped = result.get("skipped_files", {"by_folder": [], "by_gitignore": []})
    elif isinstance(result, dict):
        # assume full file_map (old behavior)
        file_map = result
        summary = {}
        skipped = {"by_folder": [], "by_gitignore": []}
    else:
        logging.error("Unexpected return type from walk_directory(): %s", type(result))
        return

    # === Summary ===
    total_files = len(file_map)
    total_lines = sum(info.get("lines", 0) for info in file_map.values())
    total_size = sum(info.get("size_bytes", 0) for info in file_map.values())

    langs = {}
    for info in file_map.values():
        lang = info.get("language", "unknown")
        langs[lang] = langs.get(lang, 0) + 1

    print("\n📊 Project Summary")
    print(f"  Total files scanned: {total_files}")
    print(f"  Total lines: {total_lines:,}")
    print(f"  Total size: {total_size / 1024:.2f} KB")
    print("  Languages detected:")
    for lang, count in sorted(langs.items(), key=lambda x: x[1], reverse=True):
        print(f"    {lang}: {count} files")

    # === Skipped Files ===
    print("\n🚫 Skipped Files Summary:")
    print(f"  By folder exclusion: {len(skipped.get('by_folder', []))}")
    print(f"  By .gitignore rules: {len(skipped.get('by_gitignore', []))}")
    # Print a few names if present
    for k in ("by_folder", "by_gitignore"):
        items = skipped.get(k, [])
        if items:
            print(f"\n  Sample skipped ({k}):")
            for s in items[:10]:
                print(f"    - {s}")

    # === Sample Metadata ===
    print("\n🔍 Sample File Metadata:")
    for i, (path, meta) in enumerate(file_map.items()):
        print(f"- {path}")
        print(f"    Language: {meta.get('language')}")
        print(f"    Size: {meta.get('size_bytes')} bytes")
        print(f"    Lines: {meta.get('lines')}")
        print(f"    Hash: {meta.get('hash', '')[:16]}...")
        if "notebook_cells" in meta:
            print(f"    Notebook cells: {len(meta['notebook_cells'])}")
        if i >= 4:  # limit to 5 files
            break

    clear_lang_cache()

    if AUTO_DELETE_TEMP:
        cleanup_temp_dir(extracted_path)
    print("\n✅ Code Review completed successfully!")

if __name__ == "__main__":
    main()
