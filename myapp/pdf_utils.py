import logging, os, io
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

# Note: xhtml2pdf depends on reportlab; import it lazily inside the fallback to avoid
# noisy import errors at startup when reportlab isn't available.


def generate_pdf(html_string: str, output_path: Optional[str] = None) -> Optional[bytes]:
    """Generate PDF bytes from HTML with multiple fallbacks.

    Order of backends:
    1) WeasyPrint
    2) pdfkit (wkhtmltopdf)
    3) xhtml2pdf (pisa)

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

    # Fallback xhtml2pdf (basic HTML/CSS support)
    try:
        # Import lazily to avoid hard dependency at startup
        from xhtml2pdf import pisa  # type: ignore
        mem = io.BytesIO()
        # xhtml2pdf expects bytes; ensure utf-8
        pisa_status = pisa.CreatePDF(src=html_string, dest=mem, encoding='utf-8')
        if not pisa_status.err:
            pdf_bytes = mem.getvalue()
            if output_path:
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, 'wb') as f:
                    f.write(pdf_bytes)
            return pdf_bytes
        else:
            logger.debug(f"xhtml2pdf generation reported errors (code={pisa_status.err})")
    except Exception as e:
        # Keep quiet at INFO level; this backend is optional
        logger.debug(f"xhtml2pdf generation failed: {e}")

    return None

def weasyprint_supported():
    return _WEASYPRINT_AVAILABLE
