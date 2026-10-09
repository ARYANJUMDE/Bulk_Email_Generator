"""
Integration tests for FastAPI application routes, status lifecycle, and certificate downloads.
"""

from uuid import UUID
from fastapi.testclient import TestClient
import pytest

from app.main import app, jobs
from app.models import CertificateStatus

client = TestClient(app)


class TestSystemEndpoints:
    """Tests for system and discovery endpoints."""

    def test_health_check_endpoint(self):
        """Test the health check endpoint returns 200 and healthy payload."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "running" in data["message"]

    def test_root_endpoint_metadata(self):
        """Test the root route returns application information and endpoint index."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Bulk Certificate Generator API"
        assert "/docs" in data["docs"]
        assert "generate" in data["endpoints"]
        assert "status" in data["endpoints"]


class TestGenerateCertificatesEndpoint:
    """Integration tests for the /api/v1/generate-certificates endpoint."""

    def test_post_generate_certificates_success_202(self):
        """Test submitting a valid batch of recipients returns HTTP 202 Accepted and job ID."""
        payload = {
            "recipients": [
                {"name": "Evelyn Reed", "email": "evelyn@example.com"},
                {"name": "Franklin Clark", "email": "franklin@example.com"},
            ],
            "course_name": "Full-Stack API Development with FastAPI",
            "issue_date": "2026-10-09",
            "organization": "Modern Web Academy",
        }
        response = client.post("/api/v1/generate-certificates", json=payload)
        assert response.status_code == 202
        data = response.json()

        assert "job_id" in data
        assert UUID(data["job_id"])  # Valid UUID
        assert data["total_recipients"] == 2
        assert data["status"] in [CertificateStatus.GENERATED, CertificateStatus.PENDING]
        assert data["job_id"] in jobs

    def test_post_generate_certificates_validation_error_on_empty_recipients(self):
        """Test submitting an empty recipient list triggers HTTP 422 Unprocessable Entity."""
        payload = {
            "recipients": [],
            "course_name": "Python Foundations",
        }
        response = client.post("/api/v1/generate-certificates", json=payload)
        assert response.status_code == 422

    def test_post_generate_certificates_validation_error_on_invalid_email(self):
        """Test submitting an invalid email address format triggers HTTP 422."""
        payload = {
            "recipients": [{"name": "Bad Email User", "email": "not-an-email"}],
            "course_name": "Python Foundations",
        }
        response = client.post("/api/v1/generate-certificates", json=payload)
        assert response.status_code == 422

    def test_post_generate_certificates_validation_error_on_missing_course_name(self):
        """Test submitting an empty course name triggers HTTP 422."""
        payload = {
            "recipients": [{"name": "Valid User", "email": "user@example.com"}],
            "course_name": "   ",
        }
        response = client.post("/api/v1/generate-certificates", json=payload)
        assert response.status_code == 422


class TestJobStatusEndpoint:
    """Integration tests for checking generation job status."""

    def test_get_status_nonexistent_job_returns_404(self):
        """Test querying an unknown job UUID returns HTTP 404 Not Found."""
        response = client.get("/api/v1/status/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404
        assert response.json()["detail"] == "Job not found"

    def test_get_status_existing_job_returns_detailed_progress(self):
        """Test querying an existing job returns progress counts and certificate URLs."""
        # 1. Create a generation job
        payload = {
            "recipients": [
                {"name": "Grace Hopper", "email": "grace@navy.mil"},
            ],
            "course_name": "Compiler Design & Architecture",
        }
        gen_response = client.post("/api/v1/generate-certificates", json=payload)
        job_id = gen_response.json()["job_id"]

        # 2. Check status
        status_response = client.get(f"/api/v1/status/{job_id}")
        assert status_response.status_code == 200
        data = status_response.json()

        assert data["job_id"] == job_id
        assert data["total"] == 1
        assert data["completed"] == 1
        assert data["failed"] == 0
        assert data["success_count"] == 1
        assert len(data["certificate_urls"]) == 1
        assert data["status"] == CertificateStatus.GENERATED


class TestCertificateDownloadEndpoint:
    """Integration tests for downloading generated certificate files."""

    def test_download_existing_certificate_pdf(self):
        """Test downloading a generated certificate returns valid PDF headers and body."""
        # Create a certificate first
        payload = {
            "recipients": [
                {"name": "Hannah Abbott", "email": "hannah@hogwarts.edu"},
            ],
            "course_name": "Herbology Advanced Studies",
        }
        gen_response = client.post("/api/v1/generate-certificates", json=payload)
        job_id = gen_response.json()["job_id"]

        status_response = client.get(f"/api/v1/status/{job_id}")
        cert_url = status_response.json()["certificate_urls"][0]
        filename = cert_url.split("/")[-1]

        # Download
        download_response = client.get(f"/api/v1/certificates/{filename}")
        assert download_response.status_code == 200
        assert download_response.headers.get("content-type") == "application/pdf"
        assert download_response.content.startswith(b"%PDF-")

    def test_download_nonexistent_certificate_returns_404(self):
        """Test downloading a non-existent certificate file returns HTTP 404."""
        response = client.get("/api/v1/certificates/non_existent_file_9999.pdf")
        assert response.status_code == 404
        assert response.json()["detail"] == "Certificate not found"

    def test_download_path_traversal_prevention(self):
        """Test that directory traversal attempts are safely handled."""
        response = client.get("/api/v1/certificates/..%2F..%2Frequirements.txt")
        assert response.status_code == 404