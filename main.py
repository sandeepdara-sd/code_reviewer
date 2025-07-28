import os
import shutil
from input_source.input_handler import process_input
from input_source.zip_handler import ask_for_zip_file, extract_zip
from input_source.git_handler import clone_repo
from analysis.code_prepare import analyze_codebase
from tech_stack.stack_detector import TechStackDetector

# Global dictionary to track cloned repositories
CLONED_REPOS = {}

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
        files = analysis_result["files"]
        if files:
            print("   - Example files:")
            for f in files[:3]:
                print(f"     - {f}")
    else:
        print("❌ Codebase analysis failed.")

def handle_git_repo_override(repo_url: str, existing_path: str) -> bool:
    """Ask user if they want to override existing repository."""
    print(f"\n⚠️  Repository already exists at: {existing_path}")
    while True:
        choice = input("Do you want to override it? (y/n): ").lower().strip()
        if choice in ['y', 'yes']:
            try:
                shutil.rmtree(existing_path)
                print(f"✅ Removed existing repository: {existing_path}")
                return True
            except Exception as e:
                print(f"❌ Failed to remove existing repository: {e}")
                return False
        elif choice in ['n', 'no']:
            print("📋 Using existing repository.")
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no.")

def main():
    """Main function to demonstrate the input handling process."""
    print("🤖 AI Code Review System with Enhanced Tech Stack Detection")

    # --- Processing a Git Repository ---
    repo_url = "https://github.com/sandeepdara-sd/ATS_Resume_Builder"
    print(f"\nProcessing Git URL: {repo_url}")

    # Check if repository already exists
    if repo_url in CLONED_REPOS and os.path.exists(CLONED_REPOS[repo_url]):
        if not handle_git_repo_override(repo_url, CLONED_REPOS[repo_url]):
            git_temp_path = CLONED_REPOS[repo_url]
        else:
            git_temp_path = clone_repo(repo_url)
            if git_temp_path:
                CLONED_REPOS[repo_url] = git_temp_path
    else:
        git_temp_path = clone_repo(repo_url)
        if git_temp_path:
            CLONED_REPOS[repo_url] = git_temp_path

    if git_temp_path:
        print(f"✅ Git repository processed successfully. Code is in: {git_temp_path}")

        # Initialize and run the enhanced detector
        detector = TechStackDetector(git_temp_path, gemini_api_key="AIzaSyA-K77-_ASoZrnJ0lezcD0zRIOc_MuZtAw")
        print("🔍 Running enhanced tech stack detection with AI assistance...")

        # Run the detection
        result_json = detector.run_detection()
        if result_json:
            print("✅ Tech stack detection complete. Results:")
            print(result_json)
        else:
            print("❌ Tech stack detection failed.")

        # Run analysis on the cloned repo
        run_analysis(git_temp_path)
    else:
        print("❌ Failed to process Git repository.")

    # --- Processing a ZIP File ---
    selected_zip_path = ask_for_zip_file()
    if selected_zip_path:
        zip_temp_path = extract_zip(selected_zip_path)
        if zip_temp_path:
            print(f"✅ ZIP file processed successfully. Code is in: {zip_temp_path}")

            # Run enhanced detection on ZIP content
            detector = TechStackDetector(zip_temp_path, gemini_api_key="AIzaSyA-K77-_ASoZrnJ0lezcD0zRIOc_MuZtAw")
            print("🔍 Running enhanced tech stack detection...")
            result_json = detector.run_detection()
            if result_json:
                print("✅ Tech stack detection complete. Results:")
                print(result_json)
            else:
                print("❌ Tech stack detection failed.")

            run_analysis(zip_temp_path)
        else:
            print("❌ Failed to process ZIP file.")
    else:
        print("📋 ZIP file processing skipped by user.")

if __name__ == "__main__":
    main()
