from flask import Flask, jsonify, request
import psutil
import platform
import datetime
import logging
import os

# ── App Setup ──────────────────────────────────────────────────────────────────
app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "1.1.0")
START_TIME = datetime.datetime.now(datetime.timezone.utc)

# Request counter
request_count = {"total": 0}

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@app.before_request
def count_requests():
    request_count["total"] += 1
    logger.info("%-6s %s", request.method, request.path)


# ── Helpers ────────────────────────────────────────────────────────────────────
def _uptime_seconds():
    return (datetime.datetime.now(datetime.timezone.utc) - START_TIME).total_seconds()


# ── Routes ─────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return jsonify({
        "service": "DevOps Monitoring API",
        "version": APP_VERSION,
        "endpoints": {
            "/health": "Application health check",
            "/metrics": "CPU, RAM, and disk metrics (JSON)",
            "/metrics/prometheus": "Metrics in Prometheus format",
            "/info": "Server information",
            "/processes": "Top 5 processes by CPU usage",
        },
        "documentation": "https://github.com/abdou-009/devops-lab",
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "version": APP_VERSION,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "uptime_seconds": round(_uptime_seconds(), 2),
        "requests_served": request_count["total"],
    })


@app.route("/metrics")
def metrics():
    try:
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        net = psutil.net_io_counters()

        return jsonify({
            "cpu_percent": cpu,
            "cpu_count": psutil.cpu_count(),
            "memory": {
                "total_gb": round(mem.total / (1024 ** 3), 2),
                "used_gb": round(mem.used / (1024 ** 3), 2),
                "available_gb": round(mem.available / (1024 ** 3), 2),
                "percent": mem.percent,
            },
            "disk": {
                "total_gb": round(disk.total / (1024 ** 3), 2),
                "used_gb": round(disk.used / (1024 ** 3), 2),
                "free_gb": round(disk.free / (1024 ** 3), 2),
                "percent": disk.percent,
            },
            "network": {
                "bytes_sent": net.bytes_sent,
                "bytes_recv": net.bytes_recv,
            },
        })
    except Exception as e:
        logger.error("Failed to collect metrics: %s", e)
        return jsonify({"error": "Unable to collect system metrics"}), 500


@app.route("/metrics/prometheus")
def metrics_prometheus():
    """Expose metrics in Prometheus text format — ready for Stage 3 Grafana."""
    try:
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage("/")

        lines = [
            "# HELP cpu_usage_percent Current CPU usage percentage",
            "# TYPE cpu_usage_percent gauge",
            f"cpu_usage_percent {cpu}",
            "",
            "# HELP memory_usage_bytes Memory usage in bytes",
            "# TYPE memory_usage_bytes gauge",
            f"memory_usage_bytes {mem.used}",
            "",
            "# HELP memory_total_bytes Total memory in bytes",
            "# TYPE memory_total_bytes gauge",
            f"memory_total_bytes {mem.total}",
            "",
            "# HELP disk_usage_bytes Disk usage in bytes",
            "# TYPE disk_usage_bytes gauge",
            f"disk_usage_bytes {disk.used}",
            "",
            "# HELP disk_total_bytes Total disk in bytes",
            "# TYPE disk_total_bytes gauge",
            f"disk_total_bytes {disk.total}",
            "",
            "# HELP app_uptime_seconds Application uptime in seconds",
            "# TYPE app_uptime_seconds gauge",
            f"app_uptime_seconds {round(_uptime_seconds(), 2)}",
            "",
            "# HELP app_requests_total Total requests served",
            "# TYPE app_requests_total counter",
            f"app_requests_total {request_count['total']}",
        ]
        return "\n".join(lines) + "\n", 200, {"Content-Type": "text/plain; charset=utf-8"}
    except Exception as e:
        logger.error("Failed to generate Prometheus metrics: %s", e)
        return "# error collecting metrics\n", 500, {"Content-Type": "text/plain; charset=utf-8"}


@app.route("/info")
def info():
    try:
        boot = datetime.datetime.fromtimestamp(
            psutil.boot_time(), tz=datetime.timezone.utc
        ).isoformat()
    except Exception:
        boot = "unknown"

    return jsonify({
        "os": platform.system(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
        "hostname": platform.node(),
        "boot_time": boot,
    })


@app.route("/processes")
def processes():
    """Return the top 5 processes by CPU usage."""
    try:
        procs = []
        for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
            try:
                procs.append(p.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        top = sorted(procs, key=lambda x: x.get("cpu_percent") or 0, reverse=True)[:5]
        return jsonify({"top_processes": top})
    except Exception as e:
        logger.error("Failed to list processes: %s", e)
        return jsonify({"error": "Unable to list processes"}), 500


# ── Error Handlers ─────────────────────────────────────────────────────────────
@app.errorhandler(404)
def not_found(_):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(_):
    return jsonify({"error": "Internal server error"}), 500


# ── Entrypoint ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    logger.info("Starting DevOps Monitoring API v%s", APP_VERSION)
    app.run(host="0.0.0.0", port=5000)
