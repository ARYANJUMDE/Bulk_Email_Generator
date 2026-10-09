"""
Utility functions for certificate generation, validation, and file handling.
"""

import datetime
import re
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

CERTS_DIR = Path("generated_certificates")


def sanitize_filename(name: str) -> str:
    """
    Sanitize recipient or course name to produce safe filenames across OS filesystems.
    Removes invalid characters and spaces.
    """
    # Remove characters that are illegal in Windows/Linux filenames: < > : " / \ | ? *
    sanitized = re.sub(r'[<>:"/\\|?*\'`]', "", name.strip())
    # Replace whitespace with underscore
    sanitized = re.sub(r"\s+", "_", sanitized)
    # Collapse consecutive underscores
    sanitized = re.sub(r"_+", "_", sanitized).strip("_")
    # Ensure it is not empty
    return sanitized or "certificate"


def validate_email(email: str) -> bool:
    """Validate an email address format with a strict regex pattern."""
    if not email or not isinstance(email, str):
        return False
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email.strip()))


def validate_recipient(recipient: Any) -> bool:
    """Validate recipient data. Returns True if valid."""
    if not recipient:
        return False
    name = getattr(recipient, "name", None)
    email = getattr(recipient, "email", None)
    if not name or not str(name).strip():
        return False
    if not email or not str(email).strip():
        return False
    return validate_email(str(email))


def _draw_certificate_decorations(canvas_obj: Any, doc: Any) -> None:
    """
    Draw elegant background, dual borders, and corner decorations on the certificate canvas.
    """
    width, height = landscape(letter)  # 792 x 612 pt
    canvas_obj.saveState()

    # 1. Soft warm background
    canvas_obj.setFillColor(colors.HexColor("#FCFDFD"))
    canvas_obj.rect(0, 0, width, height, fill=1, stroke=0)

    # 2. Outer Navy Border
    canvas_obj.setStrokeColor(colors.HexColor("#0F172A"))
    canvas_obj.setLineWidth(3)
    canvas_obj.rect(18, 18, width - 36, height - 36, fill=0, stroke=1)

    # 3. Inner Gold Accent Border
    canvas_obj.setStrokeColor(colors.HexColor("#D97706"))
    canvas_obj.setLineWidth(1)
    canvas_obj.rect(24, 24, width - 48, height - 48, fill=0, stroke=1)

    # 4. Corner Diamonds / Flourishes (Gold)
    for cx, cy in [
        (24, 24),
        (width - 24, 24),
        (24, height - 24),
        (width - 24, height - 24),
    ]:
        canvas_obj.setFillColor(colors.HexColor("#D97706"))
        canvas_obj.rect(cx - 3, cy - 3, 6, 6, fill=1, stroke=0)

    # 5. Top Header Accent Banner
    canvas_obj.setFillColor(colors.HexColor("#0F172A"))
    canvas_obj.rect(24, height - 36, width - 48, 6, fill=1, stroke=0)
    canvas_obj.setFillColor(colors.HexColor("#D97706"))
    canvas_obj.rect(width / 2 - 70, height - 38, 140, 2, fill=1, stroke=0)

    canvas_obj.restoreState()


def generate_certificate(
    recipient: Any,
    course_name: str,
    issue_date: Optional[str] = None,
    organization: Optional[str] = None,
) -> Path:
    """
    Generate a high-quality, professional landscape certificate PDF for a recipient.
    
    Returns the Path to the generated PDF file.
    """
    CERTS_DIR.mkdir(parents=True, exist_ok=True)

    cert_id = getattr(recipient, "certificate_id", None) or str(uuid.uuid4())
    recipient_name = getattr(recipient, "name", str(recipient))
    safe_name = sanitize_filename(recipient_name)
    filename = f"{cert_id}_{safe_name}.pdf"
    filepath = CERTS_DIR / filename

    if filepath.exists():
        filepath.unlink()

    # Setup document with landscape letter geometry
    doc = SimpleDocTemplate(
        str(filepath),
        pagesize=landscape(letter),
        leftMargin=40,
        rightMargin=40,
        topMargin=45,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()

    org_text = (organization or "ACADEMY OF PROFESSIONAL EXCELLENCE").strip()
    formatted_date = (
        issue_date.strip()
        if (issue_date and issue_date.strip())
        else datetime.datetime.now().strftime("%B %d, %Y")
    )

    # Typography Styles
    org_style = ParagraphStyle(
        "CertOrg",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=14,
        alignment=1,  # Center
        textColor=colors.HexColor("#64748B"),
        spaceAfter=12,
    )

    title_style = ParagraphStyle(
        "CertTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=26,
        leading=30,
        alignment=1,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=4,
    )

    subtitle_style = ParagraphStyle(
        "CertSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        alignment=1,
        textColor=colors.HexColor("#D97706"),
        spaceAfter=10,
    )

    recipient_style = ParagraphStyle(
        "CertRecipient",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=28,
        leading=34,
        alignment=1,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=2,
    )

    body_style = ParagraphStyle(
        "CertBody",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=12,
        leading=16,
        alignment=1,
        textColor=colors.HexColor("#475569"),
        spaceAfter=8,
    )

    course_style = ParagraphStyle(
        "CertCourse",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        alignment=1,
        textColor=colors.HexColor("#1E3A8A"),
        spaceAfter=22,
    )

    footer_val_style = ParagraphStyle(
        "FooterVal",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155"),
    )

    seal_style = ParagraphStyle(
        "Seal",
        parent=styles["Normal"],
        alignment=1,
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#D97706"),
    )

    sig_style = ParagraphStyle(
        "Sig",
        parent=styles["Normal"],
        alignment=2,
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1E293B"),
    )

    elements: List[Any] = []

    # 1. Organization Header
    elements.append(Paragraph(org_text.upper(), org_style))

    # 2. Main Certificate Title
    elements.append(Paragraph("CERTIFICATE OF COMPLETION", title_style))

    # 3. Subtitle
    elements.append(Paragraph("THIS IS PROUDLY PRESENTED TO", subtitle_style))

    # 4. Recipient Name
    elements.append(Paragraph(recipient_name, recipient_style))

    # 5. Decorative Gold Underline
    elements.append(
        HRFlowable(
            width="55%",
            thickness=1.5,
            color=colors.HexColor("#D97706"),
            spaceBefore=2,
            spaceAfter=14,
        )
    )

    # 6. Body statement & Course Name
    elements.append(
        Paragraph(
            "for successfully fulfilling all requirements and demonstrating proficiency in",
            body_style,
        )
    )
    elements.append(Paragraph(course_name, course_style))

    # 7. Authenticity Footer (Metadata, Official Badge, Signature)
    short_cert_id = cert_id[:16] if len(cert_id) > 16 else cert_id
    footer_data = [
        [
            Paragraph(
                f"<b>Date Issued:</b> {formatted_date}<br/><b>Certificate ID:</b> {short_cert_id}",
                footer_val_style,
            ),
            Paragraph(
                "★ ★ ★<br/><b>OFFICIAL CERTIFIED</b><br/>VERIFIED CREDENTIAL",
                seal_style,
            ),
            Paragraph(
                f"___________________________<br/><b>Authorized Signatory</b><br/>{org_text}",
                sig_style,
            ),
        ]
    ]

    footer_table = Table(footer_data, colWidths=[240, 232, 240])
    footer_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
                ("ALIGN", (0, 0), (0, 0), "LEFT"),
                ("ALIGN", (1, 0), (1, 0), "CENTER"),
                ("ALIGN", (2, 0), (2, 0), "RIGHT"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )

    elements.append(Spacer(1, 8))
    elements.append(footer_table)

    doc.build(elements, onFirstPage=_draw_certificate_decorations)
    return filepath


def generate_all_certificates(
    job_id: str,
    recipients: List[Any],
    course_name: str,
    issue_date: Optional[str] = None,
    organization: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate certificates for a list of recipients with individual failure isolation.
    """
    success_count = 0
    failed_list: List[Dict[str, Any]] = []
    certificate_urls: List[str] = []

    for i, recipient in enumerate(recipients):
        try:
            filepath = generate_certificate(
                recipient=recipient,
                course_name=course_name,
                issue_date=issue_date,
                organization=organization,
            )
            success_count += 1
            certificate_urls.append(f"/api/v1/certificates/{filepath.name}")
        except Exception as e:
            name = getattr(recipient, "name", f"recipient_{i}")
            email = getattr(recipient, "email", "")
            failed_list.append(
                {
                    "recipient_name": name,
                    "recipient_email": email,
                    "error": str(e),
                    "index": i,
                }
            )

    return {
        "job_id": job_id,
        "total_recipients": len(recipients),
        "success_count": success_count,
        "failed_count": len(failed_list),
        "certificate_urls": certificate_urls,
        "failed_recipients": failed_list,
        "status": "generated" if success_count > 0 else ("failed" if failed_list else "completed"),
    }
