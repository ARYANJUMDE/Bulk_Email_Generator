"""
Pydantic data models and schemas for the Bulk Certificate Generator application.
"""

import datetime
from typing import Any, Dict, List, Optional
import re
import uuid
from pydantic import BaseModel, Field, field_validator

from app.utils import (
    CERTS_DIR,
    generate_all_certificates,
    generate_certificate,
    validate_email,
    validate_recipient,
)


class CertificateStatus:
    """Status constants for certificate generation jobs."""
    PENDING = "pending"
    GENERATING = "generating"
    GENERATED = "generated"
    FAILED = "failed"
    COMPLETED = "completed"


class Recipient(BaseModel):
    """A single recipient for certificate generation."""
    name: str = Field(..., description="Full name of the recipient")
    email: str = Field(..., description="Email address of the recipient")
    certificate_id: Optional[str] = Field(
        None, description="Custom certificate ID (auto-generated if not provided)"
    )

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Name must not be empty")
        return v.strip()

    @field_validator("email")
    @classmethod
    def email_must_be_valid(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Email must not be empty")
        email = v.strip()
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, email):
            raise ValueError("Email must be a valid email address")
        return email


class GenerationRequest(BaseModel):
    """Request payload for bulk certificate generation."""
    recipients: List[Recipient] = Field(
        ..., min_length=1, description="List of recipients to generate certificates for"
    )
    course_name: str = Field(..., description="Name of the course or event")
    issue_date: Optional[str] = Field(None, description="Date the certificates are issued")
    organization: Optional[str] = Field(None, description="Issuing organization")

    @field_validator("course_name")
    @classmethod
    def course_name_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Course name must not be empty")
        return v.strip()


class CertificateRecord(BaseModel):
    """Record tracking certificate generation status and output files."""
    model_config = {"arbitrary_types_allowed": True}

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    recipient_name: str
    recipient_email: str
    certificate_id: str
    course_name: str
    issue_date: Optional[str] = None
    status: str = CertificateStatus.PENDING
    generated_at: Optional[datetime.datetime] = None
    error_message: Optional[str] = None
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
    completed_at: Optional[datetime.datetime] = None
    success_count: int = 0
    failed_recipients: List[Dict[str, Any]] = Field(default_factory=list)
    certificate_urls: List[str] = Field(default_factory=list)


class GenerationResponse(BaseModel):
    """Response returned upon submitting a generation request."""
    model_config = {"arbitrary_types_allowed": True}

    job_id: str
    message: str
    total_recipients: int
    status: str = CertificateStatus.PENDING


class StatusResponse(BaseModel):
    """Response model for job status checks."""
    model_config = {"arbitrary_types_allowed": True}

    job_id: str
    status: str
    total: int
    completed: int
    failed: int
    success_count: int
    failed_recipients: List[Dict[str, Any]] = Field(default_factory=list)
    certificate_urls: List[str] = Field(default_factory=list)


__all__ = [
    "CertificateStatus",
    "Recipient",
    "GenerationRequest",
    "CertificateRecord",
    "GenerationResponse",
    "StatusResponse",
    "validate_recipient",
    "validate_email",
    "generate_certificate",
    "generate_all_certificates",
    "CERTS_DIR",
]