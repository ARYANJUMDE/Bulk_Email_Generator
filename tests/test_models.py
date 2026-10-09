"""
Unit tests for Pydantic models, schemas, and validators in the Bulk Certificate Generator.
"""

from uuid import UUID
import pytest
from pydantic import ValidationError

from app.models import (
    CertificateRecord,
    CertificateStatus,
    GenerationRequest,
    GenerationResponse,
    Recipient,
    StatusResponse,
    validate_email,
    validate_recipient,
)


class TestRecipientModel:
    """Unit tests for the Recipient model."""

    def test_valid_recipient_creation(self):
        """Test creating a valid recipient with standard inputs."""
        recipient = Recipient(name="Alice Walker", email="alice.walker@example.com")
        assert recipient.name == "Alice Walker"
        assert recipient.email == "alice.walker@example.com"
        assert recipient.certificate_id is None

    def test_recipient_with_custom_certificate_id(self):
        """Test creating a recipient with an explicit certificate ID."""
        custom_id = "CERT-2026-XYZ-001"
        recipient = Recipient(
            name="Bob Martin",
            email="bob.martin@example.org",
            certificate_id=custom_id,
        )
        assert recipient.certificate_id == custom_id

    def test_recipient_strips_surrounding_whitespace(self):
        """Test that names and emails with leading/trailing spaces are stripped cleanly."""
        recipient = Recipient(name="  Carol Danvers  ", email="  carol@example.com  ")
        assert recipient.name == "Carol Danvers"
        assert recipient.email == "carol@example.com"

    def test_recipient_empty_name_raises_validation_error(self):
        """Test that an empty string name triggers a validation error."""
        with pytest.raises(ValidationError, match="Name must not be empty"):
            Recipient(name="", email="test@example.com")

    def test_recipient_whitespace_name_raises_validation_error(self):
        """Test that a whitespace-only name triggers a validation error."""
        with pytest.raises(ValidationError, match="Name must not be empty"):
            Recipient(name="     ", email="test@example.com")

    def test_recipient_invalid_email_format_raises_validation_error(self):
        """Test that a malformed email format triggers a validation error."""
        with pytest.raises(ValidationError, match="Email must be a valid email address"):
            Recipient(name="David Miller", email="not_an_email_address")

    def test_recipient_missing_at_sign_raises_validation_error(self):
        """Test that an email without '@' triggers a validation error."""
        with pytest.raises(ValidationError, match="Email must be a valid email address"):
            Recipient(name="David Miller", email="david.example.com")


class TestGenerationRequestModel:
    """Unit tests for the GenerationRequest payload model."""

    def test_generation_request_valid_minimal(self):
        """Test minimal valid request containing only recipients and course name."""
        request = GenerationRequest(
            recipients=[Recipient(name="John Doe", email="john@example.com")],
            course_name="Machine Learning Bootcamp",
        )
        assert len(request.recipients) == 1
        assert request.course_name == "Machine Learning Bootcamp"
        assert request.issue_date is None
        assert request.organization is None

    def test_generation_request_valid_with_optional_fields(self):
        """Test valid generation request with issue date and organization populated."""
        request = GenerationRequest(
            recipients=[
                Recipient(name="User One", email="user1@example.com"),
                Recipient(name="User Two", email="user2@example.com"),
            ],
            course_name="Cloud Security Architecture",
            issue_date="2026-10-09",
            organization="Global Tech Institute",
        )
        assert len(request.recipients) == 2
        assert request.issue_date == "2026-10-09"
        assert request.organization == "Global Tech Institute"

    def test_generation_request_empty_recipients_raises_validation_error(self):
        """Test that an empty recipients list triggers validation failure."""
        with pytest.raises(ValidationError):
            GenerationRequest(
                recipients=[],
                course_name="Data Science Masterclass",
            )

    def test_generation_request_empty_course_name_raises_validation_error(self):
        """Test that empty or whitespace course name triggers validation failure."""
        with pytest.raises(ValidationError, match="Course name must not be empty"):
            GenerationRequest(
                recipients=[Recipient(name="John Doe", email="john@example.com")],
                course_name="   ",
            )


class TestTrackingAndResponseModels:
    """Unit tests for tracking and response models."""

    def test_certificate_record_defaults_and_uuid(self):
        """Test CertificateRecord default attributes and valid UUID generation."""
        record = CertificateRecord(
            recipient_name="bulk-job",
            recipient_email="Python Mastery",
            certificate_id="job-101",
            course_name="Python Mastery",
        )
        assert UUID(record.id)
        assert record.status == CertificateStatus.PENDING
        assert record.success_count == 0
        assert record.failed_recipients == []
        assert record.certificate_urls == []

    def test_generation_response_model(self):
        """Test GenerationResponse payload serialization."""
        response = GenerationResponse(
            job_id="job-abc-123",
            message="Job queued",
            total_recipients=10,
            status=CertificateStatus.PENDING,
        )
        data = response.model_dump()
        assert data["job_id"] == "job-abc-123"
        assert data["total_recipients"] == 10
        assert data["status"] == "pending"

    def test_status_response_model(self):
        """Test StatusResponse data serialization and structure."""
        response = StatusResponse(
            job_id="job-xyz-789",
            status=CertificateStatus.GENERATED,
            total=3,
            completed=3,
            failed=0,
            success_count=3,
            failed_recipients=[],
            certificate_urls=["/api/v1/certificates/cert1.pdf"],
        )
        assert response.total == 3
        assert response.completed == 3
        assert len(response.certificate_urls) == 1


class TestCertificateStatusConstants:
    """Unit tests for status constant definitions."""

    def test_status_constants_values(self):
        """Verify all standard status strings exist."""
        assert CertificateStatus.PENDING == "pending"
        assert CertificateStatus.GENERATING == "generating"
        assert CertificateStatus.GENERATED == "generated"
        assert CertificateStatus.FAILED == "failed"
        assert CertificateStatus.COMPLETED == "completed"


class TestValidationHelpers:
    """Unit tests for email and recipient validation helper functions."""

    def test_validate_email_helper_matrix(self):
        """Test matrix of valid and invalid email addresses."""
        assert validate_email("user@example.com") is True
        assert validate_email("john.doe+tag@sub.domain.co.uk") is True
        assert validate_email("invalid-email") is False
        assert validate_email("@domain.com") is False
        assert validate_email("user@") is False
        assert validate_email("") is False
        assert validate_email(None) is False  # type: ignore

    def test_validate_recipient_helper(self):
        """Test validate_recipient helper function behavior."""
        valid_rec = Recipient(name="Valid User", email="user@valid.com")
        assert validate_recipient(valid_rec) is True

        assert validate_recipient(None) is False

        class InvalidDummy:
            name = ""
            email = "bad"

        assert validate_recipient(InvalidDummy()) is False