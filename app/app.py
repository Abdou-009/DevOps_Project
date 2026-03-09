from flask import Flask, jsonify
import psutil
import platform
import datetime

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.datetime.utcnow().isoformat()
    })

@app.route('/metrics')
def metrics():
    return jsonify({
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory": {
            "total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "used_gb": round(psutil.virtual_memory().used / (1024**3), 2),
            "percent": psutil.virtual_memory().percent
        },
        "disk": {
            "total_gb": round(psutil.disk_usage('/').total / (1024**3), 2),
            "used_gb": round(psutil.disk_usage('/').used / (1024**3), 2),
            "percent": psutil.disk_usage('/').percent
        }
    })

@app.route('/info')
def info():
    return jsonify({
        "os": platform.system(),
        "os_version": platform.version(),
        "python_version": platform.python_version(),
        "hostname": platform.node()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

