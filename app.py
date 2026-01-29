from flask import Flask, render_template, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import requests, json, uuid, time

app = Flask(__name__)
scheduler = BackgroundScheduler()
scheduler.start()

JOBS_FILE = "jobs.json"
jobs = {}

def save_jobs():
    with open(JOBS_FILE, "w") as f:
        json.dump(jobs, f, indent=2)

def load_jobs():
    global jobs
    try:
        with open(JOBS_FILE) as f:
            jobs = json.load(f)
    except:
        jobs = {}

load_jobs()

def ping_job(job_id):
    job = jobs.get(job_id)
    if not job:
        return
    try:
        r = requests.get(job["url"], timeout=10)
        job["last_status"] = r.status_code
        job["last_time"] = time.strftime("%H:%M:%S")
        job["fail_count"] = 0
    except:
        job["last_status"] = "ERROR"
        job["fail_count"] += 1
    save_jobs()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create", methods=["POST"])
def create():
    data = request.json
    job_id = str(uuid.uuid4())[:8]

    jobs[job_id] = {
        "url": data["url"],
        "interval": int(data["interval"]),
        "last_status": "N/A",
        "last_time": "-",
        "fail_count": 0
    }

    scheduler.add_job(
        ping_job,
        "interval",
        minutes=int(data["interval"]),
        id=job_id,
        args=[job_id]
    )

    save_jobs()
    return jsonify({"ok": True})

@app.route("/jobs")
def list_jobs():
    return jsonify(jobs)

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
