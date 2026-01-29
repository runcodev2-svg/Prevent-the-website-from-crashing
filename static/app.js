async function load() {
  const res = await fetch("/jobs");
  const data = await res.json();
  const table = document.getElementById("table");

  table.innerHTML = `
    <tr>
      <th>URL</th><th>นาที</th><th>สถานะ</th>
      <th>ล่าสุด</th><th>ล้มเหลว</th>
    </tr>
  `;

  Object.values(data).forEach(j => {
    table.innerHTML += `
      <tr>
        <td>${j.url}</td>
        <td>${j.interval}</td>
        <td>${j.last_status}</td>
        <td>${j.last_time}</td>
        <td>${j.fail_count}</td>
      </tr>
    `;
  });
}

async function create() {
  await fetch("/create", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      url: document.getElementById("url").value,
      interval: document.getElementById("interval").value
    })
  });
  load();
}

setInterval(load, 3000);
load();
