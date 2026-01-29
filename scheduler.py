import requests, json, time

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

def ping_job(job_id):
    jobs = load_jobs()
    job = jobs.get(job_id)
    if not job:
        return

    job["fail_count"] = job.get("fail_count", 0)

    try:
        r = requests.get(job["url"], timeout=10)
        job["last_status"] = r.status_code
        job["last_time"] = time.strftime("%H:%M:%S")
        job["fail_count"] = 0
    except:
        job["last_status"] = "ERROR"
        job["fail_count"] += 1

    jobs[job_id] = job
    save_jobs(jobs)
