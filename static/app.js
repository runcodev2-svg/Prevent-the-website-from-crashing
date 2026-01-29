function createJob() {
  fetch("/create", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      url: document.getElementById("url").value,
      interval: document.getElementById("interval").value
    })
  }).then(() => loadJobs())
}

function deleteJob(id) {
  if (!confirm("ลบงานนี้?")) return
  fetch(`/delete/${id}`, { method: "POST" })
    .then(() => loadJobs())
}

function editJob(id, url, interval) {
  const newUrl = prompt("URL ใหม่", url)
  if (!newUrl) return
  const newInterval = prompt("นาทีใหม่", interval)
  if (!newInterval) return

  fetch(`/edit/${id}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url: newUrl, interval: newInterval })
  }).then(() => loadJobs())
}

function loadJobs() {
  fetch("/jobs")
    .then(r => r.json())
    .then(data => {
      let html = ""
      for (const id in data) {
        const j = data[id]
        html += `
        <div class="job">
          <b>${id}</b><br>
          ${j.url}<br>
          ทุก ${j.interval} นาที<br>
          สถานะ: ${j.last_status} (${j.last_time})<br>
          <button onclick="editJob('${id}','${j.url}',${j.interval})">✏️</button>
          <button onclick="deleteJob('${id}')">🗑</button>
        </div>`
      }
      document.getElementById("jobs").innerHTML = html
    })
}

loadJobs()
setInterval(loadJobs, 5000)
