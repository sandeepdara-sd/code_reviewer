import os
from input_source.input_handler import process_input
from input_source.zip_handler import ask_for_zip_file, extract_zip
from analysis.code_prepare import analyze_codebase

def run_analysis(source_path: str):
    """Helper function to run the analysis and print results."""
    if not source_path:
        print("❌ Source code path is invalid. Skipping analysis.")
        return

    print("\n--- Phase 2: Codebase Extraction & Preparation ---")
    analysis_result = analyze_codebase(source_path)

    if analysis_result:
        metadata = analysis_result["metadata"]
        print(f"✅ Analysis complete!")
        print(f"   - Python files found: {metadata['file_count']}")
        print(f"   - Total size: {metadata['total_size_kb']} KB")
        # Optionally, print a few file names
        files = analysis_result["files"]
        if files:
            print("   - Example files:")
            for f in files[:3]: # Print the first 3 files
                print(f"     - {f}")
    else:
        print("❌ Codebase analysis failed.")

def main():
    """
    Main function to demonstrate the input handling process.
    """
    print("🤖 AI Code Review System - Input Handler Demo 🤖")

    # --- Example 1: Processing a Git Repository ---
    git_url = "https://github.com/gitpython-developers/GitPython1.git"
    print(f"\nProcessing Git URL: {git_url}")
    git_temp_path = process_input(git_url)

    if git_temp_path:
        print(f" Git repository processed successfully. Code is in: {git_temp_path}")
    else:
        print(" Failed to process Git repository.")

    # --- Example 2: Processing a ZIP File ---
    # Step 1: Ask the user to select a file
    selected_zip_path = ask_for_zip_file()

    # Step 2: If a file was selected, extract it
    if selected_zip_path:
        zip_temp_path = extract_zip(selected_zip_path)
        if zip_temp_path:
            print(f"✅ ZIP file processed successfully. Code is in: {zip_temp_path}")
        else:
            print(" Failed to process ZIP file.")
    else:
        print(" ZIP file processing skipped by user.")

if __name__ == "__main__":
    main()