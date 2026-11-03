// ========================
//     TRANSLATIONS (i18n)
// ========================

const I18N = {
  en: {
    brand_tag: "Videos Powered by AI",
    nav_generator: "Generator",
    nav_appearance: "Appearance",
    nav_banned: "Banned Words",
    nav_options: "Options",

    gen_title: "Subtitle Generator",
    gen_subtitle:
      "Transcribe and burn subtitles for a single file or a full folder",
    group_source: "Source",
    btn_select_file: "Select Media File",
    btn_select_file_sub: "Single video or audio",
    btn_select_folder: "Select Batch Folder",
    btn_select_folder_sub: "All media in folder",
    no_source_selected: "No file or folder selected yet",
    choose_source_hint: "Choose a file or folder above to start",
    mode_single_file: "Mode: Single media file",
    mode_folder_zero:
      "Folder selected (0 video/audio files found in this folder)",
    mode_folder_batch: "Mode: Folder batch ({count} media file(s) found)",

    group_destination: "Destination",
    btn_dest_folder: "Destination Folder",
    dest_folder_hint: "Auto-filled from source or click to browse...",
    lbl_output_filename: "Output file name",
    lbl_output_suffix: "Suffix (optional)",
    ph_output_filename: "Output file name",
    ph_output_suffix: "e.g. _sub (or leave empty)",

    group_transcription: "Transcription & Format",
    lbl_sub_style: "Subtitle style",
    tip_sub_style:
      "Choose the visual animation style: Simple (.srt classic lines), Karaoke (highlights spoken words), Word Pop (active word pops in size & color), or Zoom In (smooth entrance zoom).",
    lbl_output_format: "Output format",
    tip_output_format:
      "Only Video burns the subtitles directly into an .mp4 file. Only Subtitles exports just the .srt/.ass file. Both keeps the video and the subtitle file.",
    opt_only_video: "Only Video (.mp4)",
    opt_only_subs: "Only Subtitles (.srt / .ass)",
    opt_both_out: "Both (Video + Subtitles)",
    lbl_whisper_model: "Whisper model",
    tip_whisper_model:
      "Larger models offer higher transcription accuracy at the cost of processing speed and memory. 'Normal (Small)' is recommended for most videos.",
    opt_perf_efficient: "Efficient (Base)",
    opt_perf_normal: "Normal (Small)",
    opt_perf_detailed: "Detailed (Medium)",
    opt_perf_ultra: "Ultra-detailed (Large)",
    lbl_spoken_lang: "Spoken language",
    tip_spoken_lang:
      "Auto-detect identifies the language automatically. Selecting the language manually can slightly improve speed and accuracy on very short clips.",
    opt_lang_auto: "Auto-detect",
    lbl_words_per_line: "Words per line",
    tip_words_per_line:
      "Maximum number of words shown simultaneously in each subtitle phrase. Use 3–5 words for dynamic Shorts/Reels or 6–8 for horizontal videos.",
    lbl_vad_filter: "Anti-hallucination filter (VAD)",
    tip_vad_filter:
      "Voice Activity Detection (VAD) filters out silences and background music so Whisper doesn't invent phantom text. Disable only for songs, whispers, or ASMR.",

    status_ready: "Ready",
    status_starting: "Starting...",
    status_select_dest_first: "Please select a destination folder first.",
    btn_live_preview: "Live Preview",
    btn_open_output: "Open Output Folder",
    btn_generate: "Generate Subtitles",
    btn_save_changes: "Save Changes",

    app_title: "Appearance & Style Parameters",
    app_subtitle:
      "Customize typography, colors, alignment, and animation behavior",
    group_typography: "Typography",
    lbl_font_family: "Font family",
    lbl_font_size: "Font size (px)",
    lbl_bold: "Bold",
    lbl_italic: "Italic",
    lbl_uppercase: "Uppercase (ALL CAPS)",
    lbl_nopunct: "Remove punctuation",
    group_position: "Position",
    lbl_alignment: "Screen alignment",
    opt_align_bottom: "Bottom center",
    opt_align_middle: "Middle center",
    opt_align_top: "Top center",
    lbl_offset_y: "Vertical margin (px)",
    group_colors: "Colors & Outline",
    lbl_color_text: "Primary text",
    lbl_color_highlight: "Active word highlight",
    lbl_color_outline: "Outline color",
    lbl_outline_size: "Outline thickness",
    lbl_color_bg: "Shadow / Background",
    lbl_bg_opacity: "Background transparency (%)",
    group_animations: "Animation Parameters",
    lbl_wordpop_scale: "Word Pop — Scale (%)",
    lbl_zoomin_duration: "Zoom In — Duration (ms)",
    lbl_zoomin_startscale: "Zoom In — Initial scale (%)",
    lbl_zoomin_accel: "Zoom In — Acceleration",
    status_settings_loaded: "Settings loaded",
    status_settings_saved: "Settings saved successfully",

    ban_title: "Banned Words",
    ban_subtitle:
      "Words added here are censored with asterisks (***) in subtitles and a soft audio bleep in the video",
    group_audio_bleep: "Audio Bleep Censorship",
    lbl_beep_enabled: "Censor audio with soft beep",
    tip_beep_enabled:
      "When exporting video (.mp4), mutes the spoken banned word and plays a soft 750 Hz bleep tone over it.",
    lbl_beep_volume: "Beep volume",
    tip_beep_volume:
      "Adjust the loudness of the censor beep (0% = silent mute only, 35% = soft beep, 100% = loud bleep).",
    btn_test_beep: "Test Beep",
    group_add_banned: "Add Words to Censor",
    lbl_word_phrase: "Word or phrase",
    ph_banned_word: "Type word(s), separated by commas...",
    btn_add_word: "Add Word",
    ban_helper_text:
      'Matching is case-insensitive. Example: "badword" becomes "*******" in the subtitle text.',
    group_banned_list: "Banned Words List",
    btn_clear_all: "Clear All",
    ban_empty: "No banned words added yet.",
    ban_already_exists: "Word is already in the banned list",

    opt_title: "Program Options",
    opt_subtitle: "General preferences and interface language for SubWizard",
    group_general_options: "General",
    lbl_app_language: "Program language",
    window_title: "SubWizard — Videos Powered by AI",
    group_whisper_cache: "Installed Whisper Models",
    btn_open_cache_folder: "Open Cache Folder",
    btn_refresh: "Refresh",
    btn_delete_model: "Delete",
    loading_models: "Loading installed models...",
    no_models_found: "No Whisper models installed in cache yet.",
    confirm_delete_model:
      'Delete model "{name}" to free up {size}? (It will be re-downloaded if used again)',
    total_cache_size: "Total disk space:",
  },

  es: {
    brand_tag: "Videos Potenciados por IA",
    nav_generator: "Generador",
    nav_appearance: "Apariencia",
    nav_banned: "Palabras Baneadas",
    nav_options: "Opciones",

    gen_title: "Generador de Subtítulos",
    gen_subtitle:
      "Transcribe y quema subtítulos para un archivo individual o una carpeta entera",
    group_source: "Origen (Entrada)",
    btn_select_file: "Seleccionar Archivo",
    btn_select_file_sub: "Un video o audio",
    btn_select_folder: "Seleccionar Carpeta",
    btn_select_folder_sub: "Procesar carpeta en lote",
    no_source_selected: "Ningún archivo o carpeta seleccionado",
    choose_source_hint: "Elige un archivo o carpeta arriba para comenzar",
    mode_single_file: "Modo: Archivo individual",
    mode_folder_zero:
      "Carpeta seleccionada (0 archivos de video/audio encontrados)",
    mode_folder_batch:
      "Modo: Carpeta por lote ({count} archivo(s) encontrados)",

    group_destination: "Destino (Salida)",
    btn_dest_folder: "Carpeta de Destino",
    dest_folder_hint: "Se autocompleta con el origen o haz clic para elegir...",
    lbl_output_filename: "Nombre del archivo",
    lbl_output_suffix: "Sufijo (opcional)",
    ph_output_filename: "Nombre del archivo de salida",
    ph_output_suffix: "ej. _sub (o dejar vacío)",

    group_transcription: "Transcripción y Formato",
    lbl_sub_style: "Estilo de subtítulo",
    tip_sub_style:
      "Elige el estilo visual: Simple (líneas clásicas .srt), Karaoke (resalta la palabra hablada), Word Pop (la palabra activa salta en tamaño y color) o Zoom In (entrada suave con zoom).",
    lbl_output_format: "Formato de salida",
    tip_output_format:
      "Solo Video quema los subtítulos directamente en un archivo .mp4. Solo Subtítulos exporta únicamente el archivo .srt/.ass. Ambos conserva el video y el subtítulo.",
    opt_only_video: "Solo Video (.mp4)",
    opt_only_subs: "Solo Subtítulos (.srt / .ass)",
    opt_both_out: "Ambos (Video + Subtítulos)",
    lbl_whisper_model: "Modelo Whisper",
    tip_whisper_model:
      "Los modelos más grandes ofrecen mayor precisión a cambio de más tiempo de proceso y memoria. Se recomienda 'Normal (Small)' para la mayoría de videos.",
    opt_perf_efficient: "Eficiente (Base)",
    opt_perf_normal: "Normal (Small)",
    opt_perf_detailed: "Detallado (Medium)",
    opt_perf_ultra: "Ultra-detallado (Large)",
    lbl_spoken_lang: "Idioma hablado",
    tip_spoken_lang:
      "Auto-detectar identifica el idioma automáticamente. Elegir el idioma manualmente puede mejorar ligeramente la velocidad en clips muy cortos.",
    opt_lang_auto: "Auto-detectar",
    lbl_words_per_line: "Palabras por línea",
    tip_words_per_line:
      "Número máximo de palabras mostradas simultáneamente en cada frase. Usa 3–5 palabras para Shorts/Reels dinámicos o 6–8 para videos horizontales.",
    lbl_vad_filter: "Filtro anti-alucinaciones (VAD)",
    tip_vad_filter:
      "El detector de actividad de voz (VAD) filtra silencios y música de fondo para que Whisper no invente texto fantasma. Desactívalo solo para canciones, susurros o ASMR.",

    status_ready: "Listo",
    status_starting: "Iniciando...",
    status_select_dest_first:
      "Por favor selecciona primero una carpeta de destino.",
    btn_live_preview: "Vista Previa",
    btn_open_output: "Abrir Carpeta Salida",
    btn_generate: "Generar Subtítulos",
    btn_save_changes: "Guardar Cambios",

    app_title: "Apariencia y Parámetros de Estilo",
    app_subtitle:
      "Personaliza tipografía, colores, alineación y comportamiento de las animaciones",
    group_typography: "Tipografía",
    lbl_font_family: "Fuente",
    lbl_font_size: "Tamaño de fuente (px)",
    lbl_bold: "Negrita (Bold)",
    lbl_italic: "Cursiva (Italic)",
    lbl_uppercase: "Mayúsculas (ALL CAPS)",
    lbl_nopunct: "Eliminar signos de puntuación",
    group_position: "Posición",
    lbl_alignment: "Alineación en pantalla",
    opt_align_bottom: "Inferior centrada",
    opt_align_middle: "Centro de pantalla",
    opt_align_top: "Superior centrada",
    lbl_offset_y: "Margen vertical (px)",
    group_colors: "Colores y Contorno",
    lbl_color_text: "Texto principal",
    lbl_color_highlight: "Resaltado de palabra activa",
    lbl_color_outline: "Color de contorno",
    lbl_outline_size: "Grosor de contorno",
    lbl_color_bg: "Sombra / Fondo",
    lbl_bg_opacity: "Transparencia de fondo (%)",
    group_animations: "Parámetros de Animación",
    lbl_wordpop_scale: "Word Pop — Escala (%)",
    lbl_zoomin_duration: "Zoom In — Duración (ms)",
    lbl_zoomin_startscale: "Zoom In — Escala inicial (%)",
    lbl_zoomin_accel: "Zoom In — Aceleración",
    status_settings_loaded: "Ajustes cargados",
    status_settings_saved: "Ajustes guardados correctamente",

    ban_title: "Palabras Baneadas",
    ban_subtitle:
      "Las palabras añadidas aquí se censuran con asteriscos (***) en el texto y con un pitido suave en el video",
    group_audio_bleep: "Censura con Pitido de Audio",
    lbl_beep_enabled: "Censurar audio con pitido suave",
    tip_beep_enabled:
      "Al exportar video (.mp4), silencia la palabra baneada hablada y reproduce un pitido suave de 750 Hz sobre ella.",
    lbl_beep_volume: "Volumen del pitido",
    tip_beep_volume:
      "Ajusta el volumen del pitido de censura (0% = solo silenciar sin pitido, 35% = pitido suave, 100% = pitido fuerte).",
    btn_test_beep: "Probar Pitido",
    group_add_banned: "Añadir Palabras a Censurar",
    lbl_word_phrase: "Palabra o frase",
    ph_banned_word: "Escribe palabra(s), separadas por comas...",
    btn_add_word: "Añadir Palabra",
    ban_helper_text:
      'No distingue mayúsculas/minúsculas. Ejemplo: "palabra" pasa a ser "*******" en el subtítulo.',
    group_banned_list: "Lista de Palabras Baneadas",
    btn_clear_all: "Borrar Todo",
    ban_empty: "Aún no se han añadido palabras baneadas.",
    ban_already_exists: "La palabra ya está en la lista",

    opt_title: "Opciones del Programa",
    opt_subtitle: "Preferencias generales e idioma de la interfaz de SubWizard",
    group_general_options: "General",
    lbl_app_language: "Idioma del programa",
    window_title: "SubWizard — Videos Potenciados por IA",
    group_whisper_cache: "Modelos Whisper Instalados",
    btn_open_cache_folder: "Abrir Carpeta de Caché",
    btn_refresh: "Actualizar",
    btn_delete_model: "Borrar",
    loading_models: "Cargando modelos instalados...",
    no_models_found: "No hay modelos Whisper instalados en caché aún.",
    confirm_delete_model:
      '¿Eliminar el modelo "{name}" para liberar {size}? (Se volverá a descargar automáticamente si lo vuelves a usar)',
    total_cache_size: "Espacio total:",
  },
};

// ========================
//        STATE
// ========================

let currentLang = "en";
let settingsLoadedOnce = false;
let bannedWordsList = [];
let currentSourceMode = null; // 'file' | 'folder' | null

function t(key) {
  const dict = I18N[currentLang] || I18N.en;
  return dict[key] || I18N.en[key] || key;
}

function applyLanguage(lang) {
  currentLang = lang === "es" ? "es" : "en";
  document.documentElement.lang = currentLang;
  document.title = t("window_title");

  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    if (
      el.id === "input-path-display" &&
      document.getElementById("input-path").value
    ) {
      return;
    }
    if (
      el.id === "output-path-display" &&
      document.getElementById("output-path").value
    ) {
      return;
    }
    if (el.id === "label-output-filename" && currentSourceMode === "folder") {
      el.innerText = t("lbl_output_suffix");
      return;
    }
    el.innerText = t(key);
  });

  document.querySelectorAll("[data-i18n-tooltip]").forEach((el) => {
    const key = el.getAttribute("data-i18n-tooltip");
    el.setAttribute("data-tooltip", t(key));
  });

  document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
    const key = el.getAttribute("data-i18n-placeholder");
    if (el.id === "output-filename" && currentSourceMode === "folder") {
      el.placeholder = t("ph_output_suffix");
      return;
    }
    el.placeholder = t(key);
  });

  renderBannedWords();
}

async function onLanguageSelectChange(newLang) {
  applyLanguage(newLang);
  await saveConfig("options");
}

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

  if (!settingsLoadedOnce) {
    loadConfig();
  }

  if (tab === "options") {
    loadInstalledModels();
  }
}

// ========================
//        HOME
// ========================

function setOutputPath(folderPath) {
  document.getElementById("output-path").value = folderPath;
  const displayEl = document.getElementById("output-path-display");
  if (displayEl) {
    displayEl.innerText = folderPath;
    displayEl.style.color = "#ececef";
  }
  const destBtn = document.getElementById("btn-dest-folder");
  if (destBtn) {
    destBtn.classList.add("selected");
  }
}

async function selectInputFile() {
  const response = await window.pywebview.api.select_input_file();
  if (!response) return;

  currentSourceMode = "file";
  document.getElementById("input-path").value = response.path;
  const pathDisplay = document.getElementById("input-path-display");
  if (pathDisplay) {
    pathDisplay.innerText = response.path;
  }

  document.getElementById("btn-source-file")?.classList.add("selected");
  document.getElementById("btn-source-folder")?.classList.remove("selected");

  document.getElementById("input-info").innerText = t("mode_single_file");
  document.getElementById("input-info").style.color = "#30d158";

  if (response.folder) {
    setOutputPath(response.folder);
  }

  const labelName = document.getElementById("label-output-filename");
  const inputName = document.getElementById("output-filename");
  labelName.innerText = t("lbl_output_filename");
  inputName.placeholder = t("ph_output_filename");
  inputName.value = response.default_name
    ? `${response.default_name}_sub`
    : "subwizard";

  syncPreviewWindow();
}

async function selectInputFolder() {
  const response = await window.pywebview.api.select_input_folder();
  if (!response) return;

  currentSourceMode = "folder";
  document.getElementById("input-path").value = response.path;
  const pathDisplay = document.getElementById("input-path-display");
  if (pathDisplay) {
    pathDisplay.innerText = response.path;
  }

  document.getElementById("btn-source-folder")?.classList.add("selected");
  document.getElementById("btn-source-file")?.classList.remove("selected");

  if (response.folder || response.path) {
    setOutputPath(response.folder || response.path);
  }

  const infoEl = document.getElementById("input-info");
  if (response.count === 0) {
    infoEl.innerText = t("mode_folder_zero");
    infoEl.style.color = "#ff453a";
  } else {
    infoEl.innerText = t("mode_folder_batch").replace(
      "{count}",
      response.count
    );
    infoEl.style.color = "#30d158";
  }

  const labelName = document.getElementById("label-output-filename");
  const inputName = document.getElementById("output-filename");
  labelName.innerText = t("lbl_output_suffix");
  inputName.placeholder = t("ph_output_suffix");
  inputName.value = "_sub";

  syncPreviewWindow();
}

async function selectFolder() {
  const response = await window.pywebview.api.select_output_folder();
  if (response) {
    setOutputPath(response);
  }
}

async function openOutputFolder() {
  const outputPath = document.getElementById("output-path").value;
  const status = document.getElementById("status-text");

  if (!outputPath) {
    status.innerText = t("status_select_dest_first");
    status.style.color = "#ffd60a";
    return;
  }

  const res = await window.pywebview.api.open_output_folder(outputPath);
  if (res && !res.ok) {
    status.innerText = res.message || "Could not open folder.";
    status.style.color = "#ff453a";
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
  status.innerText = t("status_starting");
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
    vad_filter: document.getElementById("chk-vad-filter").checked,
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
//      LIVE PREVIEW
// ========================

function collectFormConfig() {
  const langSelect = document.getElementById("cfg-app-language");
  return {
    app_language: langSelect ? langSelect.value : currentLang,
    font: {
      family: document.getElementById("cfg-font-family").value || "Tahoma",
      size: parseInt(document.getElementById("cfg-font-size").value) || 68,
      bold: document.getElementById("cfg-font-bold").checked,
      italic: document.getElementById("cfg-font-italic").checked,
      uppercase: document.getElementById("cfg-font-uppercase").checked,
      remove_punctuation: document.getElementById("cfg-font-nopunct").checked,
    },
    colors: {
      text: document.getElementById("cfg-color-text").value || "#ffffff",
      highlight:
        document.getElementById("cfg-color-highlight").value || "#a855f7",
      outline: document.getElementById("cfg-color-outline").value || "#000000",
      background:
        document.getElementById("cfg-color-background").value || "#000000",
      background_opacity: parseInt(
        document.getElementById("cfg-bg-opacity").value ?? 100
      ),
    },
    outline_size:
      parseInt(document.getElementById("cfg-outline-size").value) || 0,
    position: {
      alignment:
        document.getElementById("cfg-alignment").value || "bottom_center",
      offset_y: parseInt(document.getElementById("cfg-offset-y").value) || 110,
    },
    styles: {
      karaoke: {},
      word_pop: {
        pop_scale:
          parseInt(document.getElementById("cfg-wordpop-scale").value) || 122,
      },
      zoom_in: {
        anim_duration:
          parseInt(document.getElementById("cfg-zoomin-duration").value) || 120,
        start_scale:
          parseInt(document.getElementById("cfg-zoomin-startscale").value) ||
          70,
        accel:
          parseFloat(document.getElementById("cfg-zoomin-accel").value) || 0.5,
      },
    },
    banned_words: [...bannedWordsList],
    banned_audio: {
      enabled: document.getElementById("cfg-beep-enabled")
        ? document.getElementById("cfg-beep-enabled").checked
        : true,
      volume: document.getElementById("cfg-beep-volume")
        ? parseInt(document.getElementById("cfg-beep-volume").value) || 0
        : 35,
    },
  };
}

async function openLivePreview() {
  const inputPath = document.getElementById("input-path").value;
  const subStyle = document.getElementById("select-sub-style").value;
  const wordsPerLine =
    parseInt(document.getElementById("words-per-line").value) || 5;
  const state = {
    input_path: inputPath,
    sub_style: subStyle,
    words_per_line: wordsPerLine,
    cfg: settingsLoadedOnce ? collectFormConfig() : null,
  };
  await window.pywebview.api.open_preview_window(state);
}

async function syncPreviewWindow() {
  if (!window.pywebview || !window.pywebview.api) return;
  const inputPath = document.getElementById("input-path").value;
  const subStyle = document.getElementById("select-sub-style").value;
  const wordsPerLine =
    parseInt(document.getElementById("words-per-line").value) || 5;
  const state = {
    input_path: inputPath,
    sub_style: subStyle,
    words_per_line: wordsPerLine,
    cfg: settingsLoadedOnce ? collectFormConfig() : null,
  };
  await window.pywebview.api.sync_preview_state(state);
}

document.addEventListener("DOMContentLoaded", () => {
  const watchedControls = document.querySelectorAll(
    "#tab-settings input, #tab-settings select, #select-sub-style, #words-per-line"
  );
  watchedControls.forEach((ctrl) => {
    ctrl.addEventListener("input", syncPreviewWindow);
    ctrl.addEventListener("change", syncPreviewWindow);
  });
});

window.addEventListener("pywebviewready", () => {
  loadConfig();
});

// ========================
//       SETTINGS
// ========================

async function loadConfig() {
  const status = document.getElementById("status-settings");

  try {
    const cfg = await window.pywebview.api.get_config();
    const systemFonts = await window.pywebview.api.get_system_fonts();

    // Language
    const appLang = cfg.app_language || "en";
    const langSelect = document.getElementById("cfg-app-language");
    if (langSelect) {
      langSelect.value = appLang;
    }
    applyLanguage(appLang);

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
    document.getElementById("cfg-font-bold").checked = !!cfg.font.bold;
    document.getElementById("cfg-font-italic").checked = !!cfg.font.italic;
    document.getElementById("cfg-font-uppercase").checked =
      !!cfg.font.uppercase;
    document.getElementById("cfg-font-nopunct").checked =
      !!cfg.font.remove_punctuation;

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

    // Banned Words & Audio Bleep
    bannedWordsList = Array.isArray(cfg.banned_words)
      ? cfg.banned_words
          .map((w) => String(w).trim().toLowerCase())
          .filter(Boolean)
      : [];
    renderBannedWords();

    const bannedAudio = cfg.banned_audio || {};
    const beepEnabledEl = document.getElementById("cfg-beep-enabled");
    const beepVolEl = document.getElementById("cfg-beep-volume");
    if (beepEnabledEl) {
      beepEnabledEl.checked = bannedAudio.enabled !== false;
    }
    if (beepVolEl) {
      const vol = bannedAudio.volume ?? 35;
      beepVolEl.value = vol;
      updateBeepVolumeLabel(vol);
    }

    settingsLoadedOnce = true;

    if (status) {
      status.innerText = t("status_settings_loaded");
      status.style.color = "#30d158";
    }
  } catch (e) {
    if (status) {
      status.innerText = "Error loading settings";
      status.style.color = "#ff453a";
    }
  }
}

function renderBannedWords() {
  const container = document.getElementById("banned-tags-container");
  const countMeta = document.getElementById("banned-count-meta");
  if (!container) return;

  if (countMeta) {
    countMeta.innerText = `(${bannedWordsList.length})`;
  }

  container.innerHTML = "";
  if (bannedWordsList.length === 0) {
    const emptySpan = document.createElement("span");
    emptySpan.className = "helper-text";
    emptySpan.textContent = t("ban_empty");
    container.appendChild(emptySpan);
    return;
  }

  bannedWordsList.forEach((word) => {
    const tag = document.createElement("span");
    tag.className = "banned-tag";

    const label = document.createElement("span");
    label.textContent = word;

    const removeBtn = document.createElement("button");
    removeBtn.type = "button";
    removeBtn.className = "banned-tag-remove";
    removeBtn.title = `× ${word}`;
    removeBtn.textContent = "×";
    removeBtn.onclick = () => removeBannedWord(word);

    tag.appendChild(label);
    tag.appendChild(removeBtn);
    container.appendChild(tag);
  });
}

async function addBannedWord() {
  const input = document.getElementById("input-banned-word");
  const statusBanned = document.getElementById("status-banned");
  if (!input) return;

  const raw = input.value || "";
  const candidates = raw
    .split(",")
    .map((w) => w.trim().toLowerCase())
    .filter(Boolean);

  if (candidates.length === 0) return;

  let added = 0;
  candidates.forEach((w) => {
    if (!bannedWordsList.includes(w)) {
      bannedWordsList.push(w);
      added++;
    }
  });

  input.value = "";
  renderBannedWords();

  if (added > 0) {
    await saveConfig("banned");
  } else if (statusBanned) {
    statusBanned.innerText = t("ban_already_exists");
    statusBanned.style.color = "#ffd60a";
  }
}

async function removeBannedWord(word) {
  bannedWordsList = bannedWordsList.filter((w) => w !== word);
  renderBannedWords();
  await saveConfig("banned");
}

async function clearBannedWords() {
  if (bannedWordsList.length === 0) return;
  bannedWordsList = [];
  renderBannedWords();
  await saveConfig("banned");
}

function updateBeepVolumeLabel(val) {
  const label = document.getElementById("beep-volume-label");
  if (label) {
    label.innerText = `${val}%`;
  }
}

function playTestBeep() {
  const volInput = document.getElementById("cfg-beep-volume");
  const volPct = volInput ? parseFloat(volInput.value) || 0 : 35;
  if (volPct <= 0) return;

  try {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    const ctx = new AudioCtx();
    const osc = ctx.createOscillator();
    const filter = ctx.createBiquadFilter();
    const gainNode = ctx.createGain();

    osc.type = "sine";
    osc.frequency.setValueAtTime(750, ctx.currentTime);

    filter.type = "lowpass";
    filter.frequency.setValueAtTime(1200, ctx.currentTime);

    const peakGain = Math.min(0.45, (volPct / 100) * 0.25);
    const now = ctx.currentTime;
    gainNode.gain.setValueAtTime(0.0001, now);
    gainNode.gain.exponentialRampToValueAtTime(peakGain, now + 0.02);
    gainNode.gain.setValueAtTime(peakGain, now + 0.28);
    gainNode.gain.exponentialRampToValueAtTime(0.0001, now + 0.34);

    osc.connect(filter);
    filter.connect(gainNode);
    gainNode.connect(ctx.destination);

    osc.start(now);
    osc.stop(now + 0.35);
    osc.onended = () => ctx.close();
  } catch (e) {
    console.error("Audio preview error:", e);
  }
}

async function saveConfig(source = "settings") {
  let statusId = "status-settings";
  if (source === "banned") statusId = "status-banned";
  if (source === "options") statusId = "status-options";
  const status = document.getElementById(statusId);

  const cfg = collectFormConfig();

  try {
    await window.pywebview.api.save_config(cfg);
    if (status) {
      status.innerText = t("status_settings_saved");
      status.style.color = "#30d158";
    }
    syncPreviewWindow();
  } catch (e) {
    if (status) {
      status.innerText = "Error saving settings";
      status.style.color = "#ff453a";
    }
  }
}

// ========================
//    WHISPER MODEL CACHE
// ========================

async function loadInstalledModels() {
  const container = document.getElementById("models-list-container");
  const sizeMeta = document.getElementById("models-total-size");
  if (!container) return;

  container.innerHTML = `
    <div class="models-empty-state">
      <span>${t("loading_models")}</span>
    </div>
  `;

  try {
    const models = await window.pywebview.api.get_installed_models();
    if (!models || models.length === 0) {
      container.innerHTML = `
        <div class="models-empty-state">
          <span>${t("no_models_found")}</span>
        </div>
      `;
      if (sizeMeta) sizeMeta.innerText = "";
      return;
    }

    const totalBytes = models.reduce((acc, m) => acc + (m.size_bytes || 0), 0);
    const totalMb = totalBytes / (1024 * 1024);
    const totalStr =
      totalMb >= 1000
        ? `${(totalMb / 1024).toFixed(2)} GB`
        : `${totalMb.toFixed(1)} MB`;

    if (sizeMeta) {
      sizeMeta.innerText = `(${t("total_cache_size")} ${totalStr})`;
    }

    container.innerHTML = "";
    models.forEach((m) => {
      const row = document.createElement("div");
      row.className = "model-item-row";

      row.innerHTML = `
        <div class="model-item-left">
          <div class="model-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="4" y="4" width="16" height="16" rx="2" />
              <rect x="9" y="9" width="6" height="6" />
              <line x1="9" y1="1" x2="9" y2="4" />
              <line x1="15" y1="1" x2="15" y2="4" />
              <line x1="9" y1="20" x2="9" y2="23" />
              <line x1="15" y1="20" x2="15" y2="23" />
              <line x1="20" y1="9" x2="23" y2="9" />
              <line x1="20" y1="14" x2="23" y2="14" />
              <line x1="1" y1="9" x2="4" y2="9" />
              <line x1="1" y1="14" x2="4" y2="14" />
            </svg>
          </div>
          <div class="model-details">
            <span class="model-title-text">${m.name}</span>
            <span class="model-folder-text">${m.folder}</span>
          </div>
        </div>
        <div class="model-item-right">
          <span class="model-size-badge">${m.size_str}</span>
          <button
            type="button"
            class="btn-delete-model"
            title="Delete this model"
          >
            ${t("btn_delete_model")}
          </button>
        </div>
      `;

      const delBtn = row.querySelector(".btn-delete-model");
      delBtn.onclick = () => deleteModel(m.id, m.name, m.size_str);

      container.appendChild(row);
    });
  } catch (e) {
    container.innerHTML = `
      <div class="models-empty-state">
        <span style="color: #ff453a;">Error loading models: ${e.message || e}</span>
      </div>
    `;
  }
}

async function deleteModel(modelId, modelName, sizeStr) {
  const confirmMsg = t("confirm_delete_model")
    .replace("{name}", modelName)
    .replace("{size}", sizeStr);

  const confirmed = window.confirm(confirmMsg);
  if (!confirmed) return;

  const status = document.getElementById("status-options");
  if (status) {
    status.innerText = `Deleting ${modelName}...`;
    status.style.color = "#ffd60a";
  }

  try {
    const res = await window.pywebview.api.delete_installed_model(modelId);
    if (res && res.ok) {
      if (status) {
        status.innerText = res.message;
        status.style.color = "#30d158";
      }
      await loadInstalledModels();
    } else {
      if (status) {
        status.innerText = (res && res.message) || "Error deleting model";
        status.style.color = "#ff453a";
      }
    }
  } catch (e) {
    if (status) {
      status.innerText = "Error deleting model";
      status.style.color = "#ff453a";
    }
  }
}

async function openModelsFolder() {
  await window.pywebview.api.open_models_cache_folder();
}
