const api = () => window.pywebview && window.pywebview.api;

let currentSceneId = null;
let currentUpdatedAt = null;

function setText(id, text) {
  document.getElementById(id).textContent = text || "";
}

function setWriteState(text) {
  setText("writeState", text);
}

function escapeHtml(value) {
  return String(value || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

async function callBridge(method, ...args) {
  if (!api()) {
    return { ok: false, error: { message: "pywebview bridge is unavailable" } };
  }
  return api()[method](...args);
}

function renderScenes(scenes) {
  const list = document.getElementById("sceneList");
  list.innerHTML = "";
  scenes.forEach((scene) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "scene-button";
    button.dataset.sceneId = scene.id;
    button.innerHTML = `<span>${escapeHtml(scene.title)}</span><span>${escapeHtml(scene.id)} · ${escapeHtml(scene.state)}</span>`;
    button.addEventListener("click", () => loadScene(scene.id));
    list.appendChild(button);
  });
}

function renderScene(scene) {
  currentSceneId = scene.id;
  currentUpdatedAt = scene.updated_at;
  setText("sceneId", scene.id);
  setText("sceneTitle", scene.title);
  setText("sceneStatus", `${scene.state}/${scene.status} · ${scene.updated_at}`);

  document.querySelectorAll(".scene-button").forEach((button) => {
    button.classList.toggle("active", button.dataset.sceneId === scene.id);
  });

  const thesis = document.getElementById("sceneThesis");
  thesis.innerHTML = Object.entries(scene.thesis || {}).map(([key, value]) => (
    `<div class="thesis-row"><div class="thesis-key">${escapeHtml(key)}</div><div>${escapeHtml(value)}</div></div>`
  )).join("");

  const layers = document.getElementById("screenplayLayers");
  layers.innerHTML = (scene.screenplay || []).map((layer) => (
    `<section class="layer"><h2>${escapeHtml(layer.name)}</h2><pre>${escapeHtml(layer.content)}</pre></section>`
  )).join("");

  const beats = document.getElementById("directorLayer");
  const rows = (scene.director_layer || []).map((beat) => (
    `<tr><td>${escapeHtml(beat.Beat)}</td><td>${escapeHtml(beat.Screenplay)}</td><td>${escapeHtml(beat["Director Intent"])}</td><td>${escapeHtml(beat.Performance)}</td></tr>`
  )).join("");
  beats.innerHTML = rows ? `<table><thead><tr><th>Beat</th><th>Screenplay</th><th>Intent</th><th>Performance</th></tr></thead><tbody>${rows}</tbody></table>` : "";

  const evidence = document.getElementById("evidenceList");
  evidence.innerHTML = (scene.evidence || []).map((item) => (
    `<div class="evidence-item">${escapeHtml(item.Tag)} · ${escapeHtml(item.Source)}<br>${escapeHtml(item.Entry)}</div>`
  )).join("");
}

async function loadScene(sceneId) {
  setWriteState("Loading scene...");
  const response = await callBridge("get_scene", sceneId);
  if (!response.ok) {
    setWriteState(response.error.message);
    return;
  }
  renderScene(response.data);
  setWriteState("Ready");
}

async function refresh() {
  setWriteState("Refreshing...");
  const response = await callBridge("get_workspace_summary");
  if (!response.ok) {
    setWriteState(response.error.message);
    return;
  }
  setText("workspacePath", response.data.workspace_root);
  renderScenes(response.data.scenes || []);
  if (response.data.default_scene_id) {
    await loadScene(response.data.default_scene_id);
  } else {
    setWriteState("No scenes found");
  }
}

async function submitDirection() {
  const text = document.getElementById("directionText").value;
  if (!currentSceneId) {
    setWriteState("No scene selected");
    return;
  }
  setWriteState("Recording...");
  const response = await callBridge(
    "submit_direction",
    currentSceneId,
    text,
    currentUpdatedAt,
  );
  if (!response.ok) {
    const data = response.data || {};
    if (response.error.code === "stale_update") {
      setWriteState(`Scene changed: expected ${data.expected_updated_at}, now ${data.actual_updated_at}`);
      await loadScene(currentSceneId);
      return;
    }
    setWriteState(response.error.message);
    return;
  }
  document.getElementById("directionText").value = "";
  renderScene(response.data.scene);
  setWriteState("Direction recorded");
}

async function renderSceneBoard() {
  setWriteState("Rendering Scene Board...");
  const response = await callBridge("render_scene_board");
  setWriteState(response.ok ? `Scene Board rendered: ${response.data.path}` : response.error.message);
}

let currentGateWorkDir = null;
let currentPendingGate = null;

function gateInput() {
  return document.getElementById("gateWorkDir").value.trim();
}

async function loadGateStatus(prefix) {
  const workDir = gateInput();
  if (!workDir) {
    setText("gateStatus", "Enter a work dir path first");
    return;
  }
  const response = await callBridge("gate_status", workDir);
  if (!response.ok) {
    setText("gateStatus", `${prefix ? prefix + " — " : ""}gate check failed: ${response.error.message}`);
    document.getElementById("gateActions").innerHTML = "";
    return;
  }
  renderGate(response.data, workDir, prefix);
}

function renderGate(gate, workDir, prefix) {
  currentGateWorkDir = workDir;
  currentPendingGate = gate.waiting ? gate.pending_gate : null;
  const actions = document.getElementById("gateActions");
  const note = prefix ? `${prefix} — ` : "";
  const onDisk = (gate.records && gate.records.length)
    ? ` | records on disk: ${gate.records.map(escapeHtml).join(", ")}`
    : "";
  if (!gate.waiting) {
    actions.innerHTML = "";
    setText("gateStatus", `${note}${gate.shot_id}: ${gate.status} @ ${gate.state}${onDisk}`);
    return;
  }
  setText("gateStatus", `${note}${gate.shot_id} waiting at ${gate.pending_gate} (retries: ${JSON.stringify(gate.retries)})${onDisk}`);
  actions.innerHTML = `
    <div class="direction-actions">
      <button id="approveGateButton" type="button">Approve ${escapeHtml(gate.pending_gate)}</button>
      <button id="denyGateButton" type="button">Deny</button>
      <input id="denyReasonInput" placeholder="Denial reason (optional)">
    </div>`;
  document.getElementById("approveGateButton").addEventListener("click", () => decideGate("approve"));
  document.getElementById("denyGateButton").addEventListener("click", () => decideGate("deny"));
}

async function decideGate(action) {
  if (!currentGateWorkDir || !currentPendingGate) {
    setText("gateStatus", "No pending gate");
    return;
  }
  let response;
  if (action === "approve") {
    response = await callBridge("approve_gate", currentGateWorkDir, currentPendingGate, "director");
  } else {
    const reason = document.getElementById("denyReasonInput").value.trim() || "unspecified";
    response = await callBridge("deny_gate", currentGateWorkDir, currentPendingGate, reason, "director");
  }
  if (!response.ok) {
    setText("gateStatus", `${action} rejected: ${response.error.message}`);
    return;
  }
  const noun = action === "approve" ? "Approval" : "Denial";
  await loadGateStatus(`${noun} recorded (${response.data.record}); a running pipeline consumes it`);
}

document.getElementById("refreshButton").addEventListener("click", refresh);
document.getElementById("sceneBoardButton").addEventListener("click", renderSceneBoard);
document.getElementById("submitDirectionButton").addEventListener("click", submitDirection);
document.getElementById("gateCheckButton").addEventListener("click", loadGateStatus);

window.addEventListener("pywebviewready", refresh);
if (!window.pywebview) {
  setWriteState("Waiting for pywebview bridge...");
}
