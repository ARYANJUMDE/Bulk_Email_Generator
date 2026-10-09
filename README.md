# Bulk Certificate Generator & Management Platform

A modern, high-performance FastAPI-based backend and interactive web platform for bulk certificate generation. This application accepts lists of recipients and renders elegant, award-grade landscape PDF certificates in bulk with robust input validation, real-time status tracking, failure isolation, and an embedded web dashboard.

---

## Features

- **Interactive Web Dashboard**: Built-in modern web UI at `/` for creating batches, loading sample data, tracking generation progress, and exploring stored certificates.
- **Bulk Certificate Generation**: Submit recipient lists via REST API (`POST /api/v1/generate-certificates`) or through the web dashboard.
- **Award-Grade Landscape Certificates**: High-fidelity vector PDF layout built with ReportLab featuring gold and navy dual borders, geometric corner flourishes, elegant typography hierarchy, official certification seal badge, and authorized signature block.
- **Strict Input Validation**: Validates recipient names and email address formats using Pydantic v2 schemas.
- **Status & Progress Tracking**: Track generation status, metrics (total, success, failed), and retrieve download links via unique Job UUIDs (`GET /api/v1/status/{job_id}`).
- **Graceful Failure Isolation**: Individual recipient generation errors do not halt or crash the rest of the batch.
- **Secure Certificate Retrieval**: Dedicated endpoints to list and download generated certificates with path traversal protection.
- **Clean Modular Architecture**: Clear separation of concerns across models, storage repository, routes, UI templates, and PDF rendering utilities.

---

## Technology Stack

- **Web Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Asynchronous Python API framework)
- **ASGI Server**: [Uvicorn](https://www.uvicorn.org/) (High-performance ASGI server)
- **PDF Generation Engine**: [ReportLab](https://www.reportlab.com/) (Vector graphics, typography & canvas layout)
- **Data Validation**: [Pydantic v2](https://docs.pydantic.dev/)
- **Testing Suite**: [Pytest](https://pytest.org/) & [HTTPX](https://www.python-httpx.org/) (`TestClient`)

---

## Project Structure

```
d:/Project/
├── app/
│   ├── __init__.py        # Package initialization, exports FastAPI app
│   ├── main.py            # FastAPI application instance, UI serving & root routing
│   ├── models.py          # Pydantic data schemas, validation models, and constants
│   ├── routes.py          # API route definitions (/api/v1/...)
│   ├── storage.py         # Job state repository and storage operations
│   ├── ui.py              # Modern embedded frontend Web Dashboard (HTML/CSS/JS)
│   └── utils.py           # ReportLab PDF rendering, filename sanitization & validators
├── tests/
│   ├── conftest.py        # Pytest fixtures and test environment isolation
│   ├── test_models.py     # Unit tests for Pydantic models & validation logic
│   ├── test_generation.py # Unit & batch tests for ReportLab PDF rendering & error isolation
│   └── test_app.py        # Integration tests for API endpoints & download security
├── generated_certificates/ # Directory storing generated certificate PDF files
├── pytest.ini             # Pytest configuration and marker definitions
├── requirements.txt       # Python project dependencies
├── .gitignore             # Git ignore configuration
└── README.md              # Project documentation
```

---

## Installation & Setup

1. **Clone the repository** and navigate to the project directory:
   ```bash
   git clone https://github.com/ARYANJUMDE/Bulk_Email_Generator.git
   cd Bulk_Email_Generator
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the test suite** (36 unique tests):
   ```bash
   pytest
   ```

4. **Start the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

---

## Accessing the Application

Once running, access the services via your browser or HTTP client:
* **Interactive Web Dashboard**: `http://127.0.0.1:8000/`
* **Interactive Swagger API Documentation**: `http://127.0.0.1:8000/docs`
* **ReDoc Specification**: `http://127.0.0.1:8000/redoc`
* **Health Check**: `http://127.0.0.1:8000/api/v1/health`

---

## API Endpoints Reference

### 1. Submit Bulk Generation Request
**`POST /api/v1/generate-certificates`**

**Request Body:**
```json
{
  "recipients": [
    {"name": "Alice Walker", "email": "alice.walker@example.com", "certificate_id": "CERT-2026-001"},
    {"name": "Benjamin Hayes", "email": "ben.hayes@example.org", "certificate_id": "CERT-2026-002"}
  ],
  "course_name": "Full-Stack Cloud Architecture Masterclass",
  "issue_date": "October 9, 2026",
  "organization": "Global Tech Institute"
}
```

**Response (`HTTP 202 Accepted`):**
```json
{
  "job_id": "60e909a1-8d2b-47e2-8ea5-0c7f1a3f0190",
  "message": "Certificate generation job started for 2 recipients",
  "total_recipients": 2,
  "status": "generated"
}
```

---

### 2. Check Generation Job Status
**`GET /api/v1/status/{job_id}`**

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
    "/api/v1/certificates/CERT-2026-001_Alice_Walker.pdf",
    "/api/v1/certificates/CERT-2026-002_Benjamin_Hayes.pdf"
  ]
}
```

---

### 3. List All Available Certificates
**`GET /api/v1/certificates`**

Returns a list of all certificate PDF files stored in the repository.

**Response:**
```json
{
  "certificates": [
    {
      "filename": "CERT-2026-001_Alexander_Wright.pdf",
      "url": "/api/v1/certificates/CERT-2026-001_Alexander_Wright.pdf",
      "size_bytes": 2801
    }
  ],
  "count": 30
}
```

---

### 4. Download Certificate PDF
**`GET /api/v1/certificates/{filename}`**

Streams the specified certificate PDF file with `application/pdf` media headers.

---

### 5. Health Check
**`GET /api/v1/health`**

Returns service health status (`{"status": "healthy", "message": "Bulk Certificate Generator API is running"}`).

---

## Design & Security Highlights

1. **Award-Grade Visual Presentation**: Built using ReportLab's vector graphics in landscape letter format. Incorporates double border lines, gold corner accents, letter-spaced typography, gold divider line, verification badge, and signature block.
2. **Failure Isolation**: Generation executes inside isolated execution blocks per recipient. If one recipient fails, the error is recorded without blocking remaining certificates.
3. **OS-Safe File Sanitization**: Filenames are sanitized to prevent illegal filesystem characters across Windows and Unix environments.
4. **Path Traversal Protection**: Certificate download endpoints validate and sanitize target filenames to prevent directory traversal vulnerabilities.
5. **Test Isolation**: Automated tests execute in an isolated temporary directory via pytest fixtures, ensuring test runs never pollute the production repository.