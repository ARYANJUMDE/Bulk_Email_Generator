"""
API Route definitions for the Bulk Certificate Generator application.
"""

import datetime
from pathlib import Path
from typing import List
import uuid

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from app.models import (
    CERTS_DIR,
    CertificateRecord,
    CertificateStatus,
    GenerationRequest,
    GenerationResponse,
    StatusResponse,
    generate_all_certificates,
    validate_recipient,
)
from app.storage import get_job, save_job

router = APIRouter(prefix="/api/v1", tags=["certificates"])


@router.post(
    "/generate-certificates",
    response_model=GenerationResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Submit bulk certificate generation request",
    description="Accept a list of recipients and generate customized certificates for each recipient.",
)
async def generate_certificates(request: GenerationRequest):
    """
    Accept a bulk certificate generation request.
    
    - **recipients**: List of recipients with name and email
    - **course_name**: Name of the course or event
    - **issue_date**: Optional issue date string (e.g., '2024-01-15')
    - **organization**: Optional issuing organization
    """
    job_id = str(uuid.uuid4())

    # Pre-validate recipients
    valid_recipients = []
    failed_recipients = []

    for recipient in request.recipients:
        if validate_recipient(recipient):
            valid_recipients.append(recipient)
        else:
            failed_recipients.append(
                {
                    "recipient": recipient.model_dump(),
                    "error": "Invalid recipient data: name and email are required with valid format",
                }
            )

    # Initialize job tracking record
    record = CertificateRecord(
        id=job_id,
        recipient_name="bulk-job",
        recipient_email=request.course_name,
        certificate_id=job_id,
        course_name=request.course_name,
        issue_date=request.issue_date,
        status=CertificateStatus.PENDING,
        failed_recipients=failed_recipients,
    )
    save_job(record)

    # Process certificate generation
    if valid_recipients:
        try:
            result = generate_all_certificates(
                job_id=job_id,
                recipients=valid_recipients,
                course_name=request.course_name,
                issue_date=request.issue_date,
                organization=request.organization,
            )
            record.status = CertificateStatus.GENERATED
            record.success_count = result.get("success_count", 0)
            record.failed_recipients.extend(result.get("failed_recipients", []))
            record.certificate_urls = result.get("certificate_urls", [])
            record.generated_at = datetime.datetime.now(datetime.timezone.utc)
        except Exception as e:
            record.status = CertificateStatus.FAILED
            record.error_message = str(e)
    else:
        record.status = CertificateStatus.FAILED
        record.error_message = "No valid recipients provided."

    record.completed_at = datetime.datetime.now(datetime.timezone.utc)
    save_job(record)

    return GenerationResponse(
        job_id=job_id,
        message=f"Certificate generation job started for {len(valid_recipients)} recipients",
        total_recipients=len(request.recipients),
        status=record.status,
    )


@router.get(
    "/status/{job_id}",
    response_model=StatusResponse,
    summary="Check generation job status",
    description="Retrieve the current status, statistics, and certificate download URLs for a job ID.",
)
async def check_status(job_id: str):
    """
    Check the status of a certificate generation job.
    
    - **job_id**: The job UUID returned from the generation request
    """
    record = get_job(job_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    failed_list = [
        {
            "name": fr.get("recipient_name") or (fr.get("recipient", {}) or {}).get("name", ""),
            "email": fr.get("recipient_email") or (fr.get("recipient", {}) or {}).get("email", ""),
            "error": fr.get("error", "Unknown error"),
        }
        for fr in (record.failed_recipients or [])
    ]

    completed_count = len(record.certificate_urls or [])
    total_count = completed_count + len(failed_list)

    return StatusResponse(
        job_id=job_id,
        status=record.status,
        total=total_count,
        completed=completed_count,
        failed=len(failed_list),
        success_count=record.success_count or completed_count,
        failed_recipients=failed_list,
        certificate_urls=record.certificate_urls or [],
    )


@router.get(
    "/certificates",
    summary="List all generated certificates",
    description="Returns a list of all generated certificate files stored on the server.",
)
async def list_certificates():
    """List all available generated certificate files."""
    if not CERTS_DIR.exists():
        return {"certificates": [], "count": 0}

    files = []
    for f in sorted(
        CERTS_DIR.glob("*.pdf"), key=lambda x: x.stat().st_mtime, reverse=True
    ):
        files.append(
            {
                "filename": f.name,
                "url": f"/api/v1/certificates/{f.name}",
                "size_bytes": f.stat().st_size,
            }
        )

    return {"certificates": files, "count": len(files)}


@router.get(
    "/certificates/{filename}",
    response_class=FileResponse,
    summary="Download generated certificate",
    description="Download a previously generated certificate PDF by filename.",
)
async def download_certificate(filename: str):
    """
    Download a generated certificate PDF.
    
    - **filename**: The filename of the certificate to download
    """
    # Prevent path traversal security vulnerabilities
    safe_name = Path(filename).name
    filepath = CERTS_DIR / safe_name

    if not filepath.exists() or not filepath.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate not found",
        )

    return FileResponse(
        path=str(filepath),
        filename=safe_name,
        media_type="application/pdf",
    )


@router.get(
    "/health",
    summary="API Health Check",
    description="Returns the health status of the API.",
)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "message": "Bulk Certificate Generator API is running",
    }