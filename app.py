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

@app.route("/delete/<job_id>", methods=["POST"])
def delete(job_id):
    jobs = load_jobs()
    if job_id in jobs:
        jobs.pop(job_id)
        try:
            scheduler.remove_job(job_id)
        except:
            pass
        save_jobs(jobs)
        return jsonify({"ok": True})
    return jsonify({"ok": False}), 404

@app.route("/edit/<job_id>", methods=["POST"])
def edit(job_id):
    data = request.json
    jobs = load_jobs()

    if job_id not in jobs:
        return jsonify({"ok": False}), 404

    jobs[job_id]["url"] = data["url"]
    jobs[job_id]["interval"] = int(data["interval"])

    try:
        scheduler.remove_job(job_id)
    except:
        pass

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

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
