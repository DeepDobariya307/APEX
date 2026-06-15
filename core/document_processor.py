"""
APEX — Document Processor
Handles PDF resume and job description ingestion.
Returns clean raw text ready for agent parsing.
"""

from __future__ import annotations

import logging
import tempfile
import os

import pdfplumber

from config import config

logger = logging.getLogger(__name__)


class DocumentProcessor:

    def process_resume(self, uploaded_file) -> str:
        if uploaded_file is None:
            raise ValueError("No resume file provided.")

        name = uploaded_file.name.lower()

        if name.endswith(".pdf"):
            return self._extract_pdf_text(
                uploaded_file,
                max_pages=config.MAX_RESUME_PAGES,
            )
        elif name.endswith((".txt", ".md")):
            return uploaded_file.read().decode("utf-8", errors="ignore")
        else:
            raise ValueError(f"Unsupported resume format: {name}. Use PDF or TXT.")

    def process_job_description(self, source) -> str:
        if source is None:
            raise ValueError("No job description provided.")

        if isinstance(source, str):
            text = source.strip()
            if not text:
                raise ValueError("Job description text is empty.")
            return text[: config.MAX_JD_CHARS]

        name = source.name.lower()
        if name.endswith(".pdf"):
            text = self._extract_pdf_text(source, max_pages=10)
        elif name.endswith((".txt", ".md")):
            text = source.read().decode("utf-8", errors="ignore")
        else:
            raise ValueError(f"Unsupported JD format: {name}. Use PDF or TXT.")

        return text[: config.MAX_JD_CHARS]

    @staticmethod
    def _extract_pdf_text(uploaded_file, max_pages: int = 10) -> str:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        try:
            pages_text: list[str] = []
            with pdfplumber.open(tmp_path) as pdf:
                pages = pdf.pages[:max_pages]
                for page in pages:
                    parts: list[str] = []

                    tables = page.extract_tables()
                    for table in tables:
                        if table and table[0]:
                            parts.append(DocumentProcessor._table_to_markdown(table))

                    text = page.extract_text()
                    if text and text.strip():
                        parts.append(text.strip())

                    if parts:
                        pages_text.append("\n\n".join(parts))

            full_text = "\n\n---PAGE BREAK---\n\n".join(pages_text)

            if not full_text.strip():
                raise ValueError("Could not extract text from PDF.")

            return full_text

        finally:
            os.unlink(tmp_path)

    @staticmethod
    def _table_to_markdown(table: list) -> str:
        if not table or not table[0]:
            return ""
        cleaned = [
            [str(cell).strip() if cell else "" for cell in row]
            for row in table
        ]
        header = cleaned[0]
        rows = cleaned[1:]
        lines = [
            "| " + " | ".join(header) + " |",
            "| " + " | ".join(["---"] * len(header)) + " |",
        ]
        for row in rows:
            while len(row) < len(header):
                row.append("")
            lines.append("| " + " | ".join(row) + " |")
        return "\n".join(lines)