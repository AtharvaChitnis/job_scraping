const form = document.getElementById("upload-form");
const fileInput = document.getElementById("resume-file");
const dropzone = document.getElementById("dropzone");
const fileName = document.getElementById("file-name");
const parseButton = document.getElementById("parse-button");
const status = document.getElementById("status");
const results = document.getElementById("results");
const resultsEmpty = document.getElementById("results-empty");
const resultsBadge = document.getElementById("results-badge");

let selectedFile = null;

function setStatus(message, isError = false) {
  status.textContent = message;
  status.classList.toggle("error", isError);
}

function setSelectedFile(file) {
  selectedFile = file;
  fileName.textContent = file ? file.name : "No file selected";
  parseButton.disabled = !file;
}

function renderList(elementId, items) {
  const list = document.getElementById(elementId);
  list.innerHTML = "";

  if (!items || items.length === 0) {
    list.classList.add("empty");
    return;
  }

  list.classList.remove("empty");

  for (const item of items) {
    const li = document.createElement("li");
    li.textContent = item;
    list.appendChild(li);
  }
}

function showResults(data) {
  document.getElementById("result-name").textContent = data.name || "—";
  document.getElementById("result-email").textContent = data.email || "—";
  document.getElementById("result-phone").textContent = data.phone || "—";

  renderList("result-organizations", data.organizations);
  renderList("result-locations", data.locations);
  renderList("result-skills", data.skills);

  resultsEmpty.classList.add("hidden");
  results.classList.remove("hidden");
  resultsBadge.textContent = "Parsed";
  resultsBadge.classList.add("success");
}

dropzone.addEventListener("dragover", (event) => {
  event.preventDefault();
  dropzone.classList.add("dragover");
});

dropzone.addEventListener("dragleave", () => {
  dropzone.classList.remove("dragover");
});

dropzone.addEventListener("drop", (event) => {
  event.preventDefault();
  dropzone.classList.remove("dragover");

  const file = event.dataTransfer.files[0];
  if (!file || !file.name.toLowerCase().endsWith(".pdf")) {
    setStatus("Please drop a PDF file.", true);
    return;
  }

  setSelectedFile(file);
  setStatus(`Selected ${file.name}.`);
});

fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];
  if (!file) {
    setSelectedFile(null);
    return;
  }

  if (!file.name.toLowerCase().endsWith(".pdf")) {
    setSelectedFile(null);
    setStatus("Please choose a PDF file.", true);
    return;
  }

  setSelectedFile(file);
  setStatus(`Selected ${file.name}.`);
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  if (!selectedFile) {
    setStatus("Choose a PDF resume first.", true);
    return;
  }

  parseButton.disabled = true;
  setStatus("Parsing resume...");
  resultsBadge.textContent = "Processing";
  resultsBadge.classList.remove("success");

  const formData = new FormData();
  formData.append("file", selectedFile);

  try {
    const response = await fetch("/api/v1/parse", {
      method: "POST",
      body: formData,
    });

    const payload = await response.json();

    if (!response.ok) {
      throw new Error(payload.detail || "Failed to parse resume.");
    }

    showResults(payload);
    setStatus("Resume parsed successfully.");
  } catch (error) {
    setStatus(error.message, true);
    resultsBadge.textContent = "Error";
    resultsBadge.classList.remove("success");
  } finally {
    parseButton.disabled = !selectedFile;
  }
});
