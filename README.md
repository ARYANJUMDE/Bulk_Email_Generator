# Bulk Certificate Generator Backend

A modern, high-performance FastAPI-based backend for bulk certificate generation. This application accepts a list of recipients and renders elegant, award-grade landscape PDF certificates in bulk with robust input validation, status tracking, and failure isolation.

## Features

- **Bulk Certificate Generation**: Submit a list of recipients in a single API request.
- **Award-Grade Landscape Certificates**: High-fidelity PDF layout with ReportLab featuring gold and navy dual borders, geometric corner flourishes, elegant typography, official certification seal badge, and signature block.
- **Strict Input Validation**: Validates recipient names and email address formats using Pydantic v2.
- **Status & Progress Tracking**: Track generation status, success/failure counts, and retrieve certificate download links via unique Job UUIDs.
- **Graceful Failure Isolation**: Individual recipient generation failures do not block or halt remaining certificates in the batch.
- **Secure Certificate Retrieval**: Dedicated endpoint to download generated certificate PDFs with path traversal protection.
- **Clean Modular Architecture**: Clear separation of concerns across models, storage, routes, and PDF rendering utilities.

## Technology Stack

- **FastAPI**: Modern, asynchronous web framework for Python
- **ReportLab**: Vector PDF generation engine for high-resolution certificate rendering
- **Pydantic v2**: High-performance data validation and settings schemas
- **Uvicorn**: Lightning-fast ASGI web server
- **Pytest & HTTPX**: Testing suite for unit, generation, and API integration testing

## Project Structure

```
d:/Project/
├── app/
│   ├── __init__.py        # Package initialization, exports FastAPI app
│   ├── main.py            # Main FastAPI application instance and root routes
│   ├── models.py          # Pydantic schemas, validation models, and constants
│   ├── routes.py          # API route definitions (/api/v1/...)
│   ├── storage.py         # Job state repository and storage operations
│   └── utils.py           # ReportLab PDF rendering, filename sanitization & validators
├── tests/
│   ├── test_models.py     # Unit tests for Pydantic models & validation logic
│   ├── test_generation.py # Unit & batch tests for ReportLab PDF rendering & error isolation
│   └── test_app.py        # Integration tests for API endpoints & download security
├── generated_certificates/ # Directory storing generated certificate PDF files
├── pytest.ini             # Pytest configuration and marker definitions
├── requirements.txt       # Python project dependencies
└── README.md              # Project documentation
```

## Installation & Setup

1. **Clone the repository** and navigate to the project directory:
   ```bash
   cd d:/Project
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run tests**:
   ```bash
   pytest
   ```

4. **Start the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

The API and interactive Swagger documentation will be available at:
- **API Base URL**: `http://127.0.0.1:8000`
- **Interactive Swagger Docs**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

## API Endpoints

### 1. Generate Certificates
**POST** `/api/v1/generate-certificates`

Submit a bulk certificate generation request.

**Request Body:**
```json
{
  "recipients": [
    {"name": "Alice Walker", "email": "alice.walker@example.com"},
    {"name": "Bob Martin", "email": "bob.martin@example.org", "certificate_id": "CERT-2026-001"}
  ],
  "course_name": "Full-Stack Cloud Architecture Masterclass",
  "issue_date": "October 9, 2026",
  "organization": "Global Tech Institute"
}
```

**Response (HTTP 202 Accepted):**
```json
{
  "job_id": "60e909a1-8d2b-47e2-8ea5-0c7f1a3f0190",
  "message": "Certificate generation job started for 2 recipients",
  "total_recipients": 2,
  "status": "generated"
}
```

### 2. Check Generation Status
**GET** `/api/v1/status/{job_id}`

Check the progress, metrics, and download URLs for a given job.

**Response:**
```json
{
  "job_id": "60e909a1-8d2b-47e2-8ea5-0c7f1a3f0190",
  "status": "generated",
  "total": 2,
  "completed": 2,
  "failed": 0,
  "success_count": 2,
  "failed_recipients": [],
  "certificate_urls": [
    "/api/v1/certificates/60e909a1_Alice_Walker.pdf",
    "/api/v1/certificates/CERT-2026-001_Bob_Martin.pdf"
  ]
}
```

### 3. Download Certificate PDF
**GET** `/api/v1/certificates/{filename}`

Download a generated certificate PDF file.

### 4. Health Check
**GET** `/api/v1/health`

Returns system health status.

## Design Highlights

1. **Award-Grade Visual Presentation**: Built using ReportLab's vector graphics in landscape letter format. Incorporates double border lines, gold corner accents, letter-spaced typography, gold divider line, verification badge, and signature block.
2. **Failure Isolation**: Generation executes inside isolated execution blocks per recipient. If one recipient fails, the error is recorded without blocking remaining certificates.
3. **OS-Safe File Sanitization**: Filenames are sanitized to prevent illegal filesystem characters across Windows and Unix environments.
4. **Path Traversal Protection**: Certificate download endpoints validate and sanitize target filenames to prevent directory traversal vulnerabilities.