"""
Unit and integration tests for PDF certificate rendering, filesystem safety, and batch generation.
"""

from pathlib import Path
import pytest
from unittest.mock import patch

from app.models import Recipient
from app.utils import (
    generate_all_certificates,
    generate_certificate,
    sanitize_filename,
)


@pytest.mark.gen
class TestCertificatePDFGeneration:
    """Tests for PDF rendering engine and ReportLab layout."""

    def test_generate_single_certificate_creates_valid_pdf(self):
        """Verify that generate_certificate produces a valid, non-empty PDF file."""
        recipient = Recipient(name="Eleanor Vance", email="eleanor@example.com")
        filepath = generate_certificate(
            recipient=recipient,
            course_name="Quantum Computing Fundamentals",
            issue_date="2026-10-09",
            organization="Physics & Tech Institute",
        )

        assert filepath.exists()
        assert filepath.is_file()
        assert filepath.suffix == ".pdf"

        # Verify PDF header magic bytes
        with open(filepath, "rb") as f:
            header = f.read(5)
            assert header == b"%PDF-", "Generated file is not a valid PDF document"

        # Verify file has substantial size
        assert filepath.stat().st_size > 1024

    def test_generate_certificate_with_custom_id_embeds_in_filename(self):
        """Verify custom certificate IDs are incorporated into the generated file path."""
        custom_id = "CUSTOM-ID-9999"
        recipient = Recipient(
            name="Gregory House",
            email="house@princeton.edu",
            certificate_id=custom_id,
        )
        filepath = generate_certificate(
            recipient=recipient,
            course_name="Diagnostic Medicine",
        )

        assert custom_id in filepath.name
        assert filepath.exists()

    def test_generate_certificate_sanitizes_dangerous_filename_characters(self):
        """Verify recipient names with slashes, colons, or quotes do not crash filesystem operations."""
        recipient = Recipient(name="John / Doe : Jr *", email="john.jr@example.com")
        filepath = generate_certificate(
            recipient=recipient,
            course_name="Web Security Testing",
        )

        assert filepath.exists()
        assert "/" not in filepath.name
        assert ":" not in filepath.name
        assert "*" not in filepath.name

    def test_generate_certificate_supports_long_names_and_course_titles(self):
        """Verify that lengthy names and course descriptions render cleanly without layout crash."""
        long_name = "Dr. Bartholomew Jo-Jo Constantine Montgomery-Smith the Third"
        long_course = (
            "Comprehensive Masterclass in Advanced Distributed Cloud Architecture, "
            "Microservices Resilience, and High-Throughput Stream Processing"
        )
        recipient = Recipient(name=long_name, email="long.name@example.org")
        filepath = generate_certificate(
            recipient=recipient,
            course_name=long_course,
            issue_date="2026-10-09",
            organization="International Academy of Systems Architecture & Software Engineering",
        )
        assert filepath.exists()
        assert filepath.stat().st_size > 1024

    def test_generate_certificate_fallback_defaults(self):
        """Verify fallback behavior when issue_date and organization are omitted."""
        recipient = Recipient(name="Jane Default", email="jane.default@example.com")
        filepath = generate_certificate(
            recipient=recipient,
            course_name="Python Automation",
            issue_date=None,
            organization=None,
        )
        assert filepath.exists()


@pytest.mark.gen
class TestBulkBatchGeneration:
    """Tests for multi-recipient bulk generation and error isolation."""

    def test_generate_all_certificates_batch_success(self):
        """Verify batch generation creates all certificates and returns summary."""
        recipients = [
            Recipient(name="User Alpha", email="alpha@example.com"),
            Recipient(name="User Beta", email="beta@example.com"),
            Recipient(name="User Gamma", email="gamma@example.com"),
        ]
        job_id = "batch-test-123"
        result = generate_all_certificates(
            job_id=job_id,
            recipients=recipients,
            course_name="Docker & Kubernetes in Production",
        )

        assert result["job_id"] == job_id
        assert result["total_recipients"] == 3
        assert result["success_count"] == 3
        assert result["failed_count"] == 0
        assert len(result["certificate_urls"]) == 3
        assert result["status"] == "generated"

    def test_generate_all_certificates_failure_isolation(self):
        """Verify that an exception generating one certificate does not halt the entire batch."""
        recipients = [
            Recipient(name="Good One", email="good1@example.com"),
            Recipient(name="Bad One", email="bad@example.com"),
            Recipient(name="Good Two", email="good2@example.com"),
        ]

        original_generate = generate_certificate

        def mock_generate(recipient, *args, **kwargs):
            if recipient.name == "Bad One":
                raise RuntimeError("Simulated PDF generation error")
            return original_generate(recipient, *args, **kwargs)

        with patch("app.utils.generate_certificate", side_effect=mock_generate):
            result = generate_all_certificates(
                job_id="batch-failure-isolation",
                recipients=recipients,
                course_name="Robust Error Handling",
            )

        assert result["total_recipients"] == 3
        assert result["success_count"] == 2
        assert result["failed_count"] == 1
        assert len(result["failed_recipients"]) == 1
        assert result["failed_recipients"][0]["recipient_name"] == "Bad One"
        assert "Simulated PDF generation error" in result["failed_recipients"][0]["error"]


class TestFilenameSanitizer:
    """Unit tests for the sanitize_filename utility."""

    def test_sanitize_filename_utility(self):
        """Verify character replacement and empty string safety."""
        assert sanitize_filename("John Doe") == "John_Doe"
        assert sanitize_filename('A < B > C : D " E / F \\ G | H ? I * J') == "A_B_C_D_E_F_G_H_I_J"
        assert sanitize_filename("   ") == "certificate"