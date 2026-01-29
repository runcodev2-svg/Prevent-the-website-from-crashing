from flask import Flask, render_template, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import uuid, json
from scheduler import ping_job

app = Flask(__name__)
scheduler = BackgroundScheduler()
scheduler.start()

JOBS_FILE = "jobs.json"

def load_jobs():
    try:
        with open(JOBS_FILE) as f:
            return json.load(f)
    except:
        return {}

def save_jobs(jobs):
    with open(JOBS_FILE, "w") as f:
        json.dump(jobs, f, indent=2)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create", methods=["POST"])
def create():
    data = request.json
    jobs = load_jobs()

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
        args=[job_id],
        replace_existing=True
    )

    save_jobs(jobs)
    return jsonify({"ok": True})

@app.route("/jobs")
def jobs():
    return jsonify(load_jobs())

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
