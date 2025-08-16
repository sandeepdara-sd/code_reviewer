"""
notebook_handler.py — Handles .ipynb (Jupyter Notebook) files for analysis.

Extracts code cells while preserving:
- Cell number
- Cell type (code/markdown)
- Original source lines
"""

import json
import logging
from pathlib import Path

def extract_ipynb_cells(file_path: Path):
    """
    Extracts all cells from a Jupyter Notebook file.

    Args:
        file_path (Path): Path to the .ipynb file.

    Returns:
        list: List of dicts with cell_number, cell_type, and source.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            notebook_data = json.load(f)

        cells_data = []
        for idx, cell in enumerate(notebook_data.get("cells", []), start=1):
            cell_type = cell.get("cell_type", "unknown")
            source_code = "".join(cell.get("source", []))

            cells_data.append({
                "cell_number": idx,
                "cell_type": cell_type,
                "source": source_code
            })

        logging.info(f"Extracted {len(cells_data)} cells from notebook: {file_path}")
        return cells_data

    except Exception as e:
        logging.error(f"Error reading notebook {file_path}: {e}")
        return []
