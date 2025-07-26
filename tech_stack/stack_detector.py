import os
import json
import re
from datetime import datetime
from collections import defaultdict
from tech_stack.tech_mapping import TECH_MAPPING


class TechStackDetector:
    def __init__(self, project_path):
        self.project_path = project_path
        self.detected_stack = defaultdict(lambda: defaultdict(list))
        self.confidence = 0.5
        self.project_meta = defaultdict(list)
        self.languages = set()

    def run_detection(self):
        """Main method to run all detection layers."""
        # Layer 1 & 2: Scan files for package managers and keywords
        for root, dirs, files in os.walk(self.project_path):
            # Skip virtual environments and node_modules
            dirs[:] = [d for d in dirs if d not in ['node_modules', 'venv', '.git']]

            # Check for package manager files
            if "package.json" in files:
                self._parse_package_json(os.path.join(root, "package.json"))
            if "requirements.txt" in files:
                self._parse_requirements_txt(os.path.join(root, "requirements.txt"))
                self.project_meta["packageManagers"].append("Pip")

            # Check for other indicators
            if "Dockerfile" in files:
                self._add_tech("docker")
            if ".github" in dirs:
                self.detected_stack["devops"]["ciCd"].append("GitHub Actions")

            # Layer 3: Analyze file content and extensions
            for file in files:
                self._detect_language_from_file(file)

        # Post-process to clean up duplicates
        self._finalize_stack()

        return self.format_output()

    def _add_tech(self, keyword):
        """Adds a technology to the stack based on the mapping."""
        if keyword in TECH_MAPPING:
            category, sub_category, tech = TECH_MAPPING[keyword]
            if category == "projectMeta":
                self.project_meta[sub_category].append(tech)
            else:
                self.detected_stack[category][sub_category].append(tech)
            self.confidence = min(0.99, self.confidence + 0.05)

    def _parse_package_json(self, file_path):
        """Parses package.json for dependencies."""
        self.project_meta["packageManagers"].append("NPM")  # or Yarn, can be refined
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                dependencies = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                for dep in dependencies:
                    self._add_tech(dep)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Warning: Could not parse {file_path}: {e}")

    def _parse_requirements_txt(self, file_path):
        """Parses requirements.txt for dependencies."""
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    dep = line.strip().split('==')[0]
                    self._add_tech(dep.lower())
        except FileNotFoundError as e:
            print(f"Warning: Could not find {file_path}: {e}")

    def _detect_language_from_file(self, filename):
        """Detects language from file extension."""
        ext_map = {
            ".js": "JavaScript", ".jsx": "JavaScript",
            ".ts": "TypeScript", ".tsx": "TypeScript",
            ".py": "Python",
            ".java": "Java",
            ".go": "Go",
            ".rb": "Ruby",
            ".php": "PHP",
            ".html": "HTML",
            ".css": "CSS",
        }
        ext = os.path.splitext(filename)[1]
        if ext in ext_map:
            self.languages.add(ext_map[ext])
            if ext_map[ext] == "TypeScript":
                self._add_tech("typescript")

    def _finalize_stack(self):
        """Removes duplicates from the detected stack."""
        for category, sub_categories in self.detected_stack.items():
            for sub_category, techs in sub_categories.items():
                self.detected_stack[category][sub_category] = sorted(list(set(techs)))

        for key, values in self.project_meta.items():
            self.project_meta[key] = sorted(list(set(values)))

        self.project_meta["languagesUsed"] = sorted(list(self.languages))

    def format_output(self):
        """Formats the final output dictionary."""
        if not self.detected_stack:
            return {"status": "Unable to detect any technology stack."}

        # Basic project info (can be enhanced later)
        project_name = os.path.basename(self.project_path)

        output = {
            "projectName": project_name,
            "source": f"local/{project_name}",
            "description": "A brief description of the project.",  # Placeholder
            "stack": self.detected_stack,
            "projectMeta": self.project_meta,
            "lastAnalyzed": datetime.now().isoformat(),
            "confidenceScore": round(self.confidence, 2)
        }
        return json.dumps(output, indent=2)