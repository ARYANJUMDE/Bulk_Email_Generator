"""
Job storage and state management for the Bulk Certificate Generator.
"""
from typing import Dict, Optional
from app.models import CertificateRecord

# In-memory job repository (can be swapped with DB / Redis in production)
jobs: Dict[str, CertificateRecord] = {}


def get_job(job_id: str) -> Optional[CertificateRecord]:
    """Retrieve a certificate job record by ID."""
    return jobs.get(job_id)


def save_job(job: CertificateRecord) -> CertificateRecord:
    """Save or update a certificate job record."""
    jobs[job.id] = job
    return job
