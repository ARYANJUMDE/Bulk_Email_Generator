"""
Embedded frontend dashboard for the Bulk Certificate Generator application.
"""

def get_dashboard_html() -> str:
    """Returns a standalone, modern, responsive HTML/JS/CSS dashboard interface."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>CertifyPro - Bulk Certificate Generator</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-base: #0B0F19;
      --bg-card: #111827;
      --bg-card-hover: #1E293B;
      --border-color: #1F2937;
      --border-focus: #4F46E5;
      --text-main: #F9FAFB;
      --text-muted: #9CA3AF;
      --primary: #4F46E5;
      --primary-hover: #4338CA;
      --primary-light: #EEF2FF;
      --accent: #F59E0B;
      --success: #10B981;
      --danger: #EF4444;
      --radius-lg: 16px;
      --radius-md: 10px;
      --radius-sm: 6px;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    body {
      background-color: var(--bg-base);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    /* Top Navigation */
    header {
      border-bottom: 1px solid var(--border-color);
      background: rgba(17, 24, 39, 0.85);
      backdrop-filter: blur(12px);
      position: sticky;
      top: 0;
      z-index: 50;
      padding: 16px 24px;
    }

    .nav-container {
      max-width: 1280px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
      font-weight: 800;
      font-size: 1.25rem;
      letter-spacing: -0.02em;
      color: #FFF;
      text-decoration: none;
    }

    .brand-badge {
      background: linear-gradient(135deg, #4F46E5, #9333EA);
      color: #fff;
      padding: 6px 10px;
      border-radius: var(--radius-sm);
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
    }

    .nav-links {
      display: flex;
      gap: 12px;
      align-items: center;
    }

    .btn-nav {
      color: var(--text-muted);
      text-decoration: none;
      font-size: 0.875rem;
      font-weight: 600;
      padding: 8px 14px;
      border-radius: var(--radius-sm);
      transition: all 0.2s;
      border: 1px solid transparent;
    }

    .btn-nav:hover {
      color: var(--text-main);
      background: var(--bg-card-hover);
      border-color: var(--border-color);
    }

    .btn-nav-primary {
      background: var(--primary);
      color: #fff;
      border-color: var(--primary);
    }

    .btn-nav-primary:hover {
      background: var(--primary-hover);
      color: #fff;
    }

    /* Main Container */
    main {
      flex: 1;
      max-width: 1280px;
      width: 100%;
      margin: 0 auto;
      padding: 32px 24px 64px;
    }

    /* Hero */
    .hero {
      text-align: center;
      margin-bottom: 36px;
    }

    .hero h1 {
      font-size: 2.25rem;
      font-weight: 800;
      letter-spacing: -0.03em;
      background: linear-gradient(135deg, #FFFFFF 0%, #A5B4FC 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 12px;
    }

    .hero p {
      color: var(--text-muted);
      font-size: 1.05rem;
      max-width: 680px;
      margin: 0 auto;
    }

    /* Tabs */
    .tabs-header {
      display: flex;
      justify-content: center;
      gap: 8px;
      margin-bottom: 28px;
    }

    .tab-btn {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      padding: 10px 22px;
      border-radius: 9999px;
      font-weight: 600;
      font-size: 0.925rem;
      cursor: pointer;
      transition: all 0.2s;
    }

    .tab-btn.active {
      background: var(--primary);
      color: #fff;
      border-color: var(--primary);
      box-shadow: 0 0 20px rgba(79, 70, 229, 0.4);
    }

    /* Card Panels */
    .card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      padding: 28px;
      margin-bottom: 28px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }

    .card-title {
      font-size: 1.25rem;
      font-weight: 700;
      margin-bottom: 18px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    /* Grid Form */
    .form-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }

    .form-group {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    label {
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--text-muted);
    }

    input, textarea {
      background: #0D1321;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      padding: 10px 14px;
      color: #fff;
      font-size: 0.95rem;
      outline: none;
      transition: border-color 0.2s;
    }

    input:focus, textarea:focus {
      border-color: var(--border-focus);
      box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.2);
    }

    /* Recipients Dynamic Table */
    .table-container {
      overflow-x: auto;
      margin-bottom: 20px;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
    }

    table {
      width: 100%;
      border-collapse: collapse;
      text-align: left;
    }

    th {
      background: #0D1321;
      padding: 12px 16px;
      font-size: 0.8rem;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      border-bottom: 1px solid var(--border-color);
    }

    td {
      padding: 10px 16px;
      border-bottom: 1px solid #1F2937;
    }

    td input {
      width: 100%;
    }

    .btn-action-row {
      background: transparent;
      border: none;
      color: var(--danger);
      cursor: pointer;
      font-weight: 700;
      font-size: 1.1rem;
      padding: 4px 8px;
      border-radius: var(--radius-sm);
    }

    .btn-action-row:hover {
      background: rgba(239, 68, 68, 0.1);
    }

    /* Action Toolbar */
    .toolbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
      margin-bottom: 20px;
    }

    .btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 10px 20px;
      border-radius: var(--radius-sm);
      font-weight: 600;
      font-size: 0.925rem;
      cursor: pointer;
      border: 1px solid transparent;
      transition: all 0.2s;
    }

    .btn-secondary {
      background: #1F2937;
      color: var(--text-main);
      border-color: var(--border-color);
    }

    .btn-secondary:hover {
      background: #374151;
    }

    .btn-primary-large {
      background: linear-gradient(135deg, #4F46E5, #6366F1);
      color: #fff;
      font-size: 1rem;
      font-weight: 700;
      padding: 14px 28px;
      border-radius: var(--radius-md);
      box-shadow: 0 4px 20px rgba(79, 70, 229, 0.4);
    }

    .btn-primary-large:hover {
      opacity: 0.95;
      transform: translateY(-1px);
    }

    .btn-primary-large:disabled {
      opacity: 0.5;
      cursor: not-allowed;
      transform: none;
    }

    /* Status Result Card */
    .result-card {
      background: #0D1321;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 20px;
      margin-top: 24px;
      display: none;
    }

    .result-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 16px;
    }

    .badge-status {
      padding: 4px 12px;
      border-radius: 9999px;
      font-size: 0.8rem;
      font-weight: 700;
      text-transform: uppercase;
    }

    .badge-generated {
      background: rgba(16, 185, 129, 0.15);
      color: #34D399;
      border: 1px solid rgba(16, 185, 129, 0.3);
    }

    .badge-failed {
      background: rgba(239, 68, 68, 0.15);
      color: #F87171;
      border: 1px solid rgba(239, 68, 68, 0.3);
    }

    .links-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
      gap: 12px;
      margin-top: 14px;
    }

    .cert-link-btn {
      background: #1E293B;
      border: 1px solid #334155;
      color: #E2E8F0;
      padding: 10px 14px;
      border-radius: var(--radius-sm);
      text-decoration: none;
      font-size: 0.85rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      justify-content: space-between;
      transition: all 0.2s;
    }

    .cert-link-btn:hover {
      background: #334155;
      border-color: var(--primary);
      color: #fff;
    }

    /* Explorer Gallery */
    .search-box {
      width: 100%;
      margin-bottom: 20px;
    }

    .cert-card-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 16px;
    }

    .cert-item-card {
      background: #0D1321;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 18px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.2s;
    }

    .cert-item-card:hover {
      border-color: #4F46E5;
      transform: translateY(-2px);
    }

    .cert-name {
      font-weight: 700;
      font-size: 1rem;
      color: #F8FAFC;
      margin-bottom: 4px;
    }

    .cert-meta {
      font-size: 0.8rem;
      color: var(--text-muted);
      margin-bottom: 14px;
    }

    .cert-card-actions {
      display: flex;
      gap: 8px;
    }

    .btn-download {
      flex: 1;
      text-align: center;
      background: var(--primary);
      color: #fff;
      padding: 8px 12px;
      border-radius: var(--radius-sm);
      text-decoration: none;
      font-size: 0.85rem;
      font-weight: 600;
      transition: background 0.2s;
    }

    .btn-download:hover {
      background: var(--primary-hover);
    }

    .btn-preview {
      background: #1F2937;
      color: var(--text-main);
      padding: 8px 12px;
      border-radius: var(--radius-sm);
      text-decoration: none;
      font-size: 0.85rem;
      font-weight: 600;
    }

    .btn-preview:hover {
      background: #374151;
    }

    footer {
      border-top: 1px solid var(--border-color);
      padding: 24px;
      text-align: center;
      color: var(--text-muted);
      font-size: 0.85rem;
    }
  </style>
</head>
<body>

  <!-- Header -->
  <header>
    <div class="nav-container">
      <a href="/" class="brand">
        <span>📜 CertifyPro</span>
        <span class="brand-badge">Bulk Engine</span>
      </a>
      <div class="nav-links">
        <a href="/docs" target="_blank" class="btn-nav">⚡ Swagger API Docs</a>
        <a href="/redoc" target="_blank" class="btn-nav">📖 ReDoc</a>
        <a href="/api/v1/health" target="_blank" class="btn-nav">🟢 Health</a>
      </div>
    </div>
  </header>

  <!-- Main -->
  <main>
    <section class="hero">
      <h1>Bulk Certificate Generator</h1>
      <p>High-fidelity, award-grade PDF certificate generation engine with status tracking, failure isolation, and instant downloads.</p>
    </section>

    <!-- Tabs Header -->
    <div class="tabs-header">
      <button class="tab-btn active" id="tab-gen" onclick="switchTab('gen')">🚀 Generate Certificates</button>
      <button class="tab-btn" id="tab-repo" onclick="switchTab('repo')">📁 Repository (<span id="repo-count">30</span>)</button>
    </div>

    <!-- TAB 1: Generator Form -->
    <section id="panel-gen" class="card">
      <div class="card-title">
        <span>Course & Program Details</span>
        <button class="btn btn-secondary" onclick="loadSampleData()">✨ Load 5 Sample Recipients</button>
      </div>

      <div class="form-grid">
        <div class="form-group">
          <label>Course / Program Name *</label>
          <input type="text" id="course_name" placeholder="e.g. Advanced Cloud Architecture Masterclass" value="Advanced Full-Stack Engineering & AI Systems" />
        </div>
        <div class="form-group">
          <label>Issuing Organization</label>
          <input type="text" id="organization" placeholder="e.g. Global Tech Institute" value="Global Academy of Technology & AI" />
        </div>
        <div class="form-group">
          <label>Issue Date</label>
          <input type="text" id="issue_date" placeholder="e.g. October 9, 2026" value="October 9, 2026" />
        </div>
      </div>

      <div class="toolbar">
        <label style="font-size: 1rem; font-weight: 700; color: #FFF;">Recipient List (<span id="rec-count">2</span>)</label>
        <div style="display: flex; gap: 8px;">
          <button class="btn btn-secondary" onclick="addRecipientRow()">+ Add Row</button>
          <button class="btn btn-secondary" onclick="clearRecipients()">Clear All</button>
        </div>
      </div>

      <!-- Recipients Table -->
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th style="width: 35%;">Full Name *</th>
              <th style="width: 35%;">Email Address *</th>
              <th style="width: 20%;">Custom Cert ID (Optional)</th>
              <th style="width: 10%; text-align: center;">Action</th>
            </tr>
          </thead>
          <tbody id="recipients-body">
            <tr>
              <td><input type="text" class="rec-name" placeholder="e.g. Alice Walker" value="Alice Walker" /></td>
              <td><input type="email" class="rec-email" placeholder="alice@example.com" value="alice.walker@example.com" /></td>
              <td><input type="text" class="rec-id" placeholder="Auto-generated" value="CERT-2026-001" /></td>
              <td style="text-align: center;"><button class="btn-action-row" onclick="removeRow(this)">✕</button></td>
            </tr>
            <tr>
              <td><input type="text" class="rec-name" placeholder="e.g. Bob Martin" value="Benjamin Hayes" /></td>
              <td><input type="email" class="rec-email" placeholder="bob@example.com" value="ben.hayes@example.org" /></td>
              <td><input type="text" class="rec-id" placeholder="Auto-generated" value="CERT-2026-002" /></td>
              <td style="text-align: center;"><button class="btn-action-row" onclick="removeRow(this)">✕</button></td>
            </tr>
          </tbody>
        </table>
      </div>

      <div style="text-align: right;">
        <button id="btn-submit" class="btn btn-primary-large" onclick="submitGeneration()">
          ⚡ Generate Bulk Certificates
        </button>
      </div>

      <!-- Result Card -->
      <div id="result-card" class="result-card">
        <div class="result-header">
          <div>
            <h3 style="font-size: 1.1rem; font-weight: 700; color: #FFF; margin-bottom: 4px;">Generation Completed</h3>
            <p style="font-size: 0.85rem; color: var(--text-muted);">Job ID: <code id="res-job-id" style="color: #A5B4FC;"></code></p>
          </div>
          <span id="res-status-badge" class="badge-status badge-generated">Generated</span>
        </div>

        <div style="display: flex; gap: 20px; font-size: 0.9rem; color: #E2E8F0; margin-bottom: 12px;">
          <div><b>Total:</b> <span id="res-total">0</span></div>
          <div><b>Success:</b> <span id="res-success" style="color: #34D399;">0</span></div>
          <div><b>Failed:</b> <span id="res-failed" style="color: #F87171;">0</span></div>
        </div>

        <div id="res-links" class="links-grid"></div>
      </div>
    </section>

    <!-- TAB 2: Repository Explorer -->
    <section id="panel-repo" class="card" style="display: none;">
      <div class="card-title">
        <span>Available Generated Certificates</span>
        <button class="btn btn-secondary" onclick="loadRepository()">🔄 Refresh Repository</button>
      </div>

      <input type="text" id="repo-search" class="search-box" placeholder="🔍 Search certificates by filename or recipient..." oninput="filterRepository()" />

      <div id="repo-grid" class="cert-card-grid"></div>
    </section>
  </main>

  <footer>
    <p>CertifyPro Bulk Certificate Generator • FastAPI & ReportLab Engine • <a href="/docs" style="color: #818CF8; text-decoration: none;">Interactive OpenAPI Specification</a></p>
  </footer>

  <script>
    let repoData = [];

    function switchTab(tab) {
      document.getElementById('tab-gen').classList.toggle('active', tab === 'gen');
      document.getElementById('tab-repo').classList.toggle('active', tab === 'repo');
      document.getElementById('panel-gen').style.display = tab === 'gen' ? 'block' : 'none';
      document.getElementById('panel-repo').style.display = tab === 'repo' ? 'block' : 'none';
      if (tab === 'repo') {
        loadRepository();
      }
    }

    function updateRecCount() {
      const rows = document.querySelectorAll('#recipients-body tr');
      document.getElementById('rec-count').textContent = rows.length;
    }

    function addRecipientRow(name = '', email = '', id = '') {
      const tbody = document.getElementById('recipients-body');
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><input type="text" class="rec-name" placeholder="Full Name" value="${name}" /></td>
        <td><input type="email" class="rec-email" placeholder="Email Address" value="${email}" /></td>
        <td><input type="text" class="rec-id" placeholder="Optional Cert ID" value="${id}" /></td>
        <td style="text-align: center;"><button class="btn-action-row" onclick="removeRow(this)">✕</button></td>
      `;
      tbody.appendChild(tr);
      updateRecCount();
    }

    function removeRow(btn) {
      btn.closest('tr').remove();
      updateRecCount();
    }

    function clearRecipients() {
      document.getElementById('recipients-body').innerHTML = '';
      updateRecCount();
    }

    function loadSampleData() {
      clearRecipients();
      const samples = [
        { name: "Sophia Martinez", email: "sophia.m@example.com", id: "CERT-2026-101" },
        { name: "Liam O'Connor", email: "liam.oc@example.ie", id: "CERT-2026-102" },
        { name: "Mei-Ling Zhang", email: "mei.zhang@example.cn", id: "CERT-2026-103" },
        { name: "Noah Al-Mansoor", email: "noah.am@example.ae", id: "CERT-2026-104" },
        { name: "Charlotte Dubois", email: "c.dubois@example.fr", id: "CERT-2026-105" }
      ];
      samples.forEach(s => addRecipientRow(s.name, s.email, s.id));
    }

    async function submitGeneration() {
      const course_name = document.getElementById('course_name').value.trim();
      const organization = document.getElementById('organization').value.trim();
      const issue_date = document.getElementById('issue_date').value.trim();

      if (!course_name) {
        alert("Please enter a course name.");
        return;
      }

      const rows = document.querySelectorAll('#recipients-body tr');
      const recipients = [];

      rows.forEach(r => {
        const name = r.querySelector('.rec-name').value.trim();
        const email = r.querySelector('.rec-email').value.trim();
        const cert_id = r.querySelector('.rec-id').value.trim();
        if (name && email) {
          const rec = { name, email };
          if (cert_id) rec.certificate_id = cert_id;
          recipients.push(rec);
        }
      });

      if (recipients.length === 0) {
        alert("Please add at least one valid recipient with name and email.");
        return;
      }

      const btn = document.getElementById('btn-submit');
      btn.disabled = true;
      btn.textContent = "⏳ Generating Certificates...";

      try {
        const payload = { recipients, course_name, organization, issue_date };
        const res = await fetch('/api/v1/generate-certificates', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Generation failed");

        // Fetch final status
        const statusRes = await fetch(`/api/v1/status/${data.job_id}`);
        const statusData = await statusRes.json();

        // Display results
        document.getElementById('result-card').style.display = 'block';
        document.getElementById('res-job-id').textContent = statusData.job_id;
        document.getElementById('res-total').textContent = statusData.total;
        document.getElementById('res-success').textContent = statusData.success_count;
        document.getElementById('res-failed').textContent = statusData.failed;

        const linksContainer = document.getElementById('res-links');
        linksContainer.innerHTML = '';

        statusData.certificate_urls.forEach(url => {
          const filename = url.split('/').pop();
          const cleanLabel = filename.replace('.pdf', '').replace(/^[a-f0-9-]+_/, '').replace(/_/g, ' ');
          const a = document.createElement('a');
          a.href = url;
          a.target = '_blank';
          a.className = 'cert-link-btn';
          a.innerHTML = `<span>📄 ${cleanLabel}</span> <span>⬇️ PDF</span>`;
          linksContainer.appendChild(a);
        });

      } catch (err) {
        alert("Error: " + err.message);
      } finally {
        btn.disabled = false;
        btn.textContent = "⚡ Generate Bulk Certificates";
      }
    }

    async function loadRepository() {
      try {
        const res = await fetch('/api/v1/certificates');
        const data = await res.json();
        repoData = data.certificates || [];
        document.getElementById('repo-count').textContent = repoData.length;
        renderRepository(repoData);
      } catch (err) {
        console.error("Failed to load certificates:", err);
      }
    }

    function renderRepository(certs) {
      const grid = document.getElementById('repo-grid');
      grid.innerHTML = '';

      if (certs.length === 0) {
        grid.innerHTML = '<p style="color: var(--text-muted); grid-column: 1/-1;">No certificates found in repository.</p>';
        return;
      }

      certs.forEach(c => {
        const cleanName = c.filename.replace('.pdf', '').replace(/^[a-f0-9-]+_/, '').replace(/_/g, ' ');
        const kbSize = (c.size_bytes / 1024).toFixed(1);
        const card = document.createElement('div');
        card.className = 'cert-item-card';
        card.innerHTML = `
          <div>
            <div class="cert-name">📄 ${cleanName}</div>
            <div class="cert-meta">${c.filename} • ${kbSize} KB</div>
          </div>
          <div class="cert-card-actions">
            <a href="${c.url}" download="${c.filename}" class="btn-download">Download</a>
            <a href="${c.url}" target="_blank" class="btn-preview">Preview</a>
          </div>
        `;
        grid.appendChild(card);
      });
    }

    function filterRepository() {
      const query = document.getElementById('repo-search').value.toLowerCase();
      const filtered = repoData.filter(c => c.filename.toLowerCase().includes(query));
      renderRepository(filtered);
    }

    // Initialize
    loadRepository();
  </script>
</body>
</html>
"""
