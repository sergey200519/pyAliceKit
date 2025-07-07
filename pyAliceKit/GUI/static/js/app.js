// static/app.js
const form = document.getElementById("settingsForm");
const saveBtn = document.getElementById("saveBtn");

function fetchSettings() {
  fetch("/api/settings")
    .then(res => res.json())
    .then(data => {
      form.innerHTML = "";
      Object.entries(data).forEach(([key, value]) => {
        const input = document.createElement("input");
        input.name = key;
        input.value = value.replace(/^"|"$/g, "");
        input.placeholder = key;
        form.appendChild(input);
      });
    });
}

saveBtn.addEventListener("click", () => {
  const formData = new FormData(form);
  const settings = {};
  for (let [key, value] of formData.entries()) {
    settings[key] = value;
  }
  fetch("/api/settings", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(settings),
  }).then(() => alert("Настройки сохранены"));
});

fetchSettings();
