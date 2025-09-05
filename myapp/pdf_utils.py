import logging, os
from typing import Optional

logger = logging.getLogger(__name__)

try:
    from weasyprint import HTML  # type: ignore
    _WEASYPRINT_AVAILABLE = True
except Exception as e:  # Catch broad issues (missing cairo/pango)
    logger.warning(f"WeasyPrint import failed or unsupported: {e}")
    _WEASYPRINT_AVAILABLE = False

try:
    import pdfkit  # type: ignore
    _PDFKIT_AVAILABLE = True
except Exception as e:
    logger.warning(f"pdfkit import failed: {e}")
    _PDFKIT_AVAILABLE = False

def generate_pdf(html_string: str, output_path: Optional[str] = None) -> Optional[bytes]:
    """Generate PDF bytes from HTML using WeasyPrint first, fallback to pdfkit.

    Returns bytes or None. Writes to output_path if provided.
    """
    # Try WeasyPrint
    if _WEASYPRINT_AVAILABLE:
        try:
            pdf_bytes = HTML(string=html_string).write_pdf()
            if output_path:
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, 'wb') as f:
                    f.write(pdf_bytes)
            return pdf_bytes
        except Exception as e:
            logger.error(f"WeasyPrint generation failed: {e}")

    # Fallback pdfkit (needs wkhtmltopdf installed system-wide)
    if _PDFKIT_AVAILABLE:
        try:
            import pdfkit  # Re-import inside try for clarity
            if output_path:
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                pdfkit.from_string(html_string, output_path)
                with open(output_path, 'rb') as f:
                    return f.read()
            else:
                return pdfkit.from_string(html_string, False)
        except Exception as e:
            logger.error(f"pdfkit generation failed: {e}")

    return None

def weasyprint_supported():
    return _WEASYPRINT_AVAILABLE
