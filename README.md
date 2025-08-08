# 🤖 AI Code Review System

A multi-language, AI-powered **automated code review platform** that analyzes a full codebase, detects issues, and suggests optimized fixes — all while generating documentation.  
Designed to handle large projects with **deep static analysis, graph-based parsing, and LLM-powered smart reviews**.

📄 **Full Project Details:** [View Google Docs](https://docs.google.com/document/d/1lrdytf6-sxHl95BLKnBy_0sQK6FDWNwUccg-BmpppIw/edit?copiedFromTrash&tab=t.a8h28zcqff53)  

---

## 📌 Features

- **Multi-language support** (Python, JavaScript, Java, C/C++, Go, Rust, PHP, etc.)
- **Git & ZIP Input** — Clone repos or upload archives
- **Code Parsing & Graph Building**  
  - AST parsing for function/class extraction  
  - File dependency & function call graphs
- **Static Analysis** (Bugs, Security, Performance, Complexity, Test Coverage)
- **Tech Stack Detection** from source files and dependency manifests
- **Duplicate Code Detection** (intra/inter-file)
- **LLM-Powered Smart Review**  
  - Suggests improvements with explanations  
  - Highlights alternative implementations
- **Documentation Generator**  
  - Auto-generated README, Wiki, and dependency maps
- **Optional Auto-Fix + PR Generation**

---

## 🏗 Architecture Overview

1. **Input Handling**  
   - Clone GitHub repos or extract `.zip`/`.tar.gz`  
   - Exclude environment & build folders

2. **File Walker**  
   - Recursively scans files, classifies by language  
   - Collects metadata (lines, size, location)  

3. **Parsing & Graph Building**  
   - AST-based parsing per language  
   - File dependency and function call graphs

4. **Static Analysis**  
   - Security (Bandit, Semgrep)  
   - Code Quality (Pylint, ESLint, cppcheck)  
   - Complexity & Test Coverage  

5. **Results Aggregation**  
   - JSON/YAML with issue category, file, line, context

6. **LLM Review**  
   - Google Gemini Pro (via Google AI Pro)  
   - Optional GPT-4 / Claude integration

7. **Output & Documentation**  
   - Reports (Markdown, HTML)  
   - Dependency maps (Graphviz)  
   - GitHub Wiki export

---

## 🛠 Tech Stack

**Core**  
- Python 3.10+  
- `pathlib`, `networkx`, `ast`, `tree-sitter`  
- `pylint`, `bandit`, `radon`, `semgrep`  

**LLM Integration**  
- Google Gemini Pro (Free via Google AI Pro student pack)  
- Optional OpenAI GPT-4 / Anthropic Claude  

**Visualization**  
- Graphviz / PyDot  
- Matplotlib / Plotly for dashboards  

**Optional Tools**  
- Enry for advanced language detection  
- OSV Scanner for dependency security  

---

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/ai-code-review.git
cd ai-code-review

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
