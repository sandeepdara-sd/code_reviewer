import os
import json
import re
import yaml
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Set, Optional
import google.generativeai as genai
from tech_stack.tech_mapping import ENHANCED_TECH_MAPPING
from tech_stack.file_patterns import FILE_PATTERNS, CONFIG_PATTERNS

class TechStackDetector:
    def __init__(self, project_path: str, gemini_api_key: Optional[str] = None):
        self.project_path = project_path
        self.detected_stack = defaultdict(lambda: defaultdict(set))
        self.confidence = 0.5
        self.project_meta = defaultdict(set)
        self.languages = set()
        self.file_analysis = {}
        
        # Initialize Gemini AI if API key is provided
        self.use_ai = False
        if gemini_api_key:
            try:
                genai.configure(api_key=gemini_api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                self.use_ai = True
                print("✅ Gemini AI initialized for enhanced detection")
            except Exception as e:
                print(f"⚠️ Gemini AI initialization failed: {e}")
                print("📋 Falling back to pattern-based detection")

    def run_detection(self) -> str:
        """Main method to run all detection layers."""
        print("🔍 Starting multi-layer tech stack detection...")
        
        # Layer 1: File system analysis
        self._analyze_file_system()
        
        # Layer 2: Configuration files analysis
        self._analyze_config_files()
        
        # Layer 3: Code content analysis
        self._analyze_code_content()
        
        # Layer 4: AI-enhanced detection (if available)
        if self.use_ai:
            self._ai_enhanced_detection()
        
        # Layer 5: Pattern-based inference
        self._infer_technologies()
        
        # Finalize and clean up
        self._finalize_stack()
        
        return self.format_output()

    def _analyze_file_system(self):
        """Analyze file system structure and extensions."""
        print("📁 Analyzing file system structure...")
        
        for root, dirs, files in os.walk(self.project_path):
            # Skip common ignore directories
            dirs[:] = [d for d in dirs if d not in [
                'node_modules', 'venv', '.git', '__pycache__', 
                '.next', 'dist', 'build', 'target', '.vscode'
            ]]
            
            # Analyze directory structure
            self._analyze_directory_structure(root, dirs)
            
            # Analyze files
            for file in files:
                file_path = os.path.join(root, file)
                self._analyze_single_file(file, file_path)

    def _analyze_directory_structure(self, root: str, dirs: List[str]):
        """Analyze directory structure for framework patterns."""
        rel_path = os.path.relpath(root, self.project_path)
        
        # Common framework directory patterns
        if 'src' in dirs and 'public' in dirs:
            self._add_tech('react_structure')
        if 'app' in dirs and 'pages' in dirs:
            self._add_tech('nextjs_structure')
        if 'components' in dirs:
            self._add_tech('component_architecture')
        if 'migrations' in dirs:
            self._add_tech('database_migrations')
        if '.github' in dirs:
            self._add_tech('github_actions')
        if 'terraform' in dirs or 'tf' in dirs:
            self._add_tech('terraform')

    def _analyze_single_file(self, filename: str, file_path: str):
        """Analyze individual files for technology indicators."""
        # Check file patterns
        for pattern, techs in FILE_PATTERNS.items():
            if re.match(pattern, filename, re.IGNORECASE):
                for tech in techs:
                    self._add_tech(tech)

        # Language detection
        self._detect_language_from_file(filename)
        
        # Store file info for AI analysis
        if self.use_ai and self._should_analyze_file(filename):
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()[:2000]  # First 2000 chars
                    self.file_analysis[filename] = content
            except Exception:
                pass

    def _analyze_config_files(self):
        """Deep analysis of configuration files."""
        print("⚙️ Analyzing configuration files...")
        
        for root, dirs, files in os.walk(self.project_path):
            dirs[:] = [d for d in dirs if d not in ['node_modules', 'venv', '.git']]
            
            for file in files:
                file_path = os.path.join(root, file)
                
                if file == "package.json":
                    self._parse_package_json(file_path)
                elif file == "requirements.txt":
                    self._parse_requirements_txt(file_path)
                elif file == "Pipfile":
                    self._parse_pipfile(file_path)
                elif file == "composer.json":
                    self._parse_composer_json(file_path)
                elif file == "Gemfile":
                    self._parse_gemfile(file_path)
                elif file == "go.mod":
                    self._parse_go_mod(file_path)
                elif file == "pom.xml":
                    self._parse_pom_xml(file_path)
                elif file in ["docker-compose.yml", "docker-compose.yaml"]:
                    self._parse_docker_compose(file_path)
                elif file in CONFIG_PATTERNS:
                    self._parse_generic_config(file_path, file)

    def _analyze_code_content(self):
        """Analyze code content for technology patterns."""
        print("📝 Analyzing code patterns...")
        
        for root, dirs, files in os.walk(self.project_path):
            dirs[:] = [d for d in dirs if d not in ['node_modules', 'venv', '.git']]
            
            for file in files:
                if self._is_code_file(file):
                    file_path = os.path.join(root, file)
                    self._analyze_code_file(file_path)

    def _ai_enhanced_detection(self):
        """Use Gemini AI for enhanced technology detection."""
        print("🤖 Running AI-enhanced detection...")
        
        if not self.file_analysis:
            return
        
        # Prepare context for AI
        context = {
            "project_structure": list(self.file_analysis.keys())[:20],
            "sample_files": dict(list(self.file_analysis.items())[:5])
        }
        
        prompt = f"""
        Analyze this codebase and identify the technology stack:
        
        Project Structure: {context['project_structure']}
        
        Sample File Contents:
        {json.dumps(context['sample_files'], indent=2)}
        
        Please identify:
        1. Frontend frameworks/libraries
        2. Backend frameworks
        3. Databases
        4. Cloud services
        5. DevOps tools
        6. Testing frameworks
        7. Authentication methods
        8. UI libraries
        9. State management
        10. Build tools
        
        Return a JSON object with detected technologies and confidence scores.
        """
        
        try:
            response = self.model.generate_content(prompt)
            ai_result = json.loads(response.text)
            
            # Process AI results
            for category, techs in ai_result.items():
                if isinstance(techs, list):
                    for tech in techs:
                        self._add_tech(tech.lower().replace(' ', '_'))
                        
            self.confidence = min(0.95, self.confidence + 0.2)
            print("✅ AI analysis completed")
            
        except Exception as e:
            print(f"⚠️ AI analysis failed: {e}")

    def _parse_package_json(self, file_path: str):
        """Enhanced package.json parsing."""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                
            # Detect package manager
            if os.path.exists(os.path.join(os.path.dirname(file_path), "yarn.lock")):
                self.project_meta["packageManagers"].add("Yarn")
            elif os.path.exists(os.path.join(os.path.dirname(file_path), "pnpm-lock.yaml")):
                self.project_meta["packageManagers"].add("PNPM")
            else:
                self.project_meta["packageManagers"].add("NPM")
            
            # Analyze dependencies
            all_deps = {}
            all_deps.update(data.get("dependencies", {}))
            all_deps.update(data.get("devDependencies", {}))
            all_deps.update(data.get("peerDependencies", {}))
            
            for dep, version in all_deps.items():
                self._add_tech(dep)
                
            # Analyze scripts for additional tech
            scripts = data.get("scripts", {})
            for script_name, script_content in scripts.items():
                self._analyze_script_content(script_content)
                
        except Exception as e:
            print(f"Warning: Could not parse package.json: {e}")

    def _parse_requirements_txt(self, file_path: str):
        """Enhanced requirements.txt parsing."""
        self.project_meta["packageManagers"].add("Pip")
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        dep = re.split(r'[>=<~!]', line)[0]
                        self._add_tech(dep.lower().replace('-', '_'))
        except Exception as e:
            print(f"Warning: Could not parse requirements.txt: {e}")

    def _parse_docker_compose(self, file_path: str):
        """Parse docker-compose files for service detection."""
        try:
            with open(file_path, 'r') as f:
                data = yaml.safe_load(f)
            
            services = data.get('services', {})
            for service_name, config in services.items():
                image = config.get('image', '')
                if image:
                    self._analyze_docker_image(image)
                    
        except Exception as e:
            print(f"Warning: Could not parse docker-compose: {e}")

    def _analyze_docker_image(self, image: str):
        """Analyze Docker image for technology detection."""
        image_lower = image.lower()
        if 'postgres' in image_lower:
            self._add_tech('postgresql')
        elif 'mysql' in image_lower:
            self._add_tech('mysql')
        elif 'redis' in image_lower:
            self._add_tech('redis')
        elif 'nginx' in image_lower:
            self._add_tech('nginx')
        elif 'mongodb' in image_lower:
            self._add_tech('mongodb')

    def _infer_technologies(self):
        """Infer additional technologies based on detected patterns."""
        print("🔍 Inferring additional technologies...")
        
        # If React is detected, likely using JSX
        if any('react' in tech.lower() for techs in self.detected_stack.values() for tech_list in techs.values() for tech in tech_list):
            self.languages.add("JSX")
            
        # If TypeScript files found, add TypeScript
        if "TypeScript" in self.languages:
            self._add_tech('typescript')
            
        # Database ORM inference
        detected_orms = []
        for category in self.detected_stack.values():
            for subcategory in category.values():
                detected_orms.extend([tech for tech in subcategory if 'orm' in tech.lower() or tech.lower() in ['prisma', 'sequelize', 'typeorm']])
        
        if detected_orms and not any('database' in cat for cat in self.detected_stack.keys()):
            self._add_tech('database_implied')

    def _add_tech(self, keyword: str):
        """Enhanced technology addition with better categorization."""
        keyword = keyword.lower().strip()
        
        if keyword in ENHANCED_TECH_MAPPING:
            category, sub_category, tech_name = ENHANCED_TECH_MAPPING[keyword]
            
            if category == "projectMeta":
                self.project_meta[sub_category].add(tech_name)
            else:
                self.detected_stack[category][sub_category].add(tech_name)
                
            self.confidence = min(0.99, self.confidence + 0.03)

    def _detect_language_from_file(self, filename: str):
        """Enhanced language detection."""
        ext_map = {
            ".js": "JavaScript", ".jsx": "JavaScript",
            ".ts": "TypeScript", ".tsx": "TypeScript",
            ".py": "Python", ".pyx": "Python",
            ".java": "Java", ".kt": "Kotlin",
            ".go": "Go", ".rs": "Rust",
            ".rb": "Ruby", ".php": "PHP",
            ".html": "HTML", ".htm": "HTML",
            ".css": "CSS", ".scss": "SCSS", ".sass": "SASS",
            ".vue": "Vue", ".svelte": "Svelte",
            ".swift": "Swift", ".m": "Objective-C",
            ".cpp": "C++", ".c": "C", ".h": "C/C++",
            ".cs": "C#", ".vb": "VB.NET",
            ".sql": "SQL", ".yml": "YAML", ".yaml": "YAML"
        }
        
        ext = os.path.splitext(filename)[1].lower()
        if ext in ext_map:
            self.languages.add(ext_map[ext])

    def _should_analyze_file(self, filename: str) -> bool:
        """Determine if file should be analyzed by AI."""
        code_extensions = {'.js', '.jsx', '.ts', '.tsx', '.py', '.java', '.go', '.rb', '.php'}
        config_files = {'package.json', 'requirements.txt', 'Dockerfile', 'docker-compose.yml'}
        
        return (os.path.splitext(filename)[1].lower() in code_extensions or 
                filename in config_files)

    def _is_code_file(self, filename: str) -> bool:
        """Check if file is a code file."""
        code_extensions = {'.js', '.jsx', '.ts', '.tsx', '.py', '.java', '.go', '.rb', '.php', '.html', '.css', '.vue', '.svelte'}
        return os.path.splitext(filename)[1].lower() in code_extensions

    def _analyze_code_file(self, file_path: str):
        """Analyze code file for technology patterns."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # Look for import/require patterns
            imports = re.findall(r'(?:import|require|from)\s+[\'"]([^\'\"]+)[\'"]', content)
            for imp in imports:
                self._add_tech(imp.split('/')[0])
                
            # Look for specific patterns
            if 'useState' in content or 'useEffect' in content:
                self._add_tech('react_hooks')
            if 'styled-components' in content:
                self._add_tech('styled_components')
            if 'GraphQL' in content or 'gql`' in content:
                self._add_tech('graphql')
                
        except Exception:
            pass

    def _analyze_script_content(self, script: str):
        """Analyze package.json scripts for technology hints."""
        if 'webpack' in script:
            self._add_tech('webpack')
        if 'vite' in script:
            self._add_tech('vite')
        if 'jest' in script:
            self._add_tech('jest')
        if 'cypress' in script:
            self._add_tech('cypress')

    def _parse_pipfile(self, file_path: str):
        """Parse Pipfile for Python dependencies."""
        self.project_meta["packageManagers"].add("Pipenv")
        # Implementation for Pipfile parsing

    def _parse_composer_json(self, file_path: str):
        """Parse composer.json for PHP dependencies."""
        self.project_meta["packageManagers"].add("Composer")
        # Implementation for composer.json parsing

    def _parse_gemfile(self, file_path: str):
        """Parse Gemfile for Ruby dependencies."""
        self.project_meta["packageManagers"].add("Bundler")
        # Implementation for Gemfile parsing

    def _parse_go_mod(self, file_path: str):
        """Parse go.mod for Go dependencies."""
        self.project_meta["packageManagers"].add("Go Modules")
        # Implementation for go.mod parsing

    def _parse_pom_xml(self, file_path: str):
        """Parse pom.xml for Java dependencies."""
        self.project_meta["packageManagers"].add("Maven")
        # Implementation for pom.xml parsing

    def _parse_generic_config(self, file_path: str, filename: str):
        """Parse generic configuration files."""
        # Implementation for various config files
        pass

    def _finalize_stack(self):
        """Clean up and finalize the detected stack."""
        # Convert sets to sorted lists
        for category, sub_categories in self.detected_stack.items():
            for sub_category, techs in sub_categories.items():
                self.detected_stack[category][sub_category] = sorted(list(techs))

        for key, values in self.project_meta.items():
            self.project_meta[key] = sorted(list(values))

        self.project_meta["languagesUsed"] = sorted(list(self.languages))

    def format_output(self) -> str:
        """Format the final output with enhanced information."""
        if not self.detected_stack and not self.project_meta:
            return json.dumps({"status": "Unable to detect any technology stack."}, indent=2)

        project_name = os.path.basename(self.project_path)
        
        # Convert defaultdict to regular dict for JSON serialization
        stack_dict = {}
        for category, sub_categories in self.detected_stack.items():
            stack_dict[category] = dict(sub_categories)

        output = {
            "projectName": project_name,
            "source": f"local/{project_name}",
            "description": f"Automatically analyzed project with {len(self.languages)} programming languages detected",
            "detectionMethod": "AI-Enhanced" if self.use_ai else "Pattern-Based",
            "stack": stack_dict,
            "projectMeta": dict(self.project_meta),
            "statistics": {
                "totalTechnologies": sum(len(techs) for cat in stack_dict.values() for techs in cat.values()),
                "categoriesDetected": len(stack_dict),
                "languagesCount": len(self.languages)
            },
            "lastAnalyzed": datetime.now().isoformat(),
            "confidenceScore": round(self.confidence, 2)
        }
        
        return json.dumps(output, indent=2)

