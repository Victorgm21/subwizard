// ========================
//        TABS
// ========================

function switchTab(tab, btnElement) {
  document
    .querySelectorAll(".tab-content")
    .forEach((el) => el.classList.remove("active"));
  document
    .querySelectorAll(".tab-btn")
    .forEach((el) => el.classList.remove("active"));

  document.getElementById(`tab-${tab}`).classList.add("active");
  if (btnElement) {
    btnElement.classList.add("active");
  }

  if (tab === "settings") {
    loadConfig();
  }
}

// ========================
//        HOME
// ========================

async function selectInputFile() {
  const response = await window.pywebview.api.select_input_file();
  if (!response) return;

  document.getElementById("input-path").value = response.path;
  document.getElementById("input-info").innerText = "Mode: Single file";
  document.getElementById("input-info").style.color = "#98989d";

  // En modo archivo individual, sugerimos el nombre original + "_sub"
  const labelName = document.getElementById("label-output-filename");
  const inputName = document.getElementById("output-filename");
  labelName.innerText = "File name";
  inputName.placeholder = "Output file name";
  inputName.value = response.default_name ? `${response.default_name}_sub` : "subwizard";
}

async function selectInputFolder() {
  const response = await window.pywebview.api.select_input_folder();
  if (!response) return;

  document.getElementById("input-path").value = response.path;

  const infoEl = document.getElementById("input-info");
  if (response.count === 0) {
    infoEl.innerText = "Folder selected (0 video/audio files found in this folder)";
    infoEl.style.color = "#ff453a";
  } else {
    infoEl.innerText = `Mode: Folder batch (${response.count} media file(s) found)`;
    infoEl.style.color = "#30d158";
  }

  // En modo carpeta, cada archivo mantiene su nombre original + un sufijo opcional
  const labelName = document.getElementById("label-output-filename");
  const inputName = document.getElementById("output-filename");
  labelName.innerText = "Suffix (optional)";
  inputName.placeholder = "e.g. _sub (or leave empty)";
  inputName.value = "_sub";
}

async function selectFolder() {
  const response = await window.pywebview.api.select_output_folder();
  if (response) {
    document.getElementById("output-path").value = response;
  }
}

function updateProgressStatus(message, color = "#98989d") {
  const status = document.getElementById("status-text");
  if (status) {
    status.innerText = message;
    status.style.color = color;
  }
}

async function generateSubtitles() {
  const btn = document.getElementById("btn-generate");
  const status = document.getElementById("status-text");

  btn.disabled = true;
  status.innerText = "Starting...";
  status.style.color = "#ffd60a";

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

  try {
    const result = await window.pywebview.api.receive_form_data(data);
    status.innerText = result.message;
    status.style.color = result.ok ? "#30d158" : "#ff453a";
  } catch (e) {
    status.innerText = "Unexpected error occurred";
    status.style.color = "#ff453a";
  } finally {
    btn.disabled = false;
  }
}

// ========================
//       SETTINGS
// ========================

async function loadConfig() {
  const status = document.getElementById("status-settings");

  try {
    const cfg = await window.pywebview.api.get_config();
    const systemFonts = await window.pywebview.api.get_system_fonts();

    // Font (cargar fuentes del sistema en el select)
    const fontSelect = document.getElementById("cfg-font-family");
    fontSelect.innerHTML = "";

    if (cfg.font.family && !systemFonts.includes(cfg.font.family)) {
      systemFonts.unshift(cfg.font.family);
    }

    systemFonts.forEach((fontName) => {
      const opt = document.createElement("option");
      opt.value = fontName;
      opt.textContent = fontName;
      fontSelect.appendChild(opt);
    });

    fontSelect.value = cfg.font.family;
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
    status.style.color = "#30d158";
  } catch (e) {
    status.innerText = "Error loading settings";
    status.style.color = "#ff453a";
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
    status.style.color = "#30d158";
  } catch (e) {
    status.innerText = "Error saving settings";
    status.style.color = "#ff453a";
  }
}
