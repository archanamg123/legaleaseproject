from services.exporters import (
    format_txt,
    format_docx,
    format_pdf,
    format_html_preview,
)


SAMPLE_TEXT = """
FREELANCE WORK CONTRACT

Effective Date: 2026-09-26

PARTIES

Jane Doe (Freelancer)
TechNova Inc. (Client)

TERMS AND CONDITIONS

1. Payment must be made within 30 days.
2. Confidentiality must be maintained.
3. Work must be delivered by the agreed deadline.

SIGNATURES

Party 1: __________________________
Party 2: __________________________
"""


def test_txt_export():

    result = format_txt(
        SAMPLE_TEXT
    )

    assert isinstance(result, bytes)

    assert b"FREELANCE WORK CONTRACT" in result


def test_docx_export():

    result = format_docx(
        SAMPLE_TEXT,
        "Freelance Work Contract"
    )

    assert isinstance(result, bytes)

    # DOCX files are ZIP-based files.
    assert result[:2] == b"PK"


def test_pdf_export():

    result = format_pdf(
        SAMPLE_TEXT,
        "Freelance Work Contract"
    )

    assert isinstance(result, bytes)

    # PDF magic number.
    assert result.startswith(b"%PDF")


def test_html_preview():

    result = format_html_preview(
        SAMPLE_TEXT
    )

    assert "<h3>" in result

    assert "FREELANCE WORK CONTRACT" in result