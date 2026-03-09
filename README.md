# 🖥️ DevOps Monitoring API

A **production-ready REST API** for real-time system metrics monitoring, built with Python Flask and containerized with Docker.

> Part of a **6-stage DevOps platform** demonstrating the full software delivery lifecycle — from containerization to GitOps.

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | API overview & available endpoints |
| `/health` | GET | Health check with uptime & request count |
| `/metrics` | GET | CPU, RAM, disk & network metrics (JSON) |
| `/metrics/prometheus` | GET | Metrics in Prometheus exposition format |
| `/info` | GET | Server & OS information |
| `/processes` | GET | Top 5 processes by CPU usage |

### Example Responses

<details>
<summary><code>GET /health</code></summary>

```json
{
  "status": "healthy",
  "version": "1.1.0",
  "timestamp": "2026-03-09T21:40:15.911822",
  "uptime_seconds": 3842.17,
  "requests_served": 128
}
```
</details>

<details>
<summary><code>GET /metrics</code></summary>

```json
{
  "cpu_percent": 12.5,
  "cpu_count": 4,
  "memory": {
    "total_gb": 30.65,
    "used_gb": 12.82,
    "available_gb": 17.83,
    "percent": 41.8
  },
  "disk": {
    "total_gb": 386.43,
    "used_gb": 318.26,
    "free_gb": 68.17,
    "percent": 82.4
  },
  "network": {
    "bytes_sent": 1048576,
    "bytes_recv": 2097152
  }
}
```
</details>

---

## 🚀 Quick Start

### Docker (Recommended)

```bash
docker-compose up --build
```

The API will be available at `http://localhost:5000`

### Local Development

```bash
cd app
pip install -r requirements.txt
python app.py
```

---

## 🧪 Testing

```bash
pip install pytest
pytest tests/ -v
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| **Python 3.11** | Application runtime |
| **Flask** | REST API framework |
| **psutil** | System metrics collection |
| **Gunicorn** | Production WSGI server |
| **Docker** | Containerization |
| **Render** | Cloud deployment |

---

## 📁 Project Structure

```
devops-lab/
├── app/
│   ├── app.py              # Flask API application
│   └── requirements.txt    # Pinned Python dependencies
├── tests/
│   └── test_app.py         # Unit tests (pytest)
├── Dockerfile              # Multi-layer, non-root, healthcheck
├── docker-compose.yml      # Resource limits, logging, healthcheck
├── .dockerignore
└── README.md
```

---

## 🔒 Production Hardening

- ✅ Non-root container user
- ✅ Gunicorn WSGI server (not Flask dev server)
- ✅ Docker health checks
- ✅ Resource limits (CPU & memory)
- ✅ Structured JSON logging
- ✅ Error handling on all endpoints
- ✅ Prometheus-ready metrics export
- ✅ Pinned dependency versions

---

## 🌐 Live Demo

🔗 **[https://devops-lab-i12g.onrender.com](https://devops-lab-i12g.onrender.com)**

Try it:
```bash
curl https://devops-lab-i12g.onrender.com/health
curl https://devops-lab-i12g.onrender.com/metrics
curl https://devops-lab-i12g.onrender.com/metrics/prometheus
```

---

## 🗺️ Roadmap

| Stage | Focus | Status |
|---|---|---|
| **1** | App + Docker + Cloud Deploy | ✅ Complete |
| **2** | CI/CD Pipeline (GitHub Actions) | ⬜ Next |
| **3** | Monitoring & Alerting (Grafana) | ⬜ |
| **4** | Infrastructure as Code (Terraform) | ⬜ |
| **5** | Kubernetes (k3s, Helm) | ⬜ |
| **6** | GitOps (ArgoCD) | ⬜ |
