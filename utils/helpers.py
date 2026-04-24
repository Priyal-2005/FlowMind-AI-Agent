"""
Helper Utilities — FlowMind AI

Provides lightweight utility functions for:
- File input processing (PDF / TXT upload support)
- Export functionality (JSON / CSV download)

These are intentionally kept simple and dependency-light.
"""

import csv
import io
import json
from typing import Any, Union


# ── FILE INPUT SUPPORT ──────────────────────────────────────


def extract_text_from_file(uploaded_file) -> str:
    """
    Extract plain text from an uploaded file (Streamlit UploadedFile object).

    Supports:
        - .txt  → direct UTF-8 read
        - .pdf  → page-by-page text extraction via PyPDF2

    Args:
        uploaded_file: A Streamlit UploadedFile object with .name and .read().

    Returns:
        Extracted text as a single string, with pages separated by newlines.
        Returns an empty string if extraction fails.
    """
    if uploaded_file is None:
        return ""

    filename = uploaded_file.name.lower()

    # ── Plain text files ──────────────────────────
    if filename.endswith(".txt"):
        try:
            return uploaded_file.read().decode("utf-8")
        except Exception:
            return ""

    # ── PDF files ─────────────────────────────────
    if filename.endswith(".pdf"):
        try:
            from PyPDF2 import PdfReader

            reader = PdfReader(uploaded_file)
            pages = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    pages.append(text.strip())
            return "\n\n".join(pages)
        except ImportError:
            return "[Error] PyPDF2 is required for PDF support. Install with: pip install PyPDF2"
        except Exception:
            return ""

    return ""


# ── EXPORT FUNCTIONALITY ────────────────────────────────────


def export_to_json(data: Any, indent: int = 2) -> str:
    """
    Serialize workflow output to a formatted JSON string.

    Args:
        data:   Any JSON-serializable data (dict, list, WorkflowState.to_dict(), etc.)
        indent: Number of spaces for indentation (default: 2).

    Returns:
        Pretty-printed JSON string ready for download.
    """
    return json.dumps(data, indent=indent, default=str, ensure_ascii=False)


def export_to_csv(tasks: list) -> str:
    """
    Convert a list of task dictionaries to a CSV string.

    Exports the following columns per task:
        ID, Title, Owner, Priority, Status, Deadline, Risk Flag, Progress

    Args:
        tasks: List of task dicts (as produced by the Execution Agent).

    Returns:
        CSV-formatted string with headers, ready for download.
    """
    if not tasks:
        return ""

    output = io.StringIO()
    writer = csv.writer(output)

    # Header row
    headers = ["ID", "Title", "Owner", "Priority", "Status", "Deadline", "Risk Flag", "Progress (%)"]
    writer.writerow(headers)

    # Data rows
    for task in tasks:
        writer.writerow([
            task.get("id", ""),
            task.get("title", ""),
            task.get("owner", "UNASSIGNED"),
            task.get("priority", "P2"),
            task.get("status", "pending"),
            task.get("deadline", "—"),
            task.get("risk_flag", "LOW"),
            task.get("progress", 0),
        ])

    return output.getvalue()
