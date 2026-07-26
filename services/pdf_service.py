"""
PDF text extraction using pdfplumber.
Kept synchronous internally (pdfplumber has no async API) but run inside
asyncio.to_thread from the handler so it doesn't block the event loop.
"""
import logging

import pdfplumber

logger = logging.getLogger(__name__)


class PDFExtractionError(Exception):
    """Raised when a PDF can't be read or contains no extractable text."""


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts and concatenates text from every page of a PDF.
    Raises PDFExtractionError on failure or if no text is found
    (e.g. scanned/image-only PDFs — OCR is out of scope for this MVP).
    """
    try:
        pages_text = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    pages_text.append(text)
    except Exception as e:
        logger.exception("Failed to open/parse PDF at %s", file_path)
        raise PDFExtractionError(f"Could not read PDF file: {e}") from e

    full_text = "\n\n".join(pages_text).strip()

    if not full_text:
        raise PDFExtractionError(
            "No extractable text found in this PDF. It may be scanned/image-based, "
            "which isn't supported yet."
        )

    return full_text
