// ========================
//        TABS
// ========================

function switchTab(tab) {
  document
    .querySelectorAll(".tab-content")
    .forEach((el) => el.classList.remove("active"));
  document
    .querySelectorAll(".tab-btn")
    .forEach((el) => el.classList.remove("active"));

  document.getElementById(`tab-${tab}`).classList.add("active");
  event.target.classList.add("active");

  if (tab === "settings") {
    loadConfig();
  }
}

// ========================
//        HOME
// ========================

async function selectInputFile() {
  const response = await window.pywebview.api.select_input_file();
  if (response) {
    document.getElementById("input-path").value = response;
  }
}

async function selectFolder() {
  const response = await window.pywebview.api.select_output_folder();
  if (response) {
    document.getElementById("output-path").value = response;
  }
}

async function generateSubtitles() {
  const btn = document.getElementById("btn-generate");
  const status = document.getElementById("status-text");

  btn.disabled = true;
  status.innerText = "Processing...";

  const data = {
    input_path: document.getElementById("input-path").value,
    output_path: document.getElementById("output-path").value,
    output_filename: document.getElementById("output-filename").value,
    words_per_line: document.getElementById("words-per-line").value,
    performance: document.getElementById("select-performance").value,
    output_format: document.getElementById("select-output-type").value,
    language: document.getElementById("select-language").value,
    sub_style: document.getElementById("select-sub-style").value,
  };

  const result = await window.pywebview.api.receive_form_data(data);

  status.innerText = result;
  btn.disabled = false;
}

// ========================
//       SETTINGS
// ========================

async function loadConfig() {
  const status = document.getElementById("status-settings");

  try {
    const cfg = await window.pywebview.api.get_config();

    // Font
    document.getElementById("cfg-font-family").value = cfg.font.family;
    document.getElementById("cfg-font-size").value = cfg.font.size;
    document.getElementById("cfg-font-bold").checked = cfg.font.bold;
    document.getElementById("cfg-font-italic").checked = cfg.font.italic;

    // Colors
    document.getElementById("cfg-color-text").value = cfg.colors.text;
    document.getElementById("cfg-color-highlight").value = cfg.colors.highlight;
    document.getElementById("cfg-color-outline").value = cfg.colors.outline;
    document.getElementById("cfg-color-background").value =
      cfg.colors.background;
    document.getElementById("cfg-bg-opacity").value =
      cfg.colors.background_opacity;

    // Position
    document.getElementById("cfg-alignment").value = cfg.position.alignment;
    document.getElementById("cfg-offset-y").value = cfg.position.offset_y;

    // Outline
    document.getElementById("cfg-outline-size").value = cfg.outline_size;

    // Word Pop
    document.getElementById("cfg-wordpop-scale").value =
      cfg.styles.word_pop.pop_scale;

    // Zoom In
    document.getElementById("cfg-zoomin-duration").value =
      cfg.styles.zoom_in.anim_duration;
    document.getElementById("cfg-zoomin-startscale").value =
      cfg.styles.zoom_in.start_scale;
    document.getElementById("cfg-zoomin-accel").value =
      cfg.styles.zoom_in.accel;

    status.innerText = "Settings loaded";
    status.style.color = "#4caf50";
  } catch (e) {
    status.innerText = "Error loading settings";
    status.style.color = "#e74c3c";
  }
}

async function saveConfig() {
  const status = document.getElementById("status-settings");

  const cfg = {
    font: {
      family: document.getElementById("cfg-font-family").value,
      size: parseInt(document.getElementById("cfg-font-size").value),
      bold: document.getElementById("cfg-font-bold").checked,
      italic: document.getElementById("cfg-font-italic").checked,
    },
    colors: {
      text: document.getElementById("cfg-color-text").value,
      highlight: document.getElementById("cfg-color-highlight").value,
      outline: document.getElementById("cfg-color-outline").value,
      background: document.getElementById("cfg-color-background").value,
      background_opacity: parseInt(
        document.getElementById("cfg-bg-opacity").value
      ),
    },
    outline_size: parseInt(document.getElementById("cfg-outline-size").value),
    position: {
      alignment: document.getElementById("cfg-alignment").value,
      offset_y: parseInt(document.getElementById("cfg-offset-y").value),
    },
    styles: {
      karaoke: {},
      word_pop: {
        pop_scale: parseInt(document.getElementById("cfg-wordpop-scale").value),
      },
      zoom_in: {
        anim_duration: parseInt(
          document.getElementById("cfg-zoomin-duration").value
        ),
        start_scale: parseInt(
          document.getElementById("cfg-zoomin-startscale").value
        ),
        accel: parseFloat(document.getElementById("cfg-zoomin-accel").value),
      },
    },
  };

  try {
    const result = await window.pywebview.api.save_config(cfg);
    status.innerText = result;
    status.style.color = "#4caf50";
  } catch (e) {
    status.innerText = "Error saving settings";
    status.style.color = "#e74c3c";
  }
}
